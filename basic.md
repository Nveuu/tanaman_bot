Berikut **contoh dashboard chatbot sederhana menggunakan Streamlit**, **ditulis dengan Python** dan **cocok dijalankan dari Jupyter Notebook** (menggunakan streamlit run).

Saya buat **versi paling sederhana dan mudah dipahami**, cocok untuk:

- chatbot biasa (rule-based / placeholder AI)
- bahan demo
- pondasi untuk dikembangkan ke LLM (OpenAI, Ollama, dll)

**1️⃣ Persiapan Environment**

Jalankan di **cell pertama notebook**:

!pip install streamlit

⚠️ Streamlit **tidak berjalan langsung inline** di notebook, tapi **file .py-nya dibuat dari notebook lalu dijalankan**.

**2️⃣ Buat File chatbot_app.py dari Notebook**

Jalankan **cell berikut** untuk membuat file Streamlit:

%%writefile chatbot_app.py  
import streamlit as st  
\# ---------------------------  
\# **Konfigurasi halaman**  
\# ---------------------------  
st.set_page_config(  
page_title="Chatbot Sederhana",  
page_icon="🤖",  
layout="centered"  
)  
st.title("🤖 Chatbot Sederhana")  
st.caption("Dashboard chatbot sederhana menggunakan Streamlit")  
\# ---------------------------  
\# **Inisialisasi session state  
**\# ---------------------------  
if "messages" not in st.session_state:  
st.session_state.messages = \[\]  
\# ---------------------------  
\# **Fungsi respon chatbot**  
\# ---------------------------  
def chatbot_response(user_input):  
user_input = user_input.lower()  
if "halo" in user_input or "hai" in user_input:  
return "Halo! 👋 Ada yang bisa saya bantu?"  
elif "nama" in user_input:  
return "Saya adalah chatbot sederhana berbasis Streamlit 🤖"  
elif "terima kasih" in user_input:  
return "Sama-sama 😊"  
else:  
return "Maaf, saya belum mengerti pertanyaan Anda."  
\# ---------------------------  
\# **Tampilkan riwayat chat  
**\# ---------------------------  
for msg in st.session_state.messages:  
with st.chat_message(msg\["role"\]):  
st.write(msg\["content"\])  
\# ---------------------------  
\# **Input pengguna  
**\# ---------------------------  
user_input = st.chat_input("Ketik pesan Anda...")  
if user_input:  
\# Simpan pesan user  
st.session_state.messages.append(  
{"role": "user", "content": user_input}  
)  
with st.chat_message("user"):  
st.write(user_input)  
\# Respon chatbot  
response = chatbot_response(user_input)  
st.session_state.messages.append(  
{"role": "assistant", "content": response}  
)  
with st.chat_message("assistant"):  
st.write(response)

**3️⃣ Jalankan Streamlit dari Notebook**

Di **cell berikutnya**, jalankan:

!streamlit run chatbot_app.py

📌 Browser akan terbuka otomatis ke:

<http://localhost:8501>

**4️⃣ Tampilan Dashboard (Fitur)**

✔ Chat bubble (user & bot)  
✔ Session chat (tidak hilang saat kirim pesan)  
✔ Dashboard clean & modern  
✔ Mudah dikembangkan ke AI/LLM

**5️⃣ Struktur Sederhana (Ringkasan)**

chatbot_app.py  
│  
├── Header & konfigurasi  
├── Session state (chat history)  
├── Fungsi respon chatbot  
├── Tampilan chat  
└── Input user

**6️⃣ Upgrade yang Bisa Saya Tambahkan (Opsional)**

**Kalau Anda mau, saya bisa lanjutkan ke:**

- 🔌 Integrasi **OpenAI / Ollama / Gemini**
- 🧠 Chatbot berbasis **knowledge base (PDF / TXT)**
- 🏥 Chatbot RS / Akademik / Audit TI (sesuai background Anda)
- 📊 Sidebar dashboard (statistik chat)
- 💾 Simpan chat ke database / CSV
- 🎨 UI lebih profesional

👉 Tinggal bilang:  
**"lanjutkan ke versi AI"** atau **"tambahkan fitur X"**

