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
    send_mail('Letter with password reset code!', f"Your reset code {code}", 'asdq2780@gmail.com', [email, ],
              fail_silently=False)


def send_notification(user_email, order_id, price):
    send_mail(
        'Уведомление о создании заказа!',
        f"""Вы создали заказ №{order_id}, \n полная стоимость вашего заказа: {price}. 
        \nСпасибо за то что выбрали нас!""",
        'from@example.com',
        [user_email],
        fail_silently=False
    )


def send_recommendation(user_email, order, *args):
    send_mail(
        'Рекомендация для покупок!',
        f'Вы сделали заказ товары: {[i["product"].title for i in order].replace("[", "").replace("]", "")}'
        f' в количестве: {[i["quantity"] for i in order]}, мы также рекомендуем вам эти: {[i.title for i in args[0]]} '
        f'товары из данных категорий с наивысшим рейтингом!;)',
        'finally@done.com',
        [user_email],
        fail_silently=False
    )
