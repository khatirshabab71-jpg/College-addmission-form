r"""
College Admission Form - Python Backend Server
Handles student submission requests, validates data, stores records locally in JSON,
and automatically generates individual PDF application documents in D:\data stored.
"""

import http.server
import socketserver
import json
import os
import re
import urllib.parse
from datetime import datetime

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# 1. CONSTANTS & FOLDER PATH SETUP
PORT = 5000
DATA_FOLDER = r"D:\data stored"
JSON_FILE_PATH = os.path.join(DATA_FOLDER, "students.json")

def ensure_data_storage():
    r"""
    Ensures that the target data folder and JSON storage file exist.
    If D:\data stored does not exist, it creates it automatically.
    If students.json does not exist, it creates an empty list [].
    """
    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)
        if not os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
            print(f"[SUCCESS] Created new storage file at: {JSON_FILE_PATH}")
    except Exception as e:
        print(f"[ERROR] Could not setup storage folder/file at {DATA_FOLDER}: {e}")
        raise RuntimeError(f"Storage folder access error: {e}")

def get_next_student_id(students_list):
    """
    Generates an auto-incrementing student ID (e.g., STU001, STU002, STU003).
    Ensures no duplicate IDs by inspecting both JSON records and existing PDFs in D:\\data stored.
    """
    existing_nums = []
    
    # 1. Extract IDs from existing JSON records
    for s in students_list:
        sid = s.get("studentId", "")
        match = re.match(r"^STU(\d+)$", str(sid))
        if match:
            existing_nums.append(int(match.group(1)))
            
    # 2. Extract IDs from existing PDF files in DATA_FOLDER
    if os.path.exists(DATA_FOLDER):
        for fname in os.listdir(DATA_FOLDER):
            match = re.match(r"^STU(\d+)\.pdf$", fname, re.IGNORECASE)
            if match:
                existing_nums.append(int(match.group(1)))
                
    max_num = max(existing_nums) if existing_nums else 0
    candidate_num = max(len(students_list) + 1, max_num + 1)
    
    # Ensure candidate PDF file does not exist unexpectedly
    while True:
        candidate_id = f"STU{candidate_num:03d}"
        pdf_path = os.path.join(DATA_FOLDER, f"{candidate_id}.pdf")
        id_in_json = any(s.get("studentId") == candidate_id for s in students_list)
        if not os.path.exists(pdf_path) and not id_in_json:
            return candidate_id
        candidate_num += 1

def validate_student_data(student_data):
    """
    Validates incoming student admission form fields.
    Returns (is_valid: bool, error_message: str or None)
    """
    if not isinstance(student_data, dict):
        return False, "Payload must be a JSON object."
        
    required_fields = [
        ("fullName", "Full Name"),
        ("fatherName", "Father's Name"),
        ("dob", "Date of Birth"),
        ("gender", "Gender"),
        ("cnic", "CNIC / B-Form Number"),
        ("phone", "Phone Number"),
        ("email", "Email Address"),
        ("previousSchool", "Previous School/College Name"),
        ("qualification", "Previous Qualification"),
        ("passingYear", "Passing Year"),
        ("obtainedMarks", "Obtained Marks"),
        ("totalMarks", "Total Marks"),
        ("department", "Desired Program / Department"),
        ("address", "Permanent Address"),
        ("city", "City"),
        ("province", "Province"),
        ("guardianName", "Guardian Name"),
        ("relationship", "Guardian Relationship"),
        ("guardianPhone", "Guardian Phone Number")
    ]
    
    for key, label in required_fields:
        val = str(student_data.get(key, "")).strip()
        if not val:
            return False, f"Missing required field: {label}"

    # Numeric validations
    try:
        obt = float(student_data.get("obtainedMarks", 0))
        tot = float(student_data.get("totalMarks", 0))
        if obt < 0 or tot <= 0:
            return False, "Obtained marks must be >= 0 and total marks > 0."
        if obt > tot:
            return False, "Obtained marks cannot exceed total marks."
    except (ValueError, TypeError):
        return False, "Obtained and total marks must be valid numbers."

    try:
        yr = int(student_data.get("passingYear", 0))
        if yr < 1990 or yr > 2030:
            return False, "Passing year must be a valid year."
    except (ValueError, TypeError):
        return False, "Passing year must be an integer."

    return True, None

