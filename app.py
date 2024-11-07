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
    transcription = '''[0.00s -> 2.82s]  سلام وقت شما به خیر سلیمی هستم بفرموید
[2.82s -> 9.20s]  آهی سلیمی من یه نیم ساعت پیش هم تماس گرفتم با شما به نظرم صحبت کردم
[9.20s -> 11.14s]  من امیرمتی هستم
[11.14s -> 14.90s]  گفتم موجودی من تو نکسوکارت دیده نمیشه
[14.90s -> 20.12s]  گفتید که با پشیبانی ویپا تماس رو گیرم
[20.12s -> 23.70s]  موجودی نقده کارتتون اصلا ربطی به فاراوی نداره آهی امیرمتی
[23.70s -> 26.20s]  خبت به کجا ربط داره
[26.20s -> 28.26s]  شما با کارگزاری فاراوی تماس گرفتید
[28.26s -> 30.04s]  کارگزاری فاراوی آیا بانک هست
[30.04s -> 34.10s]  شما مبلغ نقدی که به کارت نکسو واریز میکنید
[34.10s -> 37.74s]  باید توی موجودی نقد حساب دیژیتالتون باشه
[37.74s -> 41.34s]  این موجودی نقد حساب دیژیتال رو توی ویپا تماس باید چک کنید
[41.34s -> 44.36s]  اگر نمیبین اجازه بدید صحبتم کامل بشه
[44.36s -> 48.72s]  اگر موجودی نقد حساب دیژیتالتون رو مشاهده نمیفرمایید
[48.72s -> 50.44s]  دو مورد داره
[50.44s -> 54.16s]  یا مشکل از بانک پاسارگاده که موجودی نقدتون رو به روز نکرده
[54.16s -> 55.26s]  و خلالی داره
[55.26s -> 60.34s]  یا از مبدع مشکلی داشته که این مبلغ به موجودی نقدتون واریز نشده
[60.34s -> 62.38s]  الان شما با 1561 تماس گرفتید
[62.38s -> 64.36s]  پشتیبانی برگزاری فاراوی
[64.36s -> 68.44s]  ما کارت نکسو و محصول مشترکمون با بانک پاسارگاده
[68.44s -> 70.20s]  امور عملیات بانکی
[70.20s -> 72.38s]  مثل واریز ورچه نقد به کارت
[72.38s -> 75.26s]  طبیعتا از پاسارگاد باید فیگیری بشه
[75.26s -> 78.48s]  شما اگر گردش حسابتونو توی ویپاد میبینید
[78.48s -> 80.50s]  و موجودی نقد کارتتون صفره
[80.50s -> 82.92s]  پس از بانک پاسارگاد باید فیگیری کنید
[82.92s -> 85.44s]  خب عرض کردم من الان بهشون زنگ زدم
[85.44s -> 88.68s]  گفتم من دو تا واریز دارم
[88.68s -> 90.72s]  گردش داره
[90.72s -> 94.48s]  درسته ولی موجودیه منو میزنه صفر
[94.48s -> 99.52s]  اگر توی صندوق یه دونه ده تومن و یه دونه حدودن هشتومن سرمایه گذار کرد
[99.52s -> 100.54s]  اینا منظورتونه
[100.54s -> 101.04s]  7.7
[101.04s -> 102.52s]  7.7
[102.52s -> 104.98s]  بله این دوتا مدنظرتونه
[105.26s -> 105.72s]  بله
[105.72s -> 109.44s]  خب آیا امیر مدهی چرا شما سالتونو درست نمیپرسید
[109.44s -> 112.00s]  من چند بار خدمتون گفتم موجودی نقد
[112.00s -> 115.02s]  شما توی صندوق سرمایه گذاری کردید دوبار
[115.02s -> 119.78s]  موجودی صندوق با موجودی نقد فرق داره
[119.78s -> 124.90s]  طبیعتا در برنامه ویپاد موجودی صندوق قابل مشاهده نیست
[124.90s -> 128.10s]  باید در سایت فارابیزون این موجودی رو ببینید
[128.10s -> 129.58s]  لینکش رو براتون نرسال کردم
[129.58s -> 131.72s]  اصلا راه نمایاره مطالعه نکردید
[131.72s -> 136.62s]  لینکش رو براتون اصلا کردم
[136.62s -> 140.06s]  وارد سایت میشید موجودی صندوقتونو میتونید مشاهده بفرمایید
[140.06s -> 140.72s]  بله مرسی
[141.30s -> 143.24s]  زنده باشید خدا نیهتار شما باشه
[143.24s -> 143.56s]  خدا
[143.56s -> 173.54s]  باشید خدا
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