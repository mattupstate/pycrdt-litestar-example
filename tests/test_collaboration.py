from playwright.sync_api import BrowserContext, Page, expect

from conftest import ServerInfo


def test_has_title(app_server: ServerInfo, context: BrowserContext):
    # Peter does this
    first_page = context.new_page()
    first_page.goto(app_server.uri)

    codemirror_value = first_page.evaluate("() => window.myEditor.getValue()")
    assert codemirror_value == "", "codemirror should be empty"
    first_page.get_by_role("textbox").fill("Peter")
    codemirror_value = first_page.evaluate("() => window.myEditor.getValue()")
    assert codemirror_value == "Peter"

    # Then Mary does this
    second_page = context.new_page()
    second_page.goto(app_server.uri)

    codemirror_value = second_page.evaluate("() => window.myEditor.getValue()")
    assert codemirror_value == "Peter"

    textfield = second_page.get_by_role("textbox")
    textfield.focus()
    second_page.keyboard.press("End")
    textfield.type(" Mary")

    codemirror_value = second_page.evaluate("() => window.myEditor.getValue()")
    assert codemirror_value == "Peter Mary"

    # Then Peter should also see this
    codemirror_value = first_page.evaluate("() => window.myEditor.getValue()")
    assert codemirror_value == "Peter Mary"
