import sqlite3
from flask import Flask, render_template, request, jsonify #, send_file, make_response
from flask_cors import CORS
import os
import time  # To simulate a long-running process
import math

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize the SQLite database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS transcriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        filename TEXT NOT NULL,
                        size INTEGER NOT NULL,
                        transcription TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        revision_count INTEGER DEFAULT 0
                    )''')
    conn.commit()
    conn.close()

# Get db connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Format file size in Bytes, KB, MB ...
def format_file_size(size_in_bytes):
    if size_in_bytes == 0:
        return '0 Bytes'
    k = 1024
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = int(math.floor(math.log(size_in_bytes, k)))
    p = math.pow(k, i)
    s = round(size_in_bytes / p, 2)
    return f"{s} {sizes[i]}"

# Route for the main page
@app.route('/')
def index():
    # Retrieve history from the database
    conn = get_db_connection()
    transcriptions = conn.execute('SELECT * FROM transcriptions').fetchall()
    conn.close()

    formatted_transcriptions = [
        {
            "id": t["id"],
            "request_at": t["request_at"],
            "filename": t["filename"],
            "size": format_file_size(t["size"]),
            "transcription": t["transcription"],
            "summary": t["summary"],
        }
        for t in transcriptions
    ]

    return render_template('index.html', transcriptions=formatted_transcriptions)



# Route for autosaving
@app.route('/autosave', methods=['POST'])
def autosave():
    data = request.get_json()
    
    content = data.get('content')
    id = data.get('id')
    
    if not content or not id:
        return jsonify({"error": "Invald data!"}), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""UPDATE transcriptions SET transcription = ?, revision_count = revision_count + 1 WHERE id = ? """, (content, id))
    conn.commit()

    return jsonify({"message": "Content saved successfully"}), 200


# @app.route('/audio/<filename>')
# def stream_audio(filename):
#     file_path = f'./uploads/{filename}'
#     # return send_file(path, mimetype='audio/mpeg', as_attachment=False)
#     response = make_response(send_file(file_path))
#     response.headers['Content-Type'] = 'audio/mpeg'  # یا نوع صوتی مناسب برای فایل شما
#     response.headers['Content-Disposition'] = 'inline'  # تنظیم برای پخش مستقیم
#     return response


# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)

    # Get the file size in bytes
    file_size = os.path.getsize(file_path)

    # Simulate transcription (you will replace this with actual processing)
    transcription = '''[0.00s -> 3.16s]  سلام وقتتون به خیر حیباللهی هستم بفرمایید
[3.16s -> 5.22s]  بنابی الله خوب استی
[5.22s -> 6.72s]  ممنونم تندات
[6.72s -> 10.70s]  داداش من سه هفته پیش خوب تو
[10.70s -> 15.78s]  بارابی حساب باست کرده بودم اهراز هویت هم کرده بودم
[15.78s -> 20.52s]  الان من می خواهم بدونم کارتم کجاست اصلا
[20.52s -> 22.12s]  نمی دونم
[22.12s -> 28.92s]  به قول معروف اگه شما دست رسی از اونجا دارید محمد اندر خور و آفر هستم
[28.92s -> 32.92s]  درخواست کارت فیزیکی شما ثبت گردید؟
[33.52s -> 37.08s]  چون من الان نمی بینم درخواست ثبت گرده باشید به صورت
[37.08s -> 39.72s]  آخه اینجا تو منو هم هیچی نمی آله
[39.72s -> 42.32s]  برمان
[42.32s -> 47.92s]  توی صفحه فارابیزون که وارد می شید بخش کارت نکسو رو می بینید؟
[49.04s -> 49.70s]  می زن
[49.70s -> 53.22s]  کارت نکسو
[53.22s -> 55.70s]  شما دست رسی داری اینجا
[55.70s -> 60.94s]  من دست رسی دارم شما فقط وارد سایت شدید چیزی که می بینم
[60.94s -> 64.70s]  صفحه نکسو کارت رو دیدید ولی کاری انجام ندادید اونجا
[65.70s -> 68.42s]  الان من وارد برنامه که می شم خوب
[68.42s -> 69.70s]  کدوم برنامه؟
[70.72s -> 72.70s]  همین برنامه فارابی خوب
[72.70s -> 76.30s]  نه این اسم برنامه رو بگید
[76.30s -> 79.04s]  سایت اگر وارد می شید اسم سایت رو بگید
[79.04s -> 82.20s]  اگر برنامه اپلیکیشن فارابی کسو رو می گید که
[82.20s -> 85.04s]  خب اون ارتباطی به کارت نداره
[85.04s -> 91.04s]  شما باید بگید توی سایت فارابی زون در بخش کارت نکسو درخواست بدید
[91.04s -> 95.42s]  لینک فارابی زون رو به شماره سف نوصد و چهارده
[95.42s -> 97.04s]  آخر سف سی سد ارتباطی به کارت نداره
[97.04s -> 99.04s]  برنامه بگید که هم توی این سایت برید
[99.04s -> 101.04s]  مرسی سلامت باشیم
[101.04s -> 103.04s]  خواهش میکنم
[103.04s -> 105.04s]  عمر دیگه ای داشته باشید دخل من
[105.04s -> 107.04s]  مرسی سلامت باشید
[107.04s -> 109.04s]  روزتون به خیلی به نظرسنجی بست میشید خواده نگیست
[109.04s -> 111.04s]  خدا
'''
    # transcription = f"Transcription for {audio_file.filename}:" + '''
    # [0.00s -> 3.00s] Lorem Ipsum is simply dummy text of the printing and typesettin
    # '''
    summary = f"Summary for {audio_file.filename}"

    # Simulate transcription (replace with actual transcription code)
    time.sleep(2)  # Simulate a time-consuming task (e.g., audio processing)

    # Save transcription and file name to SQLite database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO transcriptions (filename, size, transcription, summary) VALUES (?, ?, ?, ?)', (audio_file.filename, file_size, transcription, summary))
    conn.commit()

    # Get the ID of the inserted record
    last_id = c.lastrowid
    
    # Retrieve the record with the given id
    c.execute('SELECT * FROM transcriptions WHERE id = ?', (last_id,))
    record = c.fetchone()  # Fetch the first result

    conn.close()

    return jsonify({
        'id': last_id,
        'request_at': record[1],
        'filename': audio_file.filename,
        'size': file_size,
        'transcription': transcription,
        'summary': summary
    }), 200

# Initialize the database before running the app
if __name__ == '__main__':
    init_db()
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)