from typing import Any

# qustions are question closures
def game_create(questions):
  score = 0
  saving_grace_cnt = 1
  curr_question: Any = None
  question_answered = False
  
  def play():
    nonlocal questions, curr_question, question_answered
    for question in questions:
      curr_question = question
      question_answered = False
      while not question_answered:
        curr_question["print_question"]()
        print("Twoj wybor: ", end="")
        cmd = input().strip()
        handle_command(cmd)
    print("Odpowiedziano na wszystkie pytania!!!\nKONIEC GRY\nWynik: ", score)

  def handle_command(cmd: str):
    nonlocal score, saving_grace_cnt, curr_question, question_answered
    correct_answer = curr_question["get_correct_answer"]()
    if cmd == correct_answer:
      score += 1
      question_answered = True
      print("Odpowiedz poprawna!\nWynik: ", score)
    elif cmd in ["A", "B", "C", "D"]: print("Odpowiedz bledna.\nKONIEC GRY\nWynik: ", score); exit()
    elif cmd == "K" and saving_grace_cnt <= 0: print("Brak kol ratunkowych do wykorzystania!")
    elif cmd == "K":
      saving_grace_cnt -= 1
      answers = curr_question["get_answers"]()
      new_answers = {"A": answers["A"]} if "A" != correct_answer else {"B": answers["B"]}
      new_answers[correct_answer] = answers[correct_answer]
      curr_question["set_answers"](new_answers)
    elif cmd == "exit": print("KONIEC GRY\nWynik: ", score); exit()
    else: print("Nie rozpoznana komenda")
      
  return {
    "play": play,
  }