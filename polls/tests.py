"""Tests for ku polls."""

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    """Create a question with the given `question_text`.

    Args:
        question_text
        days
    Returns: Question object
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Tests for question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions \
        whose pub_date is in the future.

        Returns: False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions \
        whose pub_date is older than 1 day.

        Returns: False
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions \
        whose pub_date is within the last day.

        Returns: True
        """
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_old_question(self):
        """is_published returns True for questions \
        whose pub_date is older than current time.

        Returns: True
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published returns False for questions \
        whose pub_date is newer than current time.

        Returns: False
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_ongoing_question(self):
        """is_published() return True for questions \
        whose pub_date is less than or equal to current time.

        Returns: True
        """
        time = timezone.now()
        ongoing_question = Question(pub_date=time)
        self.assertIs(ongoing_question.is_published(), True)

    def test_can_vote_with_expired_question(self):
        """can_vote returns False for questions \
        whose end_date is older than current time.

        Returns: False
        """
        pub_date = timezone.now() - datetime.timedelta(days=7)
        end_date = timezone.now() - datetime.timedelta(days=1)
        expired_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(expired_question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote returns False for question \
        whose pub_dateis newer than current time.

        Returns: False
        """
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=7)
        future_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_ongoing_question(self):
        """can_vote returns True for questions whose pub_date is older \
        than current time and end_date is newer than current time.

        Returns: True
        """
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=7)
        ongoing_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ongoing_question.can_vote(), True)


class QuestionIndexViewTests(TestCase):
    """Tests for question index."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the \
        index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on \
        the index page.

        Returns: True
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions \
        are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Tests for question detail."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future.

        Returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        past_question.end_date = timezone.now() + datetime.timedelta(days=10)
        past_question.save()
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
