

import datetime
import os

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.


@python_2_unicode_compatible
class Question(models.Model):
    """ here is the question models. contain question_text, description, pub_date and image
    """
    question_text = models.CharField(max_length=200)
    question_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="polls/static/polls/media")
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """return the boolean value if the question are the latest published """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True
        was_published_recently.short_description = 'Published recently?'

    @property
    def imagename(self):
       """return the images path"""
       return ('polls/media/'+str(self.image).split('/')[-1])


@python_2_unicode_compatible
class Choice(models.Model):
    """ objects contain the choices and votes of each question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
