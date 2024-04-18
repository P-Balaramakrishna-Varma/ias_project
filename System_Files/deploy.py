import os
import sys
from paths import dependency_files_folder_path, deployed_models_folder_path
import json
import zipfile
sys.path.append("..")
print("Hello from deployment")

userID = sys.argv[1]
model = sys.argv[2]

print(f"Making the model {model} ready for deployment for user {userID}")

print("The dependency files in your folder are :\n")
user_dependencies_folder = os.path.join(dependency_files_folder_path, userID)

files = os.listdir(user_dependencies_folder)

for file in files:
    print(file+ " :")
    # Also print the file contents
    with open(os.path.join(user_dependencies_folder, file), "r") as f:
        print(f.read())
    print("--------------------------------------------")

dependency_file = input("Type file name : ")
# Search this file inside the user's folder
dependency_file_path = os.path.join(user_dependencies_folder, dependency_file)

# Read the file contents
with open(dependency_file_path, 'r') as f:
    dependencies = json.load(f)
dependencies = dependencies['requirements']
print(dependencies)

dependency_file_name = userID + "_" + dependency_file.split(".")[0] + ".txt"

with open(dependency_file_name, 'w') as f:
    for req in dependencies.items():
        f.write(req[0]+"==" + req[1]+'\n')
    f.write(model)

print("Done")

user_deployed_models_folder = os.path.join(deployed_models_folder_path, userID)

# Create a folder if it does not exist with the user ID
if not os.path.exists(user_deployed_models_folder):
    os.makedirs(user_deployed_models_folder)

# Check number of files in the user_deployed_models_folder
files = os.listdir(user_deployed_models_folder)
count = len(files)

# Create a folder for the model
dependency_zip_name = userID + "_deployment_" + str(count) + ".zip"
dependency_zip_path = os.path.join(user_deployed_models_folder, dependency_zip_name)

# Create a zip file with the dependencies and the model
with zipfile.ZipFile(dependency_zip_path, 'w') as z:
    z.write(dependency_file_name)

# Move the zip file to the user's folder
os.rename(dependency_zip_path, os.path.join(user_deployed_models_folder, dependency_zip_name))

# Remove the dependency file
os.remove(dependency_file_name)