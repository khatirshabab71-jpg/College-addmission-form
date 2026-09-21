"""
College Admission Form - Python Backend Server
Handles student submission requests and stores data locally in JSON format.
"""

import http.server
import socketserver
import json
import os
from datetime import datetime

# 1. CONSTANTS & FOLDER PATH SETUP
PORT = 5000
DATA_FOLDER = r"C:\Users\Laptop Valley\Desktop\data stored"
JSON_FILE_PATH = os.path.join(DATA_FOLDER, "students.json")

def ensure_data_storage():
    """
    Ensures that the target data folder and JSON storage file exist.
    If the folder does not exist, it creates it automatically.
    If the students.json file does not exist, it creates an empty list [].
    """
    try:
        # Create folder if it does not exist
        os.makedirs(DATA_FOLDER, exist_ok=True)
        
        # Create empty JSON file if it does not exist
        if not os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
            print(f"[SUCCESS] Created new storage file at: {JSON_FILE_PATH}")
    except Exception as e:
        print(f"[ERROR] Could not setup storage folder/file: {e}")

def get_next_student_id(students_list):
    """
    Generates auto-incrementing student ID (e.g., STU001, STU002, STU003).
    """
    count = len(students_list) + 1
    return f"STU{count:03d}"

def save_student_data(student_data):
    """
    Reads existing students from JSON, appends new student, and saves back to file.
    Returns (success_boolean, result_message_or_student_id)
    """
    ensure_data_storage()
    
    try:
        # Step A: Read existing students from file
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            students = json.load(file)
        
        # Step B: Generate unique Student ID & Timestamp
        student_id = get_next_student_id(students)
        student_data["studentId"] = student_id
        student_data["submissionTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Step C: Append new student to list
        students.append(student_data)
        
        # Step D: Save updated list back to JSON file
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        
        print(f"[SUCCESS] Saved student record: {student_id} ({student_data.get('fullName', 'N/A')})")
        return True, student_id
        
    except Exception as e:
        print(f"[ERROR] Failed to save student data: {e}")
        return False, str(e)


# 2. HTTP REQUEST HANDLER
class AdmissionRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom Request Handler to receive HTTP POST requests from JavaScript fetch().
    """
    
    def do_OPTIONS(self):
        """Handle CORS pre-flight browser requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """Handle incoming student admission form submissions"""
        if self.path == "/api/submit":
            try:
                # Read incoming JSON payload size and content
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON string into Python dictionary
                student_info = json.loads(post_data.decode("utf-8"))
                
                # Save to JSON file
                success, result = save_student_data(student_info)
                
                # Send HTTP Response back to JavaScript
                self.send_response(200 if success else 500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response_payload = {
                    "success": success,
                    "message": "Admission Submitted Successfully!" if success else "Failed to save record.",
                    "studentId": result if success else None,
                    "error": None if success else result
                }
                
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))
                
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                error_response = {"success": False, "message": "Invalid data format.", "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

# 3. START SERVER FUNCTION
def run_server():
    ensure_data_storage()
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), AdmissionRequestHandler) as httpd:
            print("==================================================")
            print(f"[SERVER STARTED] Running on http://127.0.0.1:{PORT}")
            print(f"[STORAGE FOLDER] {DATA_FOLDER}")
            print(f"[STORAGE FILE]   {JSON_FILE_PATH}")
            print("==================================================")
            print("Press Ctrl+C in terminal to stop the server.\n")
            httpd.serve_forever()
    except OSError:
        print("==================================================")
        print(f"[INFO] Python server is ALREADY running on http://127.0.0.1:{PORT}!")
        print("You can submit the admission form right now.")
        print("==================================================")

if __name__ == "__main__":
    run_server()
