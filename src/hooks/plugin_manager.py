import pluggy
from plugins import *
from .hookspecs import IndicatorSpec

def get_plugin_manager():
	pm = pluggy.PluginManager("indicator")
	pm.add_hookspecs(IndicatorSpec)
	for class_imported in classes:
		pm.register(globals()[class_imported]())
	return pm