![](data:image/x-wmf;base64,183GmgAAAAAAAB4AGgB4AAAAAABtVwEACQAAA/oBAAABAJ8BAAAAAAQAAAADAQgABQAAAAsCAAAAAAUAAAAMAhoAHgADAAAAHgAHAAAA/AIAAP///wAAAAQAAAAtAQAACQAAAB0GIQDwABoAHgAAAAAABAAAAC0BAAAJAAAAHQYhAPAAGgAMAAAAEgAFAAAACwIAAAAABQAAAAwCGgAeAAUAAAABAv///wAFAAAALgEAAAAABQAAAAIBAQAAAJ8BAABACSAAzAAAAAAAEAAQAAUAAQAoAAAAEAAAABAAAAABABgAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAAA////////////////////////////////////////////////////////////////oKCg4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlp////////////////////////////////////////////////4+Pj////oKCgaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlp4+Pj////oKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCg////BAAAACcB//8DAAAAAAA=)

apakah anda bisa membuat chatbotnya lebih advance tidak hanya menjawab halo atau hi, jadi chatbotnya sudah menggunakan model sederhana saja. saya tidak menggunakan laptop yang terlalu cangiih

Bisa 👍 dan **sangat bisa dibuat advance tapi tetap ringan**, tanpa laptop canggih.

Pendekatan terbaik untuk kondisi Anda adalah **chatbot berbasis Machine Learning klasik (NLP sederhana)**, **BUKAN LLM**.  
Model ini:

✅ Tidak butuh GPU  
✅ Tidak butuh internet  
✅ Cepat  
✅ Cocok untuk laptop spesifikasi rendah  
✅ Sudah "berpikir" (klasifikasi intent), bukan sekadar if-else

**🎯 Konsep Chatbot yang Akan Kita Buat**

**Arsitektur ringan & realistis:**

User Input  
↓  
TF-IDF Vectorizer  
↓  
Model ML (Multinomial Naive Bayes)  
↓  
Prediksi Intent  
↓  
Response Template

Model ini **belajar dari data**, bukan hardcode "halo → halo".

**🧠 Teknologi yang Digunakan**

| **Komponen** | **Alasan**                 |
| ------------ | -------------------------- |
| Python       | ringan                     |
| scikit-learn | cepat & stabil             |
| TF-IDF       | NLP klasik, sangat efisien |
| Naive Bayes  | model super ringan         |
| Streamlit    | UI sederhana               |

**1️⃣ Install Library (Notebook Cell)**

!pip install streamlit scikit-learn pandas

**2️⃣ Dataset Sederhana (Intent-based)**

Ini **bisa Anda kembangkan sendiri** nanti (tinggal tambah baris).

import pandas as pd  
data = {  
"text": \[  
"halo", "hai", "selamat pagi", "selamat siang",  
"siapa kamu", "kamu siapa", "nama kamu siapa",  
"apa fungsi kamu", "kamu bisa apa",  
"terima kasih", "makasih banyak",  
"selamat tinggal", "dadah", "bye"  
\],  
"intent": \[  
"greeting", "greeting", "greeting", "greeting",  
"identity", "identity", "identity",  
"function", "function",  
"thanks", "thanks",  
"goodbye", "goodbye", "goodbye"  
\]  
}  
df = pd.DataFrame(data)  
df

**3️⃣ Training Model ML Ringan**

from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.naive_bayes import MultinomialNB  
\# Vectorizer  
vectorizer = TfidfVectorizer()  
X = vectorizer.fit_transform(df\["text"\])  
\# Model  
model = MultinomialNB()  
model.fit(X, df\["intent"\])

**4️⃣ Fungsi Respon Chatbot (SMART)**

responses = {  
"greeting": "Halo! 👋 Ada yang bisa saya bantu?",  
"identity": "Saya chatbot sederhana berbasis Machine Learning 🤖",  
"function": "Saya bisa menjawab pertanyaan dasar secara otomatis.",  
"thanks": "Sama-sama 😊",  
"goodbye": "Sampai jumpa 👋"  
}  
def chatbot_response(text):  
vec = vectorizer.transform(\[text\])  
intent = model.predict(vec)\[0\]  
return responses.get(intent, "Maaf, saya belum paham.")

**5️⃣ Buat Dashboard Streamlit (Advance tapi Ringan)**

%%writefile chatbot_app.py  
import streamlit as st  
import pickle  
st.set_page_config(page_title="Chatbot ML Ringan", page_icon="🤖")  
st.title("🤖 Chatbot Machine Learning Sederhana")  
st.caption("Ringan • Offline • Tanpa GPU")  
\# Load model  
with open("model.pkl", "rb") as f:  
model, vectorizer, responses = pickle.load(f)  
if "messages" not in st.session_state:  
st.session_state.messages = \[\]  
def chatbot_response(text):  
vec = vectorizer.transform(\[text\])  
intent = model.predict(vec)\[0\]  
return responses.get(intent, "Maaf, saya belum paham.")  
for msg in st.session_state.messages:  
with st.chat_message(msg\["role"\]):  
st.write(msg\["content"\])  
user_input = st.chat_input("Ketik pesan...")  
if user_input:  
st.session_state.messages.append({"role": "user", "content": user_input})  
with st.chat_message("user"):  
st.write(user_input)  
response = chatbot_response(user_input)  
st.session_state.messages.append({"role": "assistant", "content": response})  
with st.chat_message("assistant"):  
st.write(response)

**6️⃣ Simpan Model (Sekali Saja)**

import pickle  
with open("model.pkl", "wb") as f:  
pickle.dump((model, vectorizer, responses), f)

**7️⃣ Jalankan Chatbot**

!streamlit run chatbot_app.py

**🧪 Contoh Percakapan**

**User:**

"selamat siang bot"

**Bot:**

"Halo! 👋 Ada yang bisa saya bantu?"

**User:**

"kamu bisa apa saja?"

**Bot:**

"Saya bisa menjawab pertanyaan dasar secara otomatis."

➡️ Ini **bukan if-else**, tapi **hasil klasifikasi ML**.

**🚀 Kenapa Ini Cocok untuk Anda?**

Sebagai:

- 🎓 Mahasiswa magister informatika
- 🧠 Belajar ML
- 💻 Laptop tidak terlalu canggih

Model ini:

- Cocok untuk **skripsi / tesis awal**
- Bisa dikaitkan ke **chatbot RS / audit TI**
- Bisa diklaim sebagai **AI klasik (bukan rule-based)**

**🔥 Mau Naik Level Lagi?**

Saya bisa bantu:

- 📄 Chatbot berbasis **dokumen (PDF/Word)**
- 🏥 Chatbot **RS / Akademik**
- 🧠 Tambah **confidence score**
- 📊 Dashboard analitik
- 🔄 Online training (update data tanpa retrain)

👉 Tinggal bilang:  
**"lanjut ke chatbot berbasis dokumen"** atau **"tingkatkan kecerdasannya"**

# 🤖 Chatbot Berbasis Dokumen (PDF/TXT)

Model ini dapat:

- membaca dokumen
- mencari informasi paling relevan
- menjawab berdasarkan isi dokumen
- berjalan offline
- tanpa GPU
- tanpa LLM besar

Pendekatan ini disebut:

Retrieval-Based Chatbot menggunakan TF-IDF + Cosine Similarity

Arsitekturnya:

**Dokumen  
↓  
Preprocessing  
↓  
TF-IDF Vectorization  
↓  
Cosine Similarity  
↓  
Ambil kalimat paling relevan  
↓  
Jawaban chatbot**

Ini jauh lebih pintar dibanding intent chatbot biasa.

# 🎯 Cocok Untuk

Anda bisa gunakan untuk:

- chatbot akademik
- chatbot kampus
- chatbot SOP
- chatbot audit COBIT 2019
- chatbot DMBOK
- chatbot rumah sakit
- chatbot dokumen kebijakan

# 1️⃣ Install Library

Jalankan di notebook:

!pip install streamlit scikit-learn nltk PyPDF2

# 2️⃣ Siapkan Dokumen

Buat file teks sederhana:

## dokumen.txt

Contoh isi:

COBIT 2019 adalah framework tata kelola teknologi informasi.  
Framework ini digunakan untuk meningkatkan governance dan management TI.  
DMBOK adalah framework untuk tata kelola data organisasi.  
Machine learning merupakan cabang kecerdasan buatan yang memungkinkan sistem belajar dari data.

Anda nanti bisa mengganti dengan:

- PDF tesis
- SOP kampus
- Buku
- Modul kuliah
- Dokumen audit

# 3️⃣ Training Knowledge Base

Jalankan di notebook:

import nltk  
nltk.download('punkt')

## Load dan Pecah Dokumen

from nltk.tokenize import sent_tokenize  
with open("dokumen.txt", "r", encoding="utf-8") as f:  
text = f.read()  
sentences = sent_tokenize(text)  
print(sentences)

# 4️⃣ TF-IDF dan Similarity Engine

from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.metrics.pairwise import cosine_similarity  
vectorizer = TfidfVectorizer()  
X = vectorizer.fit_transform(sentences)

# 5️⃣ Fungsi Chatbot Pintar

def chatbot_response(user_input):  
user_vector = vectorizer.transform(\[user_input\])  
similarity = cosine_similarity(user_vector, X)  
index = similarity.argmax()  
score = similarity\[0\]\[index\]  
if score < 0.1:  
return "Maaf, informasi tidak ditemukan dalam dokumen."  
return sentences\[index\]

# 6️⃣ Testing di Notebook

while True:  
user = input("Anda : ")  
if user.lower() == "keluar":  
break  
response = chatbot_response(user)  
print("Bot :", response)

# 🧪 Contoh Hasil

## Input

Apa itu COBIT 2019?

## Output

COBIT 2019 adalah framework tata kelola teknologi informasi.

# 🚀 Sekarang Kita Buat Dashboard Streamlit

# 7️⃣ Streamlit Chatbot Dokumen

## Buat file chatbot_doc.py

Di notebook:

%%writefile chatbot_doc.py  
import streamlit as st  
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.metrics.pairwise import cosine_similarity  
from nltk.tokenize import sent_tokenize  
import nltk  
nltk.download('punkt')  
\# =========================  
\# Load dokumen  
\# =========================  
with open("dokumen.txt", "r", encoding="utf-8") as f:  
text = f.read()  
sentences = sent_tokenize(text)  
\# =========================  
\# TF-IDF  
\# =========================  
vectorizer = TfidfVectorizer()  
X = vectorizer.fit_transform(sentences)  
\# =========================  
\# Fungsi chatbot  
\# =========================  
def chatbot_response(user_input):  
user_vector = vectorizer.transform(\[user_input\])  
similarity = cosine_similarity(user_vector, X)  
index = similarity.argmax()  
score = similarity\[0\]\[index\]  
if score < 0.1:  
return "Maaf, informasi tidak ditemukan dalam dokumen."  
return sentences\[index\]  
\# =========================  
\# UI Streamlit  
\# =========================  
st.set_page_config(  
page_title="Chatbot Dokumen",  
page_icon="🤖"  
)  
st.title("🤖 Chatbot Berbasis Dokumen")  
st.caption("TF-IDF + Cosine Similarity")  
if "messages" not in st.session_state:  
st.session_state.messages = \[\]  
\# tampilkan history  
for msg in st.session_state.messages:  
with st.chat_message(msg\["role"\]):  
st.write(msg\["content"\])  
\# input user  
user_input = st.chat_input("Tanyakan sesuatu...")  
if user_input:  
st.session_state.messages.append(  
{"role":"user","content":user_input}  
)  
with st.chat_message("user"):  
st.write(user_input)  
response = chatbot_response(user_input)  
st.session_state.messages.append(  
{"role":"assistant","content":response}  
)  
with st.chat_message("assistant"):  
st.write(response)

# 8️⃣ Jalankan Dashboard

!streamlit run chatbot_doc.py

# 🔥 Ini Sudah AI Sungguhan?

✅ YA.

Karena:

- menggunakan NLP
- menggunakan vector space model
- similarity computation
- retrieval intelligence
- knowledge base

Walaupun:

- bukan deep learning
- bukan GPT
- bukan transformer

Tetapi ini:  
✅ ringan  
✅ realistis  
✅ cocok penelitian  
✅ cocok laptop biasa

# 🎓 Sangat Cocok untuk Topik Tesis

Contoh judul:

### 📌 Akademik

"Implementasi Chatbot Akademik Menggunakan TF-IDF dan Cosine Similarity"

### 📌 Audit TI

"Chatbot Tata Kelola TI Berbasis COBIT 2019 Menggunakan NLP"

### 📌 Rumah Sakit

"Knowledge-Based Chatbot untuk Layanan Informasi Rumah Sakit"

# 🚀 Upgrade Berikutnya yang Bisa Kita Buat

## Level 2

- upload PDF langsung
- multi dokumen
- preprocessing Bahasa Indonesia
- stemming Sastrawi
- confidence score

## Level 3

- semantic search
- sentence transformer ringan
- mini local LLM

## Level 4

- RAG sederhana
- chatbot PDF cerdas seperti ChatGPT

Kalau mau, berikutnya saya bisa bantu membuat:

- 📄 Chatbot langsung membaca PDF
- 🇮🇩 NLP Bahasa Indonesia lebih akurat
- 🧠 Semantic chatbot lebih pintar
- 💾 Simpan histori chat
- 📊 Dashboard profesional
- 🏥 Chatbot khusus COBIT / DMBOK / RS

Tinggal pilih salah satu.

Bagus. Untuk Bahasa Indonesia, kualitas chatbot bisa meningkat cukup signifikan jika kita menambahkan pipeline NLP yang benar.

Karena Anda menggunakan laptop yang tidak terlalu kuat, solusi terbaik adalah:

**🎯 NLP Bahasa Indonesia Ringan tetapi Akurat**

Kita akan menambahkan:

| **Teknik NLP**    | **Fungsi**                    |
| ----------------- | ----------------------------- |
| Case Folding      | huruf kecil semua             |
| Tokenizing        | memecah kata                  |
| Stopword Removal  | menghapus kata tidak penting  |
| Stemming Sastrawi | mengubah kata ke bentuk dasar |
| TF-IDF            | representasi numerik          |
| Cosine Similarity | pencarian jawaban             |

**🚀 Hasilnya Akan Lebih Pintar**

Contoh:

**User bertanya:**

Bagaimana tata kelola teknologi informasi?

Meski dokumen berisi:

Tata kelola TI digunakan untuk meningkatkan governance organisasi.

Bot tetap bisa memahami konteks.

**📦 Install Library**

Jalankan di notebook:

!pip install streamlit scikit-learn nltk Sastrawi PyPDF2

**🧠 Arsitektur NLP Indonesia**

**Input User**  
↓  
**Preprocessing Bahasa Indonesia  
↓  
Stemming Sastrawi  
↓  
TF-IDF  
↓  
Cosine Similarity  
↓  
Jawaban paling relevan**

**1️⃣ Download NLTK Resource**

import nltk  
nltk.download('punkt')  
nltk.download('stopwords')

**2️⃣ Import Library NLP Indonesia**

import re  
import string  
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

**3️⃣ Inisialisasi Stemmer dan Stopword**

factory = StemmerFactory()  
stemmer = factory.create_stemmer()  
stop_words = set(stopwords.words('indonesian'))

**4️⃣ Fungsi Preprocessing Indonesia**

Ini bagian paling penting.

def preprocessing(text):  
\# lowercase  
text = text.lower()  
\# hapus angka  
text = re.sub(r'\\d+', '', text)  
\# hapus tanda baca  
text = text.translate(str.maketrans('', '', string.punctuation))  
\# tokenisasi  
tokens = word_tokenize(text)  
\# hapus stopword  
tokens = \[word for word in tokens if word not in stop_words\]  
\# stemming  
tokens = \[stemmer.stem(word) for word in tokens\]  
\# gabung kembali  
text = ' '.join(tokens)  
return text

**5️⃣ Load Dokumen**

**Contoh dokumen.txt**

COBIT 2019 adalah framework tata kelola teknologi informasi.  
Framework ini digunakan untuk meningkatkan governance dan manajemen TI organisasi.  
Machine learning adalah cabang kecerdasan buatan yang memungkinkan sistem belajar dari data.  
DMBOK digunakan untuk tata kelola data perusahaan.

**6️⃣ Pecah Kalimat**

from nltk.tokenize import sent_tokenize  
with open("dokumen.txt", "r", encoding="utf-8") as f:  
text = f.read()  
sentences = sent_tokenize(text)

**7️⃣ Preprocessing Semua Kalimat**

clean_sentences = \[preprocessing(sentence) for sentence in sentences\]

**8️⃣ TF-IDF yang Lebih Akurat**

from sklearn.feature_extraction.text import TfidfVectorizer  
vectorizer = TfidfVectorizer()  
X = vectorizer.fit_transform(clean_sentences)

**9️⃣ Fungsi Chatbot Pintar Bahasa Indonesia**

from sklearn.metrics.pairwise import cosine_similarity  
def chatbot_response(user_input):  
clean_input = preprocessing(user_input)  
user_vector = vectorizer.transform(\[clean_input\])  
similarity = cosine_similarity(user_vector, X)  
index = similarity.argmax()  
score = similarity\[0\]\[index\]  
if score < 0.15:  
return "Maaf, informasi tidak ditemukan."  
return sentences\[index\]

**🔟 Testing di Notebook**

while True:  
user = input("Anda : ")  
if user.lower() == "keluar":  
break  
response = chatbot_response(user)  
print("Bot :", response)

**🧪 Contoh Hasil NLP Indonesia**

**User:**

Apa fungsi tata kelola TI?

**Bot:**

Framework ini digunakan untuk meningkatkan governance dan manajemen TI organisasi.

**🚀 Sekarang Buat Streamlit yang Lebih Profesional**

**chatbot_nlp.py**

%%writefile chatbot_nlp.py  
import streamlit as st  
import re  
import string  
import nltk  
from nltk.tokenize import word_tokenize  
from nltk.tokenize import sent_tokenize  
from nltk.corpus import stopwords  
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.metrics.pairwise import cosine_similarity  
\# =========================  
\# **Download resource**  
\# =========================  
nltk.download('punkt')  
nltk.download('stopwords')  
\# =========================  
\# **Stemmer Indonesia**  
\# =========================  
factory = StemmerFactory()  
stemmer = factory.create_stemmer()  
stop_words = set(stopwords.words('indonesian'))  
\# =========================  
\# **Preprocessing  
**\# =========================  
def preprocessing(text):  
text = text.lower()  
text = re.sub(r'\\d+', '', text)  
text = text.translate(  
str.maketrans('', '', string.punctuation)  
)  
tokens = word_tokenize(text)  
tokens = \[  
word for word in tokens  
if word not in stop_words  
\]  
tokens = \[  
stemmer.stem(word)  
for word in tokens  
\]  
return ' '.join(tokens)  
\# =========================  
**\# Load dokumen**  
\# =========================  
with open("dokumen.txt", "r", encoding="utf-8") as f:  
text = f.read()  
sentences = sent_tokenize(text)  
clean_sentences = \[  
preprocessing(sentence)  
for sentence in sentences  
\]  
\# =========================  
\# **TF-IDF**  
\# =========================  
vectorizer = TfidfVectorizer()  
X = vectorizer.fit_transform(clean_sentences)  
\# =========================  
\# **Chatbot response  
**\# =========================  
def chatbot_response(user_input):  
clean_input = preprocessing(user_input)  
user_vector = vectorizer.transform(\[clean_input\])  
similarity = cosine_similarity(user_vector, X)  
index = similarity.argmax()  
score = similarity\[0\]\[index\]  
if score < 0.15:  
return "Maaf, jawaban tidak ditemukan dalam dokumen."  
return sentences\[index\]  
\# =========================  
\# **Streamlit UI**  
\# =========================  
st.set_page_config(  
page_title="Chatbot NLP Indonesia",  
page_icon="🤖"  
)  
st.title("🤖 Chatbot NLP Bahasa Indonesia")  
st.caption("TF-IDF + Sastrawi + Cosine Similarity")  
if "messages" not in st.session_state:  
st.session_state.messages = \[\]  
for msg in st.session_state.messages:  
with st.chat_message(msg\["role"\]):  
st.write(msg\["content"\])  
user_input = st.chat_input(  
"Tanyakan sesuatu..."  
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
