from celery import Celery


def make_celery(app_name=__name__):
    return Celery(
        app_name,
        broker="amqp://admin:mypass@rabbitmq:5672",
        backend="amqp://admin:mypass@rabbitmq:5672",
    )


celery = make_celery()
