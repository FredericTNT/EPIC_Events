from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsClientSalesContact(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Vérifier si l'utilisateur est authentifié et pour les méthodes autres que SAFE_METHODS (GET, HEAD, OPTIONS)
        si l'utilisateur est administrateur ou le contact commercial du client
        """
        if (request.method in SAFE_METHODS) or request.user.is_superuser:
            return request.user.is_authenticated
        return (obj.sales_contact == request.user) and request.user.is_authenticated

