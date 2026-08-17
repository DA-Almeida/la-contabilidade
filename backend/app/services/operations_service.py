from datetime import date, datetime
from decimal import Decimal
from ..extensions import db
from ..models import Customer, CustomerAssignment, EmployeeProfile, Task, TaskTransition, User

WORKFLOW = {"criado":{"em_analise"},"em_analise":{"em_andamento","aguardando_cliente"},"em_andamento":{"aguardando_cliente","concluido"},"aguardando_cliente":{"em_andamento","concluido"},"concluido":set()}
def _date(v): return date.fromisoformat(v) if v else None
def customers(): return Customer.query.order_by(Customer.legal_name).all()
def employees(): return EmployeeProfile.query.join(User).order_by(User.name).all()
def create_customer(d):
    for f in ('legal_name','tax_id','person_type','tax_regime'):
        if not str(d.get(f,'')).strip(): raise ValueError(f'Campo obrigatório: {f}.')
    if Customer.query.filter_by(tax_id=d['tax_id'].strip()).first(): raise ValueError('CNPJ/CPF já cadastrado.')
    c=Customer(legal_name=d['legal_name'].strip(),trade_name=d.get('trade_name'),tax_id=d['tax_id'].strip(),person_type=d['person_type'],company_size=d.get('company_size'),tax_regime=d['tax_regime'],status=d.get('status','ativo'),monthly_fee=Decimal(str(d['monthly_fee'])) if d.get('monthly_fee') else None,email=d.get('email'),phone=d.get('phone'),city=d.get('city'),state=d.get('state'),started_on=_date(d.get('started_on')),notes=d.get('notes'))
    db.session.add(c);db.session.commit();return c
def create_employee(d):
    user=db.session.get(User,d.get('user_id'))
    if not user or user.role not in {'admin','colaborador'}: raise ValueError('Selecione um usuário da equipe.')
    if EmployeeProfile.query.filter_by(user_id=user.id).first(): raise ValueError('Usuário já possui perfil de colaborador.')
    if not d.get('department') or not d.get('job_title'): raise ValueError('Setor e cargo são obrigatórios.')
    e=EmployeeProfile(user_id=user.id,department=d['department'],job_title=d['job_title'],crc_number=d.get('crc_number'),phone=d.get('phone'),hired_on=_date(d.get('hired_on')),employment_status=d.get('employment_status','ativo'));db.session.add(e);db.session.commit();return e
def assign_customer(customer_id,d,actor):
    c=db.session.get(Customer,customer_id);e=db.session.get(EmployeeProfile,d.get('employee_id'))
    if not c or not e or not d.get('department'): raise ValueError('Cliente, colaborador e setor são obrigatórios.')
    CustomerAssignment.query.filter_by(customer_id=c.id,department=d['department'],ended_at=None).update({'ended_at':datetime.utcnow()})
    a=CustomerAssignment(customer_id=c.id,employee_id=e.id,department=d['department'],assigned_by_id=actor.id);db.session.add(a);db.session.commit();return a
def create_task(d,actor):
    if not d.get('title') or not d.get('department'): raise ValueError('Título e setor são obrigatórios.')
    t=Task(customer_id=d.get('customer_id') or None,department=d['department'],assignee_id=d.get('assignee_id') or None,title=d['title'].strip(),description=d.get('description'),priority=d.get('priority','Média'),due_date=_date(d.get('due_date')),created_by_id=actor.id)
    t.transitions.append(TaskTransition(previous_status=None,new_status='criado',changed_by_id=actor.id,note='Tarefa criada'));db.session.add(t);db.session.commit();return t
def change_task(task_id,d,actor):
    t=db.session.get(Task,task_id);new=d.get('status')
    if not t: raise LookupError()
    if new not in WORKFLOW.get(t.status,set()): raise ValueError('Transição de workflow inválida.')
    old=t.status;t.status=new
    if new=='concluido':t.completed_at=datetime.utcnow()
    t.transitions.append(TaskTransition(previous_status=old,new_status=new,changed_by_id=actor.id,note=d.get('note')));db.session.commit();return t
