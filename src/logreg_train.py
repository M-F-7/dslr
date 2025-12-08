#!/usr/bin/env python3

from utils import *

def batch_gradient_descent(features_norm: list, label: list, n: int, l_rate: float = 0.025, iterations: int = 1000) -> list:
	m = len(features_norm)
	theta = [0] * (n + 1)

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

	return theta


def stochastic_gradient_descent(features_norm: list, label: list, n: int, l_rate: float = 0.01, epochs: int = 100) -> list:
	from random import shuffle

	m = len(features_norm)
	theta = [0] * (n + 1)

	for _ in range(epochs):
		indices = list(range(m))
		shuffle(indices)

		for idx in indices:
			predict = predict_probability(features_norm[idx], theta)
			error = predict - label[idx]

			theta[0] -= l_rate * error
			for j in range(n):
				theta[j + 1] -= l_rate * (error * features_norm[idx][j])

	return theta


def mini_batch_gradient_descent(features_norm: list, label: list, n: int, l_rate: float = 0.025, epochs: int = 200, batch_size: int = 32) -> list:
	from random import shuffle

	m = len(features_norm)
	theta = [0] * (n + 1)

	for _ in range(epochs):
		indices = list(range(m))
		shuffle(indices)

		for i in range(0, m, batch_size):
			batch_indices = indices[i:i + batch_size]
			gd = [0] * (n + 1)

			for idx in batch_indices:
				predict = predict_probability(features_norm[idx], theta)
				error = predict - label[idx]

				gd[0] += error
				for j in range(n):
					gd[j + 1] += (error * features_norm[idx][j])

			batch_len = len(batch_indices)
			for j in range(n + 1):
				gd[j] /= batch_len
				theta[j] -= l_rate * gd[j]

	return theta


def logreg_train(file: str="datasets/dataset_train.csv", method: str = "batch"):
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

		if method == "batch":
			theta = batch_gradient_descent(features_norm, label, n, l_rate=0.025, iterations=1000)
		elif method == "sgd":
			theta = stochastic_gradient_descent(features_norm, label, n, l_rate=0.01, epochs=100)
		elif method == "mini-batch":
			theta = mini_batch_gradient_descent(features_norm, label, n, l_rate=0.025, epochs=200, batch_size=32)
		else:
			raise ValueError(f"Unknown training method: {method}. Available: 'batch', 'sgd', 'mini-batch'")

		val_set[cl] = theta

	model = {
		"thetas": val_set,
		"norm_params": norm_params,
		"feature_names": feature_names
	}
	save_theta(model)

def main():
	logreg_train(method="batch")

if __name__ == "__main__":
	main()