"""
Script to programmatically generate all the mixin combinations
"""


import itertools
from collections.abc import Iterable, Iterator

import inflection
from black import FileMode, format_str

# Required due to the code in BASE_TEMPLATE
# pylint: disable=duplicate-code
BASE_TEMPLATE = """
'''
This module provides all combinations of the mixins provided by rest_framework.
All combinations follow the same format: {{initials}}Mixin.

The initials correspond to the following methods, in this specific order:
    - L: list()
    - R: retrieve()
    - C: create()
    - U: update()
    - P: partial_update()
    - D: delete()

So for example, to import a mixin that gives us list, retrieve and create,
we can do the following:

```
from rest_framework_mixins import LRCMixin
```
'''

from typing import Any

from django.views.generic import View
from rest_framework import mixins


class NoPutMixin:
    "A mixin that doesn't bring PUT along"

    http_method_names = [
        http_method_name
        for http_method_name in View.http_method_names
        if http_method_name != "put"
    ]


class NoPatchMixin:
    "A mixin that doesn't bring PATCH along"

    http_method_names = [
        http_method_name
        for http_method_name in View.http_method_names
        if http_method_name != "patch"
    ]


{mixins}
"""

CLASS_TEMPLATE = """class {name}({mixins}):
    '''
A mixin that provides the following default {action_noun}:

- {actions}
    '''
"""


def per_combination(combination: Iterable[str]) -> str:
    """
    Generate a string representation of a mixin combination class

        Args:
            combination: An iterable with action names

        Returns:
            A string representation of a mixin combination class
    """
    name = f"{''.join([action[0].upper() for action in combination])}Mixin"

    mixins: list[str] = []
    actions: list[str] = []
    for action_name in combination:
        actions.append(f"{inflection.underscore(action_name)}()")

        if action_name == "PartialUpdate":
            if "Update" in combination:
                continue
            action_name = "Update"

        mixins.append(f"mixins.{action_name}ModelMixin")

    if "PartialUpdate" not in combination and "Update" in combination:
        mixins.append("NoPatchMixin")
    if "Update" not in combination and "PartialUpdate" in combination:
        mixins.append("NoPutMixin")

    return CLASS_TEMPLATE.format(
        name=name,
        mixins=",".join(mixins) + ",",
        actions="\n- ".join(actions),
        action_noun="action" if len(actions) == 1 else "actions",
    )


def per_mixins(viewset_actions: list[str]) -> Iterator[str]:
    """
    Generate all mixin combinations for the given actions.

        Args:
            viewset_actions: The actions to generate the mixins for

        Returns:
            An iterator with each element being the string representation
            of a mixin combination class
    """
    for action_count in range(1, len(viewset_actions) + 1):
        for combination in itertools.combinations(viewset_actions, r=action_count):
            yield per_combination(combination)


def all_mixin_combinations() -> str:
    """
    Generates all mixin combinations for the actions provided by default by DRF.

        Returns:
            A black-formatted string with all the code
            required to be implanted onto __init__.py
    """
    code_per_class = per_mixins(
        ["List", "Retrieve", "Create", "Update", "PartialUpdate", "Destroy"]
    )
    code = BASE_TEMPLATE.format(mixins="\n".join(code_per_class))

    return format_str(code, mode=FileMode())


def main() -> None:
    "Prints to stdout the generated code"
    print(all_mixin_combinations(), end="")


if __name__ == "__main__":
    main()
