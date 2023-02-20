from .celery import app
from account_custom.send_email import send_reset_email, send_confirmation_email, send_notification


@app.task
def send_confirm_email_task(user, code):
    send_confirmation_email(user=user, code=code)


@app.task
def send_notification_task(user_email, order_id, price):
    send_notification(user_email, order_id, price)
