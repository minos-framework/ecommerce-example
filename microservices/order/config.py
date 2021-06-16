"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import PostgreSqlMinosRepository
from minos.networks import CommandBroker
from minos.networks import CommandConsumerService
from minos.networks import CommandHandlerService
from minos.networks import CommandReplyBroker
from minos.networks import CommandReplyConsumerService
from minos.networks import CommandReplyHandlerService
from minos.networks import EventBroker
from minos.networks import EventConsumerService
from minos.networks import EventHandlerService
from minos.networks import ProducerService
from minos.networks import RestService
from minos.networks import SnapshotService
from minos.saga import SagaManager

injections = {
    "command_broker": CommandBroker,
    "command_reply_broker": CommandReplyBroker,
    "event_broker": EventBroker,
    "repository": PostgreSqlMinosRepository,
    "saga_manager": SagaManager,
}

services = [
    CommandConsumerService,
    CommandHandlerService,
    CommandReplyConsumerService,
    CommandReplyHandlerService,
    EventConsumerService,
    EventHandlerService,
    RestService,
    SnapshotService,
    ProducerService,
]
