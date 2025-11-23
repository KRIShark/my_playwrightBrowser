from playwright.sync_api import sync_playwright
from playwrightBrowser import NavigateTool, ExtractTextTool

with sync_playwright() as p:
    browser = p.chromium.launch()
    navigate = NavigateTool(sync_browser=browser)
    navigate.run(url="https://example.com")
    reader = ExtractTextTool(sync_browser=browser)
    print(reader.run())