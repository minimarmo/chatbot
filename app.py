from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer  # นำเข้าฟังก์ชัน get_answer จาก chatbot.py
from chatbot2 import get_answer2

app = Flask(__name__)
CORS(app)  # เปิดการใช้งาน CORS

@app.route('/get_answer_nn', methods=['POST'])
def get_answer_nn():
    user_question = request.json.get('question')
    answer = get_answer(user_question)
    return jsonify({'answer': answer})

@app.route('/get_answer_lra', methods=['POST'])
def get_answer_lra():
   user_question = request.json.get('question')
   answer = get_answer2(user_question)
   return jsonify({'answer': answer})

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=5000)
