import os
import sys


def create_admin_structure(app_name):
    admin_path = os.path.join("apps", app_name, "admin.py")
    model_name = app_name.capitalize()

    content = f"""from django.contrib import admin
from apps.{app_name}.models import {model_name}


@admin.action(description='Teste action')
def test_action(modeladmin, request, queryset):
    for instance in queryset:
        print(instance)


# class TestInline(admin.TabularInline):
#     model = Test
#     extra = 0
#     fields = (
#         'id', 'user',
#     )

#     def get_readonly_fields(self, request, obj=None):
#         return [
#             f.name for f in self.model._meta.fields
#         ] + ['detail', ]

#     def has_delete_permission(self, request, obj=None):
#         return False

@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    list_display = (
        'id',
    )
    list_display_links = ('id', )
    fields = (
        'id',
    )
    readonly_fields = (
        'id',
    )
    search_fields = [
        'id',
    ]
    ordering = ['-created_at']

    actions = [
        test_action,
    ]

    # inlines = (
    #     TestInline,
    # )
"""

    with open(admin_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Estrutura do admin.py criada para o app '{app_name}' em {admin_path}") # noqa501


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_admin.py <nome_do_app>")
    else:
        create_admin_structure(sys.argv[1])
