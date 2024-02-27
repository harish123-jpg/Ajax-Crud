from django.urls import path
from .views import *

urlpatterns = [

    path('login/', login_view, name='login'),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path("delete/<int:id>", delete, name='delete'),
    path('@<username>/', profile, name="profile"),
]
