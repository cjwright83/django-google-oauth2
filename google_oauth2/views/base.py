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
    abort_url = None
    prompt = 'consent'
    redirect_path = None
    service_class = None
    scopes = None

    def get(self, request, *args, **kwargs):
        return self.start_auth()

    def start_auth(self):
        redirect_uri = self.request.build_absolute_uri(self.get_redirect_path())
        flow = get_flow(self.get_scopes(), redirect_uri=redirect_uri)
        authorization_url, state = flow.authorization_url(prompt=self.get_prompt())
        return HttpResponseRedirect(authorization_url)

    def get_abort_url(self):
        return self.abort_url

    def get_prompt(self):
        return self.prompt

    def get_redirect_path(self):
        return str(self.redirect_path)

    def get_service_class(self):
        return self.service_class

    def get_scopes(self):
        return self.scopes


class BaseCompleteAuthView(View):
    access_denied_url = None
    failure_url = None
    redirect_path = None
    scopes = None
    service_class = None
    success_url = None

    def get(self, request, *args, **kwargs):
        if 'error' not in request.GET and 'code' not in request.GET:
            return HttpResponseBadRequest('Request querystring must have code or error parameters.')
        if request.GET.get('error'):
            return self.access_denied(request.GET.get('error'))
        return self.access_granted(request.GET.get('code'))

    def access_denied(self, error):
        return HttpResponseRedirect(self.get_access_denied_url())

    def access_granted(self, code):
        return self.make_service_calls(self.get_auth_session(code))

    def get_auth_session(self, code):
        redirect_uri = self.request.build_absolute_uri(self.get_redirect_path())
        flow = get_flow(self.get_scopes(), redirect_uri=redirect_uri)
        flow.fetch_token(code=code)
        return flow.authorized_session()

    def make_service_calls(self, auth_session):
        service = self.get_service(auth_session)
        service.process_api_calls()
        if service.errors:
            return self.fail(service.errors)
        return self.success()

    def get_service(self, auth_session):
        return self.get_service_class()(auth_session, self.get_service_context())

    def get_service_context(self):
        return None

    def success(self):
        return HttpResponseRedirect(self.get_success_url())

    def fail(self, errors):
        return HttpResponseRedirect(self.get_failure_url())

    def get_access_denied_url(self):
        return self.access_denied_url

    def get_failure_url(self):
        return self.failure_url

    def get_redirect_path(self):
        return str(self.redirect_path)

    def get_scopes(self):
        return self.scopes

    def get_service_class(self):
        return self.service_class

    def get_success_url(self):
        return self.success_url
