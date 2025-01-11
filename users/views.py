from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserDetailSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    """Просмотр профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()


class PaymentsViewSet(viewsets.ModelViewSet):
    """Просмотр платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_method", "course_paid", "lesson_paid")
    ordering_fields = ("payment_date",)


class UserViewSet(viewsets.ModelViewSet):
    """Просмотр пользователя"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment_amount = payment.payment_amount
        product = {
            "Paid Course": payment.course_paid,
        }
        price = create_stripe_price(payment_amount, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()
