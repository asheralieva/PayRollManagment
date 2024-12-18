from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from api.models import Company, Day, RegistrationRequest, Payment, Worker, Administrator, LeaveRequest
from .serializers import (CompanySerializer, DaySerializer, RegistrationRequestSerializer,
                          PaymentSerializer, WorkerSerializer, AdministratorSerializer, LeaveRequestSerializer)

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DayViewSet(ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class RegistrationRequestViewSet(ModelViewSet):
    queryset = RegistrationRequest.objects.all()
    serializer_class = RegistrationRequestSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            worker = self.get_object()
            worker.delete()
            return Response(
                {"message": f"Сотрудник {worker.name} {worker.surname} успешно удален."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Worker.DoesNotExist:
            return Response(
                {"error": "Сотрудник не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
class AdministratorViewSet(ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

class LeaveRequestViewSet(ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    @action(detail=True, methods=['post'])
    def approve_or_reject(self, request, pk=None):
        try:
            leave_request = self.get_object()  # Получаем объект LeaveRequest
            action_type = request.data.get('action')  # Тип действия: 'approve' или 'reject'

            if action_type not in ['approve', 'reject']:
                return Response(
                    {"error": "Некорректное действие. Используйте 'approve' или 'reject'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Меняем статус в зависимости от действия
            leave_request.status = 'approved' if action_type == 'approve' else 'rejected'
            leave_request.save()

            return Response(
                {"message": f"Запрос успешно {'одобрен' if action_type == 'approve' else 'отклонен'}."},
                status=status.HTTP_200_OK
            )

        except LeaveRequest.DoesNotExist:
            return Response(
                {"error": "Запрос не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )