from django.urls import path

from apps.views.admin import AdminFormView
from apps.views.application import ApplicationListView, ApplicationFilterView, stream_video, VideoCreateView, \
    CategoryCreate, CategoryListView, delete_video
from apps.views.employee import EmployeeCreateView, EmployeeListView, delete_employee, EmployeeCreateFormView, \
    delete_category

urlpatterns = [
    path('', AdminFormView.as_view(), name='admin'),
    path('application-type', ApplicationListView.as_view(), name='application-list'),
    path('application-filter', ApplicationFilterView.as_view(), name='application-filter'),
    path('employee-create', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee-list', EmployeeListView.as_view(), name='employee-list'),
    path('delete-employee/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),

    path('employee-login', EmployeeCreateFormView.as_view(), name='employee-login'),

    path('stream/<int:video_id>/', stream_video, name='video_stream'),
    path('video-create', VideoCreateView.as_view(), name='video-create'),
    path('category-create', CategoryCreate.as_view(), name='category-create'),
    path('category-list', CategoryListView.as_view(), name='category-list'),

    path("delete-video/<int:video_id>/", delete_video, name="delete-video"),

]
