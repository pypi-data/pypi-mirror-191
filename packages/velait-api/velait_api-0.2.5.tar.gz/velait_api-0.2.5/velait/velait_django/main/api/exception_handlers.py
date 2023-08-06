from rest_framework.views import exception_handler

from velait.common.exceptions import VelaitError
from velait.velait_django.main.api.responses import APIResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    no_response = response is None

    if no_response:
        response = APIResponse(data=None, status=400)

    if not no_response and isinstance(response.data, dict):
        errors = [
            VelaitError(name=error_name, description=error_description)
            for error_name, error_description in response.data.items()
        ]
    elif no_response:
        errors = [
            VelaitError(
                name=getattr(exc, 'name', "Unknown error"),
                description=getattr(exc, 'description', "Unknown error"),
            )
        ]
    else:
        errors = response.data

    return APIResponse(
        data=None,
        status=response.status_code,
        template_name=response.template_name,
        headers=response.headers,
        exception=response.exception,
        content_type=response.content_type,
        errors=errors,
    )
