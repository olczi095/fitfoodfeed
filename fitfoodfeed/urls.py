from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from . import settings

urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('', RedirectView.as_view(url='reviews/')),
    path('reviews/', include('reviews.urls')),
    path('accounts/', include('accounts.urls'), name='accounts')
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
