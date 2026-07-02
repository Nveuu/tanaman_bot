import streamlit as st
import json
import re
import string
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Page configuration
st.set_page_config(
    page_title="FloraBot - Asisten Tanaman Hias",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NLTK resources setup
@st.cache_resource
def setup_nltk():
    import os
    # Membuat path khusus di folder /tmp yang diizinkan oleh server cloud
    nltk_dir = os.path.join('/tmp', 'nltk_data')
    if not os.path.exists(nltk_dir):
        os.makedirs(nltk_dir)
    
    # Daftarkan path baru ini ke dalam pencarian NLTK
    nltk.data.path.append(nltk_dir)
    
    try:
        # Tambahkan download 'punkt_tab' untuk versi NLTK terbaru
        nltk.download('punkt', download_dir=nltk_dir, quiet=True)
        nltk.download('punkt_tab', download_dir=nltk_dir, quiet=True)
        nltk.download('stopwords', download_dir=nltk_dir, quiet=True)
    except Exception as e:
        st.warning(f"Gagal mengunduh resource NLTK: {e}. Menggunakan fallback tokenizer.")

setup_nltk()

# Cache loading data and model training
@st.cache_resource(show_spinner="Menyiapkan data dan fitting TF-IDF model...")
def load_data_and_train():
    # Load JSON
    with open("tanaman_hias.json", "r", encoding="utf-8") as f:
        intents = json.load(f)
    
    # Initialize NLP tools
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    
    try:
        stop_words = set(stopwords.words('indonesian'))
    except Exception:
        # Fallback list of Indonesian stopwords
        stop_words = set([
            "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia", "dua", "ia",
            "seperti", "jika", "sehingga", "kembali", "dan", "tidak", "ini", "karena", "kepada",
            "oleh", "saat", "harus", "sementara", "setelah", "belum", "kami", "mereka", "sudah",
            "adalah", "baik", "dalam", "serta", "saja", "biasanya", "dengan", "secara", "tentang",
            "banyak", "adapun", "bahwa", "sebagai", "maka", "setiap", "hanya", "bisa", "kamu", "saya", "ada"
        ])

    # Preprocessing function that returns tokens
    def preprocess_tokens(text):
        # Case folding
        text = text.lower()
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Tokenize
        tokens = word_tokenize(text)
        # Stopword removal
        tokens = [w for w in tokens if w not in stop_words]
        # Stemming
        tokens = [stemmer.stem(w) for w in tokens]
        return tokens

    # Flatten patterns
    patterns_data = []
    for item in intents:
        tag = item['tag']
        responses = item['responses']
        for pattern in item['patterns']:
            tokens = preprocess_tokens(pattern)
            clean_pattern = ' '.join(tokens)
            patterns_data.append({
                'original': pattern,
                'clean': clean_pattern,
                'tokens': tokens,
                'tag': tag,
                'responses': responses
            })
            
    # Train TF-IDF
    corpus = [p['clean'] for p in patterns_data]
    vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    X = vectorizer.fit_transform(corpus)
    
    return intents, patterns_data, vectorizer, X, preprocess_tokens, stemmer, stop_words

# Load cache
intents, patterns_data, vectorizer, X, preprocess_tokens, stemmer, stop_words = load_data_and_train()

# Inject Custom CSS
st.markdown("""
<style>
    /* Import Outfit Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Apply globally */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #091710 0%, #030805 100%) !important;
        color: #e2f3e8 !important;
    }
    
    /* Header styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #52e5a4 0%, #a7f3d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        text-shadow: 0 0 30px rgba(82, 229, 164, 0.15);
    }
    
    /* Container styling for NLP Analysis card */
    .analysis-card {
        background: rgba(15, 35, 25, 0.6);
        border: 1px solid rgba(82, 229, 164, 0.2);
        border-radius: 12px;
        padding: 18px;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    .nlp-step-label {
        font-size: 0.8rem;
        color: #8ce8be;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 2px;
    }
    
    .nlp-step-val {
        font-size: 0.95rem;
        background: rgba(5, 15, 10, 0.7);
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid rgba(82, 229, 164, 0.1);
        color: #d1f2de;
        word-break: break-all;
    }
    
    /* Status tags */
    .status-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(82, 229, 164, 0.15);
        color: #52e5a4;
        border: 1px solid rgba(82, 229, 164, 0.3);
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #050e09 !important;
        border-right: 1px solid rgba(82, 229, 164, 0.15) !important;
    }
    
    /* Adjust Streamlit chat messages to match the theme */
    [data-testid="stChatMessage"] {
        background-color: rgba(15, 30, 22, 0.4) !important;
        border: 1px solid rgba(82, 229, 164, 0.1) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        color: #e2f3e8 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #e2f3e8 !important;
    }
    
    /* Reset scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #030805;
    }
    ::-webkit-scrollbar-thumb {
        background: #1b4d36;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #236647;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya FloraBot, asisten virtual Toko Tanaman Hias GreenFlora. Ada yang bisa saya bantu hari ini? Anda bisa menanyakan tentang jenis tanaman hias, harga, cara perawatan, lokasi toko, ongkir, dan lainnya! 🌿"}
    ]

if "nlp_log" not in st.session_state:
    st.session_state.nlp_log = None

# Sidebar Content
with st.sidebar:
    st.markdown("## 🌿 GreenFlora Shop")
    st.image("https://images.unsplash.com/photo-1545241047-6083a3684587?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3", use_container_width=True)
    
    st.markdown("---")
    # Mode selector
    view_mode = st.radio(
        "Tipe Tampilan",
        options=["💬 Chatbot Pelanggan (Clean)", "📊 Analisis NLP & Data Mining (Demo)"],
        index=0
    )
    st.markdown("---")

    if view_mode == "📊 Analisis NLP & Data Mining (Demo)":
        st.markdown("""
        Selamat datang di asisten pintar penjualan tanaman hias kami!
        
        **Fitur Utama NLP & Data Mining:**
        *   **Case Folding & Cleansing**
        *   **Tokenisasi**
        *   **Stopword Removal (Bahasa Indonesia)**
        *   **Stemming Sastrawi**
        *   **TF-IDF Vector Space Model**
        *   **Cosine Similarity Matching**
        
        ---
        **Topik yang Bisa Ditanyakan:**
        *   👋 Menyapa (Halo, Hai)
        *   🪴 Koleksi/Jenis Tanaman Hias
        *   🌻 Cara Perawatan
        *   ⏰ Jam Operasional Toko
        *   📍 Alamat & Lokasi
        *   🪨 Media Tanam
        *   💰 Harga Tanaman
        *   💳 Metode Pembayaran
        *   🚚 Ongkos Kirim (Bogor/Luar Kota)
        *   ⚠️ Garansi & Komplain
        """)
    else:
        st.markdown("""
        ### Asisten Virtual GreenFlora 🌿
        
        Tanyakan apa saja seputar tanaman hias dan layanan toko kami!
        
        **Topik yang Didukung:**
        *   🪴 Koleksi & Jenis Tanaman Hias
        *   🌻 Panduan Perawatan Tanaman
        *   ⏰ Jam Buka & Operasional Toko
        *   📍 Alamat & Lokasi Fisik
        *   🪨 Media Tanam yang Cocok
        *   💰 Daftar Harga & Spesifikasi
        *   💳 Pilihan Metode Pembayaran
        *   🚚 Ongkos Kirim (Bogor/Luar Kota)
        *   ⚠️ Layanan Garansi & Komplain
        
        ---
        💡 *Tips: Coba tanyakan "bagaimana cara merawat monstera?" atau "ongkir ke jakarta berapa?"*
        """)
        
    st.markdown("---")
    if st.sidebar.button("Reset Percakapan", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya FloraBot, asisten virtual Toko Tanaman Hias GreenFlora. Ada yang bisa saya bantu hari ini? Anda bisa menanyakan tentang jenis tanaman hias, harga, cara perawatan, lokasi toko, ongkir, dan lainnya! 🌿"}
        ]
        st.session_state.nlp_log = None
        st.rerun()

# Layout Configuration (Dynamic based on Tipe Tampilan)
if view_mode == "💬 Chatbot Pelanggan (Clean)":
    _, col_chat, _ = st.columns([1, 2.5, 1])
    col_nlp = None
else:
    col_chat, col_nlp = st.columns([1.4, 1.0])

def match_response(user_query):
    # Step-by-step extraction for dashboard demonstration
    step1_folding = user_query.lower()
    
    # Remove numbers
    step2_no_num = re.sub(r'\d+', '', step1_folding)
    
    # Remove punctuation
    step2_cleansing = step2_no_num.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization
    step3_tokens = word_tokenize(step2_cleansing)
    
    # Stopword removal
    step4_no_stop = [w for w in step3_tokens if w not in stop_words]
    
    # Stemming
    step5_stemmed = [stemmer.stem(w) for w in step4_no_stop]
    
    # Final cleaned query string
    clean_query = ' '.join(step5_stemmed)
    
    # Calculate similarity
    query_vector = vectorizer.transform([clean_query])
    similarities = cosine_similarity(query_vector, X)[0]
    
    # Sort matched patterns
    ranked_indices = np.argsort(similarities)[::-1]
    
    top_matches = []
    for idx in ranked_indices[:5]:
        score = similarities[idx]
        if score > 0:
            top_matches.append({
                'pattern': patterns_data[idx]['original'],
                'tag': patterns_data[idx]['tag'],
                'score': score
            })
            
    best_idx = ranked_indices[0]
    best_score = similarities[best_idx]
    
    threshold = 0.15
    if best_score < threshold:
        response = "Maaf, FloraBot belum memahami pertanyaan Anda. Coba gunakan kata kunci lain seperti 'koleksi tanaman', 'cara merawat', 'ongkir', 'alamat toko', atau 'harga tanaman'. 🌱"
        matched_tag = "None (Below Threshold)"
    else:
        matched_item = patterns_data[best_idx]
        matched_tag = matched_item['tag']
        response = random.choice(matched_item['responses'])
        
    # Get active query terms vector weights
    vector_terms = []
    vector_weights = []
    feature_names = vectorizer.get_feature_names_out()
    
    # Convert query vector sparse format to dense and get non-zero terms
    query_dense = query_vector.todense().tolist()[0]
    for idx, weight in enumerate(query_dense):
        if weight > 0:
            vector_terms.append(feature_names[idx])
            vector_weights.append(weight)
            
    # Save step-by-step logs into session state
    st.session_state.nlp_log = {
        'query': user_query,
        'folding': step1_folding,
        'cleansing': step2_cleansing,
        'tokens': step3_tokens,
        'no_stop': step4_no_stop,
        'stemmed': step5_stemmed,
        'clean_query': clean_query,
        'vector_terms': vector_terms,
        'vector_weights': vector_weights,
        'best_match': patterns_data[best_idx]['original'] if best_score >= threshold else "N/A",
        'best_tag': matched_tag,
        'best_score': best_score,
        'top_matches': top_matches
    }
    
    return response

# Main Column: Chat Interface
with col_chat:
    if view_mode == "💬 Chatbot Pelanggan (Clean)":
        st.markdown('<div class="main-title" style="text-align: center; margin-top: 20px;">🌿 FloraBot</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #8ce8be; font-size: 1.1rem; margin-bottom: 20px;">Asisten Pintar GreenFlora Shop</p>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-title">🌿 FloraBot</div>', unsafe_allow_html=True)
        st.caption("Dashboard Chatbot Pintar berbasis Indonesian NLP Klasik & TF-IDF Cosine Similarity")
    
    # Message display container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🌱" if msg["role"] == "assistant" else "👤"):
                st.write(msg["content"])
                
    # Chat Input
    user_input = st.chat_input("Tanyakan tentang Tanaman Hias (contoh: 'gimana cara rawat monstera?')")
    
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Calculate response & fill logs
        response = match_response(user_input)
        
        # Append assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to refresh conversation and updates the NLP panel
        st.rerun()

# Right Column: NLP & Data Mining Log Panel
if view_mode == "📊 Analisis NLP & Data Mining (Demo)":
    with col_nlp:
        st.markdown('<div class="analysis-card" style="margin-top: 15px;">', unsafe_allow_html=True)
        st.markdown("### 📊 NLP Preprocessing & Similarity Engine")
        st.markdown("Bagian ini menampilkan analisis matematika dan tahapan NLP dari pesan terakhir Anda.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        log = st.session_state.nlp_log
        
        if log:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown(f"#### ✉️ Input User: *\"{log['query']}\"*")
            
            # 1. Case Folding
            st.markdown('<div class="nlp-step-label">1. Case Folding & Punctuation Cleansing</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="nlp-step-val">{log["cleansing"] if log["cleansing"] else "(kosong)"}</div>', unsafe_allow_html=True)
            
            # 2. Tokenization
            st.markdown('<div class="nlp-step-label">2. Tokenisasi</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="nlp-step-val">{str(log["tokens"])}</div>', unsafe_allow_html=True)
            
            # 3. Stopword Removal
            st.markdown('<div class="nlp-step-label">3. Stopword Removal</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="nlp-step-val">{str(log["no_stop"])}</div>', unsafe_allow_html=True)
            
            # 4. Stemming (Sastrawi)
            st.markdown('<div class="nlp-step-label">4. Stemming (Bahasa Indonesia)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="nlp-step-val">{str(log["stemmed"])}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**Cleaned Query (String):** `{log['clean_query'] if log['clean_query'] else '(kosong)'}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 5. TF-IDF
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("#### 📐 Pembobotan TF-IDF Vector")
            if log['vector_terms']:
                df_tfidf = pd.DataFrame({
                    'Term': log['vector_terms'],
                    'Bobot (Weight)': log['vector_weights']
                }).sort_values(by='Bobot (Weight)', ascending=False)
                st.dataframe(df_tfidf, use_container_width=True, hide_index=True)
            else:
                st.warning("Tidak ada term input yang cocok dengan kamus data TF-IDF.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 6. Cosine Similarity Matching
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Hasil Matching Cosine Similarity")
            st.markdown(f"**Tag Intent Terpilih:** <span class='status-tag'>{log['best_tag']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Pola Paling Sesuai:** *\"{log['best_match']}\"*")
            st.markdown(f"**Skor Cosine Similarity Tertinggi:** `{log['best_score']:.4f}`")
            
            st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid rgba(82, 229, 164, 0.2);'>", unsafe_allow_html=True)
            st.markdown("**Top 5 Pola dengan Similarity Terbesar (> 0):**")
            
            if log['top_matches']:
                for i, match in enumerate(log['top_matches']):
                    st.markdown(f"**{i+1}. [{match['tag']}]** *\"{match['pattern']}\"*")
                    st.progress(float(match['score']))
                    st.caption(f"Skor Cosine Similarity: `{match['score']:.4f}`")
            else:
                st.info("Tidak ada pola yang memiliki skor kemiripan > 0.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="analysis-card" style="text-align: center; color: #888;">
                <p>Belum ada aktivitas percakapan.</p>
                <p>Silakan kirimkan pertanyaan pada kotak chat untuk melihat kalkulasi data mining dan pemrosesan NLP.</p>
            </div>
            """, unsafe_allow_html=True)
