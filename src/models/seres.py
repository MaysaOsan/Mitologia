from datetime import date
from sqlmodel import Field, SQLModel

class Ser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)
    raza: str = Field(index=True,max_length=50)
    titulo: str | None = Field(default= "Sin título", nullable=True)
    esDios: bool = Field(default=False)
    fechaDeCreacion: date | None = Field(default=None, nullable=True)

