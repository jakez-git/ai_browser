from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..core.config import get_settings


class EventHandler(Protocol):
    async def handle_create(self, path: Path) -> None: ...

    async def handle_modify(self, path: Path) -> None: ...

    async def handle_delete(self, path: Path) -> None: ...


@dataclass
class WatchService:
    """Watch the knowledge base directory for changes."""

    root: Path
    handler: EventHandler | None = None

    async def start(self) -> None:
        # TODO: integrate watchdog/async watcher implementation
        if self.handler is None:
            raise ValueError("Event handler must be configured before starting watcher")

    @classmethod
    def get_default_root(cls) -> Path:
        settings = get_settings()
        return settings.paths.knowledge_root


def get_watch_service(handler: EventHandler | None = None) -> WatchService:
    return WatchService(root=WatchService.get_default_root(), handler=handler)
