from flask import Flask, request, render_template_string, url_for, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-me' 

# --- KONFIGURASI ---
UPLOAD_DIR = "uploads"
BASELINE_FILE = "baseline.json"
USERS_FILE = "users.json"
HASH_ALGOS = ["md5", "sha1", "sha256"]

# --- SETUP DIREKTORI ---
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- FUNGSI HELPER UNTUK PENGGUNA ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- FUNGSI HELPER UNTUK FILE INTEGRITY ---
def calc_hash(path, algo="sha256", block_size=65536):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()

def load_baseline():
    # Fungsi ini sekarang akan memuat dictionary, bukan list
    if not os.path.exists(BASELINE_FILE):
        return {} # Return dictionary kosong
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Pastikan data adalah dictionary untuk kompatibilitas
            if isinstance(data, dict):
                return data
            else:
                return {} # Jika format lama (list), anggap kosong
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# --- TEMPLATE HTML (Tidak ada perubahan pada template, jadi saya persingkat) ---
LOGIN_TEMPLATE = """...""" # Tidak berubah
REGISTER_TEMPLATE = """...""" # Tidak berubah
DASHBOARD_TEMPLATE = """...""" # Tidak berubah
MAIN_TEMPLATE = """...""" # Tidak berubah

# --- (Salin semua template dari kode sebelumnya, tidak ada yang perlu diubah di sana) ---
# --- For brevity, I'm omitting the template strings as they are unchanged. ---
# --- Please use the template strings from the previous response. ---
# Template untuk Halaman Login
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-200 min-h-screen flex items-center justify-center font-sans">
  <div class="bg-gray-800 shadow-lg rounded-2xl p-8 w-full max-w-md border border-gray-700">
    <h1 class="text-2xl font-bold text-center text-indigo-400 mb-6">Login to File Checker</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="mb-4 px-4 py-2 rounded text-center {% if category == 'error' %} bg-red-900 text-red-300 {% else %} bg-green-900 text-green-300 {% endif %}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form method="post" class="space-y-4">
      <div>
        <label for="username" class="block mb-2 text-sm font-medium text-gray-400">Username</label>
        <input type="text" name="username" id="username" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500" required>
      </div>
      <div>
        <label for="password" class="block mb-2 text-sm font-medium text-gray-400">Password</label>
        <input type="password" name="password" id="password" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500" required>
      </div>
      <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition">Login</button>
    </form>
    <p class="text-center text-sm text-gray-500 mt-6">Don't have an account? <a href="{{ url_for('register') }}" class="text-indigo-400 hover:underline">Register here</a></p>
  </div>
