from flask import Blueprint

from ..controllers.operations_controller import (
    change_task_status,
    create_customer_assignment,
    create_new_customer,
    create_new_employee,
    create_new_task,
    get_customer_assignments,
    get_customer_users,
    get_customers,
    get_employees,
    get_tasks,
    get_team_users,
)
from ..services.auth_service import require_auth


operations_bp = Blueprint("operations", __name__, url_prefix="/api/operations")
operations_bp.get("/customers")(require_auth("admin", "colaborador")(get_customers))
operations_bp.post("/customers")(require_auth("admin", "colaborador")(create_new_customer))
operations_bp.get("/employees")(require_auth("admin", "colaborador")(get_employees))
operations_bp.post("/employees")(require_auth("admin", "colaborador")(create_new_employee))
operations_bp.get("/team-users")(require_auth("admin", "colaborador")(get_team_users))
operations_bp.get("/customer-users")(require_auth("admin", "colaborador")(get_customer_users))
operations_bp.get("/tasks")(require_auth("admin", "colaborador")(get_tasks))
operations_bp.post("/tasks")(require_auth("admin", "colaborador")(create_new_task))
operations_bp.patch("/tasks/<int:task_id>/status")(require_auth("admin", "colaborador")(change_task_status))
operations_bp.get("/assignments")(require_auth("admin", "colaborador")(get_customer_assignments))
operations_bp.post("/customers/<int:customer_id>/assignments")(require_auth("admin", "colaborador")(create_customer_assignment))