from django.views.generic import TemplateView
from django.shortcuts import render

class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_datasets'] = [
            {
                'title': 'Image Classification Dataset',
                'description': 'Over 1M labeled images across 100 categories',
                'price': '$999',
            },
            {
                'title': 'NLP Training Corpus',
                'description': 'Multilingual text data for language models',
                'price': '$1,499',
            },
            {
                'title': 'Time Series Financial Data',
                'description': 'Historical market data with clean annotations',
                'price': '$2,999',
            },
        ]
        return context