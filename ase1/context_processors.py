from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from ase1.models import CreateAccountForm

def authentication_info(request):
    '''
    This context processor adds all the user info into the page that is needed for the
    login form and signup form that appear in the header of every page, as well as other
    basic information about the state of the current user.

    This way the code is DRY-er: we don't need to copy these fields into every page handler.
    '''
    return {
        'login_form': AuthenticationForm(),
        'signup_form': CreateAccountForm(),
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated(),
    }
