import inspect
import site
import sys
import os
from enum import Enum
from types import ModuleType
from typing import Any, Callable, Optional, List, Tuple


# find out where packages can be installed
PACKAGE_INSTALL_LOCATIONS = site.getsitepackages()
PACKAGE_INSTALL_LOCATIONS.append(site.getusersitepackages())

for path in sys.path:
    split = path.split(os.sep)
    if len(split) > 2:
        if split[-1] == "site-packages" or split[-1] == "lib":
            PACKAGE_INSTALL_LOCATIONS.append(path)
        elif split[-2] == "site-packages" or split[-2] == "lib":
            path = os.sep.join(split[:-1])
            PACKAGE_INSTALL_LOCATIONS.append(path)

# remove site-packages or lib from the end of the path
for path in PACKAGE_INSTALL_LOCATIONS:
    if path.endswith("site-packages"):
        path = path[:len("site-packages")]
    elif path.endswith("lib"):
        path = path[:len("lib")]

# remove duplicates
PACKAGE_INSTALL_LOCATIONS = list(dict.fromkeys(PACKAGE_INSTALL_LOCATIONS))


class ModuleOrigin(Enum):
    BUILT_IN = "built-in"
    THIRD_PARTY = "third party"
    PYTHON_INTERNAL = "python internal"
    LOCAL = "local"


def get_module_member_modules(module: ModuleType) -> List[Tuple[str, ModuleType]]:
    return get_relevant_module_members(module, predicate=inspect.ismodule)


def get_module_non_module_members(module: ModuleType) -> List[Tuple[str, Any]]:
    def is_not_a_module(obj: Any) -> bool:
        return not inspect.ismodule(obj)

    return get_relevant_module_members(module, predicate=is_not_a_module)


def get_relevant_module_members(
    module: ModuleType, predicate: Optional[Callable[[Any], bool]] = None
) -> List[Tuple[str, Any]]:
    members = []
    for name, value in inspect.getmembers(module, predicate=predicate):
        if not name.startswith("__"):
            members.append((name, value))
    return members


def get_module_origin(module: ModuleType) -> ModuleOrigin:
    try:
        module_source_file = inspect.getsourcefile(module)
        if not module_source_file:
            return ModuleOrigin.BUILT_IN
    except AttributeError:
        return ModuleOrigin.BUILT_IN
    if "site-packages" in module_source_file:
        return ModuleOrigin.THIRD_PARTY
    if any(
        pkg_install_path in module_source_file
        for pkg_install_path in PACKAGE_INSTALL_LOCATIONS
    ):
        return ModuleOrigin.PYTHON_INTERNAL
    return ModuleOrigin.LOCAL
