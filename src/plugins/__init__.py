from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from collections import Counter

# iterate through the modules in the current package
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
            classes.append(attribute.__name__)
countered_classes = dict(Counter(classes))
for class_ in countered_classes.keys():
    if countered_classes[class_] > 1:
        print('The class \'{}\' appears in more than one installed plugin. You must unninstall these'.format(class_))