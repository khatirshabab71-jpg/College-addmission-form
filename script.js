/* ==========================================================================
   COLLEGE ADMISSION FORM - JAVASCRIPT ENGINE
   Concepts Covered: DOM, Event Listeners, Functions, Regex, Objects, Validation
   ========================================================================== */

// 1. DOM ELEMENT SELECTION
// document.getElementById() retrieves a specific HTML element using its unique id attribute
const admissionForm = document.getElementById("admissionForm");
const obtainedMarksInput = document.getElementById("obtainedMarks");
const totalMarksInput = document.getElementById("totalMarks");
const percentageInput = document.getElementById("percentage");
const gradeInput = document.getElementById("grade");
const summaryModal = document.getElementById("summaryModal");
const summaryContent = document.getElementById("summaryContent");

// 2. HELPER FUNCTIONS FOR CALCULATIONS

/**
 * Calculates percentage based on obtained marks and total marks.
 * Formula: (Obtained / Total) * 100
 * @param {number} obtained - Marks obtained by student
 * @param {number} total - Total maximum marks
 * @returns {number|null} - Percentage rounded to 2 decimal places, or null if invalid
 */
function calculatePercentage(obtained, total) {
    // Check if numbers are valid and total is greater than 0 to avoid division by zero
    if (isNaN(obtained) || isNaN(total) || total <= 0 || obtained < 0 || obtained > total) {
        return null;
    }
    const percentage = (obtained / total) * 100;
    return parseFloat(percentage.toFixed(2)); // String to Number conversion
}

/**
 * Calculates letter grade based on percentage percentage value.
 * Grade Scale:
 *  80% or above = A
 *  70% - 79.99% = B
 *  60% - 69.99% = C
 *  50% - 59.99% = D
 *  Below 50% = F
 * @param {number} percentage 
 * @returns {string} Letter grade
 */
function calculateGrade(percentage) {
    if (percentage === null || isNaN(percentage)) {
        return "";
    }
    
    // Conditional logic (if / else if / else)
    if (percentage >= 80) {
        return "A (Excellent)";
    } else if (percentage >= 70) {
        return "B (Good)";
    } else if (percentage >= 60) {
        return "C (Satisfactory)";
    } else if (percentage >= 50) {
        return "D (Pass)";
    } else {
        return "F (Fail)";
    }
}

/**
 * Updates the percentage and grade inputs dynamically as the user types
 */
function updatePercentageAndGrade() {
    // Number conversion using parseFloat() and obtaining input value
    const obtained = parseFloat(obtainedMarksInput.value);
    const total = parseFloat(totalMarksInput.value);

    const percentage = calculatePercentage(obtained, total);

    if (percentage !== null) {
        percentageInput.value = `${percentage}%`;
        gradeInput.value = calculateGrade(percentage);
    } else {
        percentageInput.value = "";
        gradeInput.value = "";
    }
}

// 3. REAL-TIME EVENT LISTENERS FOR MARKS CALCULATION
// 'input' event triggers immediately whenever the user changes the field text
obtainedMarksInput.addEventListener("input", updatePercentageAndGrade);
totalMarksInput.addEventListener("input", updatePercentageAndGrade);


// 4. VALIDATION HELPER FUNCTIONS

/**
 * Displays error message under a specific form input field
 * @param {string} inputId - ID of the input element
 * @param {string} errorId - ID of the error message container element
 * @param {string} message - Error description message
 */
function showError(inputId, errorId, message) {
    const inputElement = document.getElementById(inputId);
    const errorElement = document.getElementById(errorId);
    
    if (inputElement) {
        inputElement.classList.add("input-invalid");
    }
    if (errorElement) {
        errorElement.textContent = message;
    }
}

/**
 * Clears error state for a specific input field
 * @param {string} inputId 
 * @param {string} errorId 
 */
function clearError(inputId, errorId) {
    const inputElement = document.getElementById(inputId);
    const errorElement = document.getElementById(errorId);
    
    if (inputElement) {
        inputElement.classList.remove("input-invalid");
    }
    if (errorElement) {
        errorElement.textContent = "";
    }
}

/**
 * Clears all error messages across the form
 */
function clearAllErrors() {
    const errorMessages = document.querySelectorAll(".error-msg");
    const invalidInputs = document.querySelectorAll(".input-invalid");

    // Using Array loop / forEach
    errorMessages.forEach(msg => msg.textContent = "");
    invalidInputs.forEach(input => input.classList.remove("input-invalid"));
}


// 5. REGULAR EXPRESSIONS (REGEX) FOR FORMAT VALIDATION
// Email pattern: standard user@domain.com
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// CNIC format: 12345-6789012-3 (5 digits - 7 digits - 1 digit)
const cnicRegex = /^\d{5}-\d{7}-\d{1}$/;
// Phone format: e.g. 03001234567 (11 digits starting with 03)
const phoneRegex = /^03\d{9}$/;


