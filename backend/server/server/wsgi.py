import inspect
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()

# ─── ML Registry ──────────────────────────────────────────────────────────────
from apps.ml.registry import MLRegistry
from apps.ml.industry_classifier.random_forest import RandomForestClassifier
from apps.ml.industry_classifier.extra_trees import ExtraTreesClassifier

try:
    registry = MLRegistry()

    # Random Forest — production
    rf = RandomForestClassifier()
    registry.add_algorithm(
        endpoint_name="industry_classifier",
        algorithm_object=rf,
        algorithm_name="random forest",
        algorithm_status="production",
        algorithm_version="0.0.1",
        owner="Piotr",
        algorithm_description="Random Forest with simple pre- and post-processing",
        algorithm_code=inspect.getsource(RandomForestClassifier),
    )

    # Extra Trees — testing (used in A/B testing)
    et = ExtraTreesClassifier()
    registry.add_algorithm(
        endpoint_name="industry_classifier",
        algorithm_object=et,
        algorithm_name="extra trees",
        algorithm_status="testing",
        algorithm_version="0.0.1",
        owner="Piotr",
        algorithm_description="Extra Trees with simple pre- and post-processing",
        algorithm_code=inspect.getsource(ExtraTreesClassifier),
    )

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))