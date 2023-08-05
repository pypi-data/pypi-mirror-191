#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""

############ PEP 484 type annotations #############

"""

import copy
import json

from .queue import RabbitmqQueueBind
from .queue import RabbitmqQueueDeclare
from .exchange import RabbitmqExchangeBind
from .exchange import RabbitmqExchangeDeclare


def setup_exchange_declare(config: dict, exchange=None):
    if not isinstance(config.get('exchange_config'), dict):
        return
    exchange_config = copy.deepcopy(config.get('exchange_config'))
    if exchange_config.get('exchange') == exchange:
        return
    exchange = exchange or exchange_config.get('exchange')
    if not isinstance(exchange, str):
        return
    exchange_config['exchange'] = exchange
    exchange_declare = RabbitmqExchangeDeclare(
        connection_config=config.get('connection_config'),
        exchange_config=exchange_config
    )
    exchange_declare.run(True)
    exchange_declare.stop(True)
    exchange_declare = None


def setup_exchange_bind(config: dict, exchange_bind_config: dict = None):
    if json.dumps(exchange_bind_config, sort_keys=True) == json.dumps(config.get('exchange_bind_config'), sort_keys=True):
        return
    exchange_bind_config = exchange_bind_config or config.get('exchange_bind_config')
    if not isinstance(exchange_bind_config, dict):
        return
    exchange_bind_config['routing_key'] = exchange_bind_config.get('routing_key') or ''
    if not isinstance(exchange_bind_config.get('destination'), str):
        return
    if not isinstance(exchange_bind_config.get('source'), str):
        return
    if not isinstance(exchange_bind_config.get('routing_key'), str):
        return
    exchange_bind = RabbitmqExchangeBind(
        connection_config=config.get('connection_config'),
        exchange_bind_config=exchange_bind_config
    )
    exchange_bind.run(True)
    exchange_bind.stop(True)
    exchange_bind = None


def setup_queue_declare(config: dict, queue=None):
    if not isinstance(config.get('queue_config'), dict):
        return
    queue_config = copy.deepcopy(config.get('queue_config'))
    if queue_config.get('queue') == queue:
        return
    queue = queue or queue_config.get('queue')
    if not isinstance(queue, str):
        return

    queue_config['queue'] = queue
    queue_declare = RabbitmqQueueDeclare(
        connection_config=config.get('connection_config'),
        queue_config=queue_config
    )
    queue_declare.run(True)
    queue_declare.stop(True)
    queue_declare = None


def setup_queue_bind(config: dict, queue_bind_config: dict = None):
    if json.dumps(queue_bind_config, sort_keys=True) == json.dumps(config.get('queue_bind_config'), sort_keys=True):
        return
    queue_bind_config = queue_bind_config or config.get('queue_bind_config')
    if not isinstance(queue_bind_config, dict):
        return
    if not isinstance(queue_bind_config.get('queue'), str):
        return
    if not isinstance(queue_bind_config.get('exchange'), str):
        return
    queue_bind = RabbitmqQueueBind(
        connection_config=config.get('connection_config'),
        queue_bind_config=queue_bind_config
    )
    queue_bind.run(True)
    queue_bind.stop(True)
    queue_bind = None


def setup_dlq(config: dict):
    consumer_config = dict(config.get('consumer_config') or {})
    dlq = dict(consumer_config.get('dlq') or {})
    queue = dlq.get('queue')
    exchange = dlq.get('exchange')
    if not isinstance(queue, str):
        queue = consumer_config.get('queue') or config.get('queue')
        if queue is not None:
            queue = f'{queue}.dlq'
        else:
            return
    queue_bind_config = dlq.get('queue_bind_config') or {}
    if exchange is not None:
        setup_exchange_declare(config, exchange)
        queue_bind_config['exchange'] = queue_bind_config.get(
            'exchange') or exchange
    if queue is not None:
        setup_queue_declare(config, queue)
        queue_bind_config['queue'] = queue_bind_config.get('queue') or queue
        queue_bind_config['routing_key'] = queue_bind_config.get('routing_key') or queue
    setup_queue_bind(config, queue_bind_config)
