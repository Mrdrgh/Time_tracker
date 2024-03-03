from time import monotonic
from textual import on
from textual.app import App, ComposeResult
from textual.events import Mount, Key
from textual.reactive import reactive
from textual.containers import ScrollableContainer, Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Static, ProgressBar, Markdown

class Waiting(Static):
    """the actual waiting div for waiting between exercises"""
    def compose(self):
            with Static(id="progress_container"):
                yield ProgressBar(total=100, show_eta=False, id="waiting_progressbar")
                yield Mar


class WaitingApp(App):
    """a waiting div between exercises"""
    CSS = """
#progress_container {
    width: 100%;
    align: center middle;

}
#waiting_progressbar {
    width: 100%
}
#waiting_progressbar #bar {
    width: 90%;
}
Waiting {
    layout: horizontal;
    padding: 1;
    margin: 1;
    background: $boost;
    min-width: 60;
    height: 4;
}
"""
    def compose(self):
        yield Waiting()





if __name__ == "__main__":
    WaitingApp().run()