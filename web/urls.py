
from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("addform/", views.addform, name="addform"),
    path("profile/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("favourite/", views.favourite, name="favourite"),
    path('property/<int:id>/', views.propertydetail, name='property_detail'), 
    path('my-properties/', views.user_properties, name='user_properties'),
    path('mark_active/<int:id>/', views.mark_active, name='mark_active'),
    path('favorat/<int:id>/', views.favorat, name='favorat'),
    path('delete_property/<int:id>/', views.delete_property, name='delete_property'),

]