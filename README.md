# 📂 File Integrity Checker (Web & CLI)

A versatile **File Integrity Monitoring (FIM)** tool available with both a **modern web interface** and a **powerful command-line interface (CLI)**.
This application allows users to generate cryptographic hash baselines for their important files and later verify if these files have been modified.

---

## Key Features

*  **Dual Interface** → A user-friendly **web UI** for manual checks & a robust **CLI** for automation.
*  **Multi-User Support** → Web app includes secure **login & registration**. Each user has their own private baseline history.
*  **Personalized Dashboard** → Users can view the history of all uploaded files.
*  **Multiple Hash Algorithms** → MD5, SHA1, and SHA256 for thorough integrity verification.
*  **Drag & Drop Upload** → Clean, modern dark-mode UI for uploading files.
*  **Bulk Operations (CLI)** → Generate a baseline for an entire folder at once.

---

## Screenshot

> <img width="1919" height="974" alt="image" src="https://github.com/user-attachments/assets/8c3d57f8-d805-4f27-be45-1c2c3eb79b42" />

> <img width="1919" height="968" alt="image" src="https://github.com/user-attachments/assets/9df104f0-619f-49a8-88a2-ec81a88da563" />

> <img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/1877e030-c4b5-4348-bcf5-aeca107e583a" />


---

## Technology Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, TailwindCSS (via CDN), Vanilla JavaScript
* **Data Storage:** JSON (users.json, baseline.json) → portable & easy setup

---

## 📂 File Structure

```bash
.
├── web_checker.py       # Main Flask web application
├── cli_checker.py       # Command-line interface tool
├── requirements.txt     # Python dependencies
├── uploads/             # Temporary storage for uploaded files
├── users.json           # (Auto-generated) Stores user credentials
└── baseline.json        # (Auto-generated) Stores file hash baselines
```

---

## 🚀 Setup & Installation

### Prerequisites

* Python **3.7+**
* `pip` (Python package installer)

### Installation Steps

```bash
# Clone the repository
git clone <your-repository-url>
cd <repository-folder>

# Create & activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧑‍💻 How to Use

### Web Application

Run Flask server:

```bash
flask run
# or
python web_checker.py
```

Open browser → [http://127.0.0.1:5000](http://127.0.0.1:5000)

1. Register a new account & log in
2. **Generate Baseline:**

   * Upload file → Click *Generate Baseline* → Hashes saved
3. **Verify File:**

   * Upload file → Click *Verify File* → Status shown (*ORIGINAL / MODIFIED / NOT IN BASELINE*)
4. View history on your **Dashboard**

---

### Command-Line Interface (CLI)

The CLI is great for **scripting, servers, or bulk checks**.

⚠️ Note: CLI and Web use different `baseline.json` formats. Keep them separate or specify a custom file with `--baseline`.

#### Examples:

Generate baseline for one file:

```bash
python cli_checker.py --generate /path/to/document.pdf
```

Generate baseline for all files in a folder:

```bash
python cli_checker.py --generate-folder /path/to/important_docs
```

Verify a single file:

```bash
python cli_checker.py --verify /path/to/document.pdf
```

Verify all files:

```bash
python cli_checker.py --verify-all
```

Use custom baseline:

```bash
python cli_checker.py --generate /path/to/file.txt --baseline cli_baseline.json
```
📜 License

This project is licensed under the MIT License.
See LICENSE
 for details.

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
