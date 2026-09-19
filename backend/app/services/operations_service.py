from datetime import date, datetime
from decimal import Decimal

from ..extensions import db
from ..models import Customer, CustomerAssignment, EmployeeProfile, Task, TaskTransition, User


WORKFLOW = {
    "criado": {"em_analise"},
    "em_analise": {"em_andamento", "aguardando_cliente"},
    "em_andamento": {"aguardando_cliente", "concluido"},
    "aguardando_cliente": {"em_andamento", "concluido"},
    "concluido": set(),
}


def _date(value: str | None):
    return date.fromisoformat(value) if value else None


def customers():
    return Customer.query.order_by(Customer.legal_name).all()


def employees():
    return EmployeeProfile.query.join(User).order_by(User.name).all()


def team_users():
    return User.query.filter(User.role.in_({"admin", "colaborador"})).order_by(User.name).all()


def customer_users():
    return User.query.filter(User.role == "cliente").order_by(User.name).all()



def tasks():
    return Task.query.order_by(Task.created_at.desc()).all()


def tasks_by_visibility(user: User):
    """Retorna tarefas visíveis baseado na role do usuário"""
    query = Task.query.order_by(Task.created_at.desc())
    # Admins e gerentes veem todas as tarefas
    if user.role in {"admin", "gerente"}:
        return query.all()
    # Colaboradores comuns veem apenas tarefas públicas
    if user.role == "colaborador":
        query = query.filter(Task.is_private == False)
    return query.all()


def customer_by_id(customer_id: int):
    return db.session.get(Customer, customer_id)


def customer_assignments(customer_id: int | None = None, active_only: bool = False):
    query = CustomerAssignment.query.join(Customer).join(EmployeeProfile).order_by(CustomerAssignment.assigned_at.desc())
    if customer_id is not None:
        query = query.filter(CustomerAssignment.customer_id == customer_id)
    if active_only:
        query = query.filter(CustomerAssignment.ended_at.is_(None))
    return query.all()


def assignment_to_dict(assignment: CustomerAssignment) -> dict:
    return {
        "id": assignment.id,
        "customer_id": assignment.customer_id,
        "customer": assignment.customer.legal_name,
        "employee_id": assignment.employee_id,
        "employee": assignment.employee.user.name,
        "department": assignment.department,
        "assigned_at": assignment.assigned_at.isoformat(),
        "ended_at": assignment.ended_at.isoformat() if assignment.ended_at else None,
    }


def available_next_statuses(status: str) -> list[str]:
    return sorted(WORKFLOW.get(status, set()))


def create_customer(data):
    for field in ("legal_name", "tax_id", "person_type", "tax_regime"):
        if not str(data.get(field, "")).strip():
            raise ValueError(f"Campo obrigatório: {field}.")
    if Customer.query.filter_by(tax_id=data["tax_id"].strip()).first():
        raise ValueError("CNPJ/CPF já cadastrado.")
    customer = Customer(
        legal_name=data["legal_name"].strip(),
        trade_name=data.get("trade_name"),
        tax_id=data["tax_id"].strip(),
        person_type=data["person_type"],
        company_size=data.get("company_size"),
        tax_regime=data["tax_regime"],
        status=data.get("status", "ativo"),
        monthly_fee=Decimal(str(data["monthly_fee"])) if data.get("monthly_fee") else None,
        email=data.get("email"),
        phone=data.get("phone"),
        city=data.get("city"),
        state=data.get("state"),
        started_on=_date(data.get("started_on")),
        notes=data.get("notes"),
    )
    db.session.add(customer)
    db.session.commit()
    return customer


def create_employee(data):
    user = db.session.get(User, data.get("user_id"))
    if not user or user.role not in {"admin", "colaborador"}:
        raise ValueError("Selecione um usuário da equipe.")
    if EmployeeProfile.query.filter_by(user_id=user.id).first():
        raise ValueError("Usuário já possui perfil de colaborador.")
    if not data.get("department") or not data.get("job_title"):
        raise ValueError("Setor e cargo são obrigatórios.")
    employee = EmployeeProfile(
        user_id=user.id,
        department=data["department"],
        job_title=data["job_title"],
        crc_number=data.get("crc_number"),
        phone=data.get("phone"),
        hired_on=_date(data.get("hired_on")),
        employment_status=data.get("employment_status", "ativo"),
    )
    db.session.add(employee)
    db.session.commit()
    return employee


def assign_customer(customer_id, data, actor):
    customer = db.session.get(Customer, customer_id)
    employee = db.session.get(EmployeeProfile, data.get("employee_id"))
    if not customer or not employee or not data.get("department"):
        raise ValueError("Cliente, colaborador e setor são obrigatórios.")
    CustomerAssignment.query.filter_by(
        customer_id=customer.id,
        department=data["department"],
        ended_at=None,
    ).update({"ended_at": datetime.utcnow()})
    assignment = CustomerAssignment(
        customer_id=customer.id,
        employee_id=employee.id,
        department=data["department"],
        assigned_by_id=actor.id,
    )
    db.session.add(assignment)
    db.session.commit()
    return assignment


def create_task(data, actor):
    if not data.get("title") or not data.get("department"):
        raise ValueError("Título e setor são obrigatórios.")
    # Apenas admins e gerentes podem criar tarefas privadas
    is_private = False
    if actor.role in {"admin", "gerente"} and data.get("is_private", False):
        is_private = True
    task = Task(
        customer_id=data.get("customer_id") or None,
        department=data["department"],
        assignee_id=data.get("assignee_id") or None,
        title=data["title"].strip(),
        description=data.get("description"),
        priority=data.get("priority", "Média"),
        due_date=_date(data.get("due_date")),
        is_private=is_private,
        created_by_id=actor.id,
    )
    task.transitions.append(
        TaskTransition(
            previous_status=None,
            new_status="criado",
            changed_by_id=actor.id,
            note="Tarefa criada",
        )
    )
    db.session.add(task)
    db.session.commit()
    return task


def change_task(task_id, data, actor):
    task = db.session.get(Task, task_id)
    new_status = data.get("status")
    if not task:
        raise LookupError()
    if new_status not in WORKFLOW.get(task.status, set()):
        raise ValueError("Transição de workflow inválida.")
    old_status = task.status
    task.status = new_status
    if new_status == "concluido":
        task.completed_at = datetime.utcnow()
    task.transitions.append(
        TaskTransition(
            previous_status=old_status,
            new_status=new_status,
            changed_by_id=actor.id,
            note=data.get("note"),
        )
    )
    db.session.commit()
    return task
