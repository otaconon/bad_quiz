from typing import Any

# qustions are question closures
def game_create(questions):
  score = 0
  lifeline_cnt = 1
  curr_question: Any = None
  question_answered = False
  should_quit = False
  
  # returns score 
  def play() -> int:
    nonlocal questions, curr_question, question_answered, should_quit
    for question in questions:
      curr_question = question
      question_answered = False
      while not question_answered:
        curr_question["print_question"]()
        print("Twoj wybor: ", end="")
        cmd = input().strip()
        handle_command(cmd)
      if should_quit: return score
    print("Odpowiedziano na wszystkie pytania!!!\nKONIEC GRY\nWynik: ", score)
    return score

  def handle_command(cmd: str):
    nonlocal score, lifeline_cnt, curr_question, question_answered, should_quit
    correct_answer = curr_question["get_correct_answer"]()
    if cmd == correct_answer:
      score += 1
      question_answered = True
      print("Odpowiedz poprawna!\nWynik: ", score)
    elif cmd in curr_question["get_answers"]():
      print("Odpowiedz bledna.\nKONIEC GRY\nWynik: ", score)
      question_answered = True
      should_quit = True
    elif cmd == "K" and lifeline_cnt <= 0:
      print("Brak kol ratunkowych do wykorzystania!")
    elif cmd == "K":
      lifeline_cnt -= 1
      curr_question["use_lifeline"]()
    elif cmd == "exit":
      print("KONIEC GRY\nWynik: ", score)
      exit()
    else:
      print("Nie rozpoznana komenda")
      
  return {
    "play": play,
  }