// 6. FORM VALIDATION FUNCTION
function validateForm() {
    clearAllErrors();
    let isValid = true; // Boolean flag tracking form status

    // A. Student Information
    const fullName = document.getElementById("fullName").value.trim(); // String method trim()
    if (fullName === "") {
        showError("fullName", "fullNameError", "Full Name is required.");
        isValid = false;
    }

    const fatherName = document.getElementById("fatherName").value.trim();
    if (fatherName === "") {
        showError("fatherName", "fatherNameError", "Father's Name is required.");
        isValid = false;
    }

    const dob = document.getElementById("dob").value;
    if (dob === "") {
        showError("dob", "dobError", "Please select your Date of Birth.");
        isValid = false;
    }

    const gender = document.getElementById("gender").value;
    if (gender === "") {
        showError("gender", "genderError", "Please select your Gender.");
        isValid = false;
    }

    const cnic = document.getElementById("cnic").value.trim();
    if (cnic === "") {
        showError("cnic", "cnicError", "CNIC/B-Form is required.");
        isValid = false;
    } else if (!cnicRegex.test(cnic)) {
        showError("cnic", "cnicError", "Format must be 12345-6789012-3.");
        isValid = false;
    }

    const phone = document.getElementById("phone").value.trim();
    if (phone === "") {
        showError("phone", "phoneError", "Phone number is required.");
        isValid = false;
    } else if (!phoneRegex.test(phone)) {
        showError("phone", "phoneError", "Enter valid 11-digit number (e.g. 03001234567).");
        isValid = false;
    }

    const email = document.getElementById("email").value.trim();
    if (email === "") {
        showError("email", "emailError", "Email address is required.");
        isValid = false;
    } else if (!emailRegex.test(email)) {
        showError("email", "emailError", "Please enter a valid email address.");
        isValid = false;
    }

    // B. Academic Information
    const previousSchool = document.getElementById("previousSchool").value.trim();
    if (previousSchool === "") {
        showError("previousSchool", "previousSchoolError", "Previous School/College name is required.");
        isValid = false;
    }

    const qualification = document.getElementById("qualification").value;
    if (qualification === "") {
        showError("qualification", "qualificationError", "Please select previous qualification.");
        isValid = false;
    }

    const passingYear = parseInt(document.getElementById("passingYear").value);
    if (isNaN(passingYear) || passingYear < 1990 || passingYear > 2026) {
        showError("passingYear", "passingYearError", "Enter a valid passing year (1990 - 2026).");
        isValid = false;
    }

    const obtainedMarks = parseFloat(obtainedMarksInput.value);
    const totalMarks = parseFloat(totalMarksInput.value);

    if (isNaN(obtainedMarks) || obtainedMarks < 0) {
        showError("obtainedMarks", "obtainedMarksError", "Please enter valid obtained marks.");
        isValid = false;
    }
    if (isNaN(totalMarks) || totalMarks <= 0) {
        showError("totalMarks", "totalMarksError", "Please enter valid total marks.");
        isValid = false;
    }
    if (!isNaN(obtainedMarks) && !isNaN(totalMarks) && obtainedMarks > totalMarks) {
        showError("obtainedMarks", "obtainedMarksError", "Obtained marks cannot exceed total marks.");
        isValid = false;
    }

    const department = document.getElementById("department").value;
    if (department === "") {
        showError("department", "departmentError", "Please select desired department.");
        isValid = false;
    }

    // C. Address Information
    const address = document.getElementById("address").value.trim();
    if (address === "") {
        showError("address", "addressError", "Permanent address is required.");
        isValid = false;
    }

    const city = document.getElementById("city").value.trim();
    if (city === "") {
        showError("city", "cityError", "City is required.");
        isValid = false;
    }

    const province = document.getElementById("province").value.trim();
    if (province === "") {
        showError("province", "provinceError", "Province is required.");
        isValid = false;
    }

    // D. Guardian Information
    const guardianName = document.getElementById("guardianName").value.trim();
    if (guardianName === "") {
        showError("guardianName", "guardianNameError", "Guardian Name is required.");
        isValid = false;
    }

    const relationship = document.getElementById("relationship").value;
    if (relationship === "") {
        showError("relationship", "relationshipError", "Please select relationship.");
        isValid = false;
    }

    const guardianPhone = document.getElementById("guardianPhone").value.trim();
    if (guardianPhone === "") {
        showError("guardianPhone", "guardianPhoneError", "Guardian Phone Number is required.");
        isValid = false;
    } else if (!phoneRegex.test(guardianPhone)) {
        showError("guardianPhone", "guardianPhoneError", "Enter valid 11-digit number (e.g. 03001234567).");
        isValid = false;
    }

    // F. Declaration Checkbox
    const declaration = document.getElementById("declaration").checked;
    if (!declaration) {
        showError("declaration", "declarationError", "You must confirm the declaration to submit.");
        isValid = false;
    }

    return isValid;
}


