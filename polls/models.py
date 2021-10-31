"""Models for ku polls."""

import datetime

from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User


class Question(models.Model):
    """Question model for ku polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date expired', null=True, default=timezone.now)

    def __str__(self):
        """Return questions."""
        return self.question_text

    def was_published_recently(self):
        """Return True if the question is published within one day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Return True if the question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return True if the question can be voted."""
        now = timezone.now()
        return self.end_date > now >= self.pub_date


class Choice(models.Model):
    """Choice model for ku polls."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choices."""
        return self.choice_text

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        return self.choice.question

    def __str__(self):
        return f"({self.user.username}) vote ({self.choice}) for ({self.question})"
