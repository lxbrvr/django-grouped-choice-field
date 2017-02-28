# grouped-multiple-model-choice-field

### Requirements

- Django

### Description

MultipleModelChoiceField wrapper. Groups choices by specific model field.

### Using

*forms.py*

```python
    class TopicForm(forms.ModelForm):
        topics = GroupedMultipleModelChoiceField(
            group_by='theme__title',
            sort_choices_by='title',
            queryset=Topic.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )
            
    #   Animal
    #       Cats
    #       Dogs
    #
    #   News
    #       Business
    #       Science
    #       People
```

*template.html*

```
{{ form.topics }}

```

### Parameters

- **group_by** - groups choices by specific model field. Supports related fields. Required parameter.
- **sort_choices_by** - sorts choices by specific model field. Optional parameter.
