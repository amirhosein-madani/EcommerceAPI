from django.views.generic import TemplateView , ListView , DeleteView
from .models import Product , ProductStatusType
# Create your views here.


class ProductListView(ListView):
    template_name = "product/product-grid.html"
    queryset = Product.objects.filter(status=ProductStatusType.PUBLISH)
    paginate_by = 10