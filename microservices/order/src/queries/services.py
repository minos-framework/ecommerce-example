"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import UUID

from minos.common import (
    AggregateDiff,
    Event,
    MinosSagaManager,
    ModelType,
    Service,
    import_module,
    Model,
    classname,
)

# from minos.networks import (
#     subscribe,
# )

from minos.saga import (
    Saga,
    SagaContext,
    SagaExecution,
)


async def _handler(saga_manager: MinosSagaManager, diff: AggregateDiff, fn):
    execution = _build_saga_execution(diff, fn)
    # noinspection PyProtectedMember,PyUnresolvedReferences
    return await saga_manager._run(execution)


def _build_saga_execution(diff, fn):
    missing = _get_missing(diff)
    definition = _build_saga(missing)
    execution = SagaExecution.from_saga(
        definition, context=SagaContext(diff=diff, controller=classname(type(fn.__self__)), action=fn.__name__)
    )
    return execution


def _get_missing(diff: AggregateDiff) -> dict[str, list[UUID]]:
    return {
        "Product": diff.fields_diff.products,
        "Ticket": [diff.fields_diff.ticket]
    }


def _build_saga(missing: dict[str, list[UUID]]) -> Saga:
    saga = Saga("ordersQuery")

    for name, uuids in missing.items():
        saga = saga.step().invoke_participant(f"Get{name}s", _invoke_callback, uuids=uuids).on_reply(f"{name}s")

    saga = saga.commit(_build_commit_callback)

    return saga


# noinspection PyUnusedLocal
def _invoke_callback(context: SagaContext, uuids: list[UUID]):
    return ModelType.build("Query", {"uuids": list[UUID]})(uuids=uuids)


async def _build_commit_callback(context: SagaContext) -> SagaContext:
    diff = context["diff"]
    recovered = _build_recovered(context)
    diff = _put_missing(diff, recovered)

    controller = import_module(context["controller"])
    controller = controller()
    fn = getattr(controller, context["action"])
    await fn(diff)
    return context


def _build_recovered(context: SagaContext) -> dict[UUID, Model]:
    recovered = dict()
    for k in context.keys():
        if k in ("diff", "controller", "action"):
            continue
        for v in context[k]:
            recovered[v.uuid] = v
    return recovered


def _put_missing(diff: AggregateDiff, recovered: dict[UUID, Model]) -> AggregateDiff:
    diff.fields_diff.products = [recovered[uuid] for uuid in diff.fields_diff.products]
    diff.fields_diff.ticket = recovered[diff.fields_diff.ticket]
    return diff


class OrderQueryService(Service):
    """TODO"""

    # @subscribe("OrderAdded")
    async def order_created(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        await _handler(self.saga_manager, event.data, self._order_created)

    async def _order_created(self, diff) -> NoReturn:
        """TODO

        :param diff: TODO
        :return: TODO
        """
        print(diff)

    # @subscribe("OrderUpdated")
    async def order_updated(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("OrderDeleted")
    async def order_deleted(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)
