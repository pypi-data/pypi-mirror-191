import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from verbecc import Conjugator


class RandomVerb(NamedTuple):
    verb: str
    tense: str
    conjugation: str


class VerbConjugator:
    def __init__(self):
        self.languages = {
            "1": {"code": "fr", "language": "French"},
            "2": {"code": "es", "language": "Spanish"},
        }
        self.user_input = None
        self.selected_lang = None
        self.lang_code = None
        self.conjugator_instance = None
        self.conjugations = None
        self.selected_mood_and_tense = {}
        self.moods = []
        self.mood_names = []
        self.mood_tense = {}

    def display_language(self):
        print("Select a target language")
        for key in self.languages.keys():
            print(f'{key} - {self.languages[key]["language"]}')

    def get_user_input(self, prompt="--> ", user_input=None):
        user_input = user_input or input(prompt)
        return user_input

    def get_language_code(self, language):
        lang_code = None
        try:
            lang_code = self.languages[language]["code"]
        except KeyError:
            print("Enter a valid number from the list to choose a language")
            sys.exit(1)  # raise SystemExit
        return lang_code

    # def get_language_instance(self, lang_code):
    #     self.conjugator_instance = Conjugator(lang=lang_code)

    def select_single_verb(self, verb=None):
        verb_conjugation = None
        verb = verb or input("Enter the verb to practice conjugating --> ")
        try:
            verb_conjugation = self.conjugator_instance.conjugate(verb)
        except AttributeError:
            print(f"{verb} does appear to be a valid verb")
        else:
            return verb_conjugation

    def display_mood(self):
        moods = self.conjugations["moods"].keys()
        for index, mood in enumerate(moods):
            print(f"{index +1 } - {mood}")

    def validate_selected_mood(self, selected_moods):
        entries_list = list(self.conjugations["moods"])
        good_entries, bad_entries = self.validator(selected_moods, entries_list)

        if bad_entries:
            print(f"\nThe following are not valid entries {bad_entries}")
        return good_entries

    def validate_selected_tense(self, mood, selected_tenses):
        selected_mood_and_tense = {}
        tenses = list(self.conjugations["moods"][mood])
        good_entries, bad_entries = self.validator(selected_tenses, tenses)
        selected_mood_and_tense[mood] = good_entries

        if bad_entries:
            print(f"\nThe following are not valid entries {bad_entries}")
        return selected_mood_and_tense

    def select_tense(self, selected_moods, tense_lists):
        mood_tense_dict = {}
        for i, mood in enumerate(selected_moods):
            tense_list = tense_lists[i].split()
            validated_tenses = self.validate_selected_tense(mood, tense_list)
            mood_tense_dict.update(validated_tenses)
        return mood_tense_dict

    def display_tense(self, mood_name):
        tenses = list(self.conjugations["moods"][mood_name].keys())
        for index, tense in enumerate(tenses):
            print(f"{index + 1 } - {tense}")

    def validator(self, entries, item_list):
        bad_entries, good_entries = [], []
        correct_numbers = range(len(item_list))
        index = -1
        for entry in entries:
            try:
                index = int(entry) - 1
            except ValueError:
                bad_entries.append(entry)
                continue

            if index in correct_numbers:
                good_entries.append(item_list[index])
            else:
                bad_entries.append(entry)
        return good_entries, bad_entries

    def quiz_user(self):
        for mood in self.mood_tense.keys():
            tenses = self.mood_tense[mood]
            for tense in tenses:
                print(f"\nConjugate the {tense} tense in the {mood} mood")
                conjugated_pronouns = self.conjugations["moods"][mood][tense]
                for pronoun in conjugated_pronouns:
                    self.quiz_question(pronoun)

    def sanitize_data(self, verb):
        verb = verb.strip().replace(" ", "").lower()
        return verb

    def check_user_input(self, user_answer, correct_answer):
        "Check if the user entered the correct/expected conjugation"
        if self.sanitize_data(user_answer) == self.sanitize_data(correct_answer):
            print("Correct")
            return True
        else:
            print(f"Sorry the answer is {correct_answer}")
            return False

    def drill_and_practice(self):
        while True:
            self.quiz_user()
            try:
                user_repeat = input(
                    "Do you want to practice this one again? 1-Yes, 2-No --> "
                )
            except ValueError:
                print("Invalid entry")
            if user_repeat == "1":
                continue
            else:
                break

    def display_verb_conjugation(self):
        "Displays the conjugation of the verb in the selected mood and tense"

        for mood, tenses in self.mood_tense.items():
            for tense in tenses:
                print(f"\n{mood} - {tense} tense")
                conjugated_pronouns = self.conjugations["moods"][mood][tense]
                for pronoun in conjugated_pronouns:
                    print(pronoun)

    def setup(self):
        self.display_language()
        self.selected_lang = self.get_user_input()
        self.lang_code = self.get_language_code(self.selected_lang)
        self.conjugator_instance = Conjugator(self.lang_code)
        self.conjugations = self.select_single_verb()
        if not self.conjugations:
            print("Unable to continue")
            sys.exit("Exiting")
        self.display_mood()
        self.moods = self.get_user_input(
            prompt="Select the mood(s) separated by a space --> "
        )
        self.moods = self.moods.split()
        self.mood_names = self.validate_selected_mood(self.moods)

        tense_lists = []
        for mood in self.mood_names:
            self.display_tense(mood)
            tense_lists.append(
                self.get_user_input(
                    prompt="Select the tense(s) to practice, separated by a space --> "
                )
            )
        self.mood_tense = self.select_tense(self.mood_names, tense_lists)

    def display_menu(self):
        print("\nSelect an option:")
        print("1 - Display verb conjugation ")
        print("2 - Single verb quiz")
        print("3 - Common verbs quiz")
        print("4 - Exit")
        selection = input("--> ")
        return selection

    def common_verbs_quiz(self, common_verbs):
        lang_code = self.lang_code
        mood = common_verbs[lang_code]["mood"]
        new_verbs = common_verbs[lang_code]["verbs"]
        tenses = common_verbs[lang_code]["tenses"]

        verbs = defaultdict(dict)
        for verb in new_verbs:
            self.conjugations = self.select_single_verb(verb=verb)
            for tense in tenses:
                verbs[verb][tense] = {}
                verbs[verb][tense] = self.conjugations["moods"][mood][tense]

        continue_loop = True
        print("Welcome to random common verb quiz, press q to quit at anytime")
        while continue_loop:
            random_verb = self.get_random_conjugation(verbs, tenses)
            print(f"\n{random_verb.tense} - {random_verb.verb}")
            continue_loop = self.quiz_question(random_verb.conjugation)

    def get_common_verbs(self):
        common_verbs = Path("verb_conjugator") / "common_verbs.txt"
        with open(common_verbs) as file1:
            return json.loads(file1.read())

    def get_random_conjugation(self, verbs, tenses) -> RandomVerb:
        random_verb = random.choice(list(verbs.keys()))
        random_tense = random.choice(list(tenses))
        random_conjugation = random.choice(list(verbs[random_verb][random_tense]))
        return RandomVerb(random_verb, random_tense, random_conjugation)

    def quiz_question(self, pronoun):
        split_pronoun = pronoun.split()
        answer = self.get_user_input(prompt=f"-->{split_pronoun[0]} ")
        answer = answer.strip()
        if answer == "q":
            return False
        else:
            answer = f"{split_pronoun[0]} {answer}"
            split_pronoun = f"{split_pronoun[0]} {split_pronoun[1]}"
            self.check_user_input(answer, split_pronoun)
            return True

    def common_verb_quiz_setup(self):
        self.display_language()
        self.selected_lang = self.get_user_input()
        self.lang_code = self.get_language_code(self.selected_lang)
        self.conjugator_instance = Conjugator(self.lang_code)
