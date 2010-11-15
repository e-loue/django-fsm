#-*- coding: utf-8 -*-
from collections import defaultdict
from fsm.fields import FSMField, FSMKeyField


class FSMMeta(object):
    """Models methods transitions meta information"""
    def __init__(self):
        self.transitions = defaultdict()
        self.conditions  = defaultdict()

    @staticmethod
    def _get_state_field(instance):
        """Lookup for FSMField in django model instance"""
        fields = [field for field in instance._meta.fields
            if isinstance(field, FSMField) or isinstance(field, FSMKeyField)]
        found = len(fields)
        if found == 0:
            raise TypeError("No FSMField found in model")
        elif found > 1:
            raise TypeError("More than one FSMField found in model")
        return fields[0]

    @staticmethod
    def current_state(instance):
        """Return current state of Django model"""
        field_name = FSMMeta._get_state_field(instance).name
        return getattr(instance, field_name)

    def has_transition(self, instance):
        """Lookup if any transition exists from current model state"""
        return FSMMeta.current_state(instance) in self.transitions or '*' in self.transitions

    def conditions_met(self, instance):
        """Check if all conditions has been met"""
        current_state = FSMMeta.current_state(instance)
        next = self.transitions.has_key(current_state) and self.transitions[current_state] or self.transitions['*']
        return all(map(lambda f: f(instance), self.conditions[next]))
    
    def to_next_state(self, instance):
        """Switch to next state"""
        field_name = FSMMeta._get_state_field(instance).name
        curr_state = getattr(instance, field_name)
        next_state = None
        try:
            next_state = self.transitions[curr_state]
        except KeyError:
            next_state = self.transitions['*']
        setattr(instance, field_name, next_state)
