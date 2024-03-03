from time import monotonic
from textual import on
from textual.app import App, ComposeResult
from textual.events import Mount
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static
from textual.widgets import Input, Label, ProgressBar
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal

class time_displayer(Static):
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
    #     self.time_elapsed = 0
    #     self.accum_time = 0
    
    # def update_time_elapsed(self):
    #     self.time_elapsed = self.accum_time + ( monotonic() - self.start_time)
    ...

class time_display(Static):
    def compose(self):
        yield time_displayer("00.00")


class stopwatch(Static):
    """the stopwatch where there will be button and shit"""
    def compose(self):
        with ScrollableContainer(id="buttons"):
            yield Button(label="start", id="start") 
            yield Button(label="stop", id="stop")
            yield Button(label="reset", id="reset")
        with ScrollableContainer(id="time"):
            yield time_display()


class pomodoroApp(App):
    """the main entry to the pomodoro app"""
    def compose(self):
        self.sets = Input(placeholder="Number of sets")
        self.exercises = Input(placeholder="Exercises per set")
        self.work_time = Input(placeholder="Work time (seconds)")
        self.rest_time = Input(placeholder="Rest time (seconds)")

        self.current_set = 0
        self.current_exercise = 0
        self.timer = None

        yield Vertical(
            self.sets,
            self.exercises,
            self.work_time,
            self.rest_time,
            Button("Start", id="start_button", classes="success"),
            Button("Pause", id="pause_button", disabled=True),
            Button("Reset", id="reset_button", disabled=True),
            Label(id="timer_label"),
            Static(id="status_message"),
        )


if __name__ == "__main__":
    pomodoroApp().run()


# import time
# from playsound import playsound
# from textual import on
# from textual.app import App, ComposeResult
# from textual.containers import Vertical, Horizontal
# from textual.widgets import Input, Button, Label, Static

# class WorkoutIntervalTimer(App):
#     def __init__(self):
#         super().__init__()
#         self.is_running = False


#     @on(Button.Pressed)
#     def handle_button_click(self, event):
#         button_id = event.button.id

#         if button_id == "start_button":
#             self.start_timer()
#         elif button_id == "pause_button":
#             self.pause_timer()
#         elif button_id == "reset_button":
#             self.reset_timer()

#     def start_timer(self):
#         self.is_running = True
#         self.query_one("#start_button").disable()
#         self.query_one("#pause_button").enable()
#         self.query_one("#reset_button").enable()

#         self.current_set = int(self.sets.value)
#         self.current_exercise = int(self.exercises.value)
#         self.work_time_value = int(self.work_time.value)
#         self.rest_time_value = int(self.rest_time.value)

#         self.timer = self.set_interval(1, self.update_timer)

#     def pause_timer(self):
#         self.is_running = not self.is_running
#         self.timer.pause() if self.is_running else self.timer.resume()

#     def reset_timer(self):
#         self.is_running = False
#         self.query_one("#start_button").enable()
#         self.query_one("#pause_button").disable()
#         self.query_one("#reset_button").disable()

#         self.current_set = 0
#         self.current_exercise = 0
#         self.timer.cancel()
#         self.query_one("#timer_label").update("")
#         self.query_one("#status_message").update("")

#     def update_timer(self):
#         if self.is_running:
#             if self.current_exercise > 0:
#                 if self.work_time_value > 0:
#                     self.work_time_value -= 1
#                     self.query_one("#timer_label").update(f"Work: {self.work_time_value}")
#                 else:
#                     playsound("start.wav")
#                     self.work_time_value = int(self.work_time.value)
#                     self.rest_time_value = int(self.rest_time.value)

#                 if self.rest_time_value > 0:
#                     self.rest_time_value -= 1
#                     self.query_one("#timer_label").update(f"Rest: {self.rest_time_value}")
#                 else:
#                     playsound("end.wav")
#                     self.current_exercise -= 1
#                     self.rest_time_value = int(self.rest_time.value)

#             else:
#                 self.current_set -= 1
#                 if self.current_set > 0:
#                     self.current_exercise = int(self.exercises.value)
#                     self.query_one("#status_message").update(f"Set {self.current_set} started!")
#                 else:
#                     self.reset_timer()
#                     self.query_one("#status_message").update("Workout complete!")

# if __name__ == "__main__":
#     WorkoutIntervalTimer().run()
