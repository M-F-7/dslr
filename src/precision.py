#!/usr/bin/env python3

from utils import *

def evaluate_on_train():
    """
    Évalue la précision du modèle sur le dataset d'entraînement.
    """
    # Charger le modèle
    model = load_model("model/theta.json")

    headers, data = load_data("datasets/dataset_train.csv")

    # Extraire les vraies maisons
    house_idx = headers.index("Hogwarts House")
    true_houses = [row[house_idx] for row in data]

    features, feature_names = extract_feature(headers, data, model["feature_names"])
    features = fix_dataset(features)
    features_norm, _ = normalize(features, model["norm_params"])

    m = len(features_norm)
    predictions = []

    for i in range(m):
        probabilities = {}

        for house in model["thetas"]:
            theta = model["thetas"][house]
            prob = predict_probability(features_norm[i], theta)
            probabilities[house] = prob

        predicted_house = max(probabilities, key=probabilities.get)
        predictions.append(predicted_house)

    correct = 0
    total = len(true_houses)
    errors = []

    for i in range(total):
        if true_houses[i] == predictions[i]:
            correct += 1
        else:
            errors.append({
                'index': i,
                'true': true_houses[i],
                'predicted': predictions[i]
            })

    accuracy = (correct / total) * 100

    print(f"\n{'='*60}")
    print(f"ÉVALUATION SUR LE DATASET D'ENTRAÎNEMENT")
    print(f"{'='*60}")
    print(f"Total d'exemples: {total}")
    print(f"Prédictions correctes: {correct}")
    print(f"Prédictions incorrectes: {total - correct}")
    print(f"\nPRÉCISION: {accuracy:.2f}%")
    print(f"{'='*60}\n")

    if errors:
        print(f"Exemples d'erreurs (max 10):")
        for err in errors[:10]:
            print(f"  Ligne {err['index']}: Prédit={err['predicted']}, Vrai={err['true']}")
        if len(errors) > 10:
            print(f"  ... et {len(errors) - 10} autres erreurs")
        print()

    houses = set(true_houses)
    print(f"Précision par maison:")
    for house in sorted(houses):
        house_total = sum(1 for h in true_houses if h == house)
        house_correct = sum(1 for i in range(total) if true_houses[i] == house and predictions[i] == house)
        house_accuracy = (house_correct / house_total) * 100 if house_total > 0 else 0
        print(f"  {house:12s}: {house_correct:3d}/{house_total:3d} = {house_accuracy:6.2f}%")

    return accuracy

def main():
    evaluate_on_train()

if __name__ == "__main__":
    main()
