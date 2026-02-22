from fileinput import filename
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from DataBase.DataBaseConnector import DataBaseConnection
from CloudConnect.FileUpload import upload_file_to_drive
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handler():
    obj = DataBaseConnection()
    role = request.form['expertise']
    gender = request.form['gender']
    other_role = request.form['other_role']
    fname = request.form['first_name']
    lname = request.form['family_name']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']
    resumePDF = request.files['resume']
    os.makedirs("resumes", exist_ok=True)
    
    if role == "other":
        role = other_role
    data = {
        "role": role,
        "gender": gender,
        "other_role": other_role,
        "fname": fname,
        "lname": lname,
        "email": email,
        "phone": phone,
        "dob": dob,
        "address": address,
        "city": city,
        "state": state,
        "pincode": pincode,
        "resume_path": resumePDF.filename
    }
    
    if obj.getDriveStatus(role) == True:
        id = fname.strip().lower().replace(" ", "_")+"@"+phone
        print(data)
        try:
            resume_url = upload_file_to_drive(resumePDF, id)
        except Exception as e:
            print(f"Error uploading file: {e}")
            resume_url = None
            return """
                <script>
                    alert("Failed to upload the resume. Please try again.");
                    window.location.href = "/";
                </script>
            """
        candidate_data = (
            id,
            fname,
            lname,
            phone,
            email,
            dob,
            address + ", " + city + ", " + state,
            pincode,
            gender,
            resume_url
        )
        if obj.insertCandidate(role, candidate_data):
            print(resume_url)
            return """
                <script>
                    alert("Form submitted successfully!");
                    window.location.href = "/";
                </script>
            """
        else:
            return """
                <script>
                    alert("Failed to submit the form. Please try again.");
                    window.location.href = "/";
                </script>
            """
    else:
        return """
            <script>
                alert("The drive for the selected role is currently closed. Please check back later.");
                window.location.href = "/";
            </script>
        """

if __name__ == "__main__":
    app.run(debug=True)