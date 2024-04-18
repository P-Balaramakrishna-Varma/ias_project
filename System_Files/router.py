# Importing the necessary modules
import subprocess
import os
from paths import python_interpreter_path, packaging_script_path, deployment_script_path, configuration_script_path, models_folder_path, packaged_models_folder_path, deployed_models_folder_path
import sys

sys.path.append("..")
# The welcome & Login screen
print("Welcome! Kindly login with your details")

userID = input("Enter your user ID: ")

# The command line display
command_line_display = "1. I want to package my model\n2. I want to make my model ready for deployment\n3. I want to configure my model's instances\n4. Exit"

command_line_options = {
    1: "I want to package my model",
    2: "I want to make my model ready for deployment",
    3: "I want to configure my model's instances",
    4: "Exit"
}

# The command line options based on user behaviour
option_selected = int(input(command_line_display + "\nPlease select an option : "))
if option_selected == 4:
    print("Goodbye!")
else:
    if option_selected in command_line_options:
        print(f"Selected option: {command_line_options[option_selected]}")
    # If option selected is 1, then the user wants to package the model
    if option_selected==1:
        
        # Get the model file name from the user store inside the Models folder
        model = input("Type your model file name (The model must be present inside the Models folder): ")
        
        #check if the model file exists inside the Models folder
        user_folder_path = os.path.join(models_folder_path, userID)
        file_path = os.path.join(user_folder_path, model)
        if not os.path.exists(file_path):
            print(f"Model file {model} not found in the Models folder")
            exit()
        
        # Run the packaging script
        command = [python_interpreter_path, packaging_script_path, userID, model]
        subprocess.run(command)

    # If option selected is 2, then the user wants to deploy the model
    elif option_selected==2:

        # List names of all the models in the user's folder
        user_folder = os.path.join(packaged_models_folder_path, userID)
        files = os.listdir(user_folder)
        
        print("The models in your folder are :")
        
        for file in files:
            print(file)
        
        print("Select the model you want to deploy")
        model = input("Type the model file name: ")

        command = [python_interpreter_path, deployment_script_path, userID, model]
        subprocess.run(command)

    # If option selected is 3, then the user wants to configure the model's instances
    elif option_selected==3:

        user_folder = os.path.join(deployed_models_folder_path, userID)
        files = os.listdir(user_folder)

        print("The models ready for deployment in your folder are :")
        for file in files:
            print(file)
        
        model = input("Type the model file name: ")

        command = [python_interpreter_path, configuration_script_path, userID, model]
        subprocess.run(command)

