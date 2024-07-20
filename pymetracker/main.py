from datetime import datetime
import os

from models import Base, Task, Timer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from textual.containers import ScrollableContainer, Horizontal, Vertical
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, Input, Button 


class TaskForm(Static): 
    """A widget for entering task details"""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        task_details = dict()
        if event.button.id == "start_new_task":
            for field in self.query("Input"):
                #TODO: Save this task for easy re-start of a timer later
                task_details.update({field.name:field.value})
            task = Task(**task_details)
            t = TimerDisplay()
            with Session(engine) as session:
                session.add(task)
                session.commit()
                t.task_id = task.task_id
                session.expunge_all()
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

class TimerDisplay(Static):
    """A Timer Widget"""
    start_time = reactive(datetime.now)
    end_time = reactive("")
    time = reactive("")
    task_id = None

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
        timer = Timer(start = self.start_time, end=self.end_time, task_id = self.task_id)
        with Session(engine) as session:
            session.add(timer)
            session.commit()
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
        self.query_one("#new-timer").mount(TaskForm())
    
    def action_stop_timer(self) -> None:
        self.query_one(TimerDisplay).stop()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))
    engine = create_engine(f"sqlite:///{path}/data/pymetracker.db", echo=True)
    Base.metadata.create_all(engine)
    app = PymeTracker()
    app.run()