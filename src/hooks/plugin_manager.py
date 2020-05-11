import pluggy
from plugins import *
from .indicatorspecs import IndicatorSpec

def get_indicator_plugin_manager():
	"""
	Import all Hook classes that are in the plugins package
	and make this availables for be called from master sources
	"""
	pm = pluggy.PluginManager("indicator")
	pm.add_hookspecs(IndicatorSpec)
	for class_imported in classes:
		pm.register(globals()[class_imported]())
	return pm
