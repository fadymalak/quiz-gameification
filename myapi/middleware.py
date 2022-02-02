import telegram_send
from django.http import Http404
import traceback
import sys
from django.views.debug import ExceptionReporter , technical_500_response
from myapi.utils import TelegramExceptionReporter
from myapi.views.tasks import telegram_send_report

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_exception(self,request,exception):
        x = TelegramExceptionReporter(request , sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
        telegram_send_report.apply_async((x.get_traceback_text(),),countdown=10)
        # trace_back = traceback.format_exc().split("File")
        # telegram_send.send(
            # messages=[
                # "url : "+request.path + "\n" +
                # "user : " + str(request.user) + "\n" +
                # "method : " +request.method + "\n" +
                # "data : " + str(request.data if request.method=="POST" else "") + " \n" +
                # "exception : " + " \n" +
                # str(str(exception.__class__) + "\n args : " + str(exception.args)) + "\n" + 
                # str(traceback.format_exc(-2)) 
                #  ])
        return None
