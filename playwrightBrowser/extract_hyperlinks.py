from __future__ import annotations

import json
from typing import Any, Type

from pydantic import BaseModel, Field

from .base import BaseBrowserTool
from .utils import (
    aget_current_page,
    get_current_page,
)
from urllib.parse import urljoin


class ExtractHyperlinksToolInput(BaseModel):
    """Input for ExtractHyperlinksTool."""

    absolute_urls: bool = Field(
        default=False,
        description="Return absolute URLs instead of relative URLs",
    )


class ExtractHyperlinksTool(BaseBrowserTool):
    """Extract all hyperlinks on the page."""

    name: str = "extract_hyperlinks"
    description: str = "Extract all hyperlinks on the current webpage"
    args_schema: Type[BaseModel] = ExtractHyperlinksToolInput

    @staticmethod
    def _format_links(links: set[str]) -> str:
        """Return a deterministic JSON array for the collected links."""
        return json.dumps(sorted(links))

    @staticmethod
    def _normalize_link(base_url: str, href: str, absolute_urls: bool) -> str:
        """Resolve relative URLs to absolute when requested."""
        return urljoin(base_url, href) if absolute_urls else href

    def _run(
        self,
        absolute_urls: bool = False
    ) -> str:
        """Use the tool."""
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        links: set[str] = set()
        for anchor in page.query_selector_all("a"):
            href = anchor.get_attribute("href")
            if not href:
                continue
            normalized = self._normalize_link(page.url, href, absolute_urls)
            links.add(normalized)
        return self._format_links(links)

    async def _arun(
        self,
        absolute_urls: bool = False
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        links: set[str] = set()
        anchors = await page.query_selector_all("a")
        for anchor in anchors:
            href = await anchor.get_attribute("href")
            if not href:
                continue
            normalized = self._normalize_link(page.url, href, absolute_urls)
            links.add(normalized)
        return self._format_links(links)
