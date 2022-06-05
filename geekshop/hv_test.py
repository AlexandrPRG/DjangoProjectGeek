from locust import HttpUser, TaskSet, task


def index(l):
    l.client.get("/")


def products(l):
    l.client.get('/products/')


def login(l):
    l.client.post("/auth/loginl/", {"username": "avadmin", "password": 1})


def logout(l):
    l.client.post("/auth/logout/", {"username": "avadmin", "password": 1})


@task
class UserBehavior(TaskSet):
    tasks = {index: 2, products: 5}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


@task
class WebSiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
