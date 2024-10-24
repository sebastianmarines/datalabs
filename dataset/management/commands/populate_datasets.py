# datasets/management/commands/populate_datasets.py
import os
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from dataset.models import Dataset

User = get_user_model()


class Command(BaseCommand):
    help = "Populates the database with sample datasets"

    def add_arguments(self, parser):
        parser.add_argument(
            "--datasets", type=int, default=20, help="The number of datasets to create"
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate database...")

        # Sample Mexican names
        USERS_DATA = [
            {
                "username": "admin",
                "email": "admin@datalabs.com",
                "first_name": "Miguel",
                "last_name": "Ángel Ramírez",
                "is_superuser": True,
                "is_staff": True,
                "password": "admin123",
            },
            {
                "username": "user0",
                "email": "alejandra@datalabs.com",
                "first_name": "Alejandra",
                "last_name": "González Hernández",
                "password": "user123",
            },
            {
                "username": "user1",
                "email": "carlos@datalabs.com",
                "first_name": "Carlos Eduardo",
                "last_name": "López Mendoza",
                "password": "user123",
            },
            {
                "username": "user2",
                "email": "fernanda@datalabs.com",
                "first_name": "Fernanda",
                "last_name": "Torres Jiménez",
                "password": "user123",
            },
        ]

        # Create users
        users = []
        for user_data in USERS_DATA:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                email=user_data["email"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "is_superuser": user_data.get("is_superuser", False),
                    "is_staff": user_data.get("is_staff", False),
                },
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {user.get_full_name()} ({user.username})"
                    )
                )
            users.append(user)

        # Sample data
        TITLES_BY_CATEGORY = {
            "CV": [
                "Large-scale Object Detection Dataset",
                "Facial Recognition Training Set",
                "Medical Imaging Collection",
                "Autonomous Vehicle Scene Dataset",
                "Retail Product Images Database",
                "Satellite Imagery Collection",
                "Human Pose Estimation Dataset",
                "Document OCR Training Set",
            ],
            "NLP": [
                "Multilingual News Corpus",
                "Social Media Sentiment Dataset",
                "Medical Reports Collection",
                "Legal Documents Database",
                "Customer Reviews Dataset",
                "Academic Papers Corpus",
                "Conversational AI Training Set",
                "Technical Documentation Dataset",
            ],
            "TS": [
                "Stock Market Historical Data",
                "IoT Sensor Readings",
                "Weather Patterns Collection",
                "Energy Consumption Dataset",
                "Network Traffic Logs",
                "User Behavior Time Series",
                "Healthcare Monitoring Data",
                "Manufacturing Metrics Dataset",
            ],
            "STR": [
                "E-commerce Transactions Database",
                "Customer Demographics Dataset",
                "Product Catalog Database",
                "Healthcare Records Collection",
                "Real Estate Listings Dataset",
                "Financial Transactions Log",
                "HR Analytics Database",
                "Education Metrics Dataset",
            ],
            "AUD": [
                "Speech Recognition Corpus",
                "Music Genre Classification Set",
                "Environmental Sounds Collection",
                "Voice Command Dataset",
                "Acoustic Event Detection",
                "Multilingual Speech Database",
                "Audio Emotion Recognition Set",
                "Podcast Transcription Dataset",
            ],
        }

        DESCRIPTIONS = {
            "CV": "A comprehensive computer vision dataset featuring {records} high-quality images across multiple categories. "
            "Each image is professionally labeled with bounding boxes and segmentation masks. "
            "Perfect for training object detection and image classification models. "
            "Includes detailed annotations in COCO format and preprocessing scripts.",
            "NLP": "An extensive natural language processing dataset containing {records} text samples. "
            "Includes sentiment analysis, named entity recognition, and part-of-speech tags. "
            "Multi-language support covering English, Spanish, and Mandarin. "
            "Cleaned and preprocessed for immediate use in NLP tasks.",
            "TS": "Time series dataset spanning {years} years with {records} data points. "
            "Includes both raw and preprocessed data with various statistical features. "
            "Suitable for forecasting, anomaly detection, and pattern recognition tasks. "
            "Comes with comprehensive documentation and example analysis notebooks.",
            "STR": "Structured dataset containing {records} records with {fields} fields per record. "
            "Clean, normalized, and ready for analysis. "
            "Includes both categorical and numerical features with detailed data dictionary. "
            "Perfect for machine learning model training and statistical analysis.",
            "AUD": "High-quality audio dataset featuring {records} samples at {khz}kHz. "
            "Includes various acoustic environments and speaker demographics. "
            "Professionally labeled with transcriptions and metadata. "
            "Ideal for speech recognition and audio processing tasks.",
        }

        FILE_FORMATS = {
            "CV": ["JPEG", "PNG", "COCO JSON", "TFRecord"],
            "NLP": ["CSV", "JSON", "TXT", "JSONL"],
            "TS": ["CSV", "Parquet", "HDF5", "JSON"],
            "STR": ["CSV", "Parquet", "SQL Dump", "JSON"],
            "AUD": ["WAV", "MP3", "FLAC", "OGG"],
        }

        # Create datasets
        num_datasets = options["datasets"]

        for _ in range(num_datasets):
            # Random category
            category = random.choice(list(TITLES_BY_CATEGORY.keys()))

            # Random values for description placeholders
            records = random.randint(10000, 1000000)
            years = random.randint(1, 10)
            fields = random.randint(10, 100)
            khz = random.choice([8, 16, 44, 48, 96])

            # Create description with placeholders filled
            description = DESCRIPTIONS[category].format(
                records=f"{records:,}", years=years, fields=fields, khz=khz
            )

            # Create dataset
            try:
                dataset = Dataset.objects.create(
                    title=random.choice(TITLES_BY_CATEGORY[category]),
                    description=description,
                    category=category,
                    file_format=random.choice(FILE_FORMATS[category]),
                    size_in_gb=round(random.uniform(0.1, 500.0), 2),
                    number_of_records=records,
                    price=round(random.uniform(49.99, 999.99), 2),
                    license_type=random.choice(["CC0", "CC-BY", "CC-BY-SA", "CUSTOM"]),
                    sample_data_url=f"https://example.com/samples/dataset_{random.randint(1000, 9999)}",
                    creator=random.choice(users),
                    is_verified=random.choice([True, False]),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 365)),
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created dataset: {dataset.title}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating dataset: {str(e)}"))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {num_datasets} datasets")
        )
