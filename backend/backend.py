# from flask import Flask, request, jsonify
# import json
#
# app = Flask(__name__)
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     model_name = data['model_name']
#     input_text = data['input_text']
#     prediction = predict_with_model(model_name, input_text)
#     save_prediction_to_db(model_name, input_text, prediction)
#     return jsonify({'prediction': prediction})
#
# @app.route('/results', methods=['GET'])
# def results():
#     results = get_all_predictions()
#     return jsonify(results)
#
# if __name__ == '__main__':
#     app.run(port=8000)
