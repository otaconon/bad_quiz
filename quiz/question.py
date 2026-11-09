def question_create(lines: list[str]):
  question = lines[0][1]
  answers = {indicator: content for indicator, content in lines[1:5]}
  correct_answer = lines[5][1]
  
  def print_question():
    nonlocal question, answers, correct_answer
    print(question)
    for letter, ans in answers.items():
      print(f"{letter}: {ans}")
      
  def get_question(): nonlocal question; return question
  def get_answers(): nonlocal answers; return answers
  def get_correct_answer(): nonlocal correct_answer; return correct_answer
  
  return {
    "print_question": print_question,
    "get_question": get_question,
    "get_answers": get_answers,
    "get_correct_answer": get_correct_answer
  }