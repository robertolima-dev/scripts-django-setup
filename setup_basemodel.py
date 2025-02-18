import os
import sys


def create_basemodel(core_name):
    file_path = os.path.join(core_name, "models.py")

    content = """from django.db import models
from django.utils import timezone


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModelAllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, db_index=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = BaseModelManager()
    obj_all = BaseModelAllManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def force_delete(self):
        super(BaseModel, self).delete()
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Arquivo models.py criado em {file_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_basemodel.py <nome_da_pasta_core>")
    else:
        create_basemodel(sys.argv[1])
