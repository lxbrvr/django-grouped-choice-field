# -*- coding: utf-8 -*-
from functools import reduce
from itertools import groupby

from django import forms


class GroupedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, group_by, sort_choices_by=None, *args, **kwargs):
        super(GroupedModelMultipleChoiceField, self).__init__(*args, **kwargs)
        self.group_by = group_by
        self.sort_choices_by = sort_choices_by
        self.group_label = lambda group: group
        self.sort_choices_with_reverse = False

        if self.sort_choices_by and self.sort_choices_by.startswith('-'):
            self.sort_choices_with_reverse = True
            self.sort_choices_by = self.sort_choices_by.replace('-', '')

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, forms.ModelMultipleChoiceField._set_choices)


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):

    def _key_func(self, obj):
        return reduce(getattr, self.field.group_by.split('__'), obj)

    def _sort_choices(self, choices):
        return sorted(
            choices,
            key=lambda obj: getattr(obj, self.field.sort_choices_by),
            reverse=self.field.sort_choices_with_reverse,
        )

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)

        object_list = sorted(self.queryset.all(), key=self._key_func)

        for group, choices in groupby(object_list, key=self._key_func):
            if group is not None:
                if self.field.sort_choices_by:
                    choices = self._sort_choices(choices)

                yield (
                    self.field.group_label(group),
                    [self.choice(c) for c in choices]
                )