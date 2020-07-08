import sys
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from config import PLUGINS_INSTALLED_DIR
from hooks import IndicatorSpec, ListBoxRowTodoSpec

# Dynamic import all classes located here
# If the class is not subclass of allowed spec,
# this is not will be imported
# The allowed classes must be declared and decorated
# with pluggy.HookspecMarker function in the hooks package
package_dir = Path(PLUGINS_INSTALLED_DIR).resolve()
sys.path.append(PLUGINS_INSTALLED_DIR)
indicatorPluginClasses = []
listBoxRowTodoPluginClasses = []
for (_, module_name, _) in iter_modules([package_dir]):
    module = import_module(f"{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute) and issubclass(attribute, IndicatorSpec):
            globals()[attribute_name] = attribute
            class_ = attribute.__name__
            if class_ in indicatorPluginClasses:
                print(
                    "The class '{}' appears in more than one "
                    "installed plugin. "
                    "You must unninstall these".format(class_)
                )
            else:
                indicatorPluginClasses.append(class_)
        elif isclass(attribute) and issubclass(attribute, ListBoxRowTodoSpec):
            globals()[attribute_name] = attribute
            class_ = attribute.__name__
            if class_ in listBoxRowTodoPluginClasses:
                print(
                    "The class '{}' appears in more than one "
                    "installed plugin. You must unninstall these".format(
                        class_
                    )
                )
            else:
                listBoxRowTodoPluginClasses.append(class_)
        elif isclass(attribute):
            print(
                "The class {} was not imported "
                "because must be subclass of almost "
                "one class form hooks package".format(attribute.__name__)
            )
