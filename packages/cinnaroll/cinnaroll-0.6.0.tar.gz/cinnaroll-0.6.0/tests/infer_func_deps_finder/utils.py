# asserts that got contains every non-empty line from expect and only them, groups assertion errors into one
from copy import copy
from typing import List, Union, Set


def assert_lines_of_string_in_string(expect: str, got: str) -> None:
    expected_lines = get_non_empty_lines_from_string(expect)
    got_lines = get_non_empty_lines_from_string(got)
    not_found_lines: List[str] = []
    extra_lines = copy(got_lines)

    for line in expected_lines:
        if line in got_lines:
            extra_lines.remove(line)
        else:
            not_found_lines.append(line)

    error_msg = (
        f"The following expected lines were not found in resulting string: {not_found_lines}\n"
        f"The following unexpected lines were found in resulting string: {extra_lines}"
    )
    if len(not_found_lines) or len(extra_lines):
        raise AssertionError(error_msg)


def assert_used_packages_equal(expect: List[Union[str, List[str]]], got: Set[str]) -> None:
    """
    :param expect: names of packages that are supposed to be dependencies of infer code, either strings or
    list of strings - when there can be one of several options eg. in case of tensorflow with
    tensorflow or tensorflow-macos (depending on OS)
    :param got: requirements inferred by deps finder
    """
    unexpected = got.copy()
    assertion_error_message = ""

    for package in expect:
        if type(package) is str:
            if package in got:
                unexpected.remove(package)
            else:
                assertion_error_message += f"Package {package} missing from used packages.\n"
        elif type(package) is list:
            common = got.intersection(package)
            if len(common) == 0:
                assertion_error_message += f"Expected to find one of {package} in used packages, found none.\n"
            if len(common) == 1:
                unexpected.remove(common.pop())
            if len(common) > 1:
                assertion_error_message += \
                    f"Expected to find one of {package} in used packages, found {' and '.join(common)}.\n"
    if len(unexpected):
        assertion_error_message += "Found the following unexpected packages in requirements: "
        for package in unexpected:
            assertion_error_message += f"{package}, "
        assertion_error_message += "\n"
    if assertion_error_message:
        raise AssertionError(assertion_error_message)


def get_non_empty_lines_from_string(s: str) -> List[str]:
    result_lines: List[str] = []
    for line in s.split("\n"):
        if line.strip():
            result_lines.append(line)
    return result_lines
