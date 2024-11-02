import sqlite3
from flask import Flask, render_template, request, jsonify
import os
import time  # To simulate a long-running process
import math

app = Flask(__name__)
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
                        summary TEXT NOT NULL
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

    # Format the size of each file
    # formatted_transcriptions = []
    # for t in transcriptions:
    #     formatted_size = format_file_size(t['size'])  # Format the size in bytes to KB/MB
    #     formatted_transcriptions.append((t['id'], t['request_at'], t['filename'], formatted_size, t['transcription'], t['summary']))

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
    transcription = '''[0.00s -> 3.00s]  سلام وقتتون بخير یقین نو هستم بفهمت
[3.00s -> 4.48s]  salam خسته نباشید
[4.48s -> 7.10s]  ممنونم در خدمتون هستم جناب بفرمایید
[7.10s -> 9.86s]  در رابطه با نیکسوکارت دعا داشتم
[9.86s -> 12.24s]  بفهمید آقای باشدشی در خدمتون هستم
[12.24s -> 18.40s]  نیکسوکارت من الان توش 709 ملیون تومن
[18.40s -> 20.74s]  70 تومن ما پودیخته بودیم داخلش
[20.74s -> 25.60s]  بعد اول هفته الان نشون میده تو با انامال که باز میکنم
[25.60s -> 28.94s]  نشته 76 ملیون تومن نشون میده تو نیکسوکار
[28.94s -> 31.32s]  بعد دیگه قسمت دیگه دوباره نگاه میکنم
[31.32s -> 35.88s]  اینجا نمیشته 709 ملیون رو بزنی
[35.88s -> 39.44s]  چه فرقی دارم با هم چرا اینطوری اختلاف دارم
[39.44s -> 40.46s]  ارز میکنم خدمت
[40.46s -> 43.18s]  اکام متعلق باقای دانیال برشوجی منفر
[43.18s -> 43.96s]  درسته
[43.96s -> 46.46s]  ببینید تعداد واحدتون
[46.46s -> 48.12s]  تیه هر دوتا حالت یکسانه
[48.12s -> 50.96s]  یعنی دارایی شما که واحدتون هستش یکسانه
[50.96s -> 52.02s]  تفاوتش اینه
[52.02s -> 53.46s]  تعداد واحد شما
[53.46s -> 56.28s]  ضب در هزارتومن که پول رایج ملی ما هست
[58.94s -> 61.20s]  نسبت بهش دسترسی لحظهی داشته باشین
[61.20s -> 63.28s]  همین تعداد واحدتون
[63.28s -> 64.98s]  ضب در قیمت فروش روز
[64.98s -> 66.68s]  که داخل منوی صندوق هدیه
[66.68s -> 69.50s]  بالای صفحه نوشته شده قیمت خرید قیمت فروش
[69.50s -> 71.26s]  ضربه اون قیمت فروش
[71.26s -> 73.76s]  میشه دارایی که داخل صندوق هدیه
[73.76s -> 74.54s]  مشاهده میکنید
[74.54s -> 77.82s]  حالا علت تفاوت این دارایی چیه با منوی نکسوکار
[77.82s -> 79.50s]  این که شما اینجا دارایتون
[79.50s -> 81.58s]  با احدثاب سودتون میبینید
[81.58s -> 83.48s]  یعنی اینجا اون فروشی که
[83.48s -> 85.78s]  بالای صفحه هست با قیمت بیشتر از هزار تومن
[85.78s -> 87.12s]  با احدثاب سودتون هست
[87.12s -> 89.00s]  علت تفاوتش ضرفا همین مورد
[89.00s -> 92.82s]  بعد از این هفته به شیش میلی میتونه
[92.82s -> 94.14s]  من میتونم کارت بکشم
[94.14s -> 95.24s]  بردارم فرد کنم
[95.24s -> 97.34s]  دسترسی لحظهی دارید به موجودی
[97.34s -> 98.42s]  که مشاهده میکنید
[98.42s -> 100.92s]  هر جا بخوایید تراکنشتون رو انجام میدین
[100.92s -> 103.64s]  سود و اون مبلغ تراکنشتون
[103.64s -> 105.80s]  هم روز کاری بعد از تراکنش
[105.80s -> 108.66s]  به حساب سجامی پیشورد شما وارید میشن
[108.66s -> 110.92s]  تراکنش یعنی
[110.92s -> 111.16s]  بعد
[111.16s -> 116.64s]  داشت کنم
[116.64s -> 118.24s]  سود داره مگیرد
[118.24s -> 121.12s]  پس داره به ازای روزهایی که
[121.12s -> 122.78s]  داخل صندوق هدیه هست بهش
[122.78s -> 123.76s]  سود تعلق میگیر
[123.76s -> 124.30s]  حالا
[124.30s -> 125.46s]  شما فرض بکنید
[125.46s -> 126.30s]  بخوایید یه ده ملیون
[126.30s -> 128.58s]  تو من جایی تراکنشتون
[128.58s -> 132.32s]  تا قبل از امروز داشتیم
[132.32s -> 134.02s]  سودتون به ازای روز هستش
[134.02s -> 134.76s]  درسته؟
[134.76s -> 135.20s]  درسته
[135.20s -> 136.56s]  قبل اگر شما این ده ملیون تومن
[136.56s -> 138.14s]  امروز تراکنش انجام بدین
[138.16s -> 140.08s]  سود این ده ملیون تومن
[140.08s -> 142.32s]  روز کاریه بعدست تراکنش
[142.32s -> 143.60s]  فرزن امروز انجام بدین
[143.60s -> 145.80s]  سودش رو
[145.80s -> 148.32s]  روز کاری آینده
[148.32s -> 149.78s]  میاد به حساب سجامیتون
[149.78s -> 150.36s]  سودش
[151.12s -> 151.70s]  برداشت
[151.70s -> 151.96s]  بگهیش
[151.96s -> 153.22s]  وقتی تاینید ده ملیون تومن
[153.22s -> 154.18s]  برداشت میکنید
[154.18s -> 156.30s]  با احتساب سودتون برداشت میخنید
[156.30s -> 165.30s]  تراکنشتون با اصل دارایتون انجام میشه سودی که به اون ده ملیون تومنتان بمیاد به حسای بانکتون
[165.30s -> 167.30s]  متوجه نشده
[167.30s -> 171.30s]  یعنی اما به این مدید
[171.30s -> 174.30s]  اصاب خودم ورگی دارم ده ملیون تومنتان کم
[174.30s -> 176.30s]  ده ملیون تومنتان کم
[176.30s -> 183.30s]  مثلا ده تومنتان هست هست بابا ورداشتم درده تومنت بوده مثلا پنگ ملیون وردارم میشه هفتاد و یه ملیون تومنت
[183.30s -> 184.30s]  درسته؟
[184.30s -> 190.30s]  ببینید شما دو تا روش موجود داره برای برداشت از حسابتون یا از موجودی خنداتون
[190.30s -> 198.30s]  روش اول اینه که با کارت نکسو تراکنش انجام بده
[198.30s -> 200.30s]  درسته قهه هدیه فروش بزنید
[200.30s -> 202.30s]  ما الان با همدیگه صحبت کردیم
[202.30s -> 207.30s]  روال برای این شد که شما موجودی نکسوتون با قیمت هزار تومن باشه
[207.30s -> 210.30s]  درسته؟
[210.30s -> 211.30s]  درسته؟
[211.30s -> 213.30s]  درسته؟
[213.30s -> 215.30s]  درسته؟
[215.30s -> 217.30s]  درسته؟
[217.30s -> 219.30s]  درسته؟
[219.30s -> 221.30s]  درسته؟
[221.30s -> 223.30s]  درسته؟
[223.30s -> 225.30s]  درسته؟
[225.30s -> 227.30s]  درسته؟
[227.30s -> 229.30s]  درسته؟
[229.30s -> 231.30s]  درسته؟
[231.30s -> 233.30s]  درسته؟
[233.30s -> 236.54s]  ولی این تفاوت هزار تومن بیشتر
[236.54s -> 240.32s]  ما اون رو که سودتون هست فردای اون روز براتون واریز میکنیم
[240.32s -> 242.40s]  روز کاری برد میاد به حساب سجامیت
[242.40s -> 246.64s]  حالا اگه من مثلای 10 تومن رو برمیدارم
[246.64s -> 250.82s]  از سود دفاع قبلی من کم میشه؟
[250.82s -> 251.44s]  کم نمیشه
[251.44s -> 253.92s]  اون مبلغی که برداشت کردی با احتساب سودتون
[253.92s -> 256.48s]  هر مبلغی داخل صندوق دیگه بمونه
[256.48s -> 259.66s]  به ازای روزهایی که باشه به شما سود تعلق میگیره
[259.66s -> 261.58s]  اگه بخوایید دوباره برداشت بکنید
[261.58s -> 263.08s]  با احتساب سودتون هست
[263.08s -> 267.82s]  اگرم نه پایان دوره ما که میشه روز کاریه بعد از 15 هم
[267.82s -> 270.90s]  یا میاد براتون واریز میشه به حساب سجامیتون
[270.90s -> 273.34s]  یا اگر سود مرکب و فعال بکنید
[273.34s -> 275.56s]  دوباره داخل صندوق براتون سرمه گذاریم
[275.56s -> 277.72s]  یعنی به ازای سودتون واحد خریداریم
[277.72s -> 278.08s]  شروع
[278.08s -> 280.56s]  الان سود مرکب و فعال کردیم
[280.56s -> 282.88s]  الان ما دست دومن برداریم
[282.88s -> 285.14s]  اون دود مرکب از میمیره
[285.14s -> 285.66s]  دوباره
[285.66s -> 287.18s]  یا اون ثابت هستش
[287.18s -> 289.56s]  اون برای دارایی که داخل صندوق باقیمونه
[289.56s -> 291.22s]  هر میزان که باشه کار میکنه
[291.22s -> 293.24s]  ولی اگر بخوایید برداشتی انجام بدید
[293.24s -> 295.02s]  با احتساب سودتون هم
[295.02s -> 296.50s]  متوجه شدم
[296.50s -> 298.22s]  بازه
[298.22s -> 298.88s]  زن مکنم
[299.42s -> 301.88s]  خیش میکنم مارضه دیگه هست من در اخیل مایتون باشه
[301.88s -> 303.88s]  بازه
[303.88s -> 304.94s]  فعالی داشتم
[304.94s -> 306.32s]  من یه دونه کارت
[306.32s -> 306.80s]  الموز
[306.80s -> 307.18s]  میخواستم
[307.18s -> 308.04s]  کارت هم
[308.04s -> 309.38s]  عبست کنم
[309.38s -> 310.84s]  میخواستم اینو
[310.84s -> 312.10s]  بری یکی سریز گسا
[312.10s -> 313.44s]  الموز
[313.44s -> 313.96s]  گفته
[313.96s -> 314.76s]  من هرچی گشتم
[314.76s -> 315.44s]  پیدا نکردم
[315.44s -> 316.14s]  کجا باید دارم
[316.14s -> 316.56s]  الموز
[316.56s -> 317.44s]  سننا بزنم
[317.44s -> 318.88s]  پنل فارابیزون
[318.88s -> 320.24s]  منای نکسوکار
[320.24s -> 321.40s]  تنظیمات
[321.40s -> 322.32s]  نوشته شده
[322.32s -> 322.78s]  درخواست
[322.78s -> 323.26s]  الموز
[323.26s -> 323.46s]  سننا
[323.46s -> 324.26s]  از اونجا میتونن
[324.26s -> 325.02s]  درخواست بزن
[325.02s -> 326.40s]  پنل نکسوکار
[326.40s -> 327.26s]  برم بعد کجا
[327.26s -> 328.82s]  پنل فارابیزون
[328.82s -> 330.00s]  منای نکسوکار
[330.00s -> 331.36s]  تنظیمات
[331.36s -> 331.90s]  درخواست
[331.90s -> 332.70s]  سدور الموز
[332.70s -> 333.24s]  سننا
[333.24s -> 333.88s]  خب باش
[333.88s -> 335.14s]  سفاست شما
[335.14s -> 335.68s]  خیلی
[335.68s -> 336.72s]  میکرم سهنده باشید
[336.72s -> 337.32s]  روز خوش
[337.32s -> 338.24s]  من از درس انجیمان
[338.24s -> 338.84s]  تصدیل میشید
[338.84s -> 339.68s]  خدا نگه دارید
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