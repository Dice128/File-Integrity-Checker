File Integrity Checker (Web & CLI)
A versatile File Integrity Checker (FIM) tool available with both a modern web interface and a powerful command-line interface (CLI). This application allows users to generate cryptographic hash baselines for their important files and later verify if these files have been modified.

The web application is built with Flask and supports multiple users with individual, separate dashboards, while the CLI is perfect for scripting and bulk operations.

Key Features ✨
Dual Interface: A user-friendly web UI for manual checks and a robust CLI for automation.

Multi-User Support: The web app includes a secure login and registration system. Each user has their own private baseline history.

Personalized Dashboard: Logged-in users can view a history of all the files they have generated a baseline for.

Multiple Hash Algorithms: Utilizes MD5, SHA1, and SHA256 for thorough integrity verification.

Easy to Use: Features a drag-and-drop file upload system in the web interface.

Bulk Operations (CLI): The CLI can generate a baseline for an entire folder at once.

Screenshot
Here you can add a screenshot of your application's web interface.

``

Technology Stack 💻
Backend: Python, Flask

Frontend: HTML, Tailwind CSS (via CDN), vanilla JavaScript

Data Storage: Simple JSON files (users.json, baseline.json) are used for storing user and baseline data, making the application portable and easy to set up without a formal database.

File Structure 📂
.
├── web_checker.py         # Main Flask web application
├── cli_checker.py         # Command-line interface tool
├── requirements.txt       # Python dependencies
├── uploads/               # Directory for temporarily storing uploaded files
├── users.json             # (Auto-generated) Stores user credentials
└── baseline.json          # (Auto-generated) Stores file hash baselines
Setup and Installation 🚀
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.7+

pip (Python package installer)

Installation Steps
Clone the repository:

Bash

git clone <your-repository-url>
cd <repository-folder>
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:

Bash

pip install -r requirements.txt
How to Use 🧑‍💻
1. Web Application
The web application provides a graphical interface for managing your file baselines.

Run the Flask server:

Bash

flask run
Or directly:

Bash

python web_checker.py
Access the application by opening your web browser and navigating to http://127.0.0.1:5000.

Register a new account and then log in.

To generate a baseline:

Drag and drop a file or click to select one.

Click the "Generate Baseline" button. The file's hashes are now saved to your account.

To verify a file:

Upload the same file again (it can be the original or a modified version).

Click the "Verify File" button. The application will compare its current hashes with the saved baseline and show you the status (ORIGINAL, MODIFIED, or NOT IN BASELINE).

Check your Dashboard by clicking the "Dashboard" link in the navigation bar to see a history of all files you are monitoring.

2. Command-Line Interface (CLI)
The CLI is ideal for scripting, automation, or checking files on a server.

Note on CLI baseline.json: The cli_checker.py script generates a baseline.json file with a different format (a simple list) than the one used by the web application (a dictionary of users). They are not compatible. It's recommended to use them in separate folders or specify a different baseline file for the CLI using the --baseline flag.

Usage examples:

Generate a baseline for a single file:

Bash

python cli_checker.py --generate /path/to/your/document.pdf
Generate a baseline for all files in a folder:

Bash

python cli_checker.py --generate-folder /path/to/your/important_documents
Verify a single file against the baseline:

Bash

python cli_checker.py --verify /path/to/your/document.pdf
Verify all files listed in the baseline:

Bash

python cli_checker.py --verify-all
Use a custom baseline file:

Bash

python cli_checker.py --generate /path/to/file.txt --baseline cli_baseline.json
License
This project is licensed under the MIT License. See the LICENSE file for details.
