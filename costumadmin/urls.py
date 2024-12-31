from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from costumadmin import views  # Ensure the module name is correct and matches your Django app's name
from costumadmin.views import add_writing_task

urlpatterns = [
                  path('units/', views.units_view, name='units'),
                  path('add-unit/', views.add_unit, name='add_unit'),  # add_unit funksiyasini aniqlash
                  path('delete-unit/<int:unit_id>/', views.delete_unit, name='delete_unit'),
                  path('edit-unit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
                  path('books/', views.units_view, name='books'),
                  path('vocab/', views.units_view, name='vocab'),
                  path('tests/', views.units_view, name='tests'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
                   path('', views.admin_main_view, name='admin-main'),

               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
                   path('writing1/', views.writing1_view, name='task1'),
                   path('writing2/', views.writing2_view, name='task2'),
                   path('add_writing_task/', add_writing_task, name='add_writing_task'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
