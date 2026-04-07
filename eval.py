from generation import generate
import pandas as pd
import json 

cols = ["Question", "Type", "Retrieved?", "Answered?", "Notes"]
questions = []
with open("data/questions.json", 'r') as f:
    questions = json.load(f)

rows = []
for question in questions:
    answer = json.loads(generate(qst=question["question"]))
    retrieved = answer["retrieved"]
    answered = answer["answered"]
    row = [question["question"], question["type"], retrieved, answered, ""]
    rows.append(row)

df = pd.DataFrame(rows, columns=cols)
df.to_csv('data/evals/v1Eval.csv')