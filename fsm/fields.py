# -*- coding: utf-8 -*-
from django.db import models


class FSMField(models.CharField):
    """State Machine support for Django model"""

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50
        super(FSMField, self).__init__(*args, **kwargs)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class FSMKeyField(models.ForeignKey):
    """State Machine support for Django model"""
