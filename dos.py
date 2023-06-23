import nltk
import random

#Fuente de datos: Tesis de la SCJN, 9a Época- 2a Sala  https://sjf2.scjn.gob.mx/busqueda-principal-tesis
#Modeo de preguntas y respuestas: Le preguntas que tipo es un entidad, por ejemplo "aquilino" o 1455, Tribunal y te devuelve la etiqueta correspondiente
#Solo tienes que ejecutarlo con python dos.py
def train(data):
  """Trains the model on the given data."""
  model = {}
  for question, answer in data:

    for question_token in question:
      if question_token not in model:
        model[question_token] = []
      model[question_token].append(answer)
  return model

def predict(model, question):
  """Predicts the answer to the given question."""
  scores = {}
  for question_token in question:
    if question_token in model:
      for answer in model[question_token]:
        score = len(list(set(answer) & set(question)))
        scores[answer] = scores.get(answer, 0) + score
  best_answer = max(scores, key=scores.get)
  return best_answer

def main():
  """Loads the data, trains the model, and predicts the answer to a question."""
  data = []
  for line in open('train.txt', encoding="utf-8"):
    question, answer = line.strip().split('\t')
    data.append((question, answer))

  model = train(data)
  question = input('Ingresa una entidad y te digo que tipo de que tipo es: ')
  answer = predict(model, question)
  print('La respuesta es:', answer)

if __name__ == '__main__':
  main()