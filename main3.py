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
from textual.message import Message
from stopwatch_textual.test2 import stopwatch, time_display
import pyglet, webbrowser, json
from datetime import datetime


class Waiting(Static):

    time_remaining = reactive(30.0)

    
    class RestComplete(Message):
        def __init__(self, waiting_id, set_id) -> None:
            super().__init__()
            self.waiting_id = waiting_id
            self.set_id = set_id


    def __init__(self, time_remaining, id, fps):
        super().__init__()
        self.id = id
        self.original_time_remainning = time_remaining
        self.time_remaining = time_remaining
        self.fps = fps


    def compose(self):
        self.progress_bar = ProgressBar(total=self.original_time_remainning - 1 / self.fps, show_percentage=True, show_eta=False, id="progress_bar")
        yield self.progress_bar
    
    def on_mount(self):
        """on mount"""
        self.update_timer = self.set_interval(1 /self.fps, self.update_time, pause=True)
        self.update_progressbarr = self.set_interval(1 / self.fps, self.update_progressbar, pause=True)

    def update_time(self):
        self.time_remaining -= 1/self.fps

    def update_progressbar(self):
        self.progress_bar.progress += 1/self.fps

    def watch_time_remaining(self):
        if self.time_remaining <= 0:
            self.stop()
            self.post_message(self.RestComplete(self.id, self.parent.id))
            self.time_remaining = self.original_time_remainning
        self.update(f"{self.time_remaining:02.2f}")

    def start(self):
        """start the timedisplay widget of the stopwatch"""
        if self.progress_bar.percentage == 1:
            self.progress_bar.progress = 0
        self.update_timer.resume()
        self.update_progressbarr.resume()

    def stop(self):
        """pause teh timedisplay widget""" 
        self.update_timer.pause()
        self.update_progressbarr.pause()
        print(self.progress_bar.progress)
    
    def reset(self):
        self.stop()
        self.progress_bar.progress = 0
        self.time_remaining = self.original_time_remainning


