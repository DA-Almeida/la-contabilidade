from flask import jsonify, request

from ..services.lead_service import create_lead, list_leads


def create_public_lead():
    try:
        lead = create_lead(request.get_json(silent=True) or {})
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(message="Mensagem recebida. Em breve entraremos em contato.", lead=lead.to_dict()), 201


def get_leads():
    return jsonify(leads=[lead.to_dict() for lead in list_leads()])
