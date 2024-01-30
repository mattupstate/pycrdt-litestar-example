from playwright.sync_api import BrowserContext, Page

from conftest import ServerInfo


class EditorPage(Page):
    def __init__(self, context: BrowserContext, goto: str) -> None:
        self._page: Page = context.new_page()
        self._page.goto(goto)

    @property
    def editor_content(self):
        return self._page.evaluate("() => window.myEditor.getValue()")

    def fill_editor(self, content: str):
        self._page.get_by_role("textbox").fill(content)

    def append_editor(self, content: str):
        textfield = self._page.get_by_role("textbox")
        textfield.focus()
        self._page.keyboard.press("End")
        textfield.type(content)

    def __getattr__(self, name):
        return getattr(self._page, name)


def test_has_title(app_server: ServerInfo, context: BrowserContext):
    # Peter and Mary each open the editor
    peter = EditorPage(context, app_server.uri)
    mary = EditorPage(context, app_server.uri)

    # When Peter leaves a note
    peter.fill_editor("Peter was here.")
    # Then Mary should see Peter's note
    assert mary.editor_content == "Peter was here."

    # When Mary appends Peter's note
    mary.append_editor(" Mary was here.")
    # Then Peter should see both notes
    assert peter.editor_content == "Peter was here. Mary was here."
