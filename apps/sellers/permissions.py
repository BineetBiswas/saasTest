from rest_framework.permissions import BasePermission



class CompanyPermission(BasePermission):

    message = "You do not have permission to access this object"

    def has_object_permission(self, request, view, obj):
        return obj.company == request.user.company
        