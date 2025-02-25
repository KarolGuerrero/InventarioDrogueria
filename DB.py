from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import Optional, List

sqlite_file_name = "drogueria.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    productos: List["Producto"] = Relationship(back_populates="categoria")

class Proveedor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    contacto: Optional[str]
    telefono: Optional[str]
    email: Optional[str]
    productos: List["Producto"] = Relationship(back_populates="proveedor")

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    precio_compra: float
    precio_venta: float
    stock: int = 0
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    proveedor_id: Optional[int] = Field(default=None, foreign_key="proveedor.id")
    categoria: Optional[Categoria] = Relationship(back_populates="productos")
    proveedor: Optional[Proveedor] = Relationship(back_populates="productos")

class Entrada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int
    fecha: str
    producto: Optional[Producto] = Relationship()

class Salida(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int
    fecha: str
    producto: Optional[Producto] = Relationship()

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    password: str
    rol: str
    facturas: List["Factura"] = Relationship(back_populates="usuario")

class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: str
    total: float
    usuario: Optional[Usuario] = Relationship(back_populates="facturas")
    detalles: List["DetalleFactura"] = Relationship(back_populates="factura")

class DetalleFactura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="factura.id")
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int
    precio: float
    factura: Optional[Factura] = Relationship(back_populates="detalles")
    producto: Optional[Producto] = Relationship()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Base de datos creada exitosamente")
