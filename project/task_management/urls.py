from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskRetrieveUpdateViewSet,
    TaskCreateByCustomerViewSet,
    TaskCreateByEmployeeViewSet,
    TaskEmployeeActionsViewSet,
)

router = DefaultRouter()
router.register(r"", TaskRetrieveUpdateViewSet, basename="task")
router.register(
    r"customer/create-task",
    TaskCreateByCustomerViewSet,
    basename="customer-create-task",
)
router.register(
    r"employee/create-task",
    TaskCreateByEmployeeViewSet,
    basename="employee-create-task",
)
router.register(
    r"employee-actions", TaskEmployeeActionsViewSet, basename="employee-actions"
)

urlpatterns = [
    path("", include(router.urls)),
]
