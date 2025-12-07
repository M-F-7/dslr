#!/usr/bin/env python3

from sklearn.metrics import accuracy_score
import csv
import sys

def load_predictions(filename):
    """
    Charge les prédictions depuis le fichier houses.csv
    """
    predictions = []
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                predictions.append(row['Hogwarts House'])
    except Exception as e:
        print("an error has occurred:", e)
        exit(1)
    return predictions

def load_true_labels(filename):
    """
    Charge les vraies étiquettes depuis un fichier CSV
    """
    true_labels = []
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                house = row['Hogwarts House']
                if house:
                    true_labels.append(house)
    except Exception as e:
        print("an error has occurred:", e)
        exit(1)
    return true_labels

def evaluate_predictions(predictions_file, truth_file, dataset_name="TEST"):
    """
    Évalue la précision du modèle en utilisant scikit-learn

    Args:
        predictions_file: Fichier contenant les prédictions
        truth_file: Fichier contenant les vraies étiquettes
        dataset_name: Nom du dataset pour l'affichage
    """
    predictions = load_predictions(predictions_file)
    true_labels = load_true_labels(truth_file)

    if len(true_labels) == 0:
        print(f"\nerror: no labels found in {truth_file}")
        print(f"the test file does not contain true labels.")
        print(f"to evaluate on the training dataset, use:")
        print(f"  python3 src/precision.py train")
        return None

    if len(predictions) != len(true_labels):
        print(f"\nwarning: number of predictions ({len(predictions)}) != number of true labels ({len(true_labels)})")
        min_len = min(len(predictions), len(true_labels))
        predictions = predictions[:min_len]
        true_labels = true_labels[:min_len]

    accuracy = accuracy_score(true_labels, predictions)
    accuracy_percent = accuracy * 100

    min_accuracy = 98.0

    print(f"\n{'='*60}")
    print(f"evaluation on {dataset_name.lower()} dataset")
    print(f"{'='*60}")
    print(f"total examples: {len(true_labels)}")
    print(f"correct predictions: {int(accuracy * len(true_labels))}")
    print(f"incorrect predictions: {len(true_labels) - int(accuracy * len(true_labels))}")
    print(f"\naccuracy (scikit-learn): {accuracy_percent:.2f}%")
    print(f"minimum required threshold: {min_accuracy}%")
    print(f"{'='*60}\n")

    if accuracy_percent >= min_accuracy:
        print(f"success! the algorithm is comparable to the sorting hat!")
        print(f"  accuracy: {accuracy_percent:.2f}% >= {min_accuracy}%")
    else:
        print(f"failure. the algorithm does not meet the required threshold.")
        print(f"  accuracy: {accuracy_percent:.2f}% < {min_accuracy}%")
        print(f"  missing {min_accuracy - accuracy_percent:.2f}% to reach the goal.")
    print()

    houses = sorted(set(true_labels))
    print(f"accuracy per house:")
    for house in houses:
        house_indices = [i for i, h in enumerate(true_labels) if h == house]
        house_total = len(house_indices)
        house_correct = sum(1 for i in house_indices if predictions[i] == house)
        house_accuracy = (house_correct / house_total) * 100 if house_total > 0 else 0
        print(f"  {house:12s}: {house_correct:3d}/{house_total:3d} = {house_accuracy:6.2f}%")

    return accuracy_percent

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        print("evaluating on training dataset...")
        evaluate_predictions("houses.csv", "datasets/dataset_train.csv", "train")
    else:
        print("evaluating on test dataset...")
        evaluate_predictions("houses.csv", "datasets/dataset_test.csv", "test")

if __name__ == "__main__":
    main()
