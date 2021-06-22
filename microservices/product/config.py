"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    PostgreSqlRepository,
    PostgreSqlSnapshot,
)
from minos.networks import (
    CommandBroker,
    CommandConsumerService,
    CommandHandlerService,
    CommandReplyBroker,
    CommandReplyConsumerService,
    CommandReplyHandlerService,
    EventBroker,
    EventConsumerService,
    EventHandlerService,
    ProducerService,
    RestService,
    SnapshotService,
)
from minos.saga import (
    SagaManager,
)

injections = {
    "command_broker": CommandBroker,
    "command_reply_broker": CommandReplyBroker,
    "event_broker": EventBroker,
    "repository": PostgreSqlRepository,
    "saga_manager": SagaManager,
    "snapshot": PostgreSqlSnapshot,
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
