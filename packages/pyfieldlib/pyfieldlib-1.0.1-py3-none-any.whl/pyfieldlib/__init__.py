# pyfieldlib (version: 1.0.1)
#
# Copyright 2023. DuelitDev all rights reserved.
#
# This Library is distributed under the MIT License.


__all__ = ["FieldMeta", "fields"]

fields = type("fields", (property,), {})


class FieldMeta(type):
    """
    Metaclass that makes fields available.
    FieldMeta must be set to metaclass before fields can be used.
    """

    def __new__(mcs, name, bases, props):
        for k, v in props.items():
            if isinstance(v, fields):
                setattr(mcs, k, v)
        return super().__new__(mcs, name, bases, props)
