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
from stopwatch_textual.test2 import stopwatch, time_display
class Train(Static):

    def __init__(self):
        super().__init__()
        self.title = pomodoroApp.input_dictionnary[-1]["title"]
        self.number_of_sets = int(pomodoroApp.input_dictionnary[-1]["nbr_sets"])
        self.rest_time_between_sets = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_sets"])
        self.number_of_exercices = int(pomodoroApp.input_dictionnary[-1]["nbr_exercises"])
        self.time_per_exercise = int(pomodoroApp.input_dictionnary[-1]["time_per_exercise"])
        self.rest_time_between_exercises = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_exercises"])


    def compose(self):
        new_tabbed_content = TabbedContent(id=f"tabbed_content_train{pomodoroApp.number_of_tabs + 1}")
        with new_tabbed_content:
            for i in range(1 , self.number_of_sets + 1):
                pane = TabPane(f"set {i}", id="set{}".format(i))
                for i in range(1, self.number_of_exercices + 1):
                    if i != self.number_of_exercices:
                        exercise = stopwatch(self.time_per_exercise, id="exercise{}".format(i))
                    else:
                        exercise = stopwatch(self.time_per_exercise, id="last_exercise")
                    label = Label(f"exercice {i}")
                    pane.mount(label)
                    pane.mount(exercise)
                    button = Button("next set", disabled=True, id="next_set{}".format(i))
                pane.mount(Center(button))
                yield pane
    def enable_next_set_button(self):
        self.query_one("#next_set").disabled = False
    def handle_all_exercises_complete(self):
        """self explanatory"""
        list = []
        for i in range(1, self.number_of_exercices + 1):
            list.append(self.query_one("#exercise{}".format(i)))
        for i in list:
            Time_display = i.query_one(time_display)
            if Time_display.query_one(ProgressBar).progress != 1:
                return
        self.notify(message="set {} complete")
     
class pomodoroApp(App):
    CSS_PATH = "pomodoro.tcss"

    number_of_tabs = 0

    input_dictionnary = [{}]
    def compose(self):
        self.training_title = Input(placeholder="e.g leg day", type="text", max_length=7, id="title")
        self.nbr_sets = Input(placeholder="number of sets", type="integer", id="nbr_sets")
        self.rest_time_between_sets = Input(placeholder="rest time between sets", type="number", id="rest_time_between_sets")
        self.nbr_exercises = Input(placeholder="number of exercises", type="integer", id="nbr_exercises")
        self.time_per_exercise = Input(placeholder="time per exercise", type="integer", id="time_per_exercise")
        self.rest_time_between_exercises = Input(placeholder="rest time between exercises", type="number", id="rest_time_between_exercises")


        yield Header(show_clock=True)
        with TabbedContent(initial="home", id="home_tabbed_content"):
            with TabPane("progression", id="progression_tab_pane"):
                yield Button("🛖️", id="return_to_home")
            with TabPane("home", id="home"):
                with Static(id="input_div"):
                    yield self.training_title
                    yield self.nbr_sets
                    yield self.rest_time_between_sets
                    yield self.nbr_exercises
                    yield self.time_per_exercise
                    yield self.rest_time_between_exercises
                    with Center():
                        yield Button("start_training", id="train_button")
                        yield Button("progression", id="progression")



    def on_button_pressed(self, event: Button.Pressed) -> None:
        """ the handler for the pressing of a button"""
        button_id = event.button.id
        if button_id == "train_button":
            temp_dict = self.load_input_value()
            if temp_dict is not None:
                self.input_dictionnary.append(temp_dict)
                print("successful")
                print(temp_dict)
                self.reset_input_value()
                tabbed_content = self.query_one("#home_tabbed_content")
                print(self.training_title.value)
                if self.training_title.value != '':
                    training_title = self.training_title
                    pane = TabPane(f"{training_title}", id=f"train{tabbed_content.tab_count - 1}")
                pane = TabPane(f"train {tabbed_content.tab_count - 1}", id=f"train{tabbed_content.tab_count - 1}")
                self.number_of_tabs = tabbed_content.tab_count + 1
                tabbed_content.add_pane(pane)
                new_train = Train()
                pane.mount(new_train)
                self.show_tab_by_tabpane_id(f"{pane.id}")
            else:
                self.notify(message="complete all fields", severity="warning", timeout=2)

        elif button_id == "progression":
            print("moved to progression")
            self.show_tab_by_tabpane_id("progression_tab_pane")
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

    def reset_input_value(self):
        self.training_title.clear()
        self.nbr_sets.clear()
        self.rest_time_between_sets.clear()
        self.nbr_exercises.clear()
        self.rest_time_between_exercises.clear()
        self.time_per_exercise.clear()

    def load_input_value(self):
        title = self.training_title.value
        nbr_sets = self.nbr_sets.value
        rest_time_between_sets = self.rest_time_between_sets.value
        nbr_exercises = self.nbr_exercises.value
        time_per_exercise = self.time_per_exercise.value
        rest_time_between_exercises = self.rest_time_between_exercises.value
        dict = {}
        dict["title"] = title
        dict["nbr_sets"] = nbr_sets
        dict["nbr_exercises"] = nbr_exercises
        dict["time_per_exercise"] = time_per_exercise
        dict["rest_time_between_exercises"] = rest_time_between_exercises
        dict["rest_time_between_sets"] = rest_time_between_sets
        self.input_dictionnary.append(dict)
        for i in self.input_dictionnary[-1]:
            print(i)
            if not self.input_dictionnary[-1][i]:
                del self.input_dictionnary[-1]
                return None
        return self.input_dictionnary[-1]



if __name__ == "__main__":
    pomodoro = pomodoroApp()
    pomodoro.run()