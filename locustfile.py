from locust import HttpUser, task, between
import random


class LoadTestUser(HttpUser):
    wait_time = between(1, 3)
    # host = "http://your-api-url.com"  # Базовый URL API
    host = "http://localhost:8000"  # Адрес mock-сервера
    def on_start(self):
        self.auth_token = None
        self.cart_id = None  # Инициализация cart_id

        # Авторизация
        username = f"user{self.environment.runner.user_count}"
        password = f"password{self.environment.runner.user_count}"
        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            self.auth_token = response.json().get("token")
        else:
            self.environment.runner.quit()

    @task(3)
    def get_products(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        self.client.get("/api/products", headers=headers)

    @task(2)
    def add_to_cart(self):
        product_id = random.randint(1, 100)
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.client.post("/api/cart/add", json={
            "product_id": product_id
        }, headers=headers)

        # Сохраняем cart_id только при успешном ответе
        if response.status_code == 200:
            self.cart_id = response.json().get("cart_id")
        else:
            self.cart_id = None  # Сброс при ошибке

    @task(1)
    def create_order(self):
        if not self.cart_id:
            self.environment.events.request.fire(
                request_type="POST",
                name="/api/order/create",
                response_time=0,
                response_length=0,
                exception=Exception("Cart ID is missing"),
            )
            return  # Прерываем выполнение

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        self.client.post("/api/order/create", json={
            "cart_id": self.cart_id
        }, headers=headers)