from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return wrapper

    return decorator