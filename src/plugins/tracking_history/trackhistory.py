import pluggy
# Custom featured needed
from hooks import ListBoxRowTodoSpec
from configurator import Configuration
from pathlib import Path
import os
import todotxtio.todotxtio as todotxtio

# Decorator for hook. The function that was decorated with this
# will be called from de master source if it in Hookspecks availables
list_box_todospec = pluggy.HookimplMarker("list_box_todo")


class TrackingHistory(ListBoxRowTodoSpec):
    """A hook implementation namespace.
    """

    def __init__(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        self.todo_histoy = Path(
            os.path.expanduser(preferences['todo-file'])).parent.as_posix() + os.sep + 'todo.history.txt'
        todo_histoy_path = Path(self.todo_histoy)
        if not todo_histoy_path.exists():
            todo_histoy_path.touch()

    @list_box_todospec
    def after_track_time(self, todo, before_started_at, after_started_at, total_time, just_now):
        """
        This event is fired after user click on one task or close the app with a task started
        Take on account that this event is fired per task and one click may fire this event two times:
        one to finalize previous, other for initialize this
        In the original code only track total time per task. To sum all time inverted in a task
        you need to know when started it and with the current time you can sum time to total time
        With this hook you can know when was started and the total time in one step
        Arguments:
        * todo (todo object. See todotxt.io) Object that hold information
        * before_started_at: Unix time. Last started time
        * after_started_at (float): Unix time. If greater than 0 todo has initialized
                                               else the todo has being finalized
        * total_time: Acumulated time in todo
        * just_now: Unix time. Only one time instance accross call's
        """
        if before_started_at:
            list_of_todos = todotxtio.from_file(self.todo_histoy)
            new_todo_history = todotxtio.Todo(text=todo.text)
            new_todo_history.projects = todo.projects
            new_todo_history.contexts = todo.contexts
            new_todo_history.completed = True
            new_todo_history.tags['started'] = str(before_started_at)
            new_todo_history.tags['ended'] = str(just_now)
            new_todo_history.tags['step_time'] = str(just_now - before_started_at)
            new_todo_history.tags['total_time'] = str(todo.tags['total_time'])
            list_of_todos.append(new_todo_history)
            todotxtio.to_file(self.todo_histoy, list_of_todos)

        print('todo: {}, before_started_at: {}, after_started_at: {}, total_time: {}, just_now: {}'.\
              format(todo.text, before_started_at, after_started_at, total_time, just_now))
