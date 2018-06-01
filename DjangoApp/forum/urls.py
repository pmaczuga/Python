from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('not_logged', views.not_logged, name = 'not_logged'),
    path('<int:category_id>/', views.category_view, name = 'category_view'),
    path('<int:category_id>/create_thread/', views.create_thread, name = 'create_thread'),
    path('<int:category_id>/<int:thread_id>/', views.thread_view, name = 'thread_view'),
    path('<int:category_id>/<int:thread_id>/create_answer/', views.create_answer, name = 'create_answer'),
]