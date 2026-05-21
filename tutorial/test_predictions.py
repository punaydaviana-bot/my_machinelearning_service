"""
Test predictions against the Student Performance API
"""
import urllib.request
import json

PORT = 8001
BASE = f"http://127.0.0.1:{PORT}/api/v1"

def post(url, data):
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode())

# ============================================================
print("=" * 60)
print("TEST 1: Predict a LOW-performing student")
print("=" * 60)
low_student = {
    "Hours_Studied": 8,
    "Attendance": 62,
    "Parental_Involvement": "Low",
    "Access_to_Resources": "Low",
    "Extracurricular_Activities": "No",
    "Sleep_Hours": 5,
    "Previous_Scores": 55,
    "Motivation_Level": "Low",
    "Internet_Access": "No",
    "Tutoring_Sessions": 0,
    "Family_Income": "Low",
    "Teacher_Quality": "Low",
    "School_Type": "Public",
    "Peer_Influence": "Negative",
    "Physical_Activity": 1,
    "Learning_Disabilities": "Yes",
    "Parental_Education_Level": "High School",
    "Distance_from_Home": "Far",
    "Gender": "Male"
}
r = post(f"{BASE}/income_classifier/predict", low_student)
print(json.dumps(r, indent=2))
print(f">> Label: {r['label']}, Probability of High: {r['probability']:.2f}")
print()

# ============================================================
print("=" * 60)
print("TEST 2: Predict a HIGH-performing student")
print("=" * 60)
high_student = {
    "Hours_Studied": 35,
    "Attendance": 98,
    "Parental_Involvement": "High",
    "Access_to_Resources": "High",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 95,
    "Motivation_Level": "High",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 3,
    "Family_Income": "High",
    "Teacher_Quality": "High",
    "School_Type": "Private",
    "Peer_Influence": "Positive",
    "Physical_Activity": 4,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "Postgraduate",
    "Distance_from_Home": "Near",
    "Gender": "Female"
}
r = post(f"{BASE}/income_classifier/predict", high_student)
print(json.dumps(r, indent=2))
print(f">> Label: {r['label']}, Probability of High: {r['probability']:.2f}")
print()

# ============================================================
print("=" * 60)
print("TEST 3: Predict a MEDIUM student (using Extra Trees - testing)")
print("=" * 60)
medium_student = {
    "Hours_Studied": 20,
    "Attendance": 85,
    "Parental_Involvement": "Medium",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 75,
    "Motivation_Level": "Medium",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 2,
    "Family_Income": "Medium",
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male"
}
r = post(f"{BASE}/income_classifier/predict?status=testing", medium_student)
print(json.dumps(r, indent=2))
print(f">> Label: {r['label']}, Probability of High: {r['probability']:.2f}")
print()

# ============================================================
print("=" * 60)
print("ALL 3 PREDICTIONS COMPLETED SUCCESSFULLY!")
print("=" * 60)