</body>
</html>
"""
# Template untuk Halaman Register
REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Register</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-200 min-h-screen flex items-center justify-center font-sans">
  <div class="bg-gray-800 shadow-lg rounded-2xl p-8 w-full max-w-md border border-gray-700">
    <h1 class="text-2xl font-bold text-center text-indigo-400 mb-6">Create an Account</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="mb-4 px-4 py-2 rounded text-center {% if category == 'error' %} bg-red-900 text-red-300 {% else %} bg-green-900 text-green-300 {% endif %}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form method="post" class="space-y-4">
      <div>
        <label for="username" class="block mb-2 text-sm font-medium text-gray-400">Username</label>
        <input type="text" name="username" id="username" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500" required>
      </div>
      <div>
        <label for="password" class="block mb-2 text-sm font-medium text-gray-400">Password</label>
        <input type="password" name="password" id="password" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500" required>
      </div>
      <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition">Register</button>
    </form>
    <p class="text-center text-sm text-gray-500 mt-6">Already have an account? <a href="{{ url_for('login') }}" class="text-indigo-400 hover:underline">Login here</a></p>
  </div>
</body>
</html>
"""
# Template untuk Halaman Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Dashboard - File Baseline</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-200 min-h-screen flex flex-col font-sans">
  <header class="bg-gray-800 shadow">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold" style="color:#6366f1;">File Integrity Checker</h1>
      <nav class="flex items-center space-x-6">
        <a href="{{ url_for('index') }}" class="text-gray-300 hover:text-indigo-400 transition">Checker</a>
        <a href="{{ url_for('dashboard') }}" class="text-indigo-400 font-semibold">Dashboard</a>
        <span class="text-gray-500">|</span>
        <span class="text-gray-400">Welcome, <strong>{{ session['username'] }}</strong></span>
        <a href="{{ url_for('logout') }}" class="bg-red-600 px-3 py-1 rounded text-white hover:bg-red-700 transition text-sm">Logout</a>
      </nav>
    </div>
  </header>
  <main class="flex-1 container mx-auto px-6 py-8">
    <div class="bg-gray-800 shadow-lg rounded-2xl p-8 w-full border border-gray-700">
        <h2 class="text-2xl font-semibold mb-6 text-center text-gray-200">My Generated File Baselines</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-sm text-left text-gray-400">
                <thead class="text-xs text-gray-300 uppercase bg-gray-700">
                    <tr>
                        <th scope="col" class="px-6 py-3">#</th>
                        <th scope="col" class="px-6 py-3">Filename</th>
                        <th scope="col" class="px-6 py-3">Date Generated</th>
                        <th scope="col" class="px-6 py-3">Hashes (md5, sha1, sha256)</th>
                    </tr>
                </thead>
                <tbody>
                {% for item in baseline_data %}
                    <tr class="bg-gray-800 border-b border-gray-700 hover:bg-gray-700">
                        <td class="px-6 py-4 font-medium">{{ loop.index }}</td>
                        <td class="px-6 py-4 font-medium text-white">{{ item.filename }}</td>
                        <td class="px-6 py-4">{{ item.timestamp }}</td>
                        <td class="px-6 py-4 font-mono text-xs">
                            <div class="flex flex-col space-y-1">
                                <span><strong class="text-sky-400">MD5:</strong> {{ item.hashes.md5 or 'N/A' }}</span>
                                <span><strong class="text-amber-400">SHA1:</strong> {{ item.hashes.sha1 or 'N/A' }}</span>
                                <span><strong class="text-emerald-400">SHA256:</strong> {{ item.hashes.sha256 or 'N/A' }}</span>
                            </div>
                        </td>
                    </tr>
                {% else %}
                    <tr>
                        <td colspan="4" class="text-center py-8 text-gray-500">
                            You have not generated any baselines. Generate one on the Checker page.
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
  </main>
  <footer class="bg-gray-800 border-t border-gray-700 mt-8">
    <div class="max-w-7xl mx-auto px-6 py-4 text-center text-gray-500 text-sm">
      © {{year}} File Integrity Checker — Ray Egans
    </div>
  </footer>
