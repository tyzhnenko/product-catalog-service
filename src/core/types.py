from contextlib import AsyncExitStack, _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any, Callable

from fastapi import FastAPI


class FastAPIServices:
    on_startups: list[Callable[[], Any]] | None = []
    on_shutdowns: list[Callable[[], Any]] | None = []
    lifespans: list[Callable[[FastAPI], _AsyncGeneratorContextManager[Any, None]]] | None = []

    def add_startup_handler(self, handler: Callable[[], Any]) -> None:
        if self.on_startups is None:
            self.on_startups = []
        self.on_startups.append(handler)

    def add_shutdown_handler(self, handler: Callable[[], Any]) -> None:
        if self.on_shutdowns is None:
            self.on_shutdowns = []
        self.on_shutdowns.append(handler)

    def add_lifespan(self, lifespan: Callable[[FastAPI], _AsyncGeneratorContextManager[Any, None]]) -> None:
        if self.lifespans is None:
            self.lifespans = []
        self.lifespans.append(lifespan)

    def build_combined_lifespan(self) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any, None]]:
        """Run all registered lifespan context managers together."""

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):
            context_managers = []
            if self.lifespans:
                for lifespan in self.lifespans:
                    context_managers.append(lifespan(app))

            async with AsyncExitStack() as stack:
                for mgr in context_managers:
                    await stack.enter_async_context(mgr)

                yield

        return combined_lifespan
