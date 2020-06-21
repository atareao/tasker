import pluggy

list_box_todospec = pluggy.HookspecMarker("list_box_todo")


class ListBoxRowTodoSpec(object):
    """
    Hooks for src/ListBoxRowTodo. In this list you can find all the hook
    that you can use to get completed your custom features

    Think that this class is an interface. It only serves to know the list of hooks availables,
    the parameters and return classes
    """

    @list_box_todospec
    def after_track_time(
        self, todo, before_started_at, after_started_at, total_time, just_now
    ):
        """
        todo (todo object. See todotxt.io) Object that hold information
        started_at (float): Unix time. When 0 the todo has being finalizted
        total_time: Acumulated time in todo
        """
