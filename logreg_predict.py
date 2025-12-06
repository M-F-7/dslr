# z = θ₀ + θ₁*x₁ + θ₂*x₂ + ... + θₙ*xₙ

# probabilité = sigmoid(z) = 1 / (1 + e^(-z))

from utils import *

def logreg_predict(fichier_test, fichier_model):
    model = load_data("./model/theta.json")

    headers, data = load_data(fichier_test)
    features, feature_names = extract_feature(headers, data)
    features = fix_dataset(features)
    features_norm, _ = normalize(features, model["norm_params"])
    
    m = len(features_norm)
    classes = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    
    predictions = []
    
    for i in range(m):
        probabilities = {}
        
        for house in classes:
            theta = model["thetas"][house]
            prob = predict_probability(features_norm[i], theta)
            probabilities[house] = prob
        
        attribution = max(probabilities, key=probabilities.get)
        predictions.append(attribution)
    
    with open("houses.csv", "w") as f:
        f.write("Index,Hogwarts House\n")
        for i, house in enumerate(predictions):
            f.write(f"{i},{house}\n")
    
    print("prediciton saved in houses.csv")


def main():
	logreg_predict("datasets/dataset_test.csv", "model/theta.json")

if __name__ == "__main__":
	main()