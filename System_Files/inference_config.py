print("Hello from inference config manager")

# Importing the necessary modules
import os
import sys
import json
import shutil
import subprocess
import zipfile
from paths import inference_config_files_folder_path, deployed_models_folder_path, virtual_envs_folder_path
sys.path.append("..")

userID = sys.argv[1]
model_deployed = sys.argv[2]

# List all files on Inference_Configs folder
from paths import inference_config_files_folder_path
files = os.listdir(os.path.join(inference_config_files_folder_path, userID))
print("The inference config files in your folder are :")
for file in files:
    print(file)
    # Also print the file contents
    with open(os.path.join(inference_config_files_folder_path, userID, file), "r") as f:
        print(f.read())

config_file = input("Type the inference config file name : ")

# Search this file inside the user's folder
config_file_path = os.path.join(inference_config_files_folder_path, userID, config_file)
# Read the file contents
with open(config_file_path, 'r') as f:
    config = json.load(f)

configuration = config['inference_configuration'] # The number of instances to run is here

# Search for model in the user's deployed models folder
from paths import deployed_models_folder_path, system_files_folder_path
user_deployed_models_folder = os.path.join(deployed_models_folder_path, userID)
files = os.listdir(user_deployed_models_folder)

# create userID folder inside virtual_envs folder
user_virtual_env_folder_path = os.path.join(virtual_envs_folder_path, userID)
if not os.path.exists(user_virtual_env_folder_path):
    os.makedirs(user_virtual_env_folder_path)

# Coutn number of folders inside the user_virtual_env_folder_path
folders = os.listdir(user_virtual_env_folder_path)
count = len(folders)

num_instances = configuration['instances']
print(f"Creating {num_instances} virtual environments for user {userID}...")
def create_virtualenvs(n):
    for i in range(1, n + 1):
        env_name = f"env_{i}"
        print(f"Creating virtual environment {env_name}...")
        command = ["virtualenv", os.path.join(user_virtual_env_folder_path, env_name)]
        subprocess.run(command)

create_virtualenvs(num_instances)

print(num_instances, " environements created!")

# Copy the model to the virtual environments
for i in range(1, num_instances + 1):
    env_name = f"env_{i}"
    env_path = os.path.join(user_virtual_env_folder_path, env_name)
    shutil.copy(os.path.join(user_deployed_models_folder, model_deployed), env_path)

model_to_run = ""
# For each virtual environment, unzip the zip
for i in range(1, num_instances + 1):
    env_name = f"env_{i}"
    env_path = os.path.join(user_virtual_env_folder_path, env_name)
    model_path = os.path.join(env_path, model_deployed)
    with zipfile.ZipFile(model_path, 'r') as z:
        z.extractall(env_path)
    
    os.remove(model_path)

    # Search for file with .txt extension
    files = os.listdir(env_path)
    for file in files:
        if file.endswith(".txt"):
            dependency_file = file
            break
    
    # Read the file contents
    with open(os.path.join(env_path, dependency_file), 'r') as f:
        dependencies = f.read().split('\n')
        
        # Read last line of the file
        model_to_run = dependencies[-1]
    
    # Delete last line of the file
    dependencies = dependencies[:-1]
    with open(os.path.join(env_path, dependency_file), 'w') as f:
        for dep in dependencies:
            f.write(dep + '\n')

    # print(dependencies, model)

    # Install the dependencies
    print(f"Installing dependencies for virtual environment {env_name}...")
    for dep in dependencies:
        command = [os.path.join(env_path, "Scripts", "pip"), "install", dep]
        subprocess.run(command)

sys.path.append("..")

# Search for model_to_run inside Models folder
from paths import packaged_models_folder_path
# print(packaged_models_folder_path, userID)
files = os.listdir(os.path.join(packaged_models_folder_path,userID))
if model_to_run not in files:
    print(f"Model {model_to_run} not found in the Models folder")
    exit()

print("Working till here")
# Run inference.py inside each virtual environtment
for i in range(1, num_instances + 1):
    env_name = f"env_{i}"
    env_path = os.path.join(user_virtual_env_folder_path, env_name)
    inference_file_path = system_files_folder_path + "/inference.py"
    command = [os.path.join(env_path, "Scripts", "python"), inference_file_path, str(num_instances), str(i), str(userID), str(model_to_run)]
    subprocess.run(command)
