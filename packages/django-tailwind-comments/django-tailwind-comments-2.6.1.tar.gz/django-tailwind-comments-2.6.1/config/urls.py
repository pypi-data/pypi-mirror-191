import django_sql_dashboard
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('admin/', admin.site.urls),
]


def custom_error_403(request, exception):
    return render(request, '403.html', {'exception': exception})


handler403 = custom_error_403
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