</body>
</html>
"""
# Template utama
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>File Integrity Checker</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = { theme: { extend: { colors: { primary: { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' } } } } }
  </script>
</head>
<body class="bg-gray-900 text-gray-200 min-h-screen flex flex-col font-sans">
  <header class="bg-gray-800 shadow">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-primary-500">File Integrity Checker</h1>
      <nav class="flex items-center space-x-6">
        <a href="{{ url_for('index') }}" class="text-indigo-400 font-semibold">Checker</a>
        <a href="{{ url_for('dashboard') }}" class="text-gray-300 hover:text-indigo-400 transition">Dashboard</a>
        <span class="text-gray-500">|</span>
        <span class="text-gray-400">Welcome, <strong>{{ session['username'] }}</strong></span>
        <a href="{{ url_for('logout') }}" class="bg-red-600 px-3 py-1 rounded text-white hover:bg-red-700 transition text-sm">Logout</a>
      </nav>
    </div>
  </header>
  <main class="flex-1 flex items-center justify-center px-6">
    <div class="bg-gray-800 shadow-lg rounded-2xl p-8 w-full max-w-xl border border-gray-700">
      {% if not result %}
        <h2 class="text-xl font-semibold mb-6 text-center">Upload File to Check</h2>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="mb-4 px-4 py-2 rounded text-center {% if category == 'error' %} bg-red-900 text-red-300 {% else %} bg-green-900 text-green-300 {% endif %}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <div id="js-error-container" class="mb-4"></div>
        <form method="post" enctype="multipart/form-data" class="space-y-4" id="uploadForm">
          <div id="drop-zone" class="border-2 border-dashed border-primary-500 rounded-xl p-6 text-center text-gray-400 cursor-pointer hover:bg-gray-700 transition">
            <p id="drop-text">Drag & drop a file here or click to select</p>
            <input type="file" name="file" id="fileInput" class="hidden" accept=".pdf,.doc,.docx,.txt,.jpg,.png,.jpeg" />
          </div>
          <div id="preview" class="mt-4 flex flex-col items-center space-y-2"></div>
          <div class="flex space-x-4">
            <button name="action" value="verify" class="flex-1 bg-primary-600 text-white py-2 px-4 rounded-lg shadow hover:bg-primary-700 transition">Verify File</button>
            <button name="action" value="generate" class="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg shadow hover:bg-green-700 transition">Generate Baseline</button>
          </div>
        </form>
      {% else %}
        <h2 class="text-xl font-semibold mb-4 text-center">Result</h2>
        <div class="mb-4 text-center">
          <p class="text-gray-300"><strong>File:</strong> {{fname}}</p>
          <p class="mt-2 text-lg font-bold {% if status == 'ORIGINAL' %} text-green-400 {% elif status == 'MODIFIED' %} text-red-400 {% elif status == 'BASELINE GENERATED' %} text-blue-400 {% else %} text-yellow-400 {% endif %}">Status: {{status}}</p>
        </div>
        <div class="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-700">
          <h3 class="font-semibold mb-2">Hash Values:</h3>
          <ul class="text-sm space-y-1">
          {% for algo, h in hashes.items() %}
            <li><span class="font-mono text-primary-500">{{algo}}:</span> <code class="text-gray-400">{{h}}</code></li>
          {% endfor %}
          </ul>
        </div>
        <div class="flex justify-center">
          <a href="{{url_for('index')}}" class="px-6 py-2 rounded-lg bg-primary-600 text-white shadow hover:bg-primary-700 transition">Back</a>
        </div>
      {% endif %}
    </div>
  </main>
  <footer class="bg-gray-800 border-t border-gray-700">
    <div class="max-w-7xl mx-auto px-6 py-4 text-center text-gray-500 text-sm">
      © {{year}} File Integrity Checker — Ray Egans
    </div>
  </footer>
  <script>
    const uploadForm=document.getElementById("uploadForm"),dropZone=document.getElementById("drop-zone"),fileInput=document.getElementById("fileInput"),preview=document.getElementById("preview"),dropText=document.getElementById("drop-text"),jsErrorContainer=document.getElementById("js-error-container");function clearJsError(){jsErrorContainer.innerHTML=""}uploadForm.addEventListener("submit",function(e){0===fileInput.files.length&&(e.preventDefault(),jsErrorContainer.innerHTML=`<div class="bg-red-900 text-red-300 px-4 py-2 rounded text-center">Please select a file before submitting.</div>`)}),dropZone.addEventListener("click",()=>fileInput.click()),dropZone.addEventListener("dragover",e=>{e.preventDefault(),dropZone.classList.add("bg-gray-700")}),dropZone.addEventListener("dragleave",()=>{dropZone.classList.remove("bg-gray-700")}),dropZone.addEventListener("drop",e=>{e.preventDefault(),clearJsError(),dropZone.classList.remove("bg-gray-700");const t=e.dataTransfer.files[0];fileInput.files=e.dataTransfer.files,showPreview(t)}),fileInput.addEventListener("change",()=>{clearJsError();const e=fileInput.files[0];e&&showPreview(e)});function showPreview(e){preview.innerHTML="",e?(dropText.innerText="Selected file: "+e.name,e.type.startsWith("image/")?(reader=new FileReader,reader.onload=e=>{const t=document.createElement("img");t.src=e.target.result,t.className="w-24 h-24 object-cover rounded-lg shadow",preview.appendChild(t),addRemoveButton()},reader.readAsDataURL(e)):(icon=document.createElement("img"),icon.src=e.name.endsWith(".pdf")?"https://cdn-icons-png.flaticon.com/512/337/337946.png":e.name.endsWith(".doc")||e.name.endsWith(".docx")?"https://cdn-icons-png.flaticon.com/512/281/281760.png":e.name.endsWith(".txt")?"https://cdn-icons-png.flaticon.com/512/3022/3022255.png":"https://cdn-icons-png.flaticon.com/512/833/833524.png",icon.className="w-16",preview.appendChild(icon),addRemoveButton())):dropText.innerText="Drag & drop a file here or click to select"}function addRemoveButton(){const e=document.createElement("button");e.innerText="❌ Remove File",e.type="button",e.className="mt-2 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition text-sm",e.onclick=()=>{fileInput.value="",preview.innerHTML="",dropText.innerText="Drag & drop a file here or click to select",clearJsError()},preview.appendChild(e)}
  </script>
</body>
</html>
"""

