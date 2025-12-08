# z = θ₀ + θ₁*x₁ + θ₂*x₂ + ... + θₙ*xₙ
# probabilité = sigmoid(z) = 1 / (1 + e^(-z))

from utils import *

def logreg_predict(fichier_test, fichier_model):
    model = load_model(fichier_model)

    headers, data = load_data(fichier_test)
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

    with open("houses.csv", "w") as f:
        f.write("Index,Hogwarts House\n")
        for i, house in enumerate(predictions):
            f.write(f"{i},{house}\n")

    print("Predictions saved in houses.csv")


def main():
	logreg_predict("datasets/dataset_test.csv", "model/theta.json")

if __name__ == "__main__":
	main()