def generate_pdf(student_data, pdf_path):
    """
    Generates a professional PDF application document for the student using ReportLab.
    Saves directly to D:\\data stored\\STUxxx.pdf.
    """
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'HeaderSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=10
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )
    
    val_style = ParagraphStyle(
        'ValStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=0
    )

    story = []
    
    # Header Section
    story.append(Paragraph("AL SHABAB COLLEGE", title_style))
    story.append(Paragraph("OFFICIAL ADMISSION APPLICATION FORM", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))
    
    # Student ID & Timestamp Header Table
    stu_id = student_data.get("studentId", "N/A")
    timestamp = student_data.get("submissionTimestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    meta_data = [
        [
            Paragraph(f"<b>Student ID:</b> <font color='#2563EB'><b>{stu_id}</b></font>", badge_style),
            Paragraph(f"<b>Submission Date:</b> {timestamp}", ParagraphStyle('RightMeta', parent=val_style, alignment=2))
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BFDBFE')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    def make_section_table(data_tuples):
        table_data = []
        for row in data_tuples:
            row_cells = []
            for item in row:
                if item is None:
                    row_cells.extend(["", ""])
                else:
                    lbl, val = item
                    row_cells.append(Paragraph(lbl, label_style))
                    row_cells.append(Paragraph(str(val) if val != "" else "N/A", val_style))
            table_data.append(row_cells)
        
        t = Table(table_data, colWidths=[120, 150, 120, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8FAFC')),
            ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    # A. Student Information
    story.append(Paragraph("A. Student Personal Information", section_title_style))
    p_info = [
        [("Full Name:", student_data.get("fullName", "")), ("Father's Name:", student_data.get("fatherName", ""))],
        [("Date of Birth:", student_data.get("dob", "")), ("Gender:", str(student_data.get("gender", "")).capitalize())],
        [("CNIC / B-Form:", student_data.get("cnic", "")), ("Phone Number:", student_data.get("phone", ""))],
        [("Email Address:", student_data.get("email", "")), None]
    ]
    story.append(make_section_table(p_info))
    story.append(Spacer(1, 6))

    # B. Academic Information
    story.append(Paragraph("B. Academic Information", section_title_style))
    ac_info = [
        [("Previous Institute:", student_data.get("previousSchool", "")), ("Qualification:", student_data.get("qualification", ""))],
        [("Passing Year:", student_data.get("passingYear", "")), ("Obtained / Total:", f"{student_data.get('obtainedMarks', '')} / {student_data.get('totalMarks', '')}")],
        [("Percentage:", student_data.get("percentage", "")), ("Calculated Grade:", student_data.get("grade", ""))],
        [("Desired Program:", student_data.get("department", "")), None]
    ]
    story.append(make_section_table(ac_info))
    story.append(Spacer(1, 6))

    # C. Address Information
    story.append(Paragraph("C. Address Details", section_title_style))
    add_info = [
        [("Address:", student_data.get("address", "")), ("City:", student_data.get("city", ""))],
        [("Province:", student_data.get("province", "")), ("Postal Code:", student_data.get("postalCode", "N/A"))]
    ]
    story.append(make_section_table(add_info))
    story.append(Spacer(1, 6))

    # D. Guardian Information
    story.append(Paragraph("D. Guardian Details", section_title_style))
    g_info = [
        [("Guardian Name:", student_data.get("guardianName", "")), ("Relationship:", student_data.get("relationship", ""))],
        [("Guardian Phone:", student_data.get("guardianPhone", "")), ("Occupation:", student_data.get("guardianOccupation", "N/A"))]
    ]
    story.append(make_section_table(g_info))
    story.append(Spacer(1, 6))

    # E. Additional Facilities & Info
    story.append(Paragraph("E. Additional Facilities & Comments", section_title_style))
    extra_info = [
        [("Hostel Required:", student_data.get("hostel", "No")), ("Transport Required:", student_data.get("transport", "No"))],
        [("Referral Source:", student_data.get("referral", "N/A")), ("Comments:", student_data.get("comments", "N/A"))]
    ]
    story.append(make_section_table(extra_info))
    story.append(Spacer(1, 10))

    # Declaration & Signatures
    story.append(Paragraph("F. Declaration & Signatures", section_title_style))
    dec_text = "I hereby confirm that all information provided in this application form is true, correct, and complete to the best of my knowledge."
    story.append(Paragraph(dec_text, ParagraphStyle('DecText', parent=val_style, fontSize=8, textColor=colors.HexColor('#475569'))))
    story.append(Spacer(1, 20))

    sig_data = [
        [
            Paragraph("________________________<br/><b>Applicant Signature</b>", ParagraphStyle('Sig1', parent=val_style, alignment=0)),
            Paragraph("________________________<br/><b>Admissions Officer Signature</b>", ParagraphStyle('Sig2', parent=val_style, alignment=2))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)

    doc.build(story)

def save_student_data(student_data):
    r"""
    1. Validates input data.
    2. Generates unique Student ID.
    3. Generates and saves PDF to D:\data stored\<STUxxx>.pdf.
    4. Saves student JSON object to D:\data stored\students.json.
    Returns (success_boolean, student_id_or_error_msg)
    """
    ensure_data_storage()
    
    # Step 1: Backend validation
    is_valid, err_msg = validate_student_data(student_data)
    if not is_valid:
        return False, err_msg
        
    try:
        # Step 2: Read existing students
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            students = json.load(file)
        
        # Step 3: Generate unique Student ID & Timestamp
        student_id = get_next_student_id(students)
        student_data["studentId"] = student_id
        student_data["submissionTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Target PDF Path
        pdf_path = os.path.join(DATA_FOLDER, f"{student_id}.pdf")
        if os.path.exists(pdf_path):
            return False, f"PDF file {student_id}.pdf already exists unexpectedly!"

        # Step 4: Generate PDF file
        generate_pdf(student_data, pdf_path)
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
            return False, "PDF generation failed or created empty file."
            
        # Step 5: Save to JSON file
        students.append(student_data)
        try:
            with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump(students, file, indent=4)
        except Exception as json_err:
            # If JSON writing fails, cleanup generated PDF to prevent orphan files
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise json_err
            
        print(f"[SUCCESS] Saved student record & PDF: {student_id} ({student_data.get('fullName', 'N/A')}) at {pdf_path}")
        return True, student_id
        
    except Exception as e:
        print(f"[ERROR] Failed to process application: {e}")
        return False, str(e)


# 2. HTTP REQUEST HANDLER
class AdmissionRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom Request Handler to serve static files and handle API requests for form submissions & PDF downloads.
    """
    
    def do_OPTIONS(self):
        """Handle CORS pre-flight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for static files and PDF downloads"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == "/api/pdf":
            query_params = urllib.parse.parse_qs(parsed_path.query)
            student_id = query_params.get("id", [None])[0]
            self.handle_pdf_download(student_id)
        elif parsed_path.path.startswith("/api/pdf/"):
            student_id = parsed_path.path.replace("/api/pdf/", "")
            self.handle_pdf_download(student_id)
        else:
            super().do_GET()

    def handle_pdf_download(self, student_id):
        """Serves requested student PDF file securely"""
        if not student_id or not re.match(r"^STU\d+$", str(student_id)):
            self.send_error(400, "Invalid Student ID format.")
            return
            
        pdf_filename = f"{student_id}.pdf"
        pdf_path = os.path.abspath(os.path.join(DATA_FOLDER, pdf_filename))
        
        # Security: Prevent Path Traversal
        folder_abspath = os.path.abspath(DATA_FOLDER)
        if not os.path.commonpath([folder_abspath, pdf_path]) == folder_abspath:
            self.send_error(403, "Access Denied.")
            return
            
        if not os.path.exists(pdf_path):
            self.send_error(404, f"PDF file for {student_id} not found.")
            return
            
        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.send_header("Content-Disposition", f'inline; filename="{pdf_filename}"')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(pdf_bytes)
        except Exception as e:
            self.send_error(500, f"Error reading PDF file: {e}")

    def do_POST(self):
        """Handle incoming student admission form submissions"""
        if self.path == "/api/submit":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                student_info = json.loads(post_data.decode("utf-8"))
                
                # Save to JSON & Generate PDF
                success, result = save_student_data(student_info)
                
                status_code = 200 if success else 400
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response_payload = {
                    "success": success,
                    "message": "Admission Submitted and PDF Generated Successfully!" if success else f"Submission failed: {result}",
                    "studentId": result if success else None,
                    "pdfUrl": f"/api/pdf?id={result}" if success else None,
                    "error": None if success else result
                }
                
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))
                
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                error_response = {"success": False, "message": "Invalid request format.", "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

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
        print("==================================================")

if __name__ == "__main__":
    run_server()
