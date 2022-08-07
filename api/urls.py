from django.urls import path, include
from api.views import EmployeeViewSet, LoginView, ChangePasswordView, ProfileView, ManagerView, DepartmentViewSet, \
    LeaveViewSet, KPIViewSet, RequestedKPIViewSet, RequestedLeaveViewSet, ForgotPasswordView,SubmitKPIView, GetDataZK
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('employees', EmployeeViewSet, basename='employee_api')
router.register('departments', DepartmentViewSet, basename='department_api')
router.register('leaves', LeaveViewSet, basename='leave_api')
router.register('kpi', KPIViewSet, basename='kpi_api')
router.register('requested_kpi', RequestedKPIViewSet, basename='requested_kpi')
router.register('requested_leaves', RequestedLeaveViewSet, basename='requested_leave')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('manager', ManagerView.as_view()),
    path('forgot_password', ForgotPasswordView.as_view()),
    path('submit_kpi',SubmitKPIView.as_view()),
    path('zksync',GetDataZK.as_view()),

]
