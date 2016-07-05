from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class TextIn(models.Model):

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

    # define the model attributes
    slugId = models.SlugField(unique=True)
    data = models.TextField()
    lang = models.CharField(
            max_length=10,
            choices=lang_options,
            default=plain,
            )

    def is_lang(self):
        return self.lang

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.slugId
'''
class TextOut(models.Model):

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name
'''
