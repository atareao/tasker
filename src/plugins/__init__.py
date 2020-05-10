from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# Dynamic import all plugins located here
# TODO: Filter by subclasses. This mean all plugins only can overwrite a subset classes
package_dir = Path(__file__).resolve().parent
classes = []
for (_, module_name, _) in iter_modules([package_dir]):
    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute
            class_ = attribute.__name__
            if class_ in classes:
                print('The class \'{}\' appears in more than one installed plugin. You must unninstall these'.format(
                    class_))
            else:
                classes.append(class_)