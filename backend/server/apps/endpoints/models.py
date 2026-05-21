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


class MLAlgorithmStatus(models.Model):
    status = models.CharField(max_length=32)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_mlalgorithm = models.ForeignKey(
    MLAlgorithm,
    on_delete=models.CASCADE,
    related_name="status",
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.status


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

    def __str__(self):
        return str(self.created_at)


class ABTest(models.Model):
    '''
    The ABTest will keep information about A/B tests.

    Attributes:
        title: The title of test.
        created_by: The name of creator.
        created_at: The date of test creation.
        ended_at: The date of test stop.
        summary: The description with test summary, created at test stop.
        parent_mlalgorithm_1: The reference to the first MLAlgorithm.
        parent_mlalgorithm_2: The reference to the second MLAlgorithm.
    '''
    title = models.CharField(max_length=10000)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)

    parent_mlalgorithm_1 = models.ForeignKey(
        MLAlgorithm,
        on_delete=models.CASCADE,
        related_name="parent_mlalgorithm_1",
    )
    parent_mlalgorithm_2 = models.ForeignKey(
        MLAlgorithm,
        on_delete=models.CASCADE,
        related_name="parent_mlalgorithm_2",
    )

    def __str__(self):
        return self.title