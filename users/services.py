import stripe
from django_celery_beat.models import PeriodicTask

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course_paid):
    """Создает продукт в Stripe"""

    product = stripe.Product.create(name=course_paid.name)
    return product


def create_stripe_price(amount, course_paid):
    """Создает цену в Stripe"""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product_data={"name": course_paid.get("Paid Course")},
    )
    return price


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe"""

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
    )
    return session.get("id"), session.get("url")
