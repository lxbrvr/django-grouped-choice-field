# grouped-multiple-model-choice-field

Grouping of model choices by field name.

Tested on Django 1.11 and Python 3.5

### Demo

![Demo 1](examples/Demo1.png?raw=true "Demo 1")
![Demo 2](examples/Demo2.png?raw=true "Demo 2")

### Using 

##### forms.py
```python
class ArticleForm(forms.Form):
    articles = GroupedMultipleModelChoiceField(
        group_by='category__name',
        sort_choices_by='-title',
        queryset=Article.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
```

##### template.html
```
{{ form.articles }}
```

##### Arguments:
- **group_by** - groups choices by specific model field. Supports related fields. Required.
- **sort_choices_by** - sorts choices by specific model field. Support a reversed sort with adding to string start '-'. Optional.