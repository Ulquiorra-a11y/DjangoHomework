from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class IsCustomerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, object):
        if request.method in SAFE_METHODS:
            return True
        return object.owner == request.user

class CanViewStatistics(BasePermission):
    def has_permission(self,request,view):
        return request.user.has_perm('store.can_view_statistics')

class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s', ],
    }