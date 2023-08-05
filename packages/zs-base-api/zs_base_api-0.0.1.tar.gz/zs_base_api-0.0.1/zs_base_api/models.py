from model_utils.models import TimeStampedModel, UUIDModel
from rest_framework import status

from django.db import models

from zs_utils.json_utils import CustomJSONEncoder
from zs_base_api import constants


__all__ = [
    "AbstractAPIRequestLog",
]


class AbstractAPIRequestLog(TimeStampedModel, UUIDModel):
    """
    Хранение запросов к внешним сервисам
    """

    # Данные запроса
    url = models.TextField(verbose_name="URL запроса")
    method = models.CharField(
        choices=constants.HTTP_METHODS, max_length=6, verbose_name="Метод запроса"
    )
    params = models.JSONField(
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
        verbose_name="Параметры URL",
    )
    request_headers = models.JSONField(
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
        verbose_name="Хедеры запроса",
    )
    request_body = models.JSONField(
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
        verbose_name="Тело запроса",
    )

    # Данные ответа
    response_time = models.IntegerField(verbose_name="Время ответа (миллисекунда)")
    status_code = models.IntegerField(verbose_name="Код ответа")
    response_headers = models.JSONField(
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
        verbose_name="Хедеры ответа",
    )
    response_body = models.JSONField(
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
        verbose_name="Тело ответа",
    )

    @property
    def is_success(self) -> bool:
        return status.is_success(code=self.status_code)

    class Meta:
        abstract = True
