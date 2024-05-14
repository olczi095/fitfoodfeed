from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from . import settings

urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('', RedirectView.as_view(url='blog/')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('comments/', include('comments.urls', namespace='comments')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
