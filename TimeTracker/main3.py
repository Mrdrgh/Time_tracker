from time import monotonic
from textual import on
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static
from textual.widgets import Input, Label, ProgressBar
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import TabbedContent, TabPane, DataTable, MarkdownViewer
from textual.screen import Screen
from textual.message import Message
import pyglet, webbrowser, json
from datetime import datetime

class time_display(Static):
    # time_elapsed = reactive(0)
    # start_time = monotonic()
    # accum_time = 0
    # def on_mount(self):
    #     """execute the uptade time elapsed method every frame per seconde"""

    #     self.update_timer = self.set_interval(1 / 60, self.update_time_elapsed, pause=True)


    # def watch_time_elapsed(self):
    #     time = self.time_elapsed
    #     time, seconds = divmod(time, 60)
    #     hours, minutes = divmod(time, 60)
    #     time_string = f'{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}'
    #     self.update(time_string)

    # def start(self):
    #     """start the stopwatch"""
    #     self.start_time = monotonic()
    #     self.update_timer.resume()

    # def stop(self):
    #     """stop the sstopwatch"""
    #     self.update_timer.pause()
    #     self.accum_time = self.time_elapsed
    
    # def reset(self):
    #     """reset the stop watch"""
    #     self.stop()
    #     self.time_elapsed = 0
    #     self.accum_time = 0
    
    # def update_time_elapsed(self):
    #     self.time_elapsed = self.accum_time + ( monotonic() - self.start_time)

    time_remaining = reactive(30.0)
    allProgressCompleted = False

    class AllProgressCompleted(Message):
        def __init__(self, set_id) -> None:
            super().__init__()
            self.set_id = set_id
    
    class CurrentProgressCompleted(Message):
        def __init__(self, exercise_id, set_id, tabbed_content_id) -> None:
            super().__init__()
            self.exercicse_id = exercise_id
            self.set_id = set_id
            self.tabbed_content_id = tabbed_content_id
        ...

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


    def handle_all_exercises_complete(self):
        if self.id == "last_time_d" and not self.allProgressCompleted:
            self.allProgressCompleted = True
            self.notify("set complete")
            # TODO: post a message to the parent(stopwatch)
            self.post_message(self.AllProgressCompleted(self.parent.parent.id))
            print("posted message from timedisplay")

    def watch_time_remaining(self):
        if self.time_remaining <= 0:
            self.stop()
            print(self.id)
            self.post_message(self.CurrentProgressCompleted(self.parent.id,
                                                            self.parent.parent.id,
                                                            self.parent.parent.parent.parent.id)) #post a message that the current progress is completed
            print(self.parent.id)
            self.handle_all_exercises_complete() 
            self.time_remaining = self.original_time_remainning
        self.update(f"{self.time_remaining:02.2f}")
    def start(self):
        """start the timedisplay widget of the stopwatch"""
        import pyglet
        self.scroll_visible(top=True)
        sound = pyglet.resource.media('src/ping.mp3')
        sound.play()
        if self.progress_bar.percentage == 1:
            self.progress_bar.progress = 0
        self.update_timer.resume()
        self.update_progressbarr.resume()

    def stop(self):
        """pause teh timedisplay widget""" 
        self.update_timer.pause()
        self.update_progressbarr.pause()
    
    def reset(self):
        self.stop()
        self.progress_bar.progress = 0
        self.time_remaining = self.original_time_remainning

        


