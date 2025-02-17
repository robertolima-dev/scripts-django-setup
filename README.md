# README - Scripts de Automação para Django

Este repositório contém 4 scripts úteis para automatizar a criação de aplicações, model e admin no Django.

## 📌 Setup
Certifique-se de que você tem o Python instalado e que está dentro do ambiente virtual do seu projeto Django.

```sh
python -m venv venv  # Criar ambiente virtual (se necessário)
source venv/bin/activate  # Ativar no Linux/macOS
venv\Scripts\activate  # Ativar no Windows
```

Instale as dependências necessárias:
```sh
pip install -r requirements.txt
```

---

## 🏗️ Script: `setup_app.py`

Este script cria automaticamente a estrutura de diretórios e arquivos para um novo app Django.

### 📌 Uso
```sh
python setup_app.py <nome_do_app>
```

### 🎯 Exemplo
```sh
python setup_app.py product
```

### 📁 Estrutura Criada
```
apps/<nome_do_app>/
    api/
        serializers.py
        viewsets.py
    managers/
        <nome_do_app>_manager.py
    signals.py
    filters.py
```


---

## 🏗️ Script: `setup_basemodel.py`

Este script cria automaticamente um arquivo `models.py` na raiz do projeto, dentro da pasta `core`, contendo a definição do `BaseModel`.

### 📌 Uso
```sh
python setup_basemodel.py <nome_da_pasta_core>
```

### 🎯 Exemplo
```sh
python setup_basemodel.py core
```

### 📄 Exemplo de Saída (`models.py`)
```python
from django.db import models
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
```

---

## 🏗️ Script: `setup_model.py`

Este script adiciona automaticamente um modelo Django ao arquivo `models.py` do app especificado.

### 📌 Uso
```sh
python setup_model.py <nome_do_app> <campo1=tipo,parametros> <campo2=...>
```

### 🎯 Exemplo
```sh
python setup_model.py evaluation 'desc=c,225,n,b,index' 'published=b,df=False' 'status_user_type=choice(user,admin,platform),120,n,index' 'evaluation=i,df=0,n,b' 'rate=f,df=0'
```

### 📄 Exemplo de Saída (`models.py`)
```python
from django.db import models
from api_core.models import BaseModel

STATUS_USER_TYPE_CHOICES = (
    ('user', 'user'),
    ('admin', 'admin'),
    ('platform', 'platform')
)

class Evaluation(BaseModel):
    desc = models.CharField(max_length=225, blank=True, db_index=True)
    published = models.BooleanField(default=False)
    status_user_type = models.CharField(
        choices=STATUS_USER_TYPE_CHOICES,
        max_length=120,
        default='user',
        null=True, blank=True, db_index=True
    )
    evaluation = models.IntegerField(default=0, blank=True)
    rate = models.FloatField(default=0)

    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"
        ordering = ['-id']

    def __str__(self) -> str:
        return f"Evaluation {self.name}"
```

### 🔧 Parâmetros de Campo
- **c**: `CharField` (Texto) → `max_length, n=null, b=blank, index=db_index`
- **b**: `BooleanField` → `df=default`
- **f**: `FloatField` → `df=default`
- **i**: `IntegerField` → `df=default, n=null, b=blank`
- **choice(...)**: `CharField` com opções → `choice=VARIAVEL, max_length, n=null, index=db_index`

### 🚀 Observações
- O nome do modelo gerado sempre será capitalizado.
- Os scripts **não sobrescrevem arquivos existentes**, permitindo ajustes manuais pós-criação.


---

## 🏗️ Script: `setup_admin.py`

Este script cria automaticamente a estrutura do `admin.py` para um app Django.

### 📌 Uso
```sh
python setup_admin.py <nome_do_app>
```

### 🎯 Exemplo
```sh
python setup_admin.py payment
```

### 📄 Exemplo de Saída (`admin.py`)
```python
from django.contrib import admin
from apps.payment.models import Payment

@admin.action(description='Teste action')
def test_action(modeladmin, request, queryset):
    for instance in queryset:
        print(instance)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
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

    inlines = ()
```

## 🚀 Observações
- O script **sobrescreve** o arquivo `admin.py` existente no app especificado.
- O nome do modelo é capitalizado automaticamente com base no nome do app.
- A estrutura gerada segue as melhores práticas do Django Admin.

---

## 🔗 Contribuição
Se desejar contribuir, abra um Pull Request com melhorias ou novos recursos. Feedbacks são bem-vindos!

---

## 📝 Licença
Este projeto está sob a licença MIT.
