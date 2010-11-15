# -*- coding: utf-8 -*-
from functools import wraps
from fsm.exceptions import TransitionNotAllowed
from fsm.models import FSMMeta


def transition(source='*', target=None, save=False, conditions=[]):
    """Method decorator for mark allowed transition"""
    def inner_transition(func):
        if not hasattr(func, '_django_fsm'):
            setattr(func, '_django_fsm', FSMMeta())
        if isinstance(source, (list, tuple)):
            for state in source:
                func._django_fsm.transitions[state] = target
        else:
            func._django_fsm.transitions[source] = target
        func._django_fsm.conditions[target] = conditions

        @wraps(func)
        def _change_state(instance, *args, **kwargs):
            meta = func._django_fsm
            if not meta.has_transition(instance):
                raise TransitionNotAllowed("Can't switch from state '%s' using method '%s'" % (FSMMeta.current_state(instance), func.func_name))
            for condition in conditions:
                if not condition(instance):
                    return False
            func(instance, *args, **kwargs)
            meta.to_next_state(instance)
            if save:
                instance.save()
        return _change_state

    if not target:
        raise ValueError("Result state not specified")
    return inner_transition


def can_proceed(bound_method):
    """Returns True if model in state allows to call bound_method"""
    if not hasattr(bound_method, '_django_fsm'):
        raise NotImplementedError('%s method is not transition' % bound_method.im_func.__name__)
    meta = bound_method._django_fsm
    return meta.has_transition(bound_method.im_self) and meta.conditions_met(bound_method.im_self)
