# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import logging
from pika.frame import Method
from pika.channel import Channel
from pika.spec import BasicProperties, Basic
from .connection import RabbitmqConnection

LOGGER = logging.getLogger(__name__)


class RabbitmqChannel(RabbitmqConnection):

    _channel: Channel
    _channel_number: int

    def __init__(self, **kwargs):
        self._channel = None
        self._channel_number = None
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_channel()
        self.setup_channel_number()

    @property
    def channel(self) -> Channel:
        return self._channel

    @property
    def channel_is_open(self) -> bool:
        return self.channel.is_open if isinstance(self.channel, Channel) else False

    @property
    def channel_is_closed(self) -> bool:
        return self.channel.is_closed if isinstance(self.channel, Channel) else True

    @property
    def channel_is_closing(self) -> bool:
        return self.channel.is_closing if isinstance(self.channel, Channel) else True

    @property
    def channel_number(self) -> int:
        return self._channel_number

    def setup_channel(self):
        if self.channel is None:
            self._channel = self.config.get('channel')

    def setup_channel_number(self):
        if self.channel_number is None:
            self._channel_number = self.config.get('channel_number')

    def waiting_channel(self):
        self.waiting_connection()
        while not isinstance(self.channel, Channel):
            continue
        return self

    def waiting_channel_is_open(self):
        self.waiting_channel()
        while not self.channel.is_open:
            continue
        return self

    def waiting_channel_is_closed(self):
        if isinstance(self.channel, Channel):
            while not self.channel.is_closed:
                continue
        return self

    def on_connection_open_ok(self):
        self.open_channel()

    def open_channel(self):
        try:
            connection = self.waiting_connection_is_open().connection.connection
            LOGGER.info('Creating a new channel')
            connection.channel(channel_number=self.channel_number, on_open_callback=self.on_channel_open)
        except Exception as err:
            self.on_channel_open_error(err)

    def on_channel_open(self, channel: Channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self.on_channel_open_ok()

    def on_channel_open_ok(self):
        pass

    def on_channel_open_error(self, err: Exception):
        raise err

    def close_channel(self):
        if isinstance(self._channel, Channel):
            LOGGER.info('Closing the channel')
            self.channel.close()
            self.waiting_channel_is_closed()
            self._channel = None
            LOGGER.info('Channel closed')

    def basic_ack(self, delivery_tag=None, multiple=None):
        return self.waiting_channel().channel.basic_ack(
            delivery_tag=int(delivery_tag or 0),
            multiple=multiple is True
        )

    def basic_nack(self, delivery_tag=None, multiple=None, requeue=None):
        return self.waiting_channel().channel.basic_nack(
            delivery_tag=int(delivery_tag or 0),
            multiple=multiple is True,
            requeue=requeue or True
        )

    def basic_reject(self, delivery_tag=None, requeue=None):
        return self.waiting_channel().channel.basic_nack(
            delivery_tag=int(delivery_tag or 0),
            requeue=requeue or True
        )

    def basic_cancel(self, consumer_tag=None, callback=None):
        callback = self.default_on_event_ok if not callable(callback) else callback
        return self.waiting_channel().channel.basic_cancel(
            consumer_tag=consumer_tag or '',
            callback=callback
        )

    def basic_get(self, queue, callback=None, auto_ack=None):
        callback = self.default_get_callback if not callable(callback) else callback
        return self.waiting_channel().channel.basic_get(
            queue=queue,
            callback=callback,
            auto_ack=auto_ack is True
        )

    def basic_recover(self, requeue=False, callback=None):
        callback = self.default_on_event_ok if not callable(callback) else callback
        return self.waiting_channel().channel.basic_recover(
            requeue=requeue,
            callback=callback
        )

    def basic_qos(self,
                  prefetch_size=0,
                  prefetch_count=0,
                  global_qos=False,
                  callback=None):

        callback = self.default_on_event_ok if not callable(callback) else callback
        return self.waiting_channel().channel.basic_qos(
            prefetch_size=int(prefetch_size or 0),
            prefetch_count=int(prefetch_count or 1),
            global_qos=global_qos is True,
            callback=callback
        )

    def basic_consume(self,
                      queue,
                      on_message_callback,
                      auto_ack=None,
                      exclusive=None,
                      consumer_tag=None,
                      arguments=None,
                      callback=None):

        callback = self.default_on_event_ok if not callable(callback) else callback
        self.waiting_channel().channel.basic_consume(
            queue=queue,
            on_message_callback=on_message_callback,
            auto_ack=auto_ack is True,
            exclusive=exclusive is True,
            consumer_tag=consumer_tag,
            arguments=arguments,
            callback=callback
        )

    def basic_publish(self,
                      exchange: str,
                      routing_key: str,
                      body: bytes,
                      properties: BasicProperties = None,
                      mandatory: bool = None):

        return self.waiting_channel().channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=properties or BasicProperties(),
            mandatory=mandatory is True
        )

    def default_get_callback(self, channel: Channel, method: Basic.GetOk, properties: BasicProperties, body: bytes):
        LOGGER.info('Get message: %s', body)

    def default_on_event_ok(self, method_frame: Method):
        pass

    def health_check(self) -> tuple:
        try:
            health_check = super().health_check()
            if not isinstance(health_check, tuple):
                raise Exception('Unhealth')
            if not health_check[0]:
                return health_check
            if self.channel_is_closed:
                raise Exception('Rabbitmq channel is closed')
            if not self.channel_is_open:
                raise Exception('Rabbitmq channel is not open')
            return True, 'Success'
        except Exception as err:
            return False, str(err)

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_channel_is_open()

    def stop(self, blocking: bool = None):
        super().stop(blocking)
        if blocking:
            self.waiting_channel_is_closed()
