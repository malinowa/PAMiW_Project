from django.urls import path

from . import views

app_name = 'appointments-service'

urlpatterns = [
    path('', views.main_menu, name='main-menu'),
    path('register/', views.registration_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    #path('appointments-create-view/', views.AppointmentCreateView.as_view(), name='appointments-create-view'),
    path('appointments-list-view/', views.AppointmentsListView.as_view(), name='appointments-list-view'),
    path('appointments-detail-view/<pk>', views.AppointmentsDetailView.as_view(), name='appointments-detail-view'),
    path('appointments-delete-view/<pk>', views.AppointmentsDeleteView.as_view(), name='appointments-delete-view'),
    path('hospital-select-view/', views.HospitalSelectView.as_view(), name='hospital-select-view'),
    path('doctor-select-view/<pk>', views.DoctorSelectView.as_view(), name='doctor-select-view'),
    path('appointment-date-select-view/<pk>', views.AppointmentDateSelectView.as_view(), name='appointment-date-select-view'),
]