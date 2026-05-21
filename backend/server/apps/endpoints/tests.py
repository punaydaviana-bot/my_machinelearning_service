from django.test import TestCase
from rest_framework.test import APIClient


class EndpointTests(TestCase):
    def test_predict_view(self):
        client = APIClient()
        input_data = {
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
            "Gender": "Male",
        }
        classifier_url = "/api/v1/income_classifier/predict"
        response = client.post(classifier_url, input_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Low")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)