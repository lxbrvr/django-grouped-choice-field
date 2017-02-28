# grouped-multiple-model-choice-field

### Requirements

- Django

### Description

MultipleModelChoiceField wrapper. Groups choices by specific model field.

### Using

    class TopicForm(forms.ModelForm):
        your_field = GroupedMultipleModelChoiceField(
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
    #       Busines
    #       Sciece
    #       People

- **group_by** - groups choices by specific model field. Supports related fields. Required parameter.
- **sort_choices_by** - sorts choices by specific model field. Optional parameter.
