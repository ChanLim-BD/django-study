from django.contrib import admin
from django.urls import path, include

"""
원래는 주석 처리된 상태로 진행해야 맞지만, 현재는 과제의 확인을 원할하게하기 위해서 현 상태로 저장합니다.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
]
