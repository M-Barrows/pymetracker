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
        task_details = dict()
        if event.button.id == "start_new_task":
            for field in self.query("Input"):
                #TODO: Save this task for easy re-start of a timer later
                self.__setattr__(field.name,field.value)
            t = Timer()
            t.task = self
        app.query_one("#new-timer").mount(t)
        self.remove()

    def compose(self): 
        with Horizontal(id="new-task-form"):
            with Vertical():
                yield Input(placeholder="Client",type="text",name="client")
            with Vertical():
                yield Input(placeholder="Project",type="text",name="project")
            with Vertical():
                yield Input(placeholder="Description",type="text",name="description")
            with Vertical(): 
                yield Button("Start", variant="primary",id="start_new_task")

class Timer(Static):
    """A Timer Widget"""
    start_time = reactive(datetime.now)
    end_time = reactive("")
    time = reactive("")
    task = None

    def on_mount(self) -> None:
        """called when the widget is added to the app"""
        self.update_timer = self.set_interval(1/60,self.update_time,pause=False)
    
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
        self.end_time = datetime.now()
        #TODO: SAVE record to database
        self.remove()

class PymeTracker(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "./static/styles.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("n", "new_timer", "Create a new timer"),
        ("s", "stop_timer", "Stop the current timer")
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield Horizontal(id="new-timer")
        yield Footer()

    def action_new_timer(self) -> None:
        self.query_one("#new-timer").mount(Task())
    
    def action_stop_timer(self) -> None:
        self.query_one(Timer).stop()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = PymeTracker()
    app.run()