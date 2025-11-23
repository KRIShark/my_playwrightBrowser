# my_playwrightBrowser
PlaywrightBrowser is a tiny toolkit of Playwright-backed browser tools. It wraps common actions such as navigation, element inspection, hyperlink extraction, and page text collection in Pydantic-friendly tools so you can plug them straight into agent frameworks, CLI helpers, or automation scripts.
Original at https://github.com/microsoft/playwright

## Installation

Install directly from this repository:

```sh
pip install .
```

Or, if you prefer `uv` to manage dependencies in lock-step:

```sh
uv install
```

After installation the package exposes all tools under the `playwrightBrowser` namespace.

## Usage

Here's a minimal synchronous example:

```py
from playwright.sync_api import sync_playwright
from playwrightBrowser import NavigateTool, ExtractTextTool

with sync_playwright() as p:
    browser = p.chromium.launch()
    navigate = NavigateTool(sync_browser=browser)
    navigate.run(url="https://example.com")
    reader = ExtractTextTool(sync_browser=browser)
    print(reader.run())
```

The package also exposes asynchronous helpers (`aget_current_page`, `create_async_playwright_browser`, etc.) if you need async control.

## Tools

- `NavigateTool` / `NavigateBackTool`
- `ExtractTextTool`
- `ExtractHyperlinksTool`
- `GetElementsTool`
- `ClickTool`
- `CurrentWebPageTool`

## Development

- `pip install -e .` to work locally with editable installs.
- `uv install` keeps dependencies locked to `uv.lock`.

Each module is located under the `playwrightBrowser` package, so installers such as `pip` and `uv` can discover the package automatically.
