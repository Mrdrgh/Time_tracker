from time import monotonic
from textual import on
from textual.app import App
from textual.events import Mount, Key
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static, ProgressBar


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
        if self.id == "last_time_d":
            self.notify("set complete")
            self.parent.parent.parent.enable_next_set_buttone(self.parent.parent.parent)

    def watch_time_remaining(self):
        if self.time_remaining <= 0:
            self.notify(message="exercise complete\nprogression updated", timeout=2)
            self.stop()
            print(self.id)
            self.handle_all_exercises_complete() 
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

        


class stopwatch(Static):
    def __init__(self, time_remaining, id):
        super().__init__()
        self.time_remaining = time_remaining
        self.id = id
    @on(Button.Pressed, "#start")
    def start_stopwatch(self):
        self.add_class("starting")
        self.notify("starting..", timeout=2)
        self.query_one(time_display).start()

    @on(Button.Pressed, "#stop")
    def stop_stopwatch(self):
        self.remove_class("starting")
        self.query_one(time_display).stop()

    @on(Button.Pressed, "#reset")
    def reset_stopwatch(self):
        self.remove_class("starting")
        self.query_one(time_display).reset()


    def compose(self):
        yield Button("Start", variant="success", id="start")
        yield Button("Stop", variant="error", id="stop")
        yield Button("Reset", id="reset")
        if self.id != "last_exercise":
            yield time_display(self.time_remaining, id="time_d", fps=15)
        else:
            yield time_display(self.time_remaining, id="last_time_d", fps=15)


class stopwatchApp(App):
    BINDINGS = [
        ("D", "toggle_dark_mode", "tap D to toggle dark mode"),
        ("q", "quit", "q to quit"),
        ("a", "add_stopwatch", "add stopwatch"),
        ("r", "remove_stopwatch", "remove stopwatch")
    ]
    CSS = """
stopwatch {
    layout: horizontal;
    padding: 1;
    margin: 1;
    background: $boost;
    min-width: 60;
    height: 5;
}
#time_d {
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
"""

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="stopwatches"):
            yield stopwatch()
            yield stopwatch()
            yield stopwatch()
    def action_toggle_dark_mode(self):
        self.dark = not self.dark
    def action_quit(self):
        return super().action_quit()
    def action_add_stopwatch(self):
        """add a stop watch"""
        new_stopwatch = stopwatch()
        container = self.query_one("#stopwatches")
        container.mount(new_stopwatch)
        new_stopwatch.scroll_visible()
    
    def action_remove_stopwatch(self):
        """remove a stopwatch"""
        stopwatches = self.query("stopwatch")
        if stopwatches:
            stopwatches[-1].remove()
if __name__ == "__main__":
    stopwathc = stopwatchApp()
    stopwathc.run()