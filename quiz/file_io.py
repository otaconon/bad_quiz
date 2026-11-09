from question import question_create

indicators = ["Q", "A", "B", "C", "D", "S"]
expected_indicator_idx = 0

def parse_line(line: str) -> tuple[tuple[str, str], str|None]:
  global expected_indicator_idx
  curr_expected_indicator = indicators[expected_indicator_idx]
  expected_indicator_idx = (expected_indicator_idx + 1) % len(indicators)
  indicator, content = line.split("\t")
  if curr_expected_indicator == indicator:
    if indicator == "S" and content not in ["A", "B", "C", "D"]: return (("", ""), "INVALID_CORRECT_ANSWER")
    return ((indicator, content), None)
  elif curr_expected_indicator == "Q": return (("", ""), "MISSING_QUESTION")
  elif curr_expected_indicator in ["A", "B", "C", "D"]: return (("", ""), "MISSING_ANSWER")
  elif curr_expected_indicator == "S": return (("", ""), "MISSING_CORRECT_ANSWER")
  else: return (("", ""), "INVALID_LINE_INDICATOR")

def load_questions(path: str) -> tuple[list, str|None]:
  with open(path) as f:
    lines = f.readlines()
  
  questions = [] 
  question_lines = []
  for line in lines:
    line = line.strip()
    result, err = parse_line(line)
    if err != None: return ([], err)
    question_lines.append(result)
    if len(question_lines) == 6:
      questions.append(question_create(question_lines))
      question_lines = []
  return (questions, None)

def load_scores(path: str) -> list[tuple[str, int]]:
  with open(path, "r") as f:
    records = [line.strip().split("\t") for line in f.readlines()]
    records = [(name, int(value)) for name, value in records]
  return records

def write_scores(path: str, records: list[tuple[str, int]]):
  with open(path, "w") as f:
    for name, score in records: f.write(name + "\t" + str(score) + "\n")