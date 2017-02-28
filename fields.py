# -*- coding: utf-8 -*-

from itertools import groupby

from django import forms


class GroupedMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, group_by, sort_choices_by=None, *args, **kwargs):
        super(GroupedMultipleModelChoiceField, self).__init__(*args, **kwargs)
        self.group_by = group_by
        self.sort_choices_by = sort_choices_by
        self.group_label = lambda group: group

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
            key=lambda obj: getattr(obj, self.field.sort_choices_by)
        )

    def __iter__(self):
        self_queryset = sorted(self.queryset.all(), key=self._key_func)

        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)

        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = []

                for group, choices in groupby(self_queryset, key=self._key_func):
                    if self.field.sort_choices_by:
                        choices = self._sort_choices(choices)

                    self.field.choice_cache.append(
                        (
                            self.field.group_label(group),
                            [self.choice(ch) for ch in choices]
                        )
                    )

            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(self_queryset, key=self._key_func):

                if group is not None:

                    if self.field.sort_choices_by:
                        choices = self._sort_choices(choices)

                    yield (
                        self.field.group_label(group),
                        [self.choice(c) for c in choices]
                    )