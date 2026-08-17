from flask import g, jsonify, request

from ..services.fiscal_service import create_guide, create_obligation, list_guides, list_obligations


def get_guides(): return jsonify(guides=[guide.to_dict() for guide in list_guides(g.current_user)])
def get_obligations(): return jsonify(obligations=[item.to_dict() for item in list_obligations(g.current_user)])

def create_new_guide():
    try: guide = create_guide(request.get_json(silent=True) or {})
    except ValueError as error: return jsonify(error=str(error)), 400
    return jsonify(guide=guide.to_dict()), 201

def create_new_obligation():
    try: obligation = create_obligation(request.get_json(silent=True) or {})
    except ValueError as error: return jsonify(error=str(error)), 400
    return jsonify(obligation=obligation.to_dict()), 201
