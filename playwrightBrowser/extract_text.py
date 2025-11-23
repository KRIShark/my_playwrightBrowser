from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel

from .base import BaseBrowserTool
from .utils import (
    aget_current_page,
    get_current_page,
)


class ExtractTextToolInput(BaseModel):
    """Explicit no-args input for ExtractTextTool."""


class ExtractTextTool(BaseBrowserTool):
    """Tool for extracting all the text on the current webpage."""

    name: str = "extract_text"
    description: str = "Extract all the text on the current webpage"
    args_schema: Type[BaseModel] = ExtractTextToolInput

    @staticmethod
    def _get_element_text(page: Any, selector: str) -> str:
        from playwright.sync_api import Error as PlaywrightError

        try:
            return page.inner_text(selector)
        except PlaywrightError:
            return ""

    @staticmethod
    async def _aget_element_text(page: Any, selector: str) -> str:
        from playwright.async_api import Error as PlaywrightError

        try:
            return await page.inner_text(selector)
        except PlaywrightError:
            return ""

    @classmethod
    def _collect_text(cls, page: Any) -> str:
        for selector in ("body", "html"):
            text = cls._get_element_text(page, selector)
            if text:
                return text
        return page.content()

    @classmethod
    async def _acollect_text(cls, page: Any) -> str:
        for selector in ("body", "html"):
            text = await cls._aget_element_text(page, selector)
            if text:
                return text
        return await page.content()

    def _run(self) -> str:
        """Use the tool."""
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        return self._collect_text(page)

    async def _arun(
        self
    ) -> str:
        """Use the tool."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        return await self._acollect_text(page)
