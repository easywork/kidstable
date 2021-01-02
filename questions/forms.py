from django import forms
from django.forms import formset_factory 

'''
Workflow:
* create form and then fromset
* render the form by outputing context['formset'] = formset
* html 

<form id="" method="post" action=""
      enctype="multipart/form-data">

    {% csrf_token %}

    {{ formset.management_form }}
    {% for form in formset %}
        {{ form }}
    {% endfor %}


<input type="submit" name="submit" value="Submit" />

https://www.geeksforgeeks.org/django-formsets/

'''

# class QuestionForm(forms.Form):
#     question = forms.CharField(label='0', max_length=100)


