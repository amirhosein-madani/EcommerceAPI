from django.views.generic import TemplateView, ListView, DeleteView
from .models import Product, ProductStatusType , Category

# Create your views here.


class ProductListView(ListView):
    template_name = "product/product-grid.html"
    queryset = Product.objects.filter(status=ProductStatusType.PUBLISH)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    