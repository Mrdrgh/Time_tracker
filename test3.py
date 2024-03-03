from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input, Label, Button, Static
from textual import on

class InputApp(App):
    """App to display key events."""

    def compose(self):
        with Static(id="container"):
            yield Label("input")
            yield Input(placeholder="input a number", type="integer")
            yield Button("validate", id="validate")

    def is_even(n):
        return n % 2 == 0
    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "validate":
            if self.query_one(Input).value:
                new_button = Button(f"{self.query_one(Input).value}")
                self.query_one("#container").mount(new_button)

if __name__ == "__main__":
    app = InputApp()
    app.run()