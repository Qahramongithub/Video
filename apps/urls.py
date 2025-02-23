from django.urls import path

from apps.views.admin import AdminFormView
from apps.views.application import ApplicationListView, ApplicationFilterView, stream_video, VideoCreateView
from apps.views.employee import EmployeeCreateView, EmployeeListView, delete_employee, EmployeeCreateFormView

urlpatterns = [
    path('login', AdminFormView.as_view(), name='admin'),
    path('application-type', ApplicationListView.as_view(), name='application-list'),
    path('application-filter', ApplicationFilterView.as_view(), name='application-filter'),
    path('employee-create', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee-list', EmployeeListView.as_view(), name='employee-list'),
    path('delete-employee/<int:employee_id>/', delete_employee, name='delete_employee'),

    path('employee-login', EmployeeCreateFormView.as_view(), name='employee-login'),

    path('stream/<int:video_id>/', stream_video, name='video_stream'),
    path('video-create', VideoCreateView.as_view(), name='video-create'),

]
