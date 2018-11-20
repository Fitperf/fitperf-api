from rest_framework import permissions

class IsFounderOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow founders of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):

        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the founder of the object
        return obj.founder == request.user

class IsExerciseDefaultOrIsAdminOrFounder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Read-only permissions for default exercise
        if request.method in permissions.SAFE_METHODS and obj.is_default:
            return True

        # Has all permissions only for admin or founder
        return obj.founder == request.user or request.user.is_staff

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users
        return request.user.is_staff == True

class IsAdminOrFounder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Has all permissions only for admin or founder
        return obj.founder == request.user or request.user.is_staff

class IsAdminOrFounderOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.founder == request.user or request.user.is_staff