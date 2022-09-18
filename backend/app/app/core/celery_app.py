from celery import Celery

app = Celery('tasks', backend='redis://redis:6379/0', broker="amqp://guest@queue//")

app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
app.conf.task_routes = {"app.worker.add": "main-queue"}
app.conf.task_routes = {"app.worker.compress_db": "main-queue"}


