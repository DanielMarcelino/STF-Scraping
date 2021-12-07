import os
import hashlib

from src.exceptions import (
    caminho_nao_encontrado,
    sem_permissao_para_criar_arquivo,
    sem_permissao_para_criar_diretorio,
    arquivo_incompativel_com_formato_pdf,
)


def cria_diretorio(nome_diretorio: str, caminho: str = '') -> None:
    try:
        if caminho:
            try:
                os.chdir(caminho)
            except NotADirectoryError:
                caminho_nao_encontrado()
        os.mkdir(nome_diretorio)
    except FileExistsError:
        pass
    except PermissionError:
        sem_permissao_para_criar_diretorio()


def valida_pdf(binario: bytes) -> None:
    if not binario.startswith(b'%PDF'):
        arquivo_incompativel_com_formato_pdf()


def gera_md5_hash(binario: bytes) -> str:
    md5_hash = hashlib.md5()
    md5_hash.update(binario)
    md5_hash = str(md5_hash.hexdigest())
    return md5_hash


def salva_arquivo(binario: bytes, nome: str, caminho: str = '') -> None:
    try:
        with open(f'{caminho}{nome}', 'wb') as arquivo:
            arquivo.write(binario)
    except PermissionError:
        sem_permissao_para_criar_arquivo()
