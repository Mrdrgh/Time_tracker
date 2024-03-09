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
from textual.widgets import TabbedContent, TabPane, DataTable
from textual.widget import Widget
from textual.screen import Screen
from stopwatch_textual.test2 import stopwatch, time_display
import webbrowser


class TrainScreen(Screen):

    def __init__(self):
        super().__init__()
        self.title = pomodoroApp.input_dictionnary[-1]["title"]
        self.number_of_sets = int(pomodoroApp.input_dictionnary[-1]["nbr_sets"])
        self.rest_time_between_sets = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_sets"])
        self.number_of_exercices = int(pomodoroApp.input_dictionnary[-1]["nbr_exercises"])
        self.time_per_exercise = int(pomodoroApp.input_dictionnary[-1]["time_per_exercise"])
        self.rest_time_between_exercises = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_exercises"])

    def compose(self):
        with TabbedContent():
            for i in range(1 , self.number_of_sets + 1):
                        pane = TabPane(f"set {i}", id="set{}".format(i))
                        for j in range(1, self.number_of_exercices + 1):
                            if j != self.number_of_exercices:
                                exercise = stopwatch(self.time_per_exercise, id="exercise{}".format(j))
                            else:
                                exercise = stopwatch(self.time_per_exercise, id="last_exercise")
                            label = Label(f"exercice {j}")
                            pane.mount(label)
                            pane.mount(exercise)
                        
                        if i == self.number_of_sets:
                            button = Button("return to home", id="return_to_home", classes="hidden")
                        else:
                            button = Button("next set", id="next_set", classes="hidden")

                        print("i value: {}".format(i))
                        print(button.id)
                        pane.mount(Center(button))
                        yield pane

    def on_time_display_all_progress_completed(self, message: time_display.AllProgressCompleted):
        """handle when the timedisplay completes"""
        print("will activate the next tab button")
        set_id = message.set_id
        print("value of the set id is {}".format(message.set_id))
        if self.extract_integers(set_id) != self.number_of_sets:
            self.query_one("#{}".format(message.set_id)).query_one("#next_set").remove_class("hidden")
        else:
            self.query_one("#{}".format(message.set_id)).query_one("#return_to_home").remove_class("hidden")
    
    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """handle when a time display completes its progression
        Args:
            message: the message posted by the time_display class for this special case
        """
        exercise_id = message.exercicse_id
        if exercise_id != "last_exercise":
            next_exercise = "exercise{}".format(self.extract_integers(exercise_id) + 1)
            try:
                self.query_one(f"#{message.set_id}").query_one("#{}".format(next_exercise), stopwatch).start_stopwatch()
            except Exception:
                self.query_one(f"#{message.set_id}").query_one("#last_exercise", stopwatch).start_stopwatch()
    
    def extract_integers(self, string):
        import re
        integers = re.findall(r'\d+', string)
        return int("".join([i for i in integers]))

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "return_to_home":
            pomodoroApp.pop_screen(self=pomodoro)


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
        with TabbedContent(id=f"tabbed_content_train{pomodoroApp.number_of_tabs + 1}"):
            for i in range(1 , self.number_of_sets + 1):
                pane = TabPane(f"set {i}", id="set{}".format(i))
                for j in range(1, self.number_of_exercices + 1):
                    if j != self.number_of_exercices:
                        exercise = stopwatch(self.time_per_exercise, id="exercise{}".format(j))
                    else:
                        exercise = stopwatch(self.time_per_exercise, id="last_exercise")
                    label = Label(f"exercice {j}")
                    pane.mount(label)
                    pane.mount(exercise)
                
                if i == self.number_of_sets:
                    button = Button("return to home", id="return_to_home", classes="hidden")
                else:
                    button = Button("next set", id="next_set", classes="hidden")

                print("i value: {}".format(i))
                print(button.id)
                pane.mount(Center(button))
                yield pane

    def on_time_display_all_progress_completed(self, message: time_display.AllProgressCompleted):
        """handle when the timedisplay completes"""
        print("will activate the next tab button")
        set_id = message.set_id
        print("value of the set id is {}".format(message.set_id))
        if self.extract_integers(set_id) != self.number_of_sets:
            self.query_one("#{}".format(message.set_id)).query_one("#next_set").remove_class("hidden")
        else:
            self.query_one("#{}".format(message.set_id)).query_one("#return_to_home").remove_class("hidden")
    
    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """handle when a time display completes its progression
        Args:
            message: the message posted by the time_display class for this special case
        """
        exercise_id = message.exercicse_id
        if exercise_id != "last_exercise":
            next_exercise = "exercise{}".format(self.extract_integers(exercise_id) + 1)
            try:
                self.query_one(f"#{message.set_id}").query_one("#{}".format(next_exercise), stopwatch).start_stopwatch()
            except Exception:
                self.query_one(f"#{message.set_id}").query_one("#last_exercise", stopwatch).start_stopwatch()
    
    def extract_integers(self, string):
        import re
        integers = re.findall(r'\d+', string)
        return int("".join([i for i in integers]))

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "return_to_home":
            pomodoro.show_tab_by_tabpane_id("home")
     
class pomodoroApp(App):
    CSS_PATH = "pomodoro.tcss"
    Progression_cols = ["day", "training title", "sets trained", "exercises trained"]
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
                with Static(id="progression_misc"):
                    yield Button("source code", id="source_code")
                    yield Button("Home", id="return_to_home")
                with Static(id="progression_data"):
                    yield DataTable(id="progression_table")
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

    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """bell a sound when the progress of a time_display is completed"""
        # TODO: make a better sound, this one sucks
        self.bell()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """ the handler for the pressing of a button"""
        button_id = event.button.id
        if button_id == "train_button":
            temp_dict = self.load_input_value() #temporary dictionnary for the user_input
            if temp_dict is not None:
                self.input_dictionnary.append(temp_dict)

                self.reset_input_value()
                new_screen = TrainScreen()
                self.push_screen(new_screen)
            else:
                self.notify(message="complete all fields", severity="warning", timeout=2)

        elif button_id == "progression":
            print("moved to progression")
            self.show_tab_by_tabpane_id("progression_tab_pane")
        elif button_id == "return_to_home":
            self.show_tab_by_tabpane_id("home")
        elif button_id == "source_code":
            webbrowser.open("https://github.com/Mrdrgh/Time_tracker")

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
        self.title = self.training_title.value
        print("title value in load input value: {}".format(self.title)) # debugg
        nbr_sets = self.nbr_sets.value
        rest_time_between_sets = self.rest_time_between_sets.value
        nbr_exercises = self.nbr_exercises.value
        time_per_exercise = self.time_per_exercise.value
        rest_time_between_exercises = self.rest_time_between_exercises.value
        dict = {}
        dict["title"] = self.title
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