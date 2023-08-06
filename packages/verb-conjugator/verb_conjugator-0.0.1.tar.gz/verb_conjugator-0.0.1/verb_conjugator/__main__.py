import sys

from .verb_conjugator import VerbConjugator


def main():
    vc = VerbConjugator()

    while True:
        user_selection = vc.display_menu()
        if user_selection == "1":
            vc.setup()
            vc.display_verb_conjugation()
        elif user_selection == "2":
            vc.setup()
            vc.drill_and_practice()
        elif user_selection == "3":
            vc.common_verb_quiz_setup()
            verbs = vc.get_common_verbs()
            vc.common_verbs_quiz(verbs)
        else:
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
