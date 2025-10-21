from dataclasses import dataclass

@dataclass
class Estudante:
    id: int | None
    nome: str
    matricula: str
    email: str

@dataclass
class Curso:
    id: int | None
    nome: str
    carga_horaria: int | None

@dataclass
class Nota:
    id: int | None
    id_estudante: int
    id_curso: int
    nota1: float | None
    nota2: float | None
    media: float | None
