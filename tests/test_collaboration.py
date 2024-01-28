from playwright.sync_api import BrowserContext, Page

from conftest import ServerInfo


def codemirror_value(page: Page):
    return page.evaluate("() => window.myEditor.getValue()")


def test_has_title(app_server: ServerInfo, context: BrowserContext):
    # Peter does this
    peters_page = context.new_page()
    peters_page.goto(app_server.uri)

    assert codemirror_value(peters_page) == ""

    peters_page.get_by_role("textbox").fill("Peter was here.")
    assert codemirror_value(peters_page) == "Peter was here."

    # Then Mary does this
    marys_page = context.new_page()
    marys_page.goto(app_server.uri)

    assert codemirror_value(marys_page) == "Peter was here."

    textfield = marys_page.get_by_role("textbox")
    textfield.focus()
    marys_page.keyboard.press("End")
    textfield.type(" Mary was here.")

    assert codemirror_value(marys_page) == "Peter was here. Mary was here."

    # Peter should then see this
    assert codemirror_value(peters_page) == "Peter was here. Mary was here."
