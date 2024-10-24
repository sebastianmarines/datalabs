from django.conf import settings
from django.db import models
from django.urls import reverse


class Dataset(models.Model):
    CATEGORY_CHOICES = [
        ("CV", "Computer Vision"),
        ("NLP", "Natural Language Processing"),
        ("TS", "Time Series"),
        ("STR", "Structured Data"),
        ("AUD", "Audio"),
        ("OTHER", "Other"),
    ]

    LICENSE_CHOICES = [
        ("CC0", "Creative Commons Zero"),
        ("CC-BY", "Creative Commons Attribution"),
        ("CC-BY-SA", "Creative Commons Attribution-ShareAlike"),
        ("CUSTOM", "Custom License"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    file_format = models.CharField(max_length=50)
    size_in_gb = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_records = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    license_type = models.CharField(max_length=10, choices=LICENSE_CHOICES)
    sample_data_url = models.URLField(blank=True)

    # Metadata
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("dataset_detail", kwargs={"pk": self.pk})
