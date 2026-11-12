from .models import Employee
from .services import worker

SESSION_KEY = "persona"


class CurrentEmployeeMiddleware:
    """Sets `request.employee` from the session.

    In the demo there is no login: a role switcher stores the chosen employee's
    directory ID in the session. With the Bitrix24 or own login switched on, the
    same attribute is filled from the authenticated user (next stage).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        worker.ensure_started()
        external_id = request.session.get(SESSION_KEY)
        request.employee = None
        if external_id:
            request.employee = (
                Employee.objects.select_related("department").filter(external_id=external_id, is_active=True).first()
            )
        return self.get_response(request)
