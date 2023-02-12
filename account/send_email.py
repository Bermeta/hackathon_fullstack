from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте активируйте свой аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по  ссылке: \n{full_link}',
        'fromexample@gmail.com',
        [user],
        fail_silently=False
    )


def send_reset_email(user):
    code = user.activation_code
    email = user.email
    send_mail('Letter with password reset code!', f"Your reset code {code}", 'bermetzarlyk@gmail.com', [email, ],
              fail_silently=False)


def send_notification(user_email, order_id, price):
    send_mail(
        'uvedomlenie o sozdanii zakaza!',
        f"""vi sozdaly zakaz №{order_id}, \n polnaya stoimost' vashego zakaza: {price}. \nsposibo za to chto vibraly nas!""",
        'from@example.com',
        [user_email],
        fail_silently=False
    )