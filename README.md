# 🚀 Flask PDF Redactor

Este projeto é uma aplicação web construída com **Flask** e **PyMuPDF** que oferece uma ferramenta simples e eficiente para a **redação permanente** (tarjamento) de dados sensíveis (PII - *Personally Identifiable Information*) em documentos PDF com texto pesquisável.

A principal funcionalidade é garantir que o conteúdo redigido seja **removido fisicamente** do arquivo, e não apenas coberto por uma caixa preta.

## ✨ Funcionalidades Principais

* **Interface Web Simples:** Uma interface amigável para upload de arquivos PDF (apenas `.pdf`) com limite de 50 MB.
* **Redação Seletiva:** O usuário pode escolher quais categorias de PII serão redigidas antes do processamento, utilizando expressões regulares para tarjamento:
    * **Emails**
    * **CPFs**
    * **RGs**
    * **Celulares/Telefones**
    * **Endereços** (incluindo padrões de rua, avenida e CEP)
* **Processamento Seguro:** Utiliza a biblioteca **PyMuPDF** para garantir que o texto e os objetos sobrepostos sejam removidos permanentemente.
* **Gestão de Arquivos:** Lida com o *upload* de arquivos com segurança e gerencia o download do arquivo processado, salvando-o na pasta `uploads`.
* **Tecnologia:** O core da aplicação é o Flask.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3
* **Framework Web:** [Flask](https://flask.palletsprojects.com/) (`Flask>=2.0`)
* **Manipulação de PDF:** [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) (`PyMuPDF>=1.21.1`)
* **Outras Dependências:** `python-magic>=0.4.27`, `Werkzeug>=2.0`

## ⚙️ Preparação e Execução

Para configurar e rodar o projeto localmente, siga os passos abaixo:

1.  **Clonar o Repositório:** (Assumindo que você está no diretório raiz do projeto)
2.  **Preparar o Ambiente:** Crie e ative um ambiente virtual (`virtualenv`).
    ```bash
    python3 -m venv venv
    source venv/bin/activate # ou .\venv\Scripts\activate.ps1 no Windows
    ```
3.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Estrutura de Diretórios:** Certifique-se de que as pastas `utils/` e `static/` existem, conforme a estrutura do projeto.
5.  **Executar o Aplicativo:**
    ```bash
    python3 app.py
    ```
6.  Acesse `http://127.0.0.1:5000/` no seu navegador.

## 📄 Licença

Este projeto é distribuído sob a **GNU General Public License, Version 3 (GPL-3.0)**. A GPL é uma licença *copyleft* livre, que visa garantir a liberdade de compartilhar e modificar o software para todos os seus usuários.
