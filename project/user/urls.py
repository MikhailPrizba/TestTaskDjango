from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AddCustomerView,
    AddEmployeeView,
    ProfileViewSet,
    ListEmployeeViewSet,
    ListCustomerViewSet,
)

router = DefaultRouter()
router.register(r"add-customer", AddCustomerView, basename="add-customer")
router.register(r"add-employee", AddEmployeeView, basename="add-employee")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"list-employees", ListEmployeeViewSet, basename="list-employees")
router.register(r"list-customers", ListCustomerViewSet, basename="list-customers")

urlpatterns = [
    path("", include(router.urls)),
]
