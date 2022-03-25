from django.template.defaultfilters import pprint
from typing import Any, Dict
from django.views.debug import ExceptionReporter
from pkg_resources import safe_extra
from django.template import Context , Engine
from django.utils.version import get_version
from django.utils import timezone
import time
from myapi.models import User
from myapi.constants import TEMPLATE
Engine = Engine(debug=False,libraries={'i18n': 'django.templatetags.i18n'},)

def check_unique(prop,value,model=User):
    param = {prop:value}
    count = model.objects.filter(**param).count()
    return count == 0

class TelegramExceptionReporter(ExceptionReporter):
    def get_traceback_data(self) -> Dict[str, Any]:
        frames = self.get_traceback_frames()
        for i, frame in enumerate(frames):
            # if 'vars' in frame:
                # frame_vars = []
                # for k, v in frame['vars']:
                    # v = pprint(v)
                    # Trim large blobs of data
                    # if len(v) > 4096:
                        # v = '%s… <trimmed %d bytes string>' % (v[0:4096], len(v))
                    # frame_vars.append((k, v))
                # print(frame_vars)
                # frame['vars'] = frame_vars
            frame['filename'] = "\\".join(frame['filename'].split("\\")[-3:])
            frames[i] = frame

        
        c = {
            'request': self.request,
            'request_meta': self.filter.get_safe_request_meta(self.request),
            'user_str': self.request.user,
            'cookies':self.request.COOKIES.items(),
            'frames': frames[-2:],
            'postmortem':self.postmortem,
            'exception_type':self.exc_type.__name__,
            'exception_value' :str(self.exc_value),
            'url':self.request.path,
            'django_version_info':get_version(),
            "server_time":timezone.now(),
        }
        if self.request.method == "GET":
            c['data'] = self.request.GET.items()
        elif self.request.method == "POST":
            c['data'] = self.request.POST.items()


        return c
    def get_traceback_text(self) -> safe_extra:
        x = Engine.from_string(TEMPLATE)
        c = Context(self.get_traceback_data(),autoescape=False,use_l10n=False)
        return x.render(c)