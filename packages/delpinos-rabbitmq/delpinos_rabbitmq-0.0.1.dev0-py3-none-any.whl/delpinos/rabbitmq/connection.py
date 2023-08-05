# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import time
import logging
import typing
import threading
from pika import SelectConnection
from pika.adapters import select_connection
from pika.connection import Parameters, URLParameters
from delpinos.base import ObjectConfigBase

DEFAULT_RABBITMQ_CONNECTION_RETRIES = 1000
DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT = 15

LOGGER = logging.getLogger(__name__)


class RabbitmqConnectionWrapper:
    _config: dict
    _thread: threading.Thread
    _connection: SelectConnection
    _last_exeption: Exception
    _running: bool
    _closing: bool
    _attempt: int
    _parameters: Parameters
    _on_connection_open_ok_callback: typing.Callable[[], None]
    _on_connection_open_error_callback: typing.Callable[[Exception], None]
    _on_connection_close_callback: typing.Callable[[Exception], None]
    _ioloop = select_connection.IOLoop()
    _retries: int
    _timeout: int

    def __init__(
        self,
        parameters: Parameters = None,
        retries: int = None,
        timeout: int = None,
        on_connection_open_ok_callback: typing.Callable[[], None] = None,
        on_connection_open_error_callback: typing.Callable[[Exception], None] = None,
        on_connection_close_callback: typing.Callable[[Exception], None] = None
    ):
        self._thread = None
        self._connection = None
        self._last_exeption = None
        self._running = False
        self._closing = False
        self._attempt = 0
        self._parameters = parameters
        self._on_connection_open_ok_callback = on_connection_open_ok_callback
        self._on_connection_open_error_callback = on_connection_open_error_callback
        self._on_connection_close_callback = on_connection_close_callback
        self._ioloop = select_connection.IOLoop()
        self._retries = int(retries if isinstance(retries, int) else DEFAULT_RABBITMQ_CONNECTION_RETRIES)
        self._timeout = int(timeout if isinstance(retries, int) else DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT)
        self._config = dict(
            parameters=parameters,
            retries=retries,
            timeout=timeout,
            on_connection_open_ok_callback=on_connection_open_ok_callback,
            on_connection_open_error_callback=on_connection_open_error_callback,
            on_connection_close_callback=on_connection_close_callback
        )

    @property
    def ioloop(self) -> select_connection.IOLoop:
        return self._ioloop

    @property
    def is_open(self) -> bool:
        return self.connection.is_open

    @property
    def is_running(self) -> bool:
        return self._running is True

    @property
    def is_closing(self) -> bool:
        return self._closing is True

    @property
    def is_closed(self):
        return self.connection.is_closed

    @property
    def thread(self) -> threading.Thread:
        return self._thread

    @property
    def connection(self) -> SelectConnection:
        return self._connection

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def config(self) -> dict:
        return self._config

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def retries(self) -> int:
        return self._retries

    @property
    def attempt(self) -> int:
        return self._attempt

    def waiting_connection(self):
        is_running = False
        while not isinstance(self._connection, SelectConnection):
            if not is_running and not self.is_running:
                is_running = True
                self.run()
            continue
        return self

    def waiting_running(self):
        while not self.is_running:
            continue
        return self

    def waiting_connection_is_open(self):
        self.waiting_connection()
        while not self.is_open:
            continue
        return self

    def waiting_connection_is_closed(self):
        if isinstance(self._connection, SelectConnection):
            while not self.is_closed:
                continue
        return self

    def connect(self) -> SelectConnection:
        return SelectConnection(
            parameters=self._parameters,
            on_open_callback=self.on_open_callback,
            on_open_error_callback=self.on_open_error_callback,
            on_close_callback=self.on_close_callback,
            custom_ioloop=self.ioloop
        )

    def reconnect(self):
        if self.attempt >= self.retries:
            self.stop(True)
            if callable(self._on_connection_open_error_callback):
                self._on_connection_open_error_callback(self._last_exeption)
            return

        if not self.is_closing:
            self._attempt += 1
            try:
                self._running = False
                if isinstance(self.connection, SelectConnection):
                    self.connection.close()
                    self.waiting_connection_is_closed()
                    LOGGER.info('Connection Stopped')
                self.ioloop.stop()
                LOGGER.info('Connection IOLoop Stopped')
                self._connection = None
            except Exception as err:
                LOGGER.error(err)
            time.sleep(self._timeout)
            self.run(blocking=False)

    def on_open_callback(self, connection: SelectConnection):
        LOGGER.info('Connection opened')
        self._connection = connection
        self._attempt = 0
        if callable(self._on_connection_open_ok_callback):
            self._on_connection_open_ok_callback()

    def on_close_callback(self, connection, err: Exception):
        if self.is_closing:
            self.ioloop.stop()
            if callable(self._on_connection_close_callback):
                self._on_connection_close_callback(err)
        else:
            self.on_open_error_callback(connection, err)

    def on_open_error_callback(self, connection, err: Exception):
        LOGGER.warning('Connection open failed, reopening in %s seconds: (%s)', self._timeout, err)
        self._last_exeption = err
        self._connection = connection
        self.reconnect()

    def on_connection_open_ok(self):
        pass

    def on_connection_open_error(self, err: Exception):
        raise err

    def on_connection_close(self, err: Exception):
        pass

    def start_ioloop(self):

        def start():
            try:
                self.ioloop.start()
            except RuntimeError:
                pass

        self._thread = threading.Thread(target=start, daemon=True)
        self._thread.start()

    def run(self, blocking: bool = None):
        if not self.is_running:
            self._running = True
            self._closing = False
            self._connection = self.connect()
            self._thread = threading.Thread(target=self.ioloop.start, daemon=True)
            self._thread.start()
        if blocking is True:
            self.waiting_connection_is_open()

    def stop(self, blocking: bool = None):
        self._closing = True
        if self.is_running:
            LOGGER.info('Stopping Connection')
            self._running = False
            if isinstance(self.connection, SelectConnection):
                self.connection.close()
                if blocking is True:
                    self.waiting_connection_is_closed()
                LOGGER.info('Connection Stopped')
            self.ioloop.stop()
            LOGGER.info('Connection IOLoop Stopped')
            self._connection = None


