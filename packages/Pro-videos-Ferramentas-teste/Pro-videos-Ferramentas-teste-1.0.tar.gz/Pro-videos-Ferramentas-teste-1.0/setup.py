from setuptools import setup, find_packages
from pathlib import Path

setup(
    # Nome do projeto
    name='Pro-videos-Ferramentas-teste',
    # Versão do projeto
    version=1.0,
    # Descrição resumida
    description='Este pacote de teste, ferramentas de processamento de video',
    # Instruções mais detalhadas do projeto
    long_description=Path('README.md').read_text(),
    # Descrição do autor
    author='Uilson Cruz',
    # Email do autor
    author_email='uilsoncruz1996@gmal.com',
    # Palavras chaves, para facilitar a pesquisa, e ele ser facilmente
    # encontrado, lembrando que tem que ser uma lista de strings
    keywords=['Camera', 'Video', 'Processamento'],
    # Para quando o usuario instalar o pacote, ele vai pesquisar os pacotes/
    # depencias que o pacote precisa
    packages=find_packages()
)
