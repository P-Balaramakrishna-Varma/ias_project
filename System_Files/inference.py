print("Hello World!")
import sys

import tensorflow as tf

from flask import Flask, request, jsonify
import sys
import os
import threading

from paths import packaged_models_folder_path
init_port = 1000

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    #Sample code to test if Flask app is working or not


    input = request.json['input']
    print("INput received : ", input)
    output = "The input message received was :" + str(input)
    # files = os.listdir(os.path.join(packaged_models_folder_path,userID))
    # # Load model from packaaged_models folder
    # if model_to_run in files:
    #     model = tf.keras.models.load_model(os.path.join(packaged_models_folder_path,userID,model_to_run))
    # output = model.predict(input)

    return jsonify(output)


total_instances = int(sys.argv[1])
instance_number = int(sys.argv[2])
userID = sys.argv[3]
model_to_run = sys.argv[4]
print(total_instances, instance_number)
def run_app(instance_number):
    app.run(debug=True, port=init_port+instance_number, use_reloader=False)


if __name__ == '__main__':
    # app.run(debug=True, port=5000+int(sys.argv[1]))

    threads = []
    for i in range(total_instances):
        # print(init_port+i)
        t = threading.Thread(target=run_app, args=(init_port+i,))
        t.start()
        print("Running on port ", init_port+i)
        threads.append(t)

    for t in threads:
        t.join()