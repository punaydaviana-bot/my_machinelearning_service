import inspect

from django.test import TestCase

from apps.ml.industry_classifier.random_forest import RandomForestClassifier
from apps.ml.registry import MLRegistry


class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            "year": 2024,
            "pandemic_exposure": 8.0,
            "geopolitical_exposure": 7.0,
            "natural_disaster_exposure": 6.0,
            "tariff_exposure": 8.5,
            "logistics_exposure": 9.0,
            "energy_exposure": 5.0,
            "labor_exposure": 6.5,
            "cyber_exposure": 7.2,
            "overall_vulnerability": 7.5,
            "inventory_days": 40,
            "supplier_concentration_hhi": 0.35,
            "just_in_time_dependency": 0.5,
            "nearshoring_score_2024": 0.4
        }
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"], response.get("message", "No message"))
        self.assertIn("label", response)

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)

        endpoint_name = "industry_classifier"
        algorithm_object = RandomForestClassifier()
        algorithm_name = "random forest"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Piotr"
        algorithm_description = "Random Forest with simple pre- and post-processing"
        algorithm_code = inspect.getsource(RandomForestClassifier)

        registry.add_algorithm(
            endpoint_name,
            algorithm_object,
            algorithm_name,
            algorithm_status,
            algorithm_version,
            algorithm_owner,
            algorithm_description,
            algorithm_code,
        )

        self.assertEqual(len(registry.endpoints), 1)