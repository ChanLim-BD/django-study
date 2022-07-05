from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django_pydenticon.views import image as pydenticon_image


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),
    path('', login_required(TemplateView.as_view(template_name='root.html')), name='root'), # re_path는 모든 주소에 맵핑된다. (정규표현식이라서)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

