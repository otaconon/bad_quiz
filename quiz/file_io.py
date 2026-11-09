from question import question_create
from pathlib import Path

INDICATORS = ["Q", "A", "B", "C", "D", "S"]

def parse_line(line: str, expected_indicator: str) -> tuple[tuple[str, str], str | None]:
  indicator, content = line.split("\t")
  if indicator not in INDICATORS: return (("", ""), "INVALID_LINE_INDICATOR")
  if indicator != expected_indicator:
    if expected_indicator == "Q": return (("", ""), "MISSING_QUESTION")
    if expected_indicator in ["A", "B", "C", "D"]: return (("", ""), "MISSING_ANSWER")
    if expected_indicator == "S": return (("", ""), "MISSING_CORRECT_ANSWER")
  if indicator == "S" and content not in ["A", "B", "C", "D"]: return (("", ""), "INVALID_CORRECT_ANSWER")
  return ((indicator, content), None)

def load_questions(path: Path) -> tuple[list, str|None]:
  with open(path) as f:
    lines = f.readlines()
  
  questions = [] 
  question_lines = []
  for i, line in enumerate(lines):
    line = line.strip()
    expected_indicator = INDICATORS[i % len(INDICATORS)]
    result, err = parse_line(line.strip(), expected_indicator)
    if err != None: return ([], err)
    question_lines.append(result)
    if len(question_lines) == 6:
      questions.append(question_create(question_lines))
      question_lines = []
  if len(question_lines) != 0: return ([], "MISSING_LINES")
  return (questions, None)

def load_scores(path: Path) -> list[tuple[str, int]]:
  with open(path, "r+") as f: records = [line.rstrip("\r\n").split("\t") for line in f]
  if any(not name or any(c.isspace() for c in name) for name, _ in records): raise ValueError("Invalid player name")
  return [(name, int(value)) for name, value in records]

def write_scores(path: Path, records: list[tuple[str, int]]):
  with open(path, "w") as f:
    for name, score in records: f.write(name + "\t" + str(score) + "\n")