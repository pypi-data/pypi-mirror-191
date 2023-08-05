# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
import uuid
import json
import hashlib
from datetime import datetime
from flask import Flask, Response, request
from pika.spec import BasicProperties
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqProducer(RabbitmqChannel):
    _app_id: str
    _exchange: str
    _routing_key: str
    _producer_config: dict

    def __init__(self, **kwargs):
        self._app_id = None
        self._exchange = None
        self._routing_key = None
        self._producer_config = None
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_app_id()
        self.setup_exchange()
        self.setup_routing_key()
        self.setup_producer_config()

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def exchange(self) -> str:
        return self._exchange

    @property
    def routing_key(self) -> str:
        return self._routing_key

    @property
    def producer_config(self) -> dict:
        return self._producer_config

    def setup_app_id(self):
        if self.app_id is None:
            self._app_id = self.config.get('app_id')

    def setup_exchange(self):
        if self.exchange is None:
            self._exchange = self.config.get('exchange', dict(self.config.get('exchange_config', {})).get('exchange'))

    def setup_routing_key(self):
        if self.routing_key is None:
            self._routing_key = self.config.get('routing_key', dict(self.config.get('queue_bind_config', {})).get('routing_key'))

    def setup_producer_config(self):
        if self._producer_config is None:
            self._producer_config = {k: v for k, v in dict(self.config.get('producer_config', {})).items() if v is not None}

        self._producer_config = dict(
            exchange=self._producer_config.get('exchange', self.exchange),
            routing_key=self._producer_config.get('routing_key', self.routing_key),
            properties=self._producer_config.get('properties') or BasicProperties(),
            mandatory=self._producer_config.get('mandatory') is True
        )
        if isinstance(self._producer_config.get('properties'), dict):
            self._producer_config['properties'] = BasicProperties(**self._producer_config.get('properties'))
        if not isinstance(self._producer_config.get('properties'), BasicProperties):
            self._producer_config['properties'] = BasicProperties()

        if self.app_id is None:
            self._app_id = self._producer_config.get('properties').app_id
        if self.exchange is None:
            self._exchange = self._producer_config.get('exchange')
        if self.routing_key is None:
            self._routing_key = self._producer_config.get('routing_key')

    def publish(self, body: bytes,
                exchange: str = None,
                routing_key: str = None,
                properties: BasicProperties = None,
                mandatory: bool = None):

        mandatory = self._producer_config.get('mandatory') if mandatory is None else mandatory
        return self.basic_publish(
            exchange=exchange or self._producer_config.get('exchange'),
            routing_key=routing_key or self._producer_config.get('routing_key'),
            body=body,
            properties=properties or self._producer_config.get('properties'),
            mandatory=mandatory is True
        )


class RabbitmqFlaskProducer(RabbitmqProducer):
    _flask_app: Flask

    def __init__(self, **kwargs):
        self._flask_app = None
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_flask_app()

    def validate(self):
        super().validate()
        self.check_flask_app()

    @property
    def flask_app(self) -> Flask:
        return self._flask_app

    def setup_flask_app(self):
        if self.flask_app is None:
            self._flask_app = self.config.get('flask_app')

    def check_flask_app(self):
        if not isinstance(self.flask_app, Flask):
            raise TypeError('flask_app is required, valid instance of flask.Flask')


