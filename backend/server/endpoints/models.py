from django.db import models


class Endpoint(models.Model):
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MLAlgorithm(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    code = models.TextField()

    version = models.CharField(max_length=128)

    owner = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    parent_endpoint = models.ForeignKey(
        Endpoint,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class MLRequest(models.Model):
    input_data = models.TextField()

    full_response = models.TextField()

    response = models.TextField()

    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    parent_mlalgorithm = models.ForeignKey(
        MLAlgorithm,
        on_delete=models.CASCADE
    )