"""
This module provides all combinations of the mixins provided by rest_framework.
All combinations follow the same format: {initials}Mixin.

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
"""

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


class LMixin(
    mixins.ListModelMixin,
):
    """
    A mixin that provides the following default action:

    - list()
    """


class RMixin(
    mixins.RetrieveModelMixin,
):
    """
    A mixin that provides the following default action:

    - retrieve()
    """


class CMixin(
    mixins.CreateModelMixin,
):
    """
    A mixin that provides the following default action:

    - create()
    """


class UMixin(
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default action:

    - update()
    """


class PMixin(
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default action:

    - partial_update()
    """


class DMixin(
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default action:

    - destroy()
    """


class LRMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    """


class LCMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    """


class LUMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - update()
    """


class LPMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - partial_update()
    """


class LDMixin(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - destroy()
    """


class RCMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    """


class RUMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - update()
    """


class RPMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - partial_update()
    """


class RDMixin(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - destroy()
    """


class CUMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - update()
    """


class CPMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - partial_update()
    """


class CDMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - destroy()
    """


class UPMixin(
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - update()
    - partial_update()
    """


class UDMixin(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - update()
    - destroy()
    """


class PDMixin(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - partial_update()
    - destroy()
    """


class LRCMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    """


class LRUMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - update()
    """


class LRPMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - partial_update()
    """


class LRDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - destroy()
    """


class LCUMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - update()
    """


class LCPMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - partial_update()
    """


class LCDMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - destroy()
    """


class LUPMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - update()
    - partial_update()
    """


class LUDMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - update()
    - destroy()
    """


class LPDMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - partial_update()
    - destroy()
    """


class RCUMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - update()
    """


class RCPMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - partial_update()
    """


class RCDMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - destroy()
    """


class RUPMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - update()
    - partial_update()
    """


class RUDMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - update()
    - destroy()
    """


class RPDMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - partial_update()
    - destroy()
    """


class CUPMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - update()
    - partial_update()
    """


class CUDMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - update()
    - destroy()
    """


class CPDMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - partial_update()
    - destroy()
    """


class UPDMixin(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - update()
    - partial_update()
    - destroy()
    """


class LRCUMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - update()
    """


class LRCPMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - partial_update()
    """


class LRCDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - destroy()
    """


class LRUPMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - update()
    - partial_update()
    """


class LRUDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - update()
    - destroy()
    """


class LRPDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - partial_update()
    - destroy()
    """


class LCUPMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - update()
    - partial_update()
    """


class LCUDMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - update()
    - destroy()
    """


class LCPDMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - partial_update()
    - destroy()
    """


class LUPDMixin(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - update()
    - partial_update()
    - destroy()
    """


class RCUPMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - update()
    - partial_update()
    """


class RCUDMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - update()
    - destroy()
    """


class RCPDMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - partial_update()
    - destroy()
    """


class RUPDMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - update()
    - partial_update()
    - destroy()
    """


class CUPDMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - create()
    - update()
    - partial_update()
    - destroy()
    """


class LRCUPMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - update()
    - partial_update()
    """


class LRCUDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPatchMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - update()
    - destroy()
    """


class LRCPDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    NoPutMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - partial_update()
    - destroy()
    """


class LRUPDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - update()
    - partial_update()
    - destroy()
    """


class LCUPDMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - create()
    - update()
    - partial_update()
    - destroy()
    """


class RCUPDMixin(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - retrieve()
    - create()
    - update()
    - partial_update()
    - destroy()
    """


class LRCUPDMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A mixin that provides the following default actions:

    - list()
    - retrieve()
    - create()
    - update()
    - partial_update()
    - destroy()
    """
