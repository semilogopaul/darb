from rest_framework.permissions import BasePermission

class IsAccountApproved(BasePermission):
    message = 'Your account is not approved by the admin.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_accessible()
