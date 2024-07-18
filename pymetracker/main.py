from datetime import datetime

from textual.containers import ScrollableContainer, Horizontal, Vertical
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, Input, Button 

class Task(Static): 
    """A widget for entering task details"""
    client = ""
    project = ""
    description = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_new_task":
            yield Timer()
            timer = self.query_one(Timer)
            timer.start()

    def compose(self): 
        with Horizontal():
            with Vertical():
                yield Input(placeholder="client",type="text")
            with Vertical():
                yield Input(placeholder="project",type="text")
            with Vertical():
                yield Input(placeholder="description",type="text")
            with Vertical(): 
                yield Button("Start", variant="primary",id="start_new_task")

class Timer(Static):
    """A Timer Widget"""
    start_time = reactive(datetime.now)
    time = reactive("")

    def on_mount(self) -> None:
        """called when the widget is added to the app"""
        self.update_timer = self.set_interval(1/60,self.update_time,pause=True)
    
    def update_time(self) -> None:
        """called periodically to update timers length"""
        self.time = str(datetime.now() - self.start_time)

    def watch_time(self) -> None:
        """called when time attr changes"""
        self.update(self.time)

    def start(self) -> None:
        self.start_time = datetime.now()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()

class PymeTracker(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "./static/styles.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("n", "new_timer", "Create a new timer"),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield Footer()
        yield Horizontal(id="new-timer")

    def action_new_timer(self) -> None:
        self.query_one("#new-timer").mount(Task())
    
    def action_stop_timer(self) -> None:
        raise NotImplementedError

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = PymeTracker()
    app.run()