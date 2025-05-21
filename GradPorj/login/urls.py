from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name = 'index'),
    path('upload',views.upload_file, name = 'upload_file'),
    path('track',views.track, name = 'track'),
    path('Req', views.Req, name ="Req"),
    path('login', views.login, name ="login"),
    path('logout', views.logout, name = "logout"),
    path('stddash', views.stddash, name= "stddash"),
    path('staffdash', views.staffdash, name= "staffdash"),
    path('secdash', views.secdash, name= "secdash"),
    path('staffupload', views.staffupload, name = "staffupload"),
    #path('stafftrack', views.stafftrack, name= "stafftrack"),
    #path('studenttrack', views.studenttrack, name = "studenttrack"),
    path('download/<int:file_id>/', views.download_file, name = 'download_file'),
    #path('tracking_complete', views.tracking_complete, name = 'tracking_complete'),
    path('popup', views.popup, name = 'popup'),
    path('staff_tracking', views.staff_tracking, name = 'staff_tracking'),
    path('staff_tracking_complete/<str:pk>', views.staff_tracking_complete, name= 'staff_tracking_complete'),
    path('student_tracking', views.student_tracking, name = 'student_tracking'),
    path('student_tracking_complete', views.student_tracking_complete, name= 'student_tracking_complete'),
    path('files/', views.file_list, name='file_list'),
    #path("tracking_complete", views.tracking_complete, name= 'tracking_complete'),
    path("tracking_complete/<str:pk>", views.tracking_complete, name= 'tracking_complete'),
    path("authenticatie/<str:pk>", views.authenticatie, name = "authenticatie"),
    path("authenticatie_staff/<str:pk>", views.authenticatie_staff, name = "authenticatie_staff")
   # path("tracking/<str:pk>", views.tracking, name= 'tracking')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)