import json

from jsonschema import validate
from django.http import HttpResponse

def format_response(message, status_code=200, values=[]):
    response = HttpResponse(
        json.dumps({
            'success': (str(status_code)[0] == "2"),  # when code is 2XX
            'message': message,
            'data': values,
        }),
        content_type='application/json',
        status=status_code
    )
    return response


def format_response_list_appointment(result):
    message = "List of Appointment"
    values = [
        {
            "appointment_date": i.appointment_date.strftime('%Y-%m-%d'),
            "info": i.info,
        } for i in result
    ]
    return format_response(message=message, values=values)


def validate_post(request):
    schema = {
        "type": "object",
        "properties": {
            "appointment_date": {"type": "string"},
            "info": {"type": "string"}
        },
        "required": ["appointment_date", "info"],
        "additionalProperties": False
    }
    validate(instance=request, schema=schema)


def validate_put(request):
    schema = {
        "type": "object",
        "properties": {
            "old_appointment_date": {"type": "string"},
            "new_appointment_date": {"type": "string"},
            "new_info": {"type": "string"}
        },
        "required": ["old_appointment_date", "new_appointment_date", "new_info"],
        "additionalProperties": False
    }
    validate(instance=request, schema=schema)


def validate_delete(request):
    schema = {
        "type": "object",
        "properties": {
            "appointment_date": {"type": "string"}
        },
        "required": ["appointment_date"],
        "additionalProperties": False
    }
    validate(instance=request, schema=schema)