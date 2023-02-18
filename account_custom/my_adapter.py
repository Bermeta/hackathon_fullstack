from allauth.account.adapter import DefaultAccountAdapter
from main.tasks import send_confirm_email_task


class CustomAccountAdapter(DefaultAccountAdapter):

    def pre_login(
        self,
        request,
        user,
        *,
        email_verification,
        signal_kwargs,
        email,
        signup,
        redirect_url
    ):
        if not user.is_active:
            user.create_activation_code()
            user.save()
            send_confirm_email_task.delay(user.email, user.activation_code)
            return self.respond_user_inactive(request, user)

