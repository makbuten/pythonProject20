from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredVievMixin(LoginRequiredMixin):
    login_url = 'login/'
    redirect_field_name = 'next/'