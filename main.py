import os
from flask import Flask, render_template, request
from datetime import datetime
from groq import Groq

# Kunci API Groq
AI_KEY_ENV = "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"

# Inisialisasi Client Groq dengan API Key yang benar
Client_AI = Groq(api_key=AI_KEY_ENV)

app = Flask(__name__)        
# Fungsi untuk memanggil AI Groq
def AI_Call(year):
    try:
        #call model AI 
        chat_completion = Client_AI.chat.completions.create(
            messages=[
                {
                    "role": "user", #sudut pandang sebagai user 
                    "content": f"Berikan  1 fakta seputar teknologi pada tahun {year}", #Prompt
                }
            ],
            model="llama-3.2-1b-preview",
            stream=False
        )
        ai_response = chat_completion.choices[0].message.content
        return ai_response
    except Exception:
        return "This feature cann't use for now"

# Route utama
@app.route('/')
def main():
    return render_template('index.html')

# Route mengecek usia
@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir
        ai_output = AI_Call(tahun_lahir)
      
        
        #parsing output di template element
        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output)
    return render_template('cek_usia.html', usia=None)

# RUN FLASK
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1000)
