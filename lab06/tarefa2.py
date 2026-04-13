from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional
from datetime import date

# --- Definir o esquema ---
class Utilizador(BaseModel):
    nome: str
    idade: int
    email: EmailStr
    data_nascimento: Optional[date] = None

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("O nome não pode estar vazio.")
        return v.strip()

    @field_validator("idade")
    @classmethod
    def idade_valida(cls, v):
        if v < 0:
            raise ValueError("A idade não pode ser negativa.")
        if v > 150:
            raise ValueError("A idade não é plausível.")
        return v


# --- Função auxiliar para testar ---
def validar(payload: dict):
    print(f"INPUT: {payload}")
    try:
        u = Utilizador(**payload)
        print(f"✅ VÁLIDO: {u}\n")
    except ValidationError as e:
        for err in e.errors():
            print(f"❌ ERRO em '{err['loc'][0]}': {err['msg']}")
        print()


# --- Testes ---
casos = [
    # Válidos
    {"nome": "Ana Silva", "idade": 25, "email": "ana@exemplo.com"},
    {"nome": "João", "idade": 0, "email": "joao@ubi.pt", "data_nascimento": "2000-05-10"},

    # Inválidos
    {"nome": "", "idade": 25, "email": "ana@exemplo.com"},          # nome vazio
    {"nome": "Carlos", "idade": -5, "email": "carlos@ubi.pt"},      # idade negativa
    {"nome": "Maria", "idade": 30, "email": "emailinvalido"},        # email sem @
    {"nome": "Pedro", "idade": 200, "email": "pedro@ubi.pt"},        # idade implausível
    {"idade": 22, "email": "sem_nome@ubi.pt"},                       # campo obrigatório em falta
]

print("=" * 60)
for caso in casos:
    validar(caso)