class stopwatch(Static):

    class ExerciseStarted(Message):
        def __init__(self, id, set_id):
            super().__init__()
            self.id = id
            self.set_id = set_id

    def __init__(self, time_remaining, id):
        super().__init__()
        self.time_remaining = time_remaining
        self.id = id
    
    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "start":
            self.start_stopwatch()
        elif button_id == "stop":
            self.stop_stopwatch()
        elif button_id == "reset":
            self.reset_stopwatch()

    def start_stopwatch(self):
        self.post_message(self.ExerciseStarted(self.id, self.parent.id))
        self.add_class("starting")
        self.query_one(time_display).start()

    def stop_stopwatch(self):
        self.remove_class("starting")
        self.query_one(time_display).stop()

    def reset_stopwatch(self):
        self.remove_class("starting")
        self.query_one(time_display).reset()

    class TimeDisplayComplete(Message):
        ...

    def compose(self):
        yield Button("Start", variant="success", id="start")
        yield Button("Stop", variant="error", id="stop")
        yield Button("Reset", id="reset")
        if self.id != "last_exercise":
            yield time_display(self.time_remaining, id="time_d", fps=20)
        else:
            yield time_display(self.time_remaining, id="last_time_d", fps=20)

    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """so, the time display for this stop watch has completed and sent you a message,
        thus, you will hide the stop button and replace it with the start button
        """
        self.remove_class("starting")

    def on_time_display_all_progress_completed(self, message: time_display.AllProgressCompleted):
        """post to the parent(set, tabpane) that the progress of this stopwatch has completed"""
        self.post_message(self.TimeDisplayComplete())
        self.remove_class("starting")
        print("posted message from stopwatch")

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
        self.title = TimeTracker.input_dictionnary[-1]["title"]
        self.number_of_sets = int(TimeTracker.input_dictionnary[-1]["nbr_sets"])
        self.number_of_exercices = int(TimeTracker.input_dictionnary[-1]["nbr_exercises"])
        self.time_per_exercise = int(TimeTracker.input_dictionnary[-1]["time_per_exercise"])
        self.rest_time_between_exercises = int(TimeTracker.input_dictionnary[-1]["rest_time_between_exercises"])

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
        TimeTracker.pop_screen(self=pomodoro)
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
            TimeTracker.input_dictionnary[-1]["day"] = current_time.split(" ")[0]
            TimeTracker.input_dictionnary[-1]["time"] = current_time.split(" ")[1]
            with open("src/progression.json", "a") as file:
                json.dump(pomodoro.input_dictionnary[-1], file)
                file.write('\n')
        self.scroll_end()


    def on_stopwatch_exercise_started(self, message: stopwatch.ExerciseStarted):
        """handle when an exercise started"""
        stopwatch_id = message.id
        print("started stopwatch with id : ", end="")
        print(stopwatch_id)
        if stopwatch_id != "last_exercise" and stopwatch_id != "exercise1":
            stopwatch_id_num = self.extract_integers(stopwatch_id)
            self.query_one("#{}".format(message.set_id)).query_one("#waiting{}".format(stopwatch_id_num - 1), Waiting).stop()
            self.query_one("#{}".format(message.set_id)).query_one("#exercise{}".format(stopwatch_id_num - 1), stopwatch).stop_stopwatch()
        elif stopwatch_id == "last_exercise":
            stopwatch_id_num = self.number_of_exercices
            self.query_one("#{}".format(message.set_id)).query_one("#waiting{}".format(stopwatch_id_num - 1), Waiting).stop()
            self.query_one("#{}".format(message.set_id)).query_one("#exercise{}".format(stopwatch_id_num - 1), stopwatch).stop_stopwatch()
        

    def on_time_display_current_progress_completed(self, message: time_display.CurrentProgressCompleted):
        """handle when a time display completes its progression
        Args:
            message: the message posted by the time_display class for this special case
        """
        sound = pyglet.resource.media('src/start.wav')
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
            TimeTracker.pop_screen(self=pomodoro)
        elif button_id == "next_set":
            self.scroll_home()
            set_id = event.button.parent.parent.id
            self.switch_to_tabpane_by_id(f"set{self.extract_integers(set_id) + 1}")

    def switch_to_tabpane_by_id(self, id):
        """switches to a tab pane by id"""
        self.query_one(TabbedContent).active = id




