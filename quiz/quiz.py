import argparse
import file_io
from pathlib import Path
from game import game_create

def play_quiz(questions_path: Path, scores_path: Path):
  try: questions, err = file_io.load_questions(questions_path)
  except ValueError: print("ERROR: Questions file has incorrect format: ", scores_path); exit(1)
  if err != None: print("ERROR: ", err); exit(1)
  
  try: records = file_io.load_scores(scores_path)
  except PermissionError: print("ERROR: Couldnt't open records file, permission error: ", scores_path); exit(1)
  except ValueError: print("ERROR: Scores file has incorrect format: ", scores_path); exit(1)
  
  game = game_create(questions)
  score = game["play"]()
  
  if len(records)<5 or any(s < score for _, s in records):
    print("Prosze podac imie celem zapisania wyniku: ", end="")
    name = input()
    while not name or any(c.isspace() for c in name):
      print("Podane imię zawiera niedozwolony znak.")
      print("Prosze podac imie celem zapisania wyniku: ", end="")
      name = input()
    records.append((name, score))
  records.sort(key=lambda item: item[1], reverse=True)
  
  try: questions = file_io.write_scores(scores_path, records[:min(5, len(records))])
  except OSError: print("ERROR: Failed to write scores: ", scores_path); exit(1)
  
def print_menu():
  print("1 - Zagraj ponownie")
  print("2 - Najlepsi gracze")
  print("3 - Wyjdz z gry")
  
def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="quiz")
  parser.add_argument("-q", "--questions_path", type=str, default="pytania.txt")
  parser.add_argument("-s", "--scores_path", type=str, default="wyniki.txt")
  return parser

def main(argv: list[str] | None = None):
  parser = build_parser()
  args = parser.parse_args(argv)
  questions_path = Path(args.questions_path)
  scores_path = Path(args.scores_path)
  
  choice = "1"
  while choice != "3":
    if choice == "1": play_quiz(questions_path, scores_path)
    if choice == "2": print(scores_path.read_text())
    print_menu()
    choice = input()

if __name__ == "__main__":
  main()