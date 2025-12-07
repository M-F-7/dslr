#!/usr/bin/env python3

from utils import *


def logreg_train(file: str="datasets/dataset_train.csv"):
	headers, data = load_data(file)

	features, feature_names = extract_feature(headers, data)

	houses = extraire_colonne(headers, data, "Hogwarts House")

	features = fix_dataset(features)

	m = len(features)
	n = len(feature_names)
	# print(f"exemples: {m}")
	# print(f"features: {feature_names}")
	# print(f"maisons: {set(houses)}")
	features_norm, norm_params = normalize(features)
	# print(features_norm, norm_params)

	val_set = {}
	
	# use this to store wight and bias for each house
	# then predict the probability for each house
	# then the student must be from the highest probabvility after prediction from eahc house using val_set

	#  θⱼ = θⱼ - α × (1/m) × Σ(h(x) - y) × xⱼ
	#   Où :
	#   - α = learning rate (0.1)
	#   - h(x) = prédiction
	#   - y = label réel
	#   - m = nombre d'exemples
	for cl in set(houses):
		label = [0]*m
		for j in range(m):
			if houses[j] == cl:
				label[j] = 1
			else:
				label[j] = 0

		theta = [0] * (n + 1)

		l_rate = 0.025
		iterations = 1000

		for _ in range(iterations):
			gd = [0] * (n + 1)
			for k in range(m):
				predict = predict_probability(features_norm[k], theta)
				error = predict - label[k]

				gd[0] += error
				for l in range(n):
					gd[l + 1] += (error * features_norm[k][l])

			for j in range(n + 1):
				gd[j] /= m
				theta[j] -= (l_rate * gd[j])

		val_set[cl] = theta

	model = {
		"thetas": val_set,
		"norm_params": norm_params,
		"feature_names": feature_names
	}
	save_theta(model)
				




def main():
	logreg_train()

if __name__ == "__main__":
	main()