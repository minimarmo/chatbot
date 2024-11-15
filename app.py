from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer  # นำเข้าฟังก์ชัน get_answer จาก chatbot.py

app = Flask(__name__)
CORS(app)  # เปิดการใช้งาน CORS

@app.route('/get_answer', methods=['POST'])
def chat():
    # รับคำถามจากผู้ใช้ผ่าน JSON
    user_question = request.json.get('question')

    # ใช้โมเดลที่เราได้สร้างขึ้นเพื่อหาคำตอบ
    answer = get_answer(user_question)

    # ส่งคำตอบกลับไป
    return jsonify({'answer': answer})

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=5000)
