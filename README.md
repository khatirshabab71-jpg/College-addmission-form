# 🎓 Al Shabab College - Online Admission Form System

A full-stack web application for college admissions. Students can fill out the admission application online with real-time validation, automatic grade calculation, and instant data submission stored locally via a Python backend.

---

## ✨ Features

- **Dynamic Grade & Percentage Calculator**: Automatically calculates percentage and assigns letter grades (A, B, C, D, F) as the user types their marks.
- **Form Validation**: Validates user inputs (CNIC format `12345-6789012-3`, Phone number `03XXXXXXXXX`, Email, etc.) using JavaScript Regular Expressions (Regex).
- **Python Backend Server**: Custom Python server (`server.py`) listens for submissions and generates unique Student IDs (e.g., `STU001`, `STU002`).
- **JSON Data Storage**: Saves all submitted student data into a local `students.json` file.
- **Offline Mode Fallback**: If the Python server is offline, the frontend safely handles the submission and displays the confirmation summary modal.
- **Responsive Modern UI**: Built with modern CSS featuring smooth scroll, glassmorphism UI components, and clean modal dialogs.

---

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+, Fetch API, DOM Manipulation)
- **Backend**: Python 3 (`http.server`, `socketserver`, `json`, `os`)
- **Data Storage**: JSON (`students.json`)

---

## 🚀 How to Run the Project

### Step 1: Start the Python Backend Server
1. Open terminal/command prompt in the project root folder.
2. Run the server script:
   ```bash
   
   python server.py
college-admission-form/
├── server.py                   # Python HTTP backend server
├── college-admission-form/
│   ├── index.html              # Admission form webpage
│   ├── style.css               # Styling and visual layout
│   └── script.js               # Validation logic & fetch() API request
└── .gitignore                  # Git ignore file (excludes __pycache__)
