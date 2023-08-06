import pytest
from verbecc import Conjugator

from verb_conjugator.verb_conjugator import VerbConjugator


@pytest.fixture(scope="session")
def verb_con():
    return VerbConjugator()


def test_empty_verb_conjugator_instance(verb_con):
    assert verb_con.selected_lang is None


def test_correct_language_keys(verb_con):
    test_dict = {"1": "", "2": ""}
    assert verb_con.languages.keys() == test_dict.keys()


def test_user_input(verb_con):
    "Test user input method returns what was passed in"
    user_input = verb_con.get_user_input(user_input="1")
    assert user_input == "1"


@pytest.mark.parametrize(
    "lang, expected",
    [
        ("1", "fr"),
        ("2", "es"),
    ],
)
def test_correct_language_code(verb_con, lang, expected):
    "Test if the correct language code returned when a lang is choosen"
    assert verb_con.get_language_code(lang) == expected


def test_incorrect_language_code_raises_exception(verb_con):
    "Test if the exception is raised when incorrect language option choosen"
    with pytest.raises(SystemExit):
        verb_con.get_language_code(99)


def test_nonexistent_french_verb_raises_exception(verb_con):
    "Want to test select_single_verb method"
    # verb_con.select_single_verb("verb")


def test_if_valid_french_moods_are_returned(verb_con):
    selected_moods = [1, 2, 3, 4, 5, 6]
    expected_moods = [
        "infinitif",
        "indicatif",
        "conditionnel",
        "subjonctif",
        "imperatif",
        "participe",
    ]
    verb = "aller"
    lang_code = "fr"
    conjugator_instance = Conjugator(lang_code)
    verb_con.conjugations = conjugator_instance.conjugate(verb)
    validated_moods = verb_con.validate_selected_mood(selected_moods)
    assert validated_moods == expected_moods


def test_if_invalid_moods_are_returned(verb_con):
    pass


def test_if_invalid_moods_not_returned(verb_con):
    pass


def test_validator_returns_correct_values(verb_con):
    entries = [1, 2, "d", 99, "bad", 4]
    item_list = [1, 2, 3, 4, 5, 6]
    good_entries, bad_entries = verb_con.validator(entries, item_list)
    assert good_entries == [1, 2, 4]
    assert bad_entries == ["d", 99, "bad"]


def test_sanitize_data_returns_correct(verb_con):
    assert verb_con.sanitize_data(" ALLER") == "aller"


@pytest.mark.parametrize(
    "args, expected",
    [
        (("je vais", "je vais"), True),
        (("I go", "je vais"), False),
        (("tu vas", "tu vas"), True),
        (("you go", "tu vas"), False),
    ],
)
def test_check_user_input(verb_con, args, expected):
    assert verb_con.check_user_input(*args) == expected
