import json

from http import HTTPStatus
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from projectlyte.appointment import models, helpers
# Create your views here.

class HealthAPI(View):
    def get(self, request):
        return HttpResponse(status=200)


class AppointmentAPI(View):
    def get(self, request):
        appointments = models.Appointment.objects.all()
        return helpers.format_response_list_appointment(result=appointments)

   
    def post(self, request):
        try:
            # get body
            body = json.loads(request.body)

            # validate request
            try:
                helpers.validate_post(body)
            except Exception as e:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json format is incorrect")
            
            # check existing appointment
            appointment = models.Appointment.objects.filter(appointment_date = body["appointment_date"]).first()
            if appointment:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Appointment already existed")
            
            # create new data
            models.Appointment.objects.create(
                appointment_date = body["appointment_date"],
                info = body["info"]
            )

            return helpers.format_response(message="Appointment in "+body["appointment_date"]+" is created")
        except json.decoder.JSONDecodeError as e:
            return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json is not correct")
        except Exception as e:
            return helpers.format_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message=e)


    def put(self, request):
        try:
            # get body
            body = json.loads(request.body)

            # validate request
            try:
                helpers.validate_put(body)
            except Exception as e:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json format is incorrect")
            
            # check existing appointment
            current_appointment = models.Appointment.objects.filter(appointment_date = body["old_appointment_date"]).first()
            if current_appointment:
                new_appointment = models.Appointment.objects.filter(appointment_date = body["new_appointment_date"]).first()
                if new_appointment:
                    return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="This "+body["new_appointment_date"]+" is already used")
            else:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Appointment is not found")
            
            # update data data
            current_appointment.appointment_date = body["new_appointment_date"]
            if body["new_info"]:
                current_appointment.info = body["new_info"]
            current_appointment.save()

            return helpers.format_response(message="Appointment date "+body["old_appointment_date"]+" is changed to "+body["new_appointment_date"])
        except json.decoder.JSONDecodeError as e:
            return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json is not correct")
        except Exception as e:
            return helpers.format_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message=e)


    def delete(self, request):
        try:
            # get body
            body = json.loads(request.body)

            # validate request
            try:
                helpers.validate_delete(body)
            except Exception as e:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json format is incorrect")
            
            # check existing appointment
            appointment = models.Appointment.objects.filter(appointment_date = body["appointment_date"]).first()
            if not appointment:
                return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Appointment doesn't exist")
            
            # delete data data
            appointment.delete()

            return helpers.format_response(message="Appointment date "+body["appointment_date"]+" is deleted")
        except json.decoder.JSONDecodeError as e:
            return helpers.format_response(status_code=HTTPStatus.BAD_REQUEST, message="Json is not correct")
        except Exception as e:
            return helpers.format_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message=e)