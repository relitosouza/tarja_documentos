🚀 Flask PDF Redactor

Este é um projeto de aplicação web construído com Flask e PyMuPDF que oferece uma ferramenta simples e eficiente para a redação permanente (tarjamento) de dados sensíveis (PII - Personally Identifiable Information) em documentos PDF com texto pesquisável.

A principal funcionalidade é garantir que o conteúdo redigido seja removido fisicamente do arquivo, e não apenas coberto por uma caixa preta (o que poderia ser revertido).

✨ Funcionalidades Principais
Interface Web Simples: Uma interface amigável para upload de arquivos PDF.

Redação Seletiva: O usuário pode escolher quais categorias de PII serão redigidas antes do processamento:

Emails

CPFs

RGs

Celulares/Telefones

Endereços (incluindo padrões de rua, avenida e CEP)

Processamento Seguro: Utiliza a biblioteca PyMuPDF para garantir que o texto e os objetos sobrepostos sejam removidos permanentemente após o tarjamento.

Gestão de Arquivos: Lida com o upload de arquivos com segurança (secure_filename) e gerencia o download do arquivo processado.

Limites: Suporta uploads de até 50 MB.

🛠️ Tecnologias Utilizadas
Backend: Python 3


Framework Web: Flask (Flask>=2.0)

Manipulação de PDF: PyMuPDF (fitz) (PyMuPDF>=1.21.1)

Dependencies: python-magic, Werkzeug

⚙️ Preparação e Execução
Para configurar e rodar o projeto localmente, siga os passos abaixo:

Clonar o Repositório: (Assumindo que você está no diretório raiz do projeto)

Preparar o ambiente: Criar e ativar virtualenv:

python3 -m venv venv
source venv/bin/activate # ou .\venv\Scripts\activate.ps1 no Windows PowerShell

Instalar Dependências:
pip install -r requirements.txt

Estrutura de Diretórios: Certifique-se de que a estrutura de diretórios e arquivos (incluindo utils/redact.py, templates/, e static/) esteja correta. O app.py criará a pasta uploads automaticamente.

Executar o Aplicativo:
python3 app.py

Acesse http://127.0.0.1:5000/ no seu navegador.

📄 Licença
Este projeto é distribuído sob a GNU General Public License, Version 3 (GPL-3.0). A GPL garante a liberdade de compartilhar e modificar o software para todos os seus usuários.

