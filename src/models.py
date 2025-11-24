from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CursoEmbed: 
    id_curso: int
    nome_curso: str
    carga_horaria: int
    nota1: float | None
    nota2: float | None
    media: float | None
    situacao: str | None = None

@dataclass
class Estudante:
    id: Optional[int]
    nome: str
    matricula: str
    email: str
    cursos: List[CursoEmbed] = field(default_factory=list) 
@dataclass
class Curso: 
    id: int
    nome: str
    carga_horaria: int | None

