import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# โหลดข้อมูลคำถามและคำตอบ
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

# แปลงคำถามเป็นเวกเตอร์ด้วย TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# สร้างโมเดล Logistic Regression
model = LogisticRegression()
model.fit(X, answers)

# ทดสอบโมเดล
def get_answer2(question):
    question_vector = vectorizer.transform([question])
    return model.predict(question_vector)[0]

# ตัวอย่างการทดสอบ
print(get_answer2("วิธีรีเซ็ตรหัสผ่านคืออะไร"))
