from django.urls import path, include

urlpatterns = [
    path('', include('core.account.urls')),
    path('blog/', include('core.blog.urls')),
]
