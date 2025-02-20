import os
import sys

STRUCTURE = {
    "api": ["serializers.py", "viewsets.py"],
    "managers": ["manager.py"],
    "": ["signals.py", "filters.py",]
}

TEMPLATES = {
    "api/serializers.py": """from rest_framework import serializers

from apps.{app_name}.models import {app_class}


class {app_class}Serializer(serializers.ModelSerializer):

    # user_id = serializers.PrimaryKeyRelatedField(
    #    queryset=User.objects.all(), source='user',
    # )

    class Meta:
        model = {app_class}
        fields = (
            'id',
            '',
            '',
            '',
            '',
        )
""",

    "api/viewsets.py": """from django_filters.rest_framework import DjangoFilterBackend # noqa501
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.{app_name}.api.serializers import {app_class}Serializer
from apps.{app_name}.filters import {app_class}Filter
from apps.{app_name}.models import {app_class}


class {app_class}View(viewsets.ModelViewSet):
    serializer_class = {app_class}Serializer
    queryset = {app_class}.objects.all()
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = {app_class}Filter
    search_fields = ['name', 'description']
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # queryset = queryset.filter(active=True)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # noqa501

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) # noqa501
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # noqa501

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
""",

    "managers/manager.py": """# from apps.{app_name}.models import {app_class} # noqa501


class {app_class}Manager:

    def __init__(self):
        pass

    def create_{app_name}(self, data, {app_name}_id, ):
        pass

    def update_{app_name}(self, data, {app_name}_id, ):
        pass

    def show_{app_name}(self, {app_name}_id, ):
        pass

    def list_{app_name}(self, ):
        pass

    def delete_{app_name}(self, {app_name}_id, ):
        pass
""",

    "filters.py": """import django_filters

from apps.{app_name}.models import {app_class}


class {app_class}Filter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains") # noqa501
    min_value = django_filters.NumberFilter(field_name="value", lookup_expr="gte") # noqa501
    max_value = django_filters.NumberFilter(field_name="value", lookup_expr="lte") # noqa501

    class Meta:
        model = {app_class}
        fields = ['category_name', 'max_value', 'min_value']
""",

    "signals.py": """from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.{app_name}.models import {app_class}


@receiver(post_save, sender={app_class})
def signals_{app_name}(sender, instance, created, **kwargs):
    if created:
        print('{app_class} criado')
""",
}


def create_app_structure(app_name):
    base_path = os.path.join("apps", app_name)
    app_class = app_name.capitalize()

    for folder, files in STRUCTURE.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file.format(app_name=app_name)) # noqa501
            print(file_path)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    content = TEMPLATES.get(os.path.join(folder, file.format(app_name=app_name)), "").format(app_name=app_name, app_class=app_class) # noqa501
                    f.write(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_app.py <nome_do_app>")
    else:
        create_app_structure(sys.argv[1])
        print(f"Estrutura para o app '{sys.argv[1]}' criada com sucesso!")
