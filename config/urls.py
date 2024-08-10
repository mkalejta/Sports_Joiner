"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.models import Profile, Event, Facility, Sport
from app import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Facility)
admin.site.register(Sport)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/sign_up/', views.SignUpView, name='sign_up'),
    path("", TemplateView.as_view(template_name="home.html"), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user_dashboard/<int:pk>', views.user_dashboard, name='user_dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('events/', views.events_list, name='events_list'),
    path('create_event/', views.create_event, name='create_event'),
    path('event_details/<int:pk>', views.event_details, name='event_details'),
    path('join/<int:event_id>/', views.join_event, name='join_event'),
    path('my_events/<int:pk>', views.my_events, name='my_events'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('leave_event/<int:event_id>', views.leave_event, name='leave_event')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