# --- RUTE (ROUTES) APLIKASI ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if username in users:
            flash("Username already exists.", "error")
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        save_users(users)
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
    return render_template_string(REGISTER_TEMPLATE)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if username not in users or not check_password_hash(users[username], password):
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
        session['username'] = username
        return redirect(url_for('index'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_user = session['username']
    all_baselines = load_baseline()
    
    # Ambil baseline HANYA untuk pengguna yang sedang login
    user_baseline = all_baselines.get(current_user, [])
    
    processed_baseline = []
    for entry in user_baseline:
        timestamp_str = entry.get('timestamp') 
        formatted_timestamp = "Unknown"
        if timestamp_str:
            try:
                timestamp_obj = datetime.datetime.fromisoformat(timestamp_str)
                formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                formatted_timestamp = timestamp_str
        processed_baseline.append({
            'filename': os.path.basename(entry.get('path', 'Unknown File')),
            'timestamp': formatted_timestamp,
            'hashes': { 'md5': entry.get('md5'), 'sha1': entry.get('sha1'), 'sha256': entry.get('sha256') }
        })
    
    processed_baseline.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template_string(
        DASHBOARD_TEMPLATE,
        baseline_data=processed_baseline,
        year=datetime.datetime.now().year
    )

@app.route("/", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_user = session['username']

    if request.method == "POST":
        action = request.form.get("action")
        file = request.files.get("file")
        
        if not file or file.filename == '':
            flash("You must select a file before submitting.", "error")
            return redirect(url_for('index'))

        fname = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_DIR, fname)
        file.save(save_path)

        hashes = {algo: calc_hash(save_path, algo) for algo in HASH_ALGOS}

        all_baselines = load_baseline()
        user_baseline = all_baselines.get(current_user, [])

        if action == "generate":
            new_entry = {
                "path": os.path.abspath(save_path),
                **hashes,
                "timestamp": datetime.datetime.now().isoformat()
            }
            # Hapus entri lama dari baseline pengguna ini saja
            user_baseline = [e for e in user_baseline if os.path.basename(e.get("path", "")) != fname]
            user_baseline.append(new_entry)
            
            # Update data untuk pengguna ini di dictionary utama
            all_baselines[current_user] = user_baseline

            # Simpan seluruh data kembali ke file
            with open(BASELINE_FILE, "w", encoding="utf-8") as f:
                json.dump(all_baselines, f, indent=2)

            status = "BASELINE GENERATED"
        else: # action == 'verify'
            # Cari file HANYA di baseline milik pengguna ini
            matched_entry = next((e for e in user_baseline if os.path.basename(e.get("path", "")) == fname), None)
            if matched_entry:
                status = "ORIGINAL" if all(hashes[a] == matched_entry.get(a) for a in HASH_ALGOS) else "MODIFIED"
            else:
                status = "NOT IN BASELINE FOR THIS USER"

        return render_template_string(
            MAIN_TEMPLATE,
            result=True,
            fname=fname,
            hashes=hashes,
            status=status,
            year=datetime.datetime.now().year,
        )

    return render_template_string(MAIN_TEMPLATE, result=False, year=datetime.datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)