from django.core.exceptions import ValidationError
from django.test import TestCase
from cards.forms import EmailUserCreationForm
from cards.models import Card, Player
from cards.test_utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck


class BasicMathTestCase(TestCase):
    def test_math(self):
        a = 1
        b = 1
        self.assertEqual(a + b, 2)

    # def test_failing_case(self):
    #     a = 1
    #     b = 1
    #     self.assertEqual(a+b, 1)


class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)


class ModelTestCase(TestCase):
    def setUp(self):
        self.card = Card.objects.create(suit=Card.CLUB, rank="jack")

    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        self.assertEqual(self.card.get_ranking(), 11)

    def test_get_war_result_equal(self):
        """Test get war result"""
        card_1 = Card.objects.create(suit=Card.DIAMOND, rank="three")
        card_2 = Card.objects.create(suit=Card.DIAMOND, rank="three")
        self.assertEqual(card_1.get_war_result(card_2), 0)

    def test_get_war_result_win(self):
        """Test get war result"""
        card_1 = Card.objects.create(suit=Card.DIAMOND, rank="three")
        card_2 = Card.objects.create(suit=Card.DIAMOND, rank="two")
        self.assertEqual(card_1.get_war_result(card_2), 1)

    def test_get_war_result_lose(self):
        """Test get war result"""
        card_1 = Card.objects.create(suit=Card.DIAMOND, rank="three")
        card_2 = Card.objects.create(suit=Card.DIAMOND, rank="four")
        self.assertEqual(card_1.get_war_result(card_2), -1)


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username(self):
        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}
        self.assertEqual(form.clean_username(), 'test-user')


class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))
