from django.shortcuts import redirect


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            # Check login first
            if not request.user.is_authenticated:
                return redirect('/login/')

            user_role = str(
                request.user.role
            ).lower()

            # Admin has universal access
            if user_role == 'admin':
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            allowed_roles_lower = [
                role.lower()
                for role in allowed_roles
            ]

            # Normal role check
            if user_role in allowed_roles_lower:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            # Unauthorized users
            return redirect('/login/')

        return wrapper

    return decorator