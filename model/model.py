# Step 0: Import libraries and Dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle

warnings.filterwarnings('ignore')

# Load the dataset
dataset = pd.read_csv('winequality-red.csv')

# Step 3: Data Preprocessing
dataset_X = dataset.iloc[:, :-1].values
dataset_Y = np.where(dataset['quality'] >= 6, 1, 0)

# Scale the features
scaler = MinMaxScaler(feature_range=(0, 1))
dataset_scaled = scaler.fit_transform(dataset_X)

# Convert the numpy array to dataframe
dataset_scaled = pd.DataFrame(dataset_scaled)

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    dataset_scaled, dataset_Y, test_size=0.20, random_state=42, stratify=dataset_Y)

# Step 4: Data Modelling
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)

# Evaluate the model on test set
score = rfc.score(X_test, y_test)
print("Accuracy:", score)

# Save the model
pickle.dump(rfc, open('model.sav', 'wb'))

# Load the model
model = pickle.load(open('model.sav', 'rb'))

# Test the model on new data
# input_data = np.array([[7.3, 0.65, 0.0, 1.2, 0.065, 15.0, 21.0, 0.9946, 5.40, 0.47, 12.0]])
input_data = np.array([[8.5, 0.28, 0.56, 1.8, 0.092, 35.0, 103.0, 0.9969, 3.30, 0.75, 11.0]])
input_data_scaled = scaler.transform(input_data)
prediction = model.predict(input_data_scaled)
if prediction[0] == 0:
    print('Good quality wine')
else:
    print('Bad quality wine')
