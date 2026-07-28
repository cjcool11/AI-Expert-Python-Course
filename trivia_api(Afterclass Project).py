import requests
import html
import random

def get_questions():
    r = requests.get("https://opentdb.com/api.php?amount=5&type=multiple")
    return r.json()["results"]

def run_quiz():
    score = 0
    questions = get_questions()
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {html.unescape(q['question'])}")
        answers = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(answers)
        for idx, ans in enumerate(answers, 1):
            print(f"{idx}. {html.unescape(ans)}")
        choice = input("Your answer: ")
        if answers[int(choice)-1] == q["correct_answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! Correct answer: {html.unescape(q['correct_answer'])}\n")
    print(f"Final Score: {score}/{len(questions)}")

run_quiz()
