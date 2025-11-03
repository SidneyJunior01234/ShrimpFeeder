# ShrimpFeeder

Guia de Configuração e Execução do Projeto Streamlit

Este guia fornece as instruções necessárias para configurar e executar a aplicação Streamlit em dois ambientes distintos: Windows (usando WSL 2) e Linux (Ubuntu/Debian).

1. Configuração no Windows (via WSL 2)

O WSL 2 (Windows Subsystem for Linux 2) é a maneira recomendada de executar este projeto no Windows, pois fornece um ambiente Linux completo e compatível.

Passo 1: Instalação e Configuração do WSL 2

Instalar o WSL 2: Abra o Prompt de Comando ou PowerShell (como Administrador) e execute o seguinte comando:

wsl --install


Isso instalará o WSL e a distribuição Ubuntu padrão. Siga as instruções para reiniciar o computador e criar seu nome de usuário e senha do Linux.

Verificar a Versão (Opcional): Após a reinicialização, abra o terminal do WSL e confirme a versão:

wsl -l -v


Garanta que a distribuição principal esteja configurada para a versão 2.

Passo 2: Preparação do Ambiente Linux (WSL)

Atualizar o Sistema: Dentro do seu terminal WSL, atualize a lista de pacotes:

sudo apt update && sudo apt upgrade -y


Instalar Python e Venv: Certifique-se de que o Python 3 e o módulo venv estão instalados:

sudo apt install python3 python3-venv -y


Passo 3: Clonagem do Repositório ou Download

Navegar até o Local: Navegue até o diretório onde você deseja armazenar o projeto (por exemplo, na pasta de usuário do Linux ou em um diretório montado do Windows, como /mnt/c/Users/SeuUsuario/Projetos):

cd ~
# OU para acessar o Windows:
# cd /mnt/c/Users/SeuUsuario/Documents/


Clonar (Git): Se estiver usando Git, clone o repositório:

git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]


OU

Download: Se você baixou o ZIP, descompacte-o e navegue para a pasta do projeto.

Passo 4: Configuração e Ativação do Ambiente Virtual (Venv)

Criar a Venv: Crie o ambiente virtual (recomendamos nomeá-lo .venv):

python3 -m venv .venv


Ativar a Venv: Ative o ambiente virtual para isolar as dependências do sistema:

source .venv/bin/activate


(Seu terminal exibirá (.venv) no prompt, indicando que o ambiente está ativo.)

Desativar a Venv: Para sair do ambiente virtual a qualquer momento:

deactivate


(Você deve reativá-lo para executar o projeto.)

Passo 5: Instalar Dependências

Com o ambiente virtual ATIVO, instale todas as bibliotecas necessárias listadas no requirements.txt:

pip install -r requirements.txt


Passo 6: Executar a Aplicação Streamlit

Execute o arquivo principal da aplicação (geralmente app.py):

streamlit run app.py


O Streamlit iniciará um servidor e fornecerá um link (Network URL) que você deve abrir no seu navegador Windows.

2. Configuração no Linux (Ubuntu/Debian)

As etapas para um ambiente Linux nativo são muito semelhantes, mas sem a necessidade de instalar o WSL.

Passo 1: Preparação do Ambiente

Atualizar o Sistema: Abra o terminal e atualize os pacotes:

sudo apt update && sudo apt upgrade -y


Instalar Python e Venv: Certifique-se de que o Python 3 e o módulo venv estão instalados:

sudo apt install python3 python3-venv -y


Passo 2: Clonagem do Repositório ou Download

Navegar até o Local: Navegue até o diretório de sua preferência:

cd ~/Projetos


Clonar (Git): Clone o repositório:

git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]


Passo 3: Configuração e Ativação do Ambiente Virtual (Venv)

Criar a Venv: Crie o ambiente virtual:

python3 -m venv .venv


Ativar a Venv: Ative o ambiente virtual:

source .venv/bin/activate


(Seu terminal exibirá (.venv) no prompt.)

Desativar a Venv: Para sair do ambiente virtual:

deactivate


Passo 4: Instalar Dependências

Com o ambiente virtual ATIVO, instale as dependências:

pip install -r requirements.txt


Passo 5: Executar a Aplicação Streamlit

Execute o arquivo principal da aplicação:

streamlit run app.py


O Streamlit iniciará um servidor e abrirá a aplicação em seu navegador padrão.