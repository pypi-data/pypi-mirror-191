# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205,W0613,R0801

import logging
from pika.frame import Method
from pika import validators
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqQueue(RabbitmqChannel):
    _queue: str
    _queue_config: dict

    def __init__(self, **kwargs):
        self._queue = None
        self._queue_config = None
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_queue_config()

    def validate(self):
        super().validate()
        self.check_queue()

    @property
    def queue(self) -> str:
        return self._queue

    @property
    def queue_config(self) -> dict:
        return self._queue_config

    def setup_queue(self):
        if self.queue is None:
            self._queue = self.config.get('queue')

    def setup_queue_config(self):
        if self._queue_config is None:
            self._queue_config = {k: v for k, v in dict(self.config.get('queue_config', {})).items() if v is not None}

        self._queue_config = dict(
            queue=self._queue_config.get('queue', self._queue),
            passive=self._queue_config.get('passive', False) is True,
            durable=self._queue_config.get('durable', False) is True,
            exclusive=self._queue_config.get('exclusive', False) is True,
            auto_delete=self._queue_config.get('auto_delete', False) is True,
            arguments=dict(self._queue_config.get('arguments', {}))
        )

        if self.queue is None:
            self._queue = self._queue_config.get('queue')

    def check_queue(self):
        validators.require_string(self.queue, 'queue')


class RabbitmqQueueDeclare(RabbitmqQueue):
    _queue_is_declared: bool

    def __init__(self, **kwargs):
        self._queue_is_declared = False
        super().__init__(**kwargs)

    @property
    def queue_is_declared(self) -> int:
        return self._queue_is_declared

    def waiting_queue_is_declared(self):
        while not self.queue_is_declared:
            continue
        return self

    def on_channel_open_ok(self):
        self.queue_declare()

    def queue_declare(self):
        LOGGER.info('Declaring queue: %s', self.queue_config)
        self.channel.queue_declare(**self.queue_config, callback=self.on_queue_declare_ok)

    def on_queue_declare_ok(self, method_frame: Method):
        LOGGER.info('Queue declared: %s', self.queue_config)
        self._queue_is_declared = True

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_queue_is_declared()


class RabbitmqQueueBind(RabbitmqQueue):
    _queue: str
    _queue_bind_config: dict
    _exchange: str
    _routing_key: str
    _queue_is_binded: False

    def __init__(self, **kwargs):
        self._queue = None
        self._queue_bind_config = None
        self._exchange = None
        self._routing_key = None
        self._queue_is_binded = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_exchange()
        self.setup_routing_key()
        self.setup_queue_bind_config()

    @property
    def queue_is_binded(self) -> int:
        return self._queue_is_binded

    @property
    def queue_bind_config(self) -> dict:
        return self._queue_bind_config

    @property
    def exchange(self) -> str:
        return self._exchange

    @property
    def routing_key(self) -> str:
        return self._routing_key

    def waiting_queue_is_binded(self):
        while not self.queue_is_binded:
            continue
        return self

    def setup_exchange(self):
        if self.exchange is None:
            self._exchange = self.config.get('exchange')

    def setup_routing_key(self):
        if self.routing_key is None:
            self._routing_key = self.config.get('routing_key')

    def setup_queue_bind_config(self):
        if self.queue_bind_config is None:
            self._queue_bind_config = {k: v for k, v in dict(self._config.get('queue_bind_config', {})).items() if v is not None}

        self._queue_bind_config = dict(
            queue=self.queue_bind_config.get('queue', self.queue),
            exchange=self.queue_bind_config.get('exchange', self.exchange) or dict(self.config.get('exchange_config', {})).get('exchange'),
            routing_key=self.queue_bind_config.get('routing_key', self.routing_key) or dict(self.config.get('exchange_bind_config', {})).get('routing_key'),
            arguments=dict(self.queue_bind_config.get('arguments', {}))
        )

        if self.queue is None:
            self._queue = self.queue_bind_config.get('queue')
        if self.exchange is None:
            self._exchange = self.queue_bind_config.get('exchange')
        if self.routing_key is None:
            self._routing_key = self.queue_bind_config.get('routing_key') or self.queue_bind_config.get('queue')

    def on_channel_open_ok(self):
        self.queue_bind()

    def queue_bind(self):
        LOGGER.info('Binding queue: %s', self.queue_bind_config)
        self.waiting_channel().channel.queue_bind(**self.queue_bind_config, callback=self.on_queue_bind_ok)

    def on_queue_bind_ok(self, method_frame: Method):

        LOGGER.info('Queue binded: %s', self.queue_bind_config)
        self._queue_is_binded = True

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_queue_is_binded()
