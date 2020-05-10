import pluggy
hookspec = pluggy.HookspecMarker("indicator")

class IndicatorSpec(object):

    @hookspec
    def get_hook_menu(self, ):
        """Return a Gtk.MenuItem().

        :return: new Menu Gtk.Menu
        """