class RabbitmqConnection(ObjectConfigBase):
    _config: dict
    _connection: RabbitmqConnectionWrapper
    _connection_config: dict
    _retries: int
    _timeout: int
    _attempt: int
    _running: bool
    _closing: bool

    def __init__(self, **kwargs):
        self._connection = None
        self._connection_config = None
        self._retries = None
        self._timeout = None
        self._attempt = 0
        self._running = False
        self._closing = False
        super().__init__(**kwargs)

    @property
    def is_open(self) -> bool:
        return self.connection.is_open

    @property
    def is_running(self) -> bool:
        return self._running is True

    @property
    def is_closing(self) -> bool:
        return self._closing is True

    @property
    def is_closed(self):
        return self.connection.is_closed

    @property
    def connection(self) -> RabbitmqConnectionWrapper:
        return self._connection

    @property
    def connection_config(self) -> dict:
        return self._connection_config

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def retries(self) -> int:
        return self._retries

    @property
    def attempt(self) -> int:
        return self._attempt

    def waiting_connection(self):
        is_running = False
        while not isinstance(self._connection, RabbitmqConnectionWrapper):
            if not is_running and not self.is_running:
                is_running = True
                self.run()
            continue
        return self

    def waiting_running(self):
        while not self.is_running:
            continue
        return self

    def waiting_connection_is_open(self):
        self.waiting_connection()
        while not self.is_open:
            continue
        return self

    def waiting_connection_is_closed(self):
        if isinstance(self._connection, RabbitmqConnectionWrapper):
            while not self.is_closed:
                continue
        return self

    def validate(self):
        pass

    def setup(self):
        self.setup_timeout()
        self.setup_retries()
        self.setup_connection_config()
        self.setup_connection()

    def setup_timeout(self):
        if self._timeout is None:
            self._timeout = self._config.get('timeout')
        self._timeout = self.timeout if isinstance(self.timeout, int) else None

    def setup_retries(self):
        if self._retries is None:
            self._retries = self._config.get('retries')
        self._retries = self.retries if isinstance(self.retries, int) else None

    def setup_connection_config(self):
        if self._connection_config is None:
            self._connection_config = {k: v for k, v in dict(self._config.get('connection_config', {})).items() if v is not None}
        else:
            self._connection_config = {k: v for k, v in dict(self._connection_config).items() if v is not None}

        parameters = self._connection_config.get('parameters', {})
        retries = self._connection_config.get('retries')
        timeout = self._connection_config.get('timeout')

        if not isinstance(parameters, (Parameters, dict)):
            parameters = {}

        if isinstance(parameters, dict):
            if self._connection_config.get('url') is not None:
                parameters = URLParameters(self._connection_config.get('url'))
            else:
                parameters = URLParameters('amqp://guest:guest@localhost:5672/%2F')

        self._connection_config['parameters'] = parameters
        self._connection_config['retries'] = int(retries if isinstance(retries, int) else DEFAULT_RABBITMQ_CONNECTION_RETRIES)
        self._connection_config['timeout'] = int(timeout if isinstance(timeout, int) else DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT)

    def setup_connection(self):
        if self.connection is None:
            self._connection = self._config.get('connection')

        if isinstance(self.connection, RabbitmqConnectionWrapper):
            self._connection_config['retries'] = self.connection.retries
            self._connection_config['timeout'] = self.connection.timeout
            self._connection_config['parameters'] = self.connection.parameters
        else:
            self._connection = None

    def on_connection_open_ok(self):
        pass

    def on_connection_open_error(self, err: Exception):
        raise err

    def on_connection_close(self, err: Exception):
        pass

    def connect(self):
        return RabbitmqConnectionWrapper(
            parameters=self.connection_config.get('parameters'),
            retries=int(self._connection_config.get('retries')),
            timeout=int(self._connection_config.get('timeout')),
            on_connection_open_ok_callback=self.on_connection_open_ok,
            on_connection_open_error_callback=self.on_connection_open_error,
            on_connection_close_callback=self.on_connection_close
        )

    def run(self, blocking: bool = None):
        if not self.is_running:
            self._running = True
            self._closing = False
            if not isinstance(self._connection, RabbitmqConnectionWrapper):
                self._connection = self.connect()
            self._connection.run(blocking)
        if blocking:
            self.waiting_connection_is_open()

    def stop(self, blocking: bool = None):
        self._closing = True
        if self.is_running and self.connection is not None:
            self._running = False
            self.connection.stop(blocking)
        self._running = False
        self._connection = None
        if blocking:
            self.waiting_connection_is_closed()

    def health_check(self) -> tuple:
        try:
            if not self.is_running:
                raise Exception('Rabbitmq connection is not running')
            if self.is_closed:
                raise Exception('Rabbitmq connection is closed')
            if not self.is_open:
                raise Exception('Rabbitmq connection is not open')
            return True, 'Success'
        except Exception as err:
            return False, str(err)
