import csv
import json
from math import exp



def sigmoid(z: int) -> float:
	"""
		return a float between 0-1.
	"""
	return (1 / (1 + exp(-z)))

def predict_probability(x: list, theta: list) -> float:
	z = theta[0]
	for i in range(1, len(theta)):
		z = z + (theta[i] * x[i - 1])
	return sigmoid(z) 


def load_data(file: str) -> list:
	data = []
	try:
		with open(file, 'r') as f:
			reader = csv.reader(f)
			headers = next(reader) 
			for row in reader:
				data.append(row)
	except Exception as e:
		print("an error occured :", e)
		exit(1)
	return headers, data

def extract_feature(headers: str, data: list, specific_features: list = None) -> list:
	"""
	Extrait les features numériques du dataset.
	Si specific_features est fourni, extrait uniquement ces features dans cet ordre.
	"""
	features = []
	feature_idx = []
	feature_names = []

	if specific_features is not None:
		# Extraire uniquement les features spécifiées
		for feature_name in specific_features:
			if feature_name in headers:
				idx = headers.index(feature_name)
				feature_idx.append(idx)
				feature_names.append(feature_name)
	else:
		# Extraire toutes les features numériques
		for i, header in enumerate(headers):
			try:
				for row in data:
					if row[i] != '':
						float(row[i])
						break
				feature_idx.append(i)
				feature_names.append(header)
			except ValueError:
				pass

	for row in data:
		feature_row = []
		for i in feature_idx:
			if row[i] == '':
				feature_row.append(None)
			else:
				feature_row.append(float(row[i]))
		features.append(feature_row)

	return features, feature_names

def fix_dataset(features: list) -> list:
	"""
	used in case we have a msising value so that it won't impact our calculation.\n
	for exemple --  z = theta[0] + theta[1] * None + theta[2] * 85.\n
	None will be replaced by the average od the dataset so that it won't matter.
	"""
	n_features = len(features[0])
	
	avg = []
	for j in range(n_features):
		valeurs = [row[j] for row in features if row[j] is not None]
		if len(valeurs) > 0:
			moyenne = sum(valeurs) / len(valeurs)
		else:
			moyenne = 0
		avg.append(moyenne)
	
	for i in range(len(features)):
		for j in range(n_features):
			if features[i][j] is None:
				features[i][j] = avg[j]
	
	return features

def extraire_colonne(headers: str, data: list, nom_colonne: str) -> list:
	index = headers.index(nom_colonne)
	return [row[index] for row in data]


def normalize(data: list, params: dict = None) -> tuple:
	if not data or not data[0]:
		return data, params

	n_features = len(data[0])
	data_norm = []

	if params is None:
		params = {}
		for j in range(n_features):
			feature_values = [row[j] for row in data]
			params[j] = {
				'min': min(feature_values),
				'max': max(feature_values)
			}

	for i in range(len(data)):
		normalized_row = []
		for j in range(n_features):
			min_val = params[j]['min']
			max_val = params[j]['max']

			if max_val - min_val == 0:
				normalized_row.append(0.0)
			else:
				normalized_value = (data[i][j] - min_val) / (max_val - min_val)
				normalized_row.append(normalized_value)

		data_norm.append(normalized_row)

	return data_norm, params

def save_theta(val_set: dict, filename: str = "model/theta.json"):
	with open(filename, 'w') as f:
		json.dump(val_set, f, indent=4)
	print("Bias and weight saved in model/theta.json")

def load_model(filename: str = "model/theta.json"):
	try:
		with open(filename, 'r') as f:
			model = json.load(f)

		# Convertir les clés de norm_params de string en int
		# (JSON convertit automatiquement les clés int en string)
		if "norm_params" in model:
			norm_params = {}
			for key, value in model["norm_params"].items():
				norm_params[int(key)] = value
			model["norm_params"] = norm_params

		return model
	except Exception as e:
		print(f"Error loading model: {e}")
		exit(1)

