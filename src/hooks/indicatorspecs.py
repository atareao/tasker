import pluggy

indicatorspec = pluggy.HookspecMarker("indicator")


class IndicatorSpec(object):
    """
    Hooks for src/Indicator. In this list you can find all the hook
    that you can use to get completed your custom features

    Think that this class is an interface. It only serves to know the list of hooks availables,
    the parameters and return classes
    """

    @indicatorspec
    def get_hook_menu(self,):
        """Return a Gtk.MenuItem() array to be showed on App indicator (System tray)

        :return: new Menu Gtk.MenuItem
        """

    @indicatorspec
    def after_init_indicator(self,):
        """Event fired after init
        """
