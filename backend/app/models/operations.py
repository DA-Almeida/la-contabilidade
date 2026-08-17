from datetime import datetime

from ..extensions import db


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True, index=True)
    legal_name = db.Column(db.String(180), nullable=False, index=True)
    trade_name = db.Column(db.String(180))
    tax_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    person_type = db.Column(db.String(10), nullable=False)
    company_size = db.Column(db.String(20))
    tax_regime = db.Column(db.String(40), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="ativo", index=True)
    monthly_fee = db.Column(db.Numeric(12, 2))
    email = db.Column(db.String(255), index=True)
    phone = db.Column(db.String(30))
    city = db.Column(db.String(120)); state = db.Column(db.String(2), index=True)
    started_on = db.Column(db.Date); notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])
    def to_dict(self): return {"id":self.id,"user_id":self.user_id,"legal_name":self.legal_name,"trade_name":self.trade_name,"tax_id":self.tax_id,"person_type":self.person_type,"company_size":self.company_size,"tax_regime":self.tax_regime,"status":self.status,"monthly_fee":float(self.monthly_fee or 0),"email":self.email,"phone":self.phone,"city":self.city,"state":self.state,"started_on":self.started_on.isoformat() if self.started_on else None,"notes":self.notes}


class EmployeeProfile(db.Model):
    __tablename__ = "employee_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False, index=True)
    department = db.Column(db.String(60), nullable=False, index=True)
    job_title = db.Column(db.String(100), nullable=False)
    crc_number = db.Column(db.String(30), index=True)
    phone = db.Column(db.String(30)); hired_on = db.Column(db.Date)
    employment_status = db.Column(db.String(30), nullable=False, default="ativo", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])
    def to_dict(self): return {"id":self.id,"user_id":self.user_id,"name":self.user.name,"email":self.user.email,"department":self.department,"job_title":self.job_title,"crc_number":self.crc_number,"phone":self.phone,"hired_on":self.hired_on.isoformat() if self.hired_on else None,"employment_status":self.employment_status,"role":self.user.role}


class CustomerAssignment(db.Model):
    __tablename__ = "customer_assignments"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False, index=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee_profiles.id"), nullable=False, index=True)
    department = db.Column(db.String(60), nullable=False, index=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, index=True)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    customer = db.relationship("Customer"); employee = db.relationship("EmployeeProfile")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), index=True)
    department = db.Column(db.String(60), nullable=False, index=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey("employee_profiles.id"), index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False, default="Média", index=True)
    status = db.Column(db.String(30), nullable=False, default="criado", index=True)
    due_date = db.Column(db.Date, index=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = db.Column(db.DateTime, index=True)
    customer = db.relationship("Customer"); assignee = db.relationship("EmployeeProfile")
    transitions = db.relationship("TaskTransition", back_populates="task", cascade="all, delete-orphan", order_by="TaskTransition.created_at")
    def to_dict(self): return {"id":self.id,"customer_id":self.customer_id,"customer":self.customer.legal_name if self.customer else None,"department":self.department,"assignee_id":self.assignee_id,"assignee":self.assignee.user.name if self.assignee else None,"title":self.title,"description":self.description,"priority":self.priority,"status":self.status,"due_date":self.due_date.isoformat() if self.due_date else None,"created_at":self.created_at.isoformat(),"completed_at":self.completed_at.isoformat() if self.completed_at else None}


class TaskTransition(db.Model):
    __tablename__ = "task_transitions"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False, index=True)
    previous_status = db.Column(db.String(30)); new_status = db.Column(db.String(30), nullable=False, index=True)
    changed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    note = db.Column(db.Text); created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    task = db.relationship("Task", back_populates="transitions")
