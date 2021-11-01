import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question


class QuestionModelTests(TestCase):
    """Test Question class in models.py."""

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions.
        whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date.
        is within the last day.
        """
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_on_time(self):
        """This test will return True if the question published on time."""
        time = timezone.now()
        is_on_time = Question(pub_date=time)
        self.assertIs(is_on_time.is_published(), True)

    def test_is_published_for_old_question(self):
        """This Test will return True for question which pub_date in past."""
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_can_vote_for_in_time_question(self):
        """This test will return True for questions which still can vote."""
        time = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=1)
        in_time_question = Question(pub_date=time, end_date=end_date)
        self.assertIs(in_time_question.can_vote(), True)

    def test_is_can_vote_for_out_of_date_question(self):
        """This test will return False for question that can't vote."""
        time = timezone.now()
        end_date = timezone.now() - datetime.timedelta(days=1)
        in_time_question = Question(pub_date=time, end_date=end_date)
        self.assertIs(in_time_question.can_vote(), False)
