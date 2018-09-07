from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View

from google_auth_oauthlib.flow import Flow


def get_flow(scopes, **kwargs):
    return Flow.from_client_secrets_file(
        client_secrets_file=settings.GOOGLE_CLIENT_SECRETS_FILE_PATH,
        scopes=scopes,
        **kwargs
    )


class BaseBeginAuthView(View):
    noauth_required = False
    abort_url = None
    prompt = 'consent'
    scopes = ()
    redirect_path = None

    def get(self, request, *args, **kwargs):
        if self.noauth_required:
            if hasattr(self.request, 'user') and self.request.user.is_anonymous():
                return self.start_auth()
        return HttpResponseRedirect(self.get_abort_url())

    def start_auth(self):
        redirect_uri = self.request.build_absolute_uri(self.get_redirect_path())
        flow = get_flow(self.get_scopes(), redirect_uri=redirect_uri)
        authorization_url, state = flow.authorization_url(prompt=self.get_prompt())
        return HttpResponseRedirect(authorization_url)

    def get_abort_url(self):
        return self.abort_url

    def get_redirect_path(self):
        return str(self.redirect_path)

    def get_scopes(self):
        return self.scopes

    def get_prompt(self):
        return self.prompt


class BaseCompleteAuthView(View):
    service_url = None
    success_url = None
    failure_url = None
    access_denied_url = None
    redirect_path = None
    scopes = ()

    def get(self, request, *args, **kwargs):
        if 'error' not in request.GET and 'code' not in request.GET:
            return HttpResponseBadRequest('Request querystring must have code or error parameters.')
        if request.GET.get('error'):
            return self.access_denied(request.GET.get('error'))
        return self.access_granted(request.GET.get('code'))

    def access_denied(self, error):
        return HttpResponseRedirect(self.get_access_denied_url(error))

    def access_granted(self, code):
        redirect_uri = self.request.build_absolute_uri(self.get_redirect_path())
        flow = get_flow(self.get_scopes(), redirect_uri=redirect_uri)
        flow.fetch_token(code=code)
        auth_session = flow.authorized_session()
        response = auth_session.get(self.get_service_url()).json()
        if self.process_service_response(response):
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(self.get_failure_url())

    def process_service_response(self, response):
        return None

    def get_scopes(self):
        return self.scopes

    def get_service_url(self):
        return self.service_url

    def get_success_url(self):
        return self.success_url

    def get_failure_url(self):
        return self.failure_url

    def get_access_denied_url(self, error):
        return self.access_denied_url

    def get_redirect_path(self):
        return str(self.redirect_path)
