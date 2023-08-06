from distutils.util import strtobool
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


__all__ = [
    "AdminModeViewMixin",
    "OnlyInstanceViewMixin",
    "NearbyIdsViewMixin",
]


class AdminModeViewMixin:
    def _user_is_staff(self, user: settings.AUTH_USER_MODEL) -> bool:
        return user.is_staff

    @property
    def admin_mode(self) -> bool:
        """
        Включен режим администратора
        """
        if not getattr(self, "_admin_mode", None):
            return self._user_is_staff(user=self.request.user) and bool(
                strtobool(self.request.GET.get("admin_mode", "false"))
            )
        return self._admin_mode

    @admin_mode.setter
    def admin_mode(self, value: bool) -> None:
        """
        Установка значения для режима администрации
        """
        self._admin_mode = value

    @property
    def no_limit(self) -> bool:
        """
        Включён режим без ограничений
        """
        if not getattr(self, "_no_limit", None):
            self._no_limit = self.admin_mode and bool(
                strtobool(self.request.GET.get("no_limit", "false"))
            )
        return self._no_limit

    @no_limit.setter
    def no_limit(self, value) -> None:
        """
        Установка значения для режима без ограничений
        """
        self._no_limit = value

    def get_user(self):
        """
        Получение пользователя user.
        В режиме администрации можно указывать любого пользователя и действовать от его лица
        """
        if self.admin_mode:
            user_id = self.request.GET.get("user_id")
            if user_id:
                User = get_user_model()
                try:
                    return User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise ValidationError({"user_id": _("Пользователь не найден.")})

        user = self.request.user
        if isinstance(user, AnonymousUser):
            user = None

        return user


class OnlyInstanceViewMixin:
    """
    View-mixin для работы с единичными объектами (к пример у User лишь один объект настроек UserSettings)
    """

    def get_object(self):
        """
        Получение единственного объекта
        """
        return self.get_queryset().first()

    def list(self, request, *args, **kwargs):
        """
        Замена отдачи списка объектов на единичный объект
        """
        if getattr(self, "no_limit", False):
            return super().list(request, *args, **kwargs)

        instance = self.get_object()
        if instance:
            data = self.get_serializer(instance).data
        else:
            data = {}

        return self.build_response(data=data)

    @action(detail=False, methods=["PUT", "PATCH"])
    def alter(self, request, *args, **kwargs):
        """
        Обновление объекта
        """
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        retrieve_serializer = self.serializer_classes.get(
            "retrieve", self.serializer_classes.get("default", self.serializer_class)
        )
        return self.build_response(data=retrieve_serializer(instance=instance).data)


class NearbyIdsViewMixin:
    """
    View-mixin для получения соседних идентификаторов
    """

    @action(detail=True, methods=["GET"])
    def get_nearby_ids(self, request, *args, **kwargs):
        """
        Получение соседних идентификаторов относительно переданного объекта
        """
        if hasattr(self, "actions_for_filterset_class"):
            if self.actions_for_filterset_class != "__all__":
                self.actions_for_filterset_class += ["get_nearby_ids"]

        qs = self.filter_queryset(self.get_queryset())
        ids = list(qs.values_list(self.lookup_field, flat=True))
        obj_id = getattr(self.get_object(), self.lookup_field)
        obj_index = ids.index(obj_id)
        prev_id = ids[obj_index - 1] if (obj_index - 1 >= 0) else None
        next_id = ids[obj_index + 1] if (obj_index + 1 <= qs.count() - 1) else None

        return Response(
            {"prev_id": prev_id, "next_id": next_id}, status=status.HTTP_200_OK
        )
