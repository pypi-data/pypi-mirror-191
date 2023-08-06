from typing import Dict, Set
import importlib_metadata

from cinnaroll_internal.infer_func_deps_finder import imports

# https://stackoverflow.com/questions/60975090/how-do-you-find-python-package-metadata-information-given-a-module/60975978#60975978
# https://importlib-metadata.readthedocs.io/en/stable/using.html#package-distributions


def get_used_third_party_packages(used_imports: Dict[str, imports.Import]) -> Set[str]:
    installed_packages = importlib_metadata.packages_distributions()

    used_packages = set()

    for _, imp in used_imports.items():
        mod = imp.module if imp.module else imp.name
        mod = mod.split('.')[0]
        if mod in installed_packages:
            used_packages.add(installed_packages[mod][0])

    return used_packages
