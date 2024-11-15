import json
from pythainlp.tokenize import word_tokenize as word_tokenize_thai
from nltk.tokenize import word_tokenize as word_tokenize_en
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import nltk

# ดาวน์โหลด resources ที่จำเป็นจาก NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

with open('qa_data_th.json', 'r', encoding='utf-8') as file:
    data_th = json.load(file)
with open('qa_data_en.json', 'r', encoding='utf-8') as file:
    data_en = json.load(file)

questions_th = [item['question'] for item in data_th]
answers_th = [item['answer'] for item in data_th]

questions_en = [item['question'] for item in data_en]
answers_en = [item['answer'] for item in data_en]

questions = questions_th + questions_en
answers = answers_th + answers_en

# ฟังก์ชันแยกคำที่รองรับทั้งภาษาไทยและภาษาอังกฤษ
def tokenize(text):
    if any("\u0e00" <= char <= "\u0e7f" for char in text):  # ตรวจสอบว่าเป็นภาษาไทยหรือไม่
        return " ".join(word_tokenize_thai(text))  # ใช้ pythainlp สำหรับภาษาไทย
    else:
        return " ".join(word_tokenize_en(text))  # ใช้ NLTK สำหรับภาษาอังกฤษ

# แยกคำในคำถามทุกข้อ
tokenized_questions = [tokenize(question) for question in questions]

# สร้าง TfidfVectorizer
vectorizer = TfidfVectorizer()

# แปลงคำถามที่แยกคำแล้วเป็นเวกเตอร์
X = vectorizer.fit_transform(tokenized_questions)

# สร้างโมเดล KNN
model = NearestNeighbors(n_neighbors=1, metric='cosine')

# ฝึกโมเดลด้วยข้อมูลคำถาม
model.fit(X)

# ฟังก์ชันสำหรับค้นหาคำตอบ
def get_answer(user_question):
    # แปลงคำถามของผู้ใช้เป็นคำที่แยกคำแล้ว
    user_question_tokenized = tokenize(user_question)
    
    # แปลงคำถามที่แยกคำแล้วเป็นเวกเตอร์
    user_question_vector = vectorizer.transform([user_question_tokenized])

    # ใช้โมเดล KNN เพื่อหาคำถามที่ใกล้เคียงที่สุด
    distances, indices = model.kneighbors(user_question_vector)

    # ตรวจสอบระยะห่าง (distance) หากสูงเกินไป (หมายถึงคำถามไม่ตรงกัน)
    if distances[0][0] > 0.5:  # ค่านี้สามารถปรับได้
        return "ขออภัย ไม่มีคำตอบสำหรับคำถามนี้ กรุณาติดต่อแอดมิน"
    else:
        # ส่งคำตอบที่ตรงกับคำถามที่ใกล้เคียงที่สุด
        return answers[indices[0][0]]

# ทดสอบ Chatbot
if __name__ == "__main__":
    user_input = "What is the return policy?"  # คำถามภาษาอังกฤษ
    print(get_answer(user_input))  # Output: Our return policy allows returns within 30 days of purchase.

    user_input = "วิธีรีเซ็ตรหัสผ่านคืออะไร?"  # คำถามภาษาไทย
    print(get_answer(user_input))  # Output: คุณสามารถรีเซ็ตรหัสผ่านได้โดยคลิกที่ 'ลืมรหัสผ่าน' บนหน้าเข้าสู่ระบบ

    # ทดสอบคำถามที่ไม่ตรงกับคำถามในฐานข้อมูล
    user_input = "วิธีการตั้งค่าบัญชีใหม่คืออะไร?"
    print(get_answer(user_input))  # Output: ข้อความ "ขออภัย โปรดติดต่อแอดมิน"
