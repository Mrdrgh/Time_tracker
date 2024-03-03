from time import monotonic
from textual import on
from textual.app import App, ComposeResult
from textual.events import Mount
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static
from textual.widgets import Input, Label, ProgressBar
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import TabbedContent, TabPane
from textual.widget import Widget
from stopwatch_textual.test import stopwatch, time_display
class Train(Static):

    def __init__(self):
        super().__init__()
        self.title = ""
        self.number_of_sets = 1
        self.rest_time_between_sets : float = 0
        self.number_of_exercices : int = 3
        self.rest_time_between_exercises : float = 0


    def compose(self):
        new_tabbed_content = TabbedContent(id=f"tabbed_content_train{pomodoroApp.number_of_tabs + 1}")
        with new_tabbed_content:
            if self.number_of_sets:
                for i in range(2):
                    pane = TabPane(f"train{i}", id="train{}".format(i))
                    for i in range(self.number_of_exercices):
                        exercise = stopwatch()
                        label = Label(f"exercice {i}")
                        pane.mount(label)
                        pane.mount(exercise)
                    yield pane

class pomodoroApp(App):
    CSS_PATH = "pomodoro.css"

    number_of_tabs = 0
    def compose(self):
        self.training_title = Input(placeholder="e.g leg day")
        self.nbr_sets = Input(placeholder="number of sets")
        self.rest_time_between_sets = Input(placeholder="rest time between sets")
        self.nbr_exercises = Input(placeholder="number of exercises")
        self.rest_time_between_exercises = Input(placeholder="rest time between exercises")


        yield Header(show_clock=True)
        with TabbedContent(initial="home", id="home_tabbed_content"):
            with TabPane("progression", id="progression"):
                yield Button("🛖️", id="return_to_home")
            with TabPane("home", id="home"):
                with Static(id="input_div"):
                    yield self.training_title
                    yield self.nbr_sets
                    yield self.rest_time_between_sets
                    yield self.nbr_exercises
                    yield self.rest_time_between_exercises
                    with Center():
                        yield Button("start_training", id="train_button")
                        yield Button("progression", id="progression")



    def on_button_pressed(self, event: Button.Pressed) -> None:
        """ the handler for the pressing of a button"""
        button_id = event.button.id
        if button_id == "train_button":
            tabbed_content = self.query_one("#home_tabbed_content")
            pane = TabPane(f"set {tabbed_content.tab_count + 1}", id=f"set{tabbed_content.tab_count + 1}")
            self.number_of_tabs = tabbed_content.tab_count + 1
            tabbed_content.add_pane(pane)
            new_train = Train()
            pane.mount(new_train)
            self.show_tab_by_tabpane_id(f"{pane.id}")

        elif button_id == "progression":
            self.show_tab_by_tabpane_id("progression")
        elif button_id == "return_to_home":
            self.show_tab_by_tabpane_id("home")

    def show_tab_by_tabpane_id(self, tabpane_id):
        """swith to a tab"""
        self.query_one("#home_tabbed_content").active = tabpane_id

    def add_pane(self):
        """ add a pane and return it's id
        Args:
            self: the big mamaaaa hhh
        Return: the pane id
        """
        tabbed_content = self.query_one(TabbedContent)
        pane_id = f"set{tabbed_content.tab_count + 1}"
        pane = TabPane(f"set {tabbed_content.tab_count + 1}", id=pane_id)
        tabbed_content.add_pane(pane)
        return pane_id


if __name__ == "__main__":
    pomodoro = pomodoroApp()
    pomodoro.run()