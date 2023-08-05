# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,W0640,R0801

import json
import logging
import threading
from typing import List, Type
from flask import Flask
from pika.channel import Channel
from pika.spec import BasicProperties, Basic
from delpinos.base import ObjectConfigBase
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqConsumer(RabbitmqChannel):
    _closing: bool
    _consuming: bool
    _consumer_config: dict
    _consumer_tag: str
    _queue: str
    _qos_is_seted: bool

    def __init__(self, **kwargs):
        self._queue = None
        self._closing = False
        self._consumer_config = None
        self._consumer_tag = None
        self._consuming = False
        self._qos_is_seted = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_queue()
        self.setup_consumer_config()

    @property
    def qos_is_seted(self) -> int:
        return self._qos_is_seted

    @property
    def queue(self) -> str:
        return self._queue

    @property
    def consumer_config(self) -> str:
        return self._consumer_config

    def waiting_qos_is_seted(self):
        while not self.qos_is_seted:
            continue
        return self

    def setup_queue(self):
        if self.queue is None:
            self._queue = self.config.get('queue', dict(self.config.get('queue_config')).get('queue'))

    def on_channel_open_ok(self):
        self.set_qos()

    def setup_consumer_config(self):
        if self._consumer_config is None:
            self._consumer_config = {k: v for k, v in dict(self._config.get('consumer_config', {})).items() if v is not None}
        else:
            self._consumer_config = {k: v for k, v in dict(self._consumer_config).items() if v is not None}

        qos = dict(self._consumer_config.get('qos', self._config.get('qos', {})))
        dlq = dict(self._consumer_config.get('dlq', self._config.get('dlq', {})))

        self._consumer_config['retries'] = int(self._consumer_config.get('retries') or self.retries)

        self._consumer_config['qos'] = dict(
            prefetch_size=qos.get('prefetch_size', 0),
            prefetch_count=qos.get('prefetch_count', 1),
            global_qos=qos.get('global_qos', False) is True
        )

        self._consumer_config['dlq'] = dict(
            enable=dlq.get('enable') is True,
            exceptions=list(dlq.get('exceptions') or []),
            exchange=dlq.get('exchange'),
            routing_key=dlq.get('routing_key')
        )

        if self._consumer_config['dlq'].get('exchange') is None or self._consumer_config['dlq'].get('routing_key') is None:
            self._consumer_config['dlq']['enable'] = False

        self._consumer_config['queue'] = self._consumer_config.get('queue') or self.queue

        if self.queue is None:
            self.queue = self.consumer_config['queue']

    def consume(self,
                queue=None,
                exclusive=None,
                consumer_tag=None,
                arguments=None,
                callback=None):

        callback = self.default_on_event_ok if not callable(callback) else callback
        return self.basic_consume(
            queue=queue or self.consumer_config.get('queue') or self.queue,
            on_message_callback=self.consume_message,
            auto_ack=False,
            exclusive=exclusive,
            consumer_tag=consumer_tag,
            arguments=arguments,
            callback=callback
        )

    def check_message_retry(self, properties: BasicProperties, body: bytes, err: Exception) -> bool:
        try:
            for exception_class in list(dict(self._consumer_config.get('dlq')).get('exceptions')):
                if isinstance(err, exception_class):
                    return False
            headers = properties.headers or {}
            retry = int(headers.get('retry') or 0) + 1
            retries = int(self._consumer_config['retries'] or self.retries)
            if retry > retries:
                return False
        except Exception:
            return False
        return True

    def consume_message(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            self.on_message(channel, basic_deliver, properties, body)
            self.on_message_ok(channel, basic_deliver, properties, body)
        except Exception as err:
            if self.check_message_retry(properties, body, err):
                self.on_message_retry(channel, basic_deliver, properties, body, err)
            else:
                self.on_message_error(channel, basic_deliver, properties, body, err)

    def on_message(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
        LOGGER.info('%s', body)

    def on_message_ok(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def on_message_retry(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes, err: Exception):
        try:
            headers = properties.headers or {}
            headers['retry'] = int(headers.get('retry') or 0) + 1
            headers['exception'] = dict(
                type=f'{err.__class__.__module__}.{err.__class__.__name__}',
                message=str(err)
            )
            properties.headers = headers
            self.basic_publish(exchange=basic_deliver.exchange, routing_key=basic_deliver.routing_key, properties=properties, body=body)
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
        except Exception:
            channel.basic_reject(delivery_tag=basic_deliver.delivery_tag)

    def on_message_error(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes, err: Exception):
        try:
            dlq = dict(self.consumer_config.get('dlq', {}))
            if dlq.get('enable') is True:
                self.basic_publish(dlq.get('exchange'), routing_key=dlq.get('routing_key'), properties=properties, body=body)
                channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            else:
                raise Exception()
        except Exception:
            channel.basic_reject(delivery_tag=basic_deliver.delivery_tag)

    def set_qos(self):
        config = self.consumer_config.get('qos')
        self.basic_qos(**config, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, method_frame):
        LOGGER.info('QOS set to: %s', self.consumer_config.get('qos'))
        self._qos_is_seted = True
        self.start_consuming()

    def start_consuming(self):
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self.consume(queue=self.consumer_config.get('queue'))
        self._consuming = True

    def add_on_cancel_callback(self):
        LOGGER.info('Adding consumer cancellation callback')
        self.waiting_channel().channel.add_on_cancel_callback(self.on_cancel_consumer_ok)

    def stop_consuming(self):
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self.basic_cancel(consumer_tag=self._consumer_tag, callback=self.on_cancel_consumer_ok)

    def on_cancel_consumer_ok(self, method_frame):
        LOGGER.info('RabbitMQ acknowledged the cancellation of the consumer: %s', self._consumer_tag)
        self._consuming = False
        self.close_channel()

    def health_check(self) -> tuple:
        try:
            health_check = super().health_check()
            if not isinstance(health_check, tuple):
                raise Exception('Unhealth')
            if not health_check[0]:
                return health_check
            if not self.is_running:
                raise Exception('Rabbitmq consumer is not running')
            if self.is_closing:
                raise Exception('Rabbitmq consumer is closing')
            return True, 'Success'
        except Exception as err:
            return False, str(err)

    def stop(self, blocking: bool = True):
        if not self._closing:
            self._closing = True
            LOGGER.info('Stopping consumer')
            if self._consuming:
                self.stop_consuming()
            LOGGER.info('Consumer Stopped')

        super().stop(blocking)

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_qos_is_seted()


class RabbitmqJsonConsumer(RabbitmqConsumer):
    def setup(self):
        super().setup()
        self.setup_consumer_config()

    def setup_consumer_config(self):
        super().setup_consumer_config()
        dlq = self._consumer_config.get('dlq') or {}
        dlq['exceptions'] = [json.JSONDecodeError]
        self._consumer_config['dlq'] = dlq

    def decode_message(self, body: bytes) -> dict:
        return dict(json.loads(body))


class RabbitmqFlaskConsumer(RabbitmqConsumer):
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

    def on_message(self, channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
        LOGGER.info('%s', body)


class RabbitmqFlaskJsonConsumer(RabbitmqFlaskConsumer, RabbitmqJsonConsumer):
    def setup(self):
        RabbitmqFlaskConsumer.setup(self)
        RabbitmqJsonConsumer.setup_consumer_config(self)


class RabbitmqConsumerMultiple(ObjectConfigBase):
    _instances: int
    _consumers: List[Type[RabbitmqConsumer]]
    _threads: List[threading.Thread]
    _consumer_class: Type[RabbitmqConsumer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._consumer_class = self.config.get('consumer_class') or RabbitmqConsumer
        self._instances = int(kwargs.get('instances', 1) or 1)
        self._consumers = []
        self._threads = []

    @property
    def threads(self) -> List[threading.Thread]:
        return self._threads

    @property
    def consumers(self) -> List[RabbitmqConsumer]:
        return self._consumers

    def add_consumer(self, number: int = None, blocking=None):
        number = number or 1
        LOGGER.info("Adding Consumer %i", number or 1)
        consumer = None
        try:
            consumer = self._consumer_class(**self._config)
            self._consumers.append(consumer)
            LOGGER.info("Starting Consumer %i", number or 1)
            consumer.run(blocking=blocking)
            LOGGER.info("Added Consumer %i", number or 1)
        except Exception as err:
            LOGGER.error(err)
            consumer = None

    def health_check(self) -> tuple:
        try:
            errors = []
            consumer_number = 0
            for consumer in self.consumers:
                try:
                    consumer_number += 1
                    health_check = consumer.health_check()
                    if not isinstance(health_check, tuple):
                        raise Exception('Unhealth')
                    if not health_check[0]:
                        raise Exception(health_check[1])
                except Exception as err:
                    errors.append(f'Consumer {consumer_number}: {err}')
            if len(errors) > 0:
                return False, ', '.join(errors)
            return True, 'Success'
        except Exception as err:
            return False, str(err)

    def run(self, blocking: bool = None):
        for i in range(0, self._instances):
            thread = threading.Thread(target=lambda: self.add_consumer(i + 1, blocking), daemon=True)
            thread.start()
            self._threads.append(thread)

    def stop(self, blocking: bool = None):
        for consumer in self.consumers:
            consumer.stop(blocking)
