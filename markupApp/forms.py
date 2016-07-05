from django import forms
from markupApp.widgets import WYMEditor
from markupApp.models import TextIn

class TextInForm(forms.ModelForm):
    # make lang variables
    plain = 'RAW';
    latex = 'TEX';
    python = 'PY';
    c = 'C';
    # make a touple of the language options
    lang_options = (
    (plain,'Plain-Text'),
    (latex,'latex'),
    (python,'python-code'),
    (c,'C-code'),
    );

    slugId = forms.SlugField()
    data = forms.CharField(widget=WYMEditor())
    lang = forms.ChoiceField(choices=lang_options)
    class Meta:
        model=TextIn
        fields=('slugId','data','lang')
