# Importing the necessary modules
import sys
import subprocess
import os
from paths import models_folder_path, packaged_models_folder_path

sys.path.append(models_folder_path)

print("Hello from packaging")
# Processing the command line arguments
userID = sys.argv[1]
model = sys.argv[2]

user_folder_path = os.path.join(models_folder_path, userID)
sys.path.append(user_folder_path)

# Importing the tensorflow model
from model import model

print("Here is the model summary :\n")
print(model.summary())

# Create a folder if it does not exist with the user ID
user_folder = os.path.join(packaged_models_folder_path, userID)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

# Count number of files in the user folder
files = os.listdir(user_folder)
count = len(files)

# Save the model in the user folder
print(userID, model, count)
saved_model_name = userID + "_model_" + str(count) + ".keras"
model.save(os.path.join(user_folder, saved_model_name))
print("Model saved successfully!")