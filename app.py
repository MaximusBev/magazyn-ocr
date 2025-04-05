from flask import Flask, request, render_template, redirect, flash, url_for
import os
import json
from datetime import datetime
import cv2
import pytesseract
import shutil

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
DATA_FILE = 'data.json'
LOG_FILE = 'ocr_log.txt'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

custom_config = r'--oem 1 --psm 4 -l pol'

def preprocess_image_cv(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Nie udało się załadować obrazu: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.medianBlur(gray, 3)
    return gray

def extract_text(image_path):
    preprocessed = preprocess_image_cv(image_path)
    return pytesseract.image_to_string(preprocessed, config=custom_config)

def save_ocr_data(image_path, text, firm_name):
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():
                data = json.loads(content)

    data.append({
        'image': image_path,
        'text': text,
        'firm': firm_name,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_ocr_result(filename, text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"[{timestamp}] {filename}\n{text}\n{'-'*60}\n")

def generate_unique_filename(folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(folder, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return unique_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    firms = []
    if os.path.exists(UPLOAD_FOLDER):
        firms = [d for d in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, d))]

    if request.method == 'POST':
        firm_name = request.form.get('firm')
        new_firm_name = request.form.get('new_firm')

        if firm_name == '__new__' and new_firm_name:
            firm_name = new_firm_name.strip()

        files = request.files.getlist('image')

        for file in files:
            if file and firm_name:
                firm_folder = os.path.join(UPLOAD_FOLDER, firm_name)
                os.makedirs(firm_folder, exist_ok=True)

                filename = generate_unique_filename(firm_folder, file.filename)
                save_path = os.path.join(firm_folder, filename)
                file.save(save_path)

                text = extract_text(save_path)
                relative_path = os.path.relpath(save_path, 'static').replace("\\", "/")

                save_ocr_data(relative_path, text, firm_name)
                log_ocr_result(relative_path, text)

        flash(f"Pliki zostały zapisane w folderze: {firm_name}", "success")
        return redirect(url_for('index'))

    return render_template('index.html', firms=firms)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    results = []

    if query and os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                if query in entry['text'].lower():
                    results.append(entry)

    return render_template('search.html', results=results if query else None)

@app.route('/zamowienia')
def manage_folders():
    firms = []
    base_path = os.path.join('static', 'uploads')
    if os.path.exists(base_path):
        firms = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return render_template('manage.html', firms=firms)

@app.route('/zamowienia/<firm_name>')
def view_firm(firm_name):
    folder_path = os.path.join(UPLOAD_FOLDER, firm_name)
    if not os.path.exists(folder_path):
        flash("Folder nie istnieje.", "error")
        return redirect(url_for('manage_folders'))

    files = os.listdir(folder_path)
    images = [os.path.join('uploads', firm_name, f).replace("\\", "/") for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('view_firm.html', firm=firm_name, images=images)

@app.route('/delete', methods=['POST'])
def delete():
    image_to_delete = request.form.get('image')
    if not image_to_delete:
        flash("Nieprawidłowe żądanie usunięcia.", "error")
        return redirect(url_for('manage_folders'))

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = [d for d in data if d['image'] != image_to_delete]
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    full_path = os.path.join('static', image_to_delete)
    if os.path.exists(full_path):
        os.remove(full_path)

    flash("Zamówienie zostało usunięte.", "success")
    return redirect(url_for('manage_folders'))

@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form.get('folder')
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

        # Видалення даних з data.json
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = [d for d in data if d['firm'] != folder_name]
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        flash(f"Folder {folder_name} został usunięty.", "success")
    else:
        flash("Nie znaleziono folderu do usunięcia.", "error")

    return redirect(url_for('manage_folders'))

@app.route('/delete_all_images/<firm_name>', methods=['POST'])
def delete_all_images(firm_name):
    folder_path = os.path.join(UPLOAD_FOLDER, firm_name)
    if not os.path.exists(folder_path):
        flash("Folder nie istnieje.", "error")
        return redirect(url_for('manage_folders'))

    # Remove images
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            os.remove(file_path)

    # Update data.json
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = [d for d in data if d['firm'] != firm_name or not d['image'].lower().endswith(('.png', '.jpg', '.jpeg'))]
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    flash(f"Wszystkie zdjęcia w folderze {firm_name} zostały usunięte.", "success")
    return redirect(url_for('view_firm', firm_name=firm_name))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
