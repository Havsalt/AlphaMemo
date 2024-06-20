"""
AlphaMemo

Script to help you memorize the position of each letter in the alphabet
"""

import random
import time
import os
from enum import Enum, auto
from string import ascii_lowercase, ascii_uppercase, digits

import keyboard
import colex
from actus import info, error, LogSection, Style


ANSWER_TIME_VARIATION = 1
ANSWER_TIME_MINIMUM   = 2
QUESTION_SLEEP_TIME   = 1
MARGIN_LEFT = 20
MARGIN_TOP  = 5
ALPHABET: list[tuple[str, str]] = list(zip(ascii_lowercase, ascii_uppercase))


class QuestionMode(Enum):
    POSITION = auto()
    CHARACTER = auto()


LEFT_DECO = " " * MARGIN_LEFT + "["

show_points = LogSection(
    "Poeng",
    left_deco=LEFT_DECO,
    style=Style(
        label=colex.PALE_GOLDENROD
    )
)
show_letter = LogSection(
    "Bokstav",
    left_deco=LEFT_DECO,
    style=Style(
        label=colex.AQUA
    )
)
show_position = LogSection(
    "Plass",
    left_deco=LEFT_DECO,
    style=show_letter.get_style_copy()
)
show_right = LogSection(
    "Ja",
    left_deco=LEFT_DECO,
    style=info.get_style_copy()
)
show_wrong = LogSection(
    "Nei",
    left_deco=LEFT_DECO,
    style=error.get_style_copy()
)
show_unanswered = LogSection(
    "Ingen svar",
    left_deco=LEFT_DECO,
    style=Style(
        label=colex.SALMON
    )
)


def main() -> int:
    key_buffer: list[keyboard.KeyboardEvent] = []

    def on_press(key: keyboard.KeyboardEvent) -> None:
        valid = ascii_lowercase + digits
        if key.name is not None and key.name in valid:
            key_buffer.append(key)
    
    keyboard.on_press(on_press)
    points = 0

    try:
        info("$[Starter snart]...")
        time.sleep(1)
        info("$[Startet]!")
        while True:
            # safe clear
            key_buffer.clear()
            os.system("cls")
            for _ in range(MARGIN_TOP):
                print()
            show_points(f"#$[{points:02}]")
            # generate question data
            char_variants = random.choice(ALPHABET)
            char = random.choice(char_variants)
            position = ascii_lowercase.index(char_variants[0]) + 1
            answer_time = random.random() * ANSWER_TIME_VARIATION + ANSWER_TIME_MINIMUM
            # print(f"Dev: {answer_time = :.2f}")
            t0 = time.time()
            answer: str | None = None
            mode = random.choice(list(QuestionMode))
            # ask question
            match mode:
                case QuestionMode.POSITION:
                    show_position(f"Plass: $[{char}]")
                case QuestionMode.CHARACTER:
                    show_letter(f"Bokstav: $[{position}]")
                # TODO: add neighbour cases
            # take answer
            while time.time() - t0 <= answer_time:
                current_key_names = [
                    key.name
                    for key in key_buffer
                    if key.name is not None
                ]
                if mode == QuestionMode.CHARACTER:
                    if current_key_names:
                        answer = current_key_names[0].lower()
                        key_buffer.clear()
                        break
                elif mode == QuestionMode.POSITION:
                    if len(str(position)) == 1 and current_key_names: # result is 1 char long
                        answer = current_key_names[0].lower() # 2 is max length of number position in alphabet
                        key_buffer.clear()
                        break
                    elif len(current_key_names) >= 2:
                        answer = "".join(current_key_names[:2]).lower() # 2 is max length of number position in alphabet
                        key_buffer.clear()
                        break
            # validate result
            match mode:
                case QuestionMode.POSITION:
                    if answer == str(position):
                        show_right(f"$[{char}] = $[{position}]")
                        points += 1
                    elif answer is None:
                        show_unanswered(f"$[{char}] = $[{position}]")
                    else:
                        show_wrong(f"($[{answer}]), $[{char}] = $[{position}]")
                case QuestionMode.CHARACTER:
                    if answer == char_variants[0]:
                        show_right(f"$[{position}] = $[{char}]")
                        points += 1
                    elif answer is None:
                        show_unanswered(f"$[{position}] = $[{char}]")
                    else:
                        show_wrong(f"($[{answer}]), $[{position}] = $[{char}]")
            # time until next question
            time.sleep(QUESTION_SLEEP_TIME)
    except KeyboardInterrupt:
        keyboard.unhook_all()
        return 0
