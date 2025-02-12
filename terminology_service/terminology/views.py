from datetime import date

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Refbook, RefbookVersion
from .serializers import RefbookElementSerializer, RefbookSerializer


class RefbookListView(APIView):
    @swagger_auto_schema(
        operation_description="Получение списка справочников, с фильтрацией по дате начала действия версий",
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Дата начала действия версии (формат ГГГГ-ММ-ДД)",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: RefbookSerializer(many=True)},
    )
    def get(self, request):
        date_param = request.query_params.get("date")
        if date_param:
            versions = RefbookVersion.objects.filter(start_date__lte=date_param)
        else:
            versions = RefbookVersion.objects.all()

        refbooks = list({version.refbook for version in versions})
        serializer = RefbookSerializer(refbooks, many=True)
        return Response({"refbooks": serializer.data})


class RefbookElementView(APIView):
    @swagger_auto_schema(
        operation_description="Получение элементов справочника по его ID и версии",
        manual_parameters=[
            openapi.Parameter("version", openapi.IN_QUERY, description="Версия справочника", type=openapi.TYPE_STRING)
        ],
        responses={200: RefbookElementSerializer(many=True)},
    )
    def get(self, request, id):
        refbook = get_object_or_404(Refbook, pk=id)
        version_param = request.query_params.get("version")

        if version_param:
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_param)
        else:
            version = refbook.versions.filter(start_date__lte=date.today()).order_by("-start_date").first()

        if version:
            elements = version.elements.all()
            serializer = RefbookElementSerializer(elements, many=True)
            return Response({"elements": serializer.data})
        else:
            return Response({"elements": []})


class CheckElementView(APIView):
    @swagger_auto_schema(
        operation_description="Валидация элемента справочника",
        manual_parameters=[
            openapi.Parameter("code", openapi.IN_QUERY, description="Код элемента", type=openapi.TYPE_STRING),
            openapi.Parameter("value", openapi.IN_QUERY, description="Значение элемента", type=openapi.TYPE_STRING),
            openapi.Parameter("version", openapi.IN_QUERY, description="Версия справочника", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description="Результат валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={"valid": openapi.Schema(type=openapi.TYPE_BOOLEAN)}
                ),
            )
        },
    )
    def get(self, request, id):
        code = request.query_params.get("code")
        value = request.query_params.get("value")
        version_param = request.query_params.get("version")

        refbook = get_object_or_404(Refbook, pk=id)
        if version_param:
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_param)
        else:
            version = refbook.versions.filter(start_date__lte=date.today()).order_by("-start_date").first()

        element = version.elements.filter(code=code, value=value).first() if version else None

        if element:
            return Response({"valid": True})
        return Response({"valid": False})
