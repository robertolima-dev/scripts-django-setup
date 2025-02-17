# README - Scripts de Automação para Django

Este repositório contém dois scripts úteis para automatizar a criação de aplicações e modelos no Django.

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

## 🏗️ Script: `setup_model.py`

Este script adiciona automaticamente um modelo Django ao arquivo `models.py` do app especificado.

### 📌 Uso
```sh
python setup_model.py <nome_do_app> <campo1=tipo,parametros> <campo2=...>
```

### 🎯 Exemplo
```sh
python setup_model.py evaluation 'desc=c,225,n,b,index' 'published=b,df=False' 'status_user_type=choice(user,admin,platform),120,n,index' 'evaluation=i,df=0,n,b' 'rate=f,df=0' 'category=Category(fk),n,index'
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, db_index=True)

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
- **fk**: `ForeignKey` → `ModeloRelacionado(fk), n=null, index=db_index`

### 🚀 Observações
- O nome do modelo gerado sempre será capitalizado.
- Os scripts **não sobrescrevem arquivos existentes**, permitindo ajustes manuais pós-criação.

---

## 🔗 Contribuição
Se desejar contribuir, abra um Pull Request com melhorias ou novos recursos. Feedbacks são bem-vindos!

---

## 📝 Licença
Este projeto está sob a licença MIT.

