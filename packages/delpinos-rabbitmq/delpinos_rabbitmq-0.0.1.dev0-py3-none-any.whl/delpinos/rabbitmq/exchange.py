# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
from pika import validators
from pika.frame import Method
from pika.exchange_type import ExchangeType
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqExchange(RabbitmqChannel):
    _exchange: str
    _exchange_config: dict

    def __init__(self, **kwargs):
        self._exchange = None
        self._exchange_config = None
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_exchange_config()
        self.setup_exchange()

    def validate(self):
        super().validate()
        self.check_exchange()

    @property
    def exchange(self) -> str:
        return self._exchange

    @property
    def exchange_config(self) -> dict:
        return self._exchange_config

    def setup_exchange(self):
        if self.exchange is None:
            self._exchange = self.config.get('exchange')

    def setup_exchange_config(self):
        if self._exchange_config is None:
            self._exchange_config = {k: v for k, v in dict(self.config.get('exchange_config', {})).items() if v is not None}

        self._exchange_config = dict(
            exchange=self._exchange_config.get('exchange', self._exchange),
            exchange_type=self._exchange_config.get('exchange_type', ExchangeType.topic),
            passive=self._exchange_config.get('passive', False) is True,
            durable=self._exchange_config.get('durable', False) is True,
            auto_delete=self._exchange_config.get('auto_delete', False) is True,
            internal=self._exchange_config.get('internal', False) is True,
            arguments=dict(self._exchange_config.get('arguments', {}))
        )

        if self.exchange is None:
            self._exchange = self._exchange_config.get('exchange')

    def check_exchange(self):
        validators.require_string(self.exchange, 'exchange')


class RabbitmqExchangeDeclare(RabbitmqExchange):
    _exchange_is_declared: bool

    def __init__(self, **kwargs):
        self._exchange_is_declared = False
        super().__init__(**kwargs)

    @property
    def exchange_is_declared(self) -> int:
        return self._exchange_is_declared

    def waiting_exchange_is_declared(self):
        while not self.exchange_is_declared:
            continue
        return self

    def on_channel_open_ok(self):
        self.exchange_declare()

    def exchange_declare(self):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declare_ok method will
        be invoked by pika.
        """

        LOGGER.info('Declaring exchange: %s', self.exchange_config)
        self.channel.exchange_declare(**self.exchange_config, callback=self.on_exchange_declare_ok)

    def on_exchange_declare_ok(self, method_frame: Method):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param dict: Config

        """
        LOGGER.info('Exchange declared: %s', self.exchange_config)
        self._exchange_is_declared = True

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_declared()


class RabbitmqExchangeBind(RabbitmqExchange):
    _exchange: str
    _exchange_bind_config: dict
    _routing_key: str
    _exchange_is_binded: False

    def __init__(self, **kwargs):
        self._exchange = None
        self._exchange_bind_config = None
        self._routing_key = None
        self._exchange_is_binded = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.setup_exchange()
        self.setup_routing_key()
        self.setup_exchange_bind_config()

    @property
    def exchange_is_binded(self) -> int:
        return self._exchange_is_binded

    @property
    def exchange_bind_config(self) -> dict:
        return self._exchange_bind_config

    @property
    def exchange(self) -> str:
        return self._exchange

    @property
    def routing_key(self) -> str:
        return self._routing_key

    def waiting_exchange_is_binded(self):
        while not self.exchange_is_binded:
            continue
        return self

    def setup_exchange(self):
        if self.exchange is None:
            self._exchange = self.config.get('exchange')

    def setup_routing_key(self):
        if self.routing_key is None:
            self._routing_key = self.config.get('routing_key')

    def setup_exchange_bind_config(self):
        if self.exchange_bind_config is None:
            self._exchange_bind_config = {k: v for k, v in dict(self._config.get('exchange_bind_config', {})).items() if v is not None}

        self._exchange_bind_config = dict(
            destination=self._exchange_bind_config.get('destination'),
            source=self._exchange_bind_config.get('source'),
            routing_key=self._exchange_bind_config.get('routing_key', self.routing_key or dict(self.config.get('queue_bind_config', {}).get('routing_key'))),
            arguments=dict(self._exchange_bind_config.get('arguments', {}))
        )

        if self.exchange is None:
            self._exchange = self._exchange_bind_config.get('exchange')
        if self.routing_key is None:
            self._routing_key = self._exchange_bind_config.get('routing_key')

    def on_channel_open_ok(self):
        self.exchange_bind()

    def exchange_bind(self):
        """Setup the exchange bind on RabbitMQ. When it is complete, the on_exchange_bind_ok method will
        be invoked by pika.
        """

        LOGGER.info('Binding exchange: %s', self.exchange_bind_config)
        self.waiting_channel().channel.exchange_bind(**self.exchange_bind_config, callback=self.on_exchange_bind_ok)

    def on_exchange_bind_ok(self, method_frame: Method):
        """Invoked by pika when the Exchange.Bind method has completed. At this
        point we will set the prefetch count for the channel.

        :param pika.frame.Method method_frame: Method: The Exchange.BindOk response frame
        :param dict: Config

        """

        LOGGER.info('Exchange binded: %s', self.exchange_bind_config)
        self._exchange_is_binded = True

    def run(self, blocking: bool = None):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_binded()