// 7. FORM SUBMISSION EVENT LISTENER
admissionForm.addEventListener("submit", function (event) {
    // CRITICAL: Prevent default browser page reload on form submit
    event.preventDefault();

    // Validate form inputs
    const isFormValid = validateForm();

    if (isFormValid) {
        // Collect radio button values
        const hostelSelected = document.querySelector('input[name="hostel"]:checked')?.value || "No";
        const transportSelected = document.querySelector('input[name="transport"]:checked')?.value || "No";

        // Create a JavaScript Object to store student admission data
        const student = {
            fullName: document.getElementById("fullName").value.trim(),
            fatherName: document.getElementById("fatherName").value.trim(),
            dob: document.getElementById("dob").value,
            gender: document.getElementById("gender").value,
            cnic: document.getElementById("cnic").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            email: document.getElementById("email").value.trim(),
            previousSchool: document.getElementById("previousSchool").value.trim(),
            qualification: document.getElementById("qualification").value,
            passingYear: document.getElementById("passingYear").value,
            obtainedMarks: document.getElementById("obtainedMarks").value,
            totalMarks: document.getElementById("totalMarks").value,
            percentage: percentageInput.value,
            grade: gradeInput.value,
            department: document.getElementById("department").value,
            address: document.getElementById("address").value.trim(),
            city: document.getElementById("city").value.trim(),
            province: document.getElementById("province").value.trim(),
            guardianName: document.getElementById("guardianName").value.trim(),
            relationship: document.getElementById("relationship").value,
            guardianPhone: document.getElementById("guardianPhone").value.trim(),
            hostel: hostelSelected,
            transport: transportSelected
        };

        // Disable submit button temporarily to prevent double submission
        const submitBtn = document.getElementById("submitBtn");
        if (submitBtn) submitBtn.disabled = true;

        // Send data to Python backend server using Fetch API
        fetch("http://127.0.0.1:5000/api/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update summary card with assigned Student ID and PDF download link
                renderSummary(student, data.studentId, data.pdfUrl);
                alert(`✅ Admission Submitted Successfully!\nAssigned Student ID: ${data.studentId}\nOfficial PDF saved to: D:\\data stored\\${data.studentId}.pdf`);
            } else {
                renderSummary(student, null, null);
                alert(`❌ Submission Failed: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("Error connecting to server:", error);
            renderSummary(student, null, null);
            alert("⚠️ Warning: Could not connect to Python server. Make sure 'python server.py' is running!");
        })
        .finally(() => {
            if (submitBtn) submitBtn.disabled = false;
            // Scroll smoothly down to summary card
            summaryModal.scrollIntoView({ behavior: 'smooth' });
        });
    }
});

/**
 * Renders the admission summary table inside summaryModal
 * @param {Object} student 
 * @param {string|null} studentId
 * @param {string|null} pdfUrl
 */
function renderSummary(student, studentId = null, pdfUrl = null) {
    let idBanner = "";
    if (studentId) {
        idBanner = `
            <div class="student-id-banner">
                Assigned Student ID: <strong>${studentId}</strong>
            </div>
        `;
    }

    summaryContent.innerHTML = `
        ${idBanner}
        <table class="summary-table">
            <tr><th>Full Name</th><td>${student.fullName}</td></tr>
            <tr><th>Father's Name</th><td>${student.fatherName}</td></tr>
            <tr><th>CNIC / B-Form</th><td>${student.cnic}</td></tr>
            <tr><th>Email & Phone</th><td>${student.email} | ${student.phone}</td></tr>
            <tr><th>Desired Department</th><td><strong style="color: var(--accent-color);">${student.department}</strong></td></tr>
            <tr><th>Previous Qualification</th><td>${student.qualification} (${student.passingYear})</td></tr>
            <tr><th>Marks & Percentage</th><td>${student.obtainedMarks} / ${student.totalMarks} (${student.percentage})</td></tr>
            <tr><th>Final Calculated Grade</th><td><span style="color: var(--success-color); font-weight: bold;">${student.grade}</span></td></tr>
            <tr><th>Guardian Information</th><td>${student.guardianName} (${student.relationship}) - ${student.guardianPhone}</td></tr>
            <tr><th>Address</th><td>${student.address}, ${student.city}, ${student.province}</td></tr>
            <tr><th>Hostel & Transport</th><td>Hostel: ${student.hostel} | Transport: ${student.transport}</td></tr>
        </table>
    `;

    const downloadPdfBtn = document.getElementById("downloadPdfBtn");
    if (downloadPdfBtn) {
        if (pdfUrl) {
            downloadPdfBtn.href = `http://127.0.0.1:5000${pdfUrl}`;
            downloadPdfBtn.classList.remove("hidden");
        } else {
            downloadPdfBtn.classList.add("hidden");
        }
    }

    summaryModal.classList.remove("hidden");
}

// Reset button listener to hide summary card and clear errors
admissionForm.addEventListener("reset", function () {
    clearAllErrors();
    summaryModal.classList.add("hidden");
});
