from django.shortcuts import redirect


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')

            user_role = str(request.user.role).lower()

            allowed_roles_lower = [
                role.lower() for role in allowed_roles
            ]

            if user_role in allowed_roles_lower:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return redirect('/login/')

        return wrapper
    return decorator