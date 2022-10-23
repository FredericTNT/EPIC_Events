from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.mixins import LoginRequiredMixin


class IsClientSalesContact(LoginRequiredMixin, BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user.is_superuser or
                    not obj.sales_contact or obj.sales_contact == request.user)