class TrainScreen(Screen):
    BINDINGS = [("q", "quit", "Quit training")]

    def __init__(self):
        super().__init__()
        self.title = pomodoroApp.input_dictionnary[-1]["title"]
        self.number_of_sets = int(pomodoroApp.input_dictionnary[-1]["nbr_sets"])
        self.rest_time_between_sets = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_sets"])
        self.number_of_exercices = int(pomodoroApp.input_dictionnary[-1]["nbr_exercises"])
        self.time_per_exercise = int(pomodoroApp.input_dictionnary[-1]["time_per_exercise"])
        self.rest_time_between_exercises = int(pomodoroApp.input_dictionnary[-1]["rest_time_between_exercises"])

    def compose(self):
        yield Footer()
        with TabbedContent():
            for i in range(1 , self.number_of_sets + 1):
                        pane = TabPane(f"set {i}", id="set{}".format(i))
                        for j in range(1, self.number_of_exercices + 1):
                            if j != self.number_of_exercices:
                                exercise = stopwatch(self.time_per_exercise, id="exercise{}".format(j))
                            else:
                                exercise = stopwatch(self.time_per_exercise, id="last_exercise")
                            label = Label(f"exercice {j}")
                            pane.mount(Center(label))
                            pane.mount(exercise)
                            if j != self.number_of_exercices:
                                pane.mount(Waiting(time_remaining=self.rest_time_between_exercises, id=f"waiting{j}", fps=20))
                        
                        if i == self.number_of_sets:
                            button = Button("return to home", id="return_to_home", classes="hidden")
                        else:
                            button = Button("next set", id="next_set", classes="hidden")

                        print("i value: {}".format(i))
                        print(button.id)
                        pane.mount(Center(button))
                        yield pane

    def action_quit(self):
        pomodoroApp.pop_screen(self=pomodoro)
        # delete the last element of the input dictionnary
        # so that the json doesn't save it into the progression file
        del pomodoro.input_dictionnary[-1]

    def on_time_display_all_progress_completed(self, message: time_display.AllProgressCompleted):
        """handle when the timedisplay completes"""
        print("will activate the next tab button")
        set_id = message.set_id
        print("value of the set id is {}".format(message.set_id))
        if self.extract_integers(set_id) != self.number_of_sets:
            self.query_one("#{}".format(message.set_id)).query_one("#next_set").remove_class("hidden")
        else:
            self.query_one("#{}".format(message.set_id)).query_one("#return_to_home").remove_class("hidden")
            # save the progression into the json file each
            # time we complete all the sets and exercises
            # also we add the current date and time so that when
            # populate the table in the progression we see the date
            # this training took place
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pomodoroApp.input_dictionnary[-1]["day"] = current_time.split(" ")[0]
            pomodoroApp.input_dictionnary[-1]["time"] = current_time.split(" ")[1]
            with open("progression.json", "a") as file:
                json.dump(pomodoro.input_dictionnary[-1], file)
                file.write('\n')
        self.scroll_end()
        
    
    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """handle when a time display completes its progression
        Args:
            message: the message posted by the time_display class for this special case
        """
        sound = pyglet.resource.media('start.wav')
        sound.play()

        exercise_id = message.exercicse_id
        if exercise_id != "last_exercise":
            self.query_one(f"#{message.set_id}").query_one(f"#waiting{self.extract_integers(exercise_id)}", Waiting).start()

    def on_waiting_rest_complete(self, message: Waiting.RestComplete):
        waiting_id = message.waiting_id
        try:
            self.query_one(f"#{message.set_id}").query_one(f"#exercise{self.extract_integers(waiting_id) + 1}", stopwatch).start_stopwatch()
        except Exception:
            self.query_one(f"#{message.set_id}").query_one(f"#last_exercise", stopwatch).start_stopwatch()

    def extract_integers(self, string):
        import re
        integers = re.findall(r'\d+', string)
        return int("".join([i for i in integers]))

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "return_to_home":
            pomodoroApp.pop_screen(self=pomodoro)
        elif button_id == "next_set":
            self.scroll_home()
            set_id = event.button.parent.parent.id
            self.switch_to_tabpane_by_id(f"set{self.extract_integers(set_id) + 1}")

    def switch_to_tabpane_by_id(self, id):
        """switches to a tab pane by id"""
        self.query_one(TabbedContent).active = id




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
            with TabPane("about", id="about"):
                with Center(id="about_misc"):
                    yield Button("source code", id="source_code")
                    yield Button("Home", id="return_to_home")
            with TabPane("progression", id="progression"):
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
                        yield Button("progression", id="progression_button")
                        yield Button("about", id="about_button")


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

        elif button_id == "about_button":
            self.show_tab_by_tabpane_id("about")
        elif button_id == "return_to_home":
            self.show_tab_by_tabpane_id("home")
        elif button_id == "source_code":
            webbrowser.open("https://github.com/Mrdrgh/Time_tracker")
        elif button_id == "progression_button":
            self.load_progression_data()
            self.show_tab_by_tabpane_id("progression")

    def show_tab_by_tabpane_id(self, tabpane_id):
        """swith to a tab"""
        self.query_one("#home_tabbed_content").active = tabpane_id

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


    def load_progression_data(self):
        try:
            with open("progression.json", "r") as file:
                data = []
                for line in file:
                    entry = json.loads(line)
                    entry["day"] = entry.get("day", "")  # Add the "day" key if not present
                    entry["time"] = entry.get("time", "")  # Add the "time" key if not present
                    data.append(entry)
                
                table = self.query_one("#progression_table", DataTable)
                table.clear(columns=True)
                table.add_columns("Day", "Time", "Title", "Number of Sets", "Number of Exercises", "Time per Exercise", "Rest Time Between Exercises", "Rest Time Between Sets")
                
                for entry in data:
                    table.add_row(
                        entry["day"],
                        entry["time"],
                        entry["title"],
                        str(entry["nbr_sets"]),
                        str(entry["nbr_exercises"]),
                        str(entry["time_per_exercise"]),
                        str(entry["rest_time_between_exercises"]),
                        str(entry["rest_time_between_sets"])
                    )
        except FileNotFoundError:
            pass  # Handle the case when the file doesn't exist yet

if __name__ == "__main__":
    pomodoro = pomodoroApp()
    pomodoro.run()