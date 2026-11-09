def question_create(lines: list[str]):
  question = lines[0][1]
  answers = {indicator: content for indicator, content in lines[1:5]}
  correct_answer = lines[5][1]
  
  def print_question():
    print(question)
    for letter, ans in answers.items():
      print(f"{letter}: {ans}")
      
  def use_lifeline():
    nonlocal answers
    new_answers = {"A": answers["A"]} if "A" != correct_answer else {"B": answers["B"]}
    new_answers[correct_answer] = answers[correct_answer]
    answers = new_answers
      
  def get_question(): return question
  def get_answers(): return answers
  def get_correct_answer(): return correct_answer
  
  return {
    "print_question": print_question,
    "use_lifeline": use_lifeline,
    "get_question": get_question,
    "get_answers": get_answers,
    "get_correct_answer": get_correct_answer
  }