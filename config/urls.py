from django.contrib import admin
from django.urls import path, include
from app import views as app_views
from app.views import SearchFormView
from user import views as user_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("Search/", SearchFormView.as_view(), name="search"),
    path('database/', include('app.urls')),
    path('', app_views.index, name="top-page"),
    path('login/', user_views.Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', user_views.AccountRegistration.as_view(), name="registration"),
    path('Settings/', user_views.Settings, name="Settings"),
    path('Settings/ProfileChange/', user_views.ProfileChangeView.as_view(), name="ProfileChange"),
    path('Profile/<str>/', user_views.Profile, name="Profile"),
    path('Settings/Username/', user_views.UsernameChangeView.as_view(), name="Username"),
    path('Settings/Email/', user_views.EmailChangeView.as_view(), name="Email"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
