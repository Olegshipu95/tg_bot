from yoomoney import Client, Quickpay
from config_reader import config
from datetime import datetime, timedelta


client = Client(config.yoomoney_token.get_secret_value())


def generate_yoomoney_link(amount, username):
    quickpay = Quickpay(
        receiver=client.account_info().account,
        quickpay_form="shop",
        targets="Оплата посещения на спикинг клуб",
        paymentType="SB",
        sum=amount,
        label=username,
        successURL="http://site.ru"
    )
    return quickpay.base_url


def check_payment_status(username):
    history = client.operation_history(label=username)
    now = datetime.now()

    for operation in history.operations:
        if operation.label == username and operation.status == "success":
            operation_time = operation.datetime.replace(tzinfo=None)
            if now - operation_time < timedelta(days=1):
                return True
    return False
