from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- SCHEMAS PARA TERMOS DE BUSCA ---
class TermoBuscaBase(BaseModel):
    palavra_chave: str

class TermoBuscaCreate(TermoBuscaBase):
    pass

class TermoBuscaResponse(TermoBuscaBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True

# --- SCHEMAS PARA USUÁRIOS ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr # Valida automaticamente se tem @ e .com
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    
    termos: List[TermoBuscaResponse] = []

    class Config:
        from_attributes = True