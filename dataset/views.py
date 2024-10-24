from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Dataset
from .forms import DatasetForm

class DatasetListView(ListView):
    model = Dataset
    template_name = 'datasets/dataset_list.html'
    context_object_name = 'datasets'
    paginate_by = 9

    def get_queryset(self):
        queryset = Dataset.objects.filter(is_active=True)
        
        # Handle search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
            
        # Handle category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Dataset.CATEGORY_CHOICES
        return context

class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = 'dataset/dataset_form.html'
    success_url = reverse_lazy('dataset_list')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class DatasetDetailView(DetailView):
    model = Dataset
    template_name = 'dataset/dataset_detail.html'
    context_object_name = 'dataset'