class TimeTracker(App):
    CSS = """
stopwatch {
    layout: horizontal;
    padding: 1;
    margin: 1;
    background: $boost;
    min-width: 60;
    height: 5;
}
time_display {
    height: 3;
    content-align: center bottom;
    text-opacity: 60%;
}

#start {
    dock: left;
    display: block;
}

#stop {
    dock: left;
    display: none;
}

#reset {
    dock: right;
}

.hidden {
    display: none;
}

.appearing {
    display: block;
}
.starting #start{
    display: none;
}

.starting #stop {
    display: block;
}

.starting #reset {
    display: block;
}

#progress_bar {
    width: 100%;
    align:  center bottom;
    height: auto;
}
#bar {
    width: 90%;
}

#train_button {
    background: $success;
    margin: 1;
    width: 20%;
}

#train_button:hover{
    background: $success-darken-2;
    width: 20%;
}

#progression_button {
    background: $secondary-background;
    margin: 1;
    width: 20%;
}

#progression_button:hover{
    background: $secondary-background-darken-2;
    width: 20%;
}

#about_button {
    background: $primary;
    margin: 1;
    width: 20%;
}

#about_button:hover{
    background: $primary-darken-2;
    width: 20%;
}

#about_misc {
    layout: horizontal;
    margin: 1;
}

#about_misc * {
    padding: 1;
    margin: 1;
    width: 15%;
}

Waiting {
    background: $boost;
    height: 5;
    content-align: center middle;
    text-opacity: 60%;
}

Waiting #progress_bar {
    margin: 1;
}

#progression_table {
    height: 70%;
    background: $boost;
}

#progression_container Horizontal{
    content-align: center middle;
}

#refresh{
    margin: 1;
    height: 3;
}

#screenshot {
    margin: 1;
    height: 3;
}
"""
    Progression_cols = ["day", "training title", "sets trained", "exercises trained"]
    number_of_tabs = 0
    input_dictionnary = [{}]


    def compose(self):
        self.training_title = Input(placeholder="training title eg: leg day", type="text", max_length=15, id="title")
        self.nbr_sets = Input(placeholder="number of sets", type="integer", id="nbr_sets")
        self.nbr_exercises = Input(placeholder="number of exercises", type="integer", id="nbr_exercises")
        self.time_per_exercise = Input(placeholder="time per exercise (seconds)", type="integer", id="time_per_exercise")
        self.rest_time_between_exercises = Input(placeholder="rest time between exercises", type="number", id="rest_time_between_exercises")

        
        yield Header(show_clock=True)
        with TabbedContent(initial="home", id="home_tabbed_content"):
            with TabPane("about", id="about"):
                with Center(id="about_misc"):
                    yield Button("source code", id="source_code")
                    yield Button("Home", id="return_to_home")
                    yield Button("light mode", id="theme")
                yield MarkdownViewer(self.README, show_table_of_contents=True)
            with TabPane("progression", id="progression"):
                with ScrollableContainer(id="progression_container"):
                    yield DataTable(id="progression_table", zebra_stripes=True)
                    with Center():
                            screenshot_button = Button("Screenshot", id="screenshot")
                            yield screenshot_button
            with TabPane("home", id="home"):
                with Static(id="input_div"):
                    yield self.training_title
                    yield self.nbr_sets
                    yield self.nbr_exercises
                    yield self.time_per_exercise
                    yield self.rest_time_between_exercises
                    with Center():
                        yield Button("start_training", id="train_button")
                        yield Button("progression", id="progression_button")
                        yield Button("about", id="about_button")


    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated):
        if event.tab.id == "--content-tab-progression":
            self.load_progression_data()
    
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
            print("switched to progression via button")
            self.load_progression_data()
            self.show_tab_by_tabpane_id("progression")
        elif button_id == "refresh":
            self.load_progression_data()
        elif button_id == "screenshot":
            self.save_screenshot(filename="progression.svg")
            self.notify(message="you can open it using a browser", title="SVG saved")
        elif button_id == "theme":
            self.dark = not self.dark
            self.query_one("#theme").label = "{} mode".format("light" if self.dark else "dark")

    def show_tab_by_tabpane_id(self, tabpane_id):
        """swith to a tab"""
        self.query_one("#home_tabbed_content").active = tabpane_id

    def reset_input_value(self):
        self.training_title.clear()
        self.nbr_sets.clear()
        self.nbr_exercises.clear()
        self.rest_time_between_exercises.clear()
        self.time_per_exercise.clear()

    def load_input_value(self):
        self.title = self.training_title.value
        print("title value in load input value: {}".format(self.title)) # debugg
        nbr_sets = self.nbr_sets.value
        nbr_exercises = self.nbr_exercises.value
        time_per_exercise = self.time_per_exercise.value
        rest_time_between_exercises = self.rest_time_between_exercises.value
        dict = {}
        dict["title"] = self.title
        dict["nbr_sets"] = nbr_sets
        dict["nbr_exercises"] = nbr_exercises
        dict["time_per_exercise"] = time_per_exercise
        dict["rest_time_between_exercises"] = rest_time_between_exercises
        self.input_dictionnary.append(dict)
        for i in self.input_dictionnary[-1]:
            print(i)
            if not self.input_dictionnary[-1][i]:
                del self.input_dictionnary[-1]
                return None
        return self.input_dictionnary[-1]


    def load_progression_data(self):
        try:
            with open("src/progression.json", "r") as file:
                data = []
                for line in file:
                    entry = json.loads(line)
                    entry["day"] = entry.get("day", "")
                    entry["time"] = entry.get("time", "")
                    
                    # Calculate the total time trained in seconds
                    total_time_seconds = int(entry["nbr_sets"]) * int(entry["nbr_exercises"]) * int(entry["time_per_exercise"])
                    
                    # Convert the total time to hours, minutes, and seconds
                    hours, remainder = divmod(total_time_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    
                    # Format the total time as "HH:MM:SS"
                    entry["total_time"] = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
                    
                    data.append(entry)

                table = self.query_one("#progression_table", DataTable)
                table.clear(columns=True)
                table.add_columns("Day", "Time", "Total Time Trained", "Title", "Number of Sets", "Number of Exercises",
                                  "Time per Exercise", "Rest Time Between Exercises")
                
                
                data.reverse()
                for entry in data:
                    table.add_row(
                        entry["day"],
                        entry["time"],
                        entry["total_time"],
                        entry["title"],
                        str(entry["nbr_sets"]),
                        str(entry["nbr_exercises"]),
                        str(entry["time_per_exercise"]),
                        str(entry["rest_time_between_exercises"]),
                    )
        except FileNotFoundError:
            pass  # Handle the case when the file doesn't exist yet
    
    README = """
# TimeTracker App Documentation

## Overview

The **TimeTracker** app is a text-based user interface (TUI) Python application built on the **Textual** framework. It allows users to track their training sessions or any other activities. Users can input details such as the training title, number of sets, number of exercises per set, and the time per exercise in seconds. The app then saves this information to a `src/progression.json` file.

## Installation

1. **Prerequisites** (only if you want to run it using python, otherwise just run the .exe file):
    - Ensure you have Python installed.
    - Install the required frameworks:
        - **Textual**: A Rapid Application Development framework for Python. It enables building sophisticated user interfaces with a simple Python API. You can run Textual apps in both the terminal and a web browser. Visit the <a href="https://textual.textualize.io/guide/">Textual Documentation</a> for more details, install it using ```pip install textual```.
        - **Pyglet**: A Python library for creating games and multimedia applications. Install it using ```pip install pyglet```.

2. **Download and Run**:
    - Clone the repository or download the source code.
    - Navigate to the project directory.
    - Run the app using either of the following methods:
        - **Console**: Execute ```python main3.py``` in the terminal.
        - **Executable (Windows)**: Use the provided `main3.exe` generated with PyInstaller. This standalone executable includes all necessary files (e.g., `src/progression.json`, `src/src/start.wav`, `src/ping.mp3.wav` ,...).

## Usage

1. **Input Details**:
    - Launch the app.
    - Enter the training title, number of sets, number of exercises per set, and exercise duration (in seconds).

2. **Progression Tracking**:
    - Completed activities are saved to the `src/progression.json` file.
    - To view your progression, use the `DataTable` class from the `Textual.widgets` package.

3. **Screenshots**:
    - Take a screenshot of your progression table.
    - Save it as `progression.svg`.
    - Open the SVG file in a web browser to visualize your progress!.

## Authors

- **Darghal Mohammed** <mrdrgh2003@gmail.com>
- **achraf menach**

Feel free to reach out if you have any questions or need further assistance!

THANKS TO THE <a href="https://textual.textualize.io/">TEXTUAL FRAMEWORK</a> TEAM!!❤️✨

"""


if __name__ == "__main__":
    pomodoro = TimeTracker()
    pomodoro.run()