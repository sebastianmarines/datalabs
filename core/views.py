from django.shortcuts import render
from django.views.generic import TemplateView

from dataset.models import Dataset


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_datasets"] = Dataset.objects.all()[:3]
        return context
