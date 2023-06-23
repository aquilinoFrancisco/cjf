import spacy
import random
import es_core_news_sm
from spacy.util import minibatch, compounding
from sklearn.model_selection import train_test_split

#Fuente de datos: Tesis de la SCJN, 9a Época- 2a Sala  https://sjf2.scjn.gob.mx/busqueda-principal-tesis

"""Este código primero carga los datos del archivo tesis.txt. Los datos son una lista de pares de texto y etiqueta. Luego, el código preprocesa los datos donde el texto es una oración, después crea los conjuntos de datos de entrenamiento y prueba.

Después de preprocesar los datos, el código entrena el modelo NER en el conjunto de datos de entrenamiento. La fase de entrenamiento implica entrenar el modelo NER en el conjunto de datos de entrenamiento para 10 iteraciones.

Una vez que se entrena el modelo, el código lo evalúa en el conjunto de datos de prueba. La fase de evaluación implica evaluar el modelo en el conjunto de datos de prueba y calcular la precisión del modelo.

El método principal del código es main(). El método main() carga los datos, preprocesa los datos, entrena el modelo y evalúa el modelo.

Para ejecutar el código, deberá instalar la biblioteca spaCy y la biblioteca sklearn. Puede instalarlos usando los siguientes comandos:

pip install scikit-learn
pip spacy

Puede ejecutar el código desde la siguente línea de comando:

python ner.py

"""

def preprocess_dataset(dataset):
    texts = []
    annotations = []
    for data in dataset:
        text, entities,*_ = data
        texts.append(text)
        annotations.append({"entities": entities})
    return texts, annotations

def train_model(train_data, labels, iterations):
    nlp = spacy.blank("es")
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner)

    for label in labels:
        ner.add_label(label)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()

        for _ in range(iterations):
            random.shuffle(train_data)
            losses = {}

            for batch in minibatch(train_data, size=compounding(4.0, 32.0, 1.001)):
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.5, losses=losses)

    return nlp

def test_model(model, test_data):
    for text, entities in test_data:
        doc = model(text)
        predicted_entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        print("Text:", text)
        print("True Entities:", entities)
        print("Predicted Entities:", predicted_entities)
        print("----------------------------------------")

def main():
    # Load the SpaCy Spanish model
    nlp = spacy.load("es_core_news_sm")

    # Load and preprocess the dataset
    dataset = []
    for receipt in open("tesis.txt", encoding="utf-8"):
        receipt = receipt.strip()
        if receipt:
            dataset.append(receipt)

    texts, annotations = preprocess_dataset(dataset)

    # Split the dataset into training and testing sets, 80% for training and 20% for test
    train_texts, test_texts, train_annotations, test_annotations = train_test_split(texts, annotations, test_size=0.2, random_state=42)

    # Train the named entity identification model
    labels,*_ = list(set([ent[2] for entities in train_annotations for ent in entities["entities"]]))
    model = train_model(list(zip(train_texts, train_annotations)), labels, iterations=10)

    # Test the trained model
    test_data = list(zip(test_texts, test_annotations))
    test_model(model, test_data)

if __name__ == "__main__":
    main()