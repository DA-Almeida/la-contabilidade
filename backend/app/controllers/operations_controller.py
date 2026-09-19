from flask import g, jsonify, request

from ..services.operations_service import (
    assignment_to_dict,
    available_next_statuses,
    assign_customer,
    customer_users,
    customer_assignments,
    customer_by_id,
    create_customer,
    create_employee,
    create_task,
    change_task,
    customers,
    employees,
    tasks,
    tasks_by_visibility,
    team_users,
)



def get_customers():
    return jsonify(customers=[item.to_dict() for item in customers()])


def create_new_customer():
    try:
        customer = create_customer(request.get_json(silent=True) or {})
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(customer=customer.to_dict()), 201


def get_employees():
    return jsonify(employees=[item.to_dict() for item in employees()])


def create_new_employee():
    try:
        employee = create_employee(request.get_json(silent=True) or {})
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(employee=employee.to_dict()), 201


def get_team_users():
    return jsonify(users=[user.to_dict() for user in team_users()])


def get_customer_users():
    return jsonify(users=[user.to_dict() for user in customer_users()])


def get_tasks():
    rows = []
    # Usar tasks_by_visibility para respeitar permissões
    for task in tasks_by_visibility(g.current_user):
        task_data = task.to_dict()
        task_data["next_statuses"] = available_next_statuses(task.status)
        rows.append(task_data)
    return jsonify(tasks=rows)



def create_new_task():
    try:
        task = create_task(request.get_json(silent=True) or {}, g.current_user)
    except ValueError as error:
        return jsonify(error=str(error)), 400
    task_data = task.to_dict()
    task_data["next_statuses"] = available_next_statuses(task.status)
    return jsonify(task=task_data), 201


def change_task_status(task_id: int):
    try:
        task = change_task(task_id, request.get_json(silent=True) or {}, g.current_user)
    except LookupError:
        return jsonify(error="Tarefa não encontrada."), 404
    except ValueError as error:
        return jsonify(error=str(error)), 400
    task_data = task.to_dict()
    task_data["next_statuses"] = available_next_statuses(task.status)
    return jsonify(task=task_data)


def get_customer_assignments():
    customer_id = request.args.get("customer_id", type=int)
    active_only = request.args.get("active_only", "false").lower() in {"1", "true", "yes"}
    if customer_id is not None and customer_by_id(customer_id) is None:
        return jsonify(error="Cliente não encontrado."), 404
    rows = [assignment_to_dict(item) for item in customer_assignments(customer_id=customer_id, active_only=active_only)]
    return jsonify(assignments=rows)


def create_customer_assignment(customer_id: int):
    try:
        assignment = assign_customer(customer_id, request.get_json(silent=True) or {}, g.current_user)
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(assignment=assignment_to_dict(assignment)), 201