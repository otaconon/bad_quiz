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
    elif cmd in ["A", "B", "C", "D"]:
      print("Odpowiedz bledna.\nKONIEC GRY\nWynik: ", score)
      exit()
    elif cmd == "K":
      print("Brak kol ratunkowych do wykorzystania!")
      saving_grace_cnt -= 1
    elif cmd == "exit":
      print("KONIEC GRY\nWynik: ", score)
      exit()
    else: print("Nie rozpoznana komenda")
      
  return {
    "play": play,
  }