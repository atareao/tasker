import pluggy
from plugins import *
from .indicatorspecs import IndicatorSpec
from .list_box_todospecs import ListBoxRowTodoSpec

def get_indicator_plugin_manager():
	"""
	Import all Hook classes that are in the plugins package
	and make this availables for be called from master sources
	"""
	pm = pluggy.PluginManager("indicator")
	pm.add_hookspecs(IndicatorSpec)
	for class_imported in indicatorPluginClasses:
		pm.register(globals()[class_imported]())
	return pm

def get_list_box_todo_plugin_manager():
	"""
	Import all Hook classes that are in the plugins package
	and make this availables for be called from master sources
	"""
	pm = pluggy.PluginManager("list_box_todo")
	pm.add_hookspecs(ListBoxRowTodoSpec)
	for class_imported in listBoxRowTodoPluginClasses:
		pm.register(globals()[class_imported]())
	return pm