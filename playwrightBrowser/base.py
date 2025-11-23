# base.py
from __future__ import annotations
from typing import Any, Optional, Tuple, TYPE_CHECKING
from pydantic import BaseModel, model_validator

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser
    from playwright.sync_api import Browser as SyncBrowser
else:
    AsyncBrowser = Any
    SyncBrowser = Any

def lazy_import_playwright_browsers() -> Tuple[type, type]:
    """Lazy import to avoid hard deps at import-time."""
    from playwright.async_api import Browser as A
    from playwright.sync_api import Browser as S
    return A, S

class BaseBrowserTool(BaseModel):
    """Base class for browser tools (framework-agnostic)."""

    sync_browser: Optional["SyncBrowser"] = None
    async_browser: Optional["AsyncBrowser"] = None

    @model_validator(mode="before")
    @classmethod
    def _validate_browser(cls, values: dict) -> Any:
        lazy_import_playwright_browsers()
        if values.get("async_browser") is None and values.get("sync_browser") is None:
            raise ValueError("Either async_browser or sync_browser must be specified.")
        return values

    @classmethod
    def from_browser(
        cls,
        sync_browser: Optional["SyncBrowser"] = None,
        async_browser: Optional["AsyncBrowser"] = None,
    ) -> "BaseBrowserTool":
        lazy_import_playwright_browsers()
        return cls(sync_browser=sync_browser, async_browser=async_browser)

    def run(self, **kwargs: Any) -> Any:
        return self._run(**kwargs)

    async def arun(self, **kwargs: Any) -> Any:
        return await self._arun(**kwargs)

    def _run(self, *args: Any, **kwargs: Any) -> Any:  # to override
        raise NotImplementedError

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:  # to override
        raise NotImplementedError