class RabbitmqFlaskApiProducer(RabbitmqFlaskProducer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_url_rules()

    def add_url_rules(self):
        self.add_api_publish_message_url_rule()

    def add_api_publish_message_url_rule(self):
        self.flask_app.add_url_rule(
            '/<app_id>/<exchange>/<routing_key>',
            '/<app_id>/<exchange>/<routing_key>',
            view_func=self._api_publish_message,
            methods=['POST']
        )

    def _get_value(self, key, *args):
        keys = []
        if isinstance(key, str):
            keys.append(key)
        elif isinstance(key, list):
            keys = key
        else:
            return None

        def get_value(data: dict):
            for key in keys:
                value = data.get(key)
                if value is not None:
                    return value
            return None

        for data in args:
            if isinstance(data, dict):
                value = get_value(data)
                if value is not None:
                    return value
        return None

    def _format_header_key(self, key):
        base = []
        for parts in str(key).split('-'):
            base.append(parts[0].upper() + (parts[1:] if len(parts) > 1 else '').lower())
        return '-'.join(base)

    def _format_header(self, headers: dict):
        new_header = {}
        for key, value in headers.items():
            if value is not None:
                new_header[self._format_header_key(key)] = str(value)
        keys = list(new_header.keys())
        keys.sort()
        return {key: new_header.get(key) for key in keys}

    def _get_data_with_prefix(self, prefix: str, data: dict = None):
        if prefix is None or data is None:
            return {}

        return dict({
            k[len(prefix):]: v for k, v in dict(data).items() if v is not None and str(k).lower().startswith(prefix)
        })

    def _api_publish_message(self, app_id: str = None, exchange: str = None, routing_key: str = None):
        headers = {}
        app_id = app_id or self.app_id
        exchange = exchange or self.exchange
        routing_key = routing_key or self.routing_key
        utcnow = datetime.utcnow()
        message_id = str(uuid.uuid4())
        timestamp = utcnow.strftime('%Y-%m-%dT%H:%M:%S.%f')
        unix_timestamp = utcnow.timestamp()
        headers.update(self._get_data_with_prefix('publish-', request.args))
        headers.update(self._get_data_with_prefix('publish-', request.headers))
        headers.update({
            'App-id': app_id,
            'Message-Id': message_id,
            'Exchange': exchange,
            'Routing-Key': routing_key,
            'Timestamp': timestamp,
            'Unix-Timestamp': str(unix_timestamp),
            'Receive-Content-Md5': request.content_md5 or request.headers.get('Content-Md5'),
            'Receive-Content-Type': request.content_type or request.headers.get('Content-Type'),
            'Receive-Content-Length': request.content_length or request.headers.get('Content-Length')
        })
        headers = self._format_header(headers)
        headers['Authorization'] = headers.get('Authorization', self._get_value(['Authorization', 'authorization'], dict(request.headers), dict(request.args)))
        response_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        }
        try:
            if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                body = dict(request.values)
            elif request.headers.get('Content-Type') == 'application/json':
                body = dict(request.json)
            else:
                body = request.data.decode('utf-8')
            if isinstance(body, dict):
                publish_body = json.dumps(body)
                headers['Content-Type'] = 'application/json; charset=utf-8'
            else:
                headers['Content-Type'] = headers.get('Receive-Content-Type')
                headers['Receive-Content-Md5'] = headers.get('Receive-Content-Md5') or hashlib.md5(request.data).hexdigest()
                headers['Receive-Content-Length'] = headers.get('Receive-Content-Length') or len(body)
                publish_body = str(body)
            headers['Content-Md5'] = hashlib.md5(publish_body.encode('utf-8')).hexdigest()
            headers['Content-Length'] = str(len(publish_body))
            headers['Receive-Content-Md5'] = headers.get('Receive-Content-Md5') or headers.get('Content-Md5')
            headers = self._format_header(headers)
            response = {
                'exchange': exchange,
                'routingKey': routing_key,
                'properties': {
                    'appId': app_id,
                    'messageId': message_id,
                    'headers': headers
                },
                'body': publish_body,
                'timestamp': timestamp,
                'unixTimestamp': unix_timestamp,
            }
            if isinstance(body, dict):
                body = json.dumps(body)
            properties = BasicProperties(
                app_id=app_id,
                message_id=message_id,
                headers=headers
            )
            self.publish(body=body, exchange=exchange, routing_key=routing_key, properties=properties)
            return Response(response=json.dumps(response), headers=response_headers, status=200, content_type=response_headers.get('Content-Type'))
        except Exception as err:
            response = {
                'error': 'Publish error'
            }
            LOGGER.error(err)
            return Response(response=json.dumps(response), headers=response_headers, status=400, content_type=response_headers.get('Content-Type'))
