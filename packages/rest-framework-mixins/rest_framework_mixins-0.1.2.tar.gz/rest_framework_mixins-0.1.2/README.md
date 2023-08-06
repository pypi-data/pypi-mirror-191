# rest-framework-mixins

## Installation

`pip install rest_framework_mixins`

## Usage

This package provides all combinations of the mixins provided by rest_framework.  
All combinations follow the same format: `{initials}Mixin.

The initials correspond to the following methods, in this specific order:

- L: `list()`  
- R: `retrieve()`  
- C: `create()`  
- U: `update()`  
- P: `partial_update()`  
- D: `delete()`  

So for example, to import a mixin that gives us list, retrieve and create,
we can do the following:

```
from rest_framework_mixins import LRCMixin

class CreateListRetrieveViewSet(LRCMixin, viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass
```

> Adapted from [DRF's documentation](https://www.django-rest-framework.org/api-guide/viewsets/#example_3)
