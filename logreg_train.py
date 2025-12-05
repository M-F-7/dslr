#!/usr/bin/env python3

from utils import *


def logreg_train(file: str="datasets/dataset_train.csv"):
	headers, data = load_data(file)

	features, feature_names = extract_feature(headers, data)

	houses = extraire_colonne(headers, data, "Hogwarts House")

	features = fix_dataset(features)

	# m = len(features)
	# print(f"exemples: {m}")
	# print(f"features: {feature_names}")
	# print(f"maisons: {set(houses)}")
	# features_norm, norm_params = normalize(features)
	# print(features_norm, norm_params)

	houses = set(houses)
	val_set = {}
	# use this to store wight and bias for each house
	# then predict the probability for each house
	# then the student must be from the highest probabvility after prediction from eahc house using val_set


def main():
	logreg_train()

if __name__ == "__main__":
	main()