from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext_lazy, ugettext as _

from django.contrib.auth import get_user_model

ERROR_MESSAGE = ugettext_lazy("Please enter the correct username and password "
                              "for a staff account. Note that both fields are case-sensitive.")


class AdminAuthenticationForm(AuthenticationForm):
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("用户名或密码错误")})
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
        if username and password:
            self.user_cache = authenticate(
                username=username, password=password)
            if self.user_cache is None:
                if u'@' in username:
                    User = get_user_model()
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        return self.cleaned_data
