from typing import Optional

from prefect.blocks.core import Block
from pydantic import SecretStr

class Conexao(Block):
    url: Optional[str] = None
    authorization: Optional[SecretStr] = None
    conection: Optional[str] = None
    usuario: Optional[str] = None
    senha: Optional[SecretStr] = None

class DataBase(Block):
    nome: Optional[str] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    database: Optional[str] = None
    port: Optional[str] = None