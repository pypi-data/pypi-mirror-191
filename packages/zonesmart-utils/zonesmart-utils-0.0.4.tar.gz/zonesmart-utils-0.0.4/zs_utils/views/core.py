from distutils.util import strtobool
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, ValidationError

from django.conf import settings
from django.http import QueryDict
from django.utils.translation import gettext as _

from zs_utils.permissions import UserHasAccess
from zs_utils.views import mixins


__all__ = [
    "CustomModelViewSet",
]


class CustomModelViewSet(mixins.AdminModeViewMixin, viewsets.ModelViewSet):
    lookup_field = "id"
    default_permission = UserHasAccess
    ignore_has_access = False
    allow_partial_update = True

    not_allowed_actions = []
    extra_allowed_actions = []

    required_filters = []
    actions_for_filterset_class = [
        "list",
        "retrieve",
    ]

    serializer_classes = {}
    serializer_class = None
    light_serializer_class = None
    verbose_serializer_class = None

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if (self.action in self.not_allowed_actions) and (
            self.action not in self.extra_allowed_actions
        ):
            return self.http_method_not_allowed(request, *args, **kwargs)

        return request

    def get_permissions(self):
        """
        Проверка прав пользователя
        """
        return super().get_permissions() + [self.default_permission()]

    def get_exception_handler_context(self) -> dict:
        """
        Формирование данных для контекста ошибки.
        """

        context = super().get_exception_handler_context()

        context["user"] = self.get_user()

        return context

    def _get_param_to_bool(self, name: str, default: str = "false"):
        return bool(strtobool(self.request.GET.get(name, default)))

    def get_serializer_class(self):
        """
        Получение класса сериализтора
        """
        # Поддержка облегченных сериализаторов
        if getattr(self, "light_serializer_class", None) and self._get_param_to_bool(
            "light"
        ):
            return self.light_serializer_class

        # Поддержка подробных сериализаторов
        if getattr(self, "verbose_serializer_class", None) and self._get_param_to_bool(
            "verbose"
        ):
            return self.verbose_serializer_class

        # Маппинг между экшенами и сериализаторами
        return self.serializer_classes.get(
            self.action, self.serializer_classes.get("default", self.serializer_class)
        )

    def get_serializer(self, *args, **kwargs):
        """
        Получение сериализтора
        """
        # Если данные передаются на прямую из request.data, то это объект QueryDict, он не изменяем, нужно копировать
        if ("data" in kwargs) and isinstance(kwargs["data"], QueryDict):
            kwargs["data"] = kwargs["data"].copy()

        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        return serializer_class(*args, **kwargs)

    def validate_filters(self) -> None:
        """
        Валидация фильтров запросов
        """
        for key in self.required_filters:
            if not self.request.GET.get(key):
                raise ValidationError({key: _("Обязательный фильтр")})

        if self.request.GET.get("limit") and (
            int(self.request.GET["limit"]) > settings.DRF_LIMIT_FILTER_MAX_VALUE
        ):
            raise ValidationError(
                {
                    "limit": _("Максимальное значение: {max_value}").format(
                        max_value=settings.DRF_LIMIT_FILTER_MAX_VALUE
                    )
                }
            )

    def limit_queryset(self, queryset):
        """
        Валидация фильтров при получении списка объектов
        """
        if self.action == "list":
            self.validate_filters()

        return queryset.filter(**self.get_queryset_filter_kwargs())

    def get_queryset(self, manager: str = "objects"):
        """
        Получение Queryset
        """
        if getattr(self, "filterset_class", None) and hasattr(
            self.filterset_class, "Meta"
        ):
            model = self.filterset_class.Meta.model
        else:
            model = self.get_serializer_class().Meta.model

        queryset = getattr(model, manager).all()

        if (self.actions_for_filterset_class == "__all__") or (
            self.action in self.actions_for_filterset_class
        ):
            queryset = self.filter_queryset(queryset=queryset)

        if not self.no_limit:
            # Обязательная фильтрация результатов для рядовых пользователей
            queryset = self.limit_queryset(queryset=queryset)

        return queryset

    def validate_data(
        self,
        *,
        serializer_class,
        many: bool = False,
        partial: bool = False,
        data: dict = None,
        location: str = None,
        raise_exception: bool = True,
        **kwargs,
    ):
        """
        Валидация данных по переданному сериализатору
        """
        if not data:
            if location:
                if location == "query":
                    data = self.request.GET.dict()
                elif location == "body":
                    data = self.request.data
                else:
                    raise ValueError("Допустимые значения 'location': 'query', 'body'.")
            else:
                if getattr(self, "action", None) in [
                    "create",
                    "update",
                    "list",
                    "get",
                    "destroy",
                ]:
                    if self.action.lower() in ["create", "update"]:
                        data = self.request.data
                    else:
                        data = self.request.GET.dict()
                else:
                    methods = getattr(self, "action_map", {}).keys()
                    if (
                        ("post" in methods)
                        or ("put" in methods)
                        or ("patch" in methods)
                    ):
                        data = self.request.data
                    else:
                        data = self.request.GET.dict()

        serializer = serializer_class(data=data, many=many, partial=partial)
        if serializer.is_valid(raise_exception=raise_exception):
            return serializer

    def get_validated_data(
        self,
        *,
        serializer_class,
        many: bool = False,
        partial: bool = False,
        data: dict = None,
        location: str = None,
        raise_exception: bool = True,
        **kwargs,
    ):
        """
        Получение провалидированных данных по переданному сериализатору
        """
        serializer = self.validate_data(
            serializer_class=serializer_class,
            many=many,
            partial=partial,
            data=data,
            location=location,
            raise_exception=raise_exception,
            **kwargs,
        )
        if serializer:
            return serializer.validated_data

    def build_response(
        self,
        message: str = None,
        data: dict = None,
        status_code: int = status.HTTP_200_OK,
        **kwargs,
    ) -> Response:
        """
        Создать ответ с переданным сообщением или данными. (Положительный по умолчанию)
        """

        if not data:
            if message:
                data = {"message": message}
        elif message:
            if isinstance(data, dict):
                data = {"message": message, **data}
            else:
                data = {"message": message, "data": data}

        return Response(data=data, status=status_code)

    def build_error_response(self, message: str = None, data: dict = None, **kwargs):
        """
        Создать ответ с ошибкой с переданным сообщением или данными
        """
        return self.build_response(
            message=message,
            data=data,
            status_code=status.HTTP_400_BAD_REQUEST,
            **kwargs,
        )

    @action(detail=False, methods=["GET"])
    def count(self, request, *args, **kwargs):
        """
        Получение кол-во объектов
        """
        return self.build_response(data={"count": self.get_queryset().count()})

    def partial_update(self, request, *args, **kwargs):
        """
        Запрет на частичное обновление
        """
        if not getattr(self, "allow_partial_update", True):
            raise MethodNotAllowed(self)
        return super().partial_update(request, *args, **kwargs)
