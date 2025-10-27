# 🐳 Guia Passo a Passo: Docker, Streamlit e Docker Hub

Este guia abrange a instalação do Docker, a execução de um contêiner Streamlit.

---

## 1️⃣ Instalando o Docker

### Windows

1.  **Baixe o Docker Desktop** em: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2.  **Instale o Docker Desktop.**
3.  **Habilite a integração com o WSL 2** (Windows Subsystem for Linux) durante a configuração (é obrigatório para a versão mais recente).
4.  Após a instalação, abra o **PowerShell** e verifique as versões:

    ```bash
    docker --version
    docker-compose --version
    ```

5.  Certifique-se de que o **Docker Desktop** esteja em execução.

---

### Linux (Ubuntu/Debian)

Para garantir a versão mais recente e estável (Docker CE) e incluir o `docker-compose`, usaremos o repositório oficial do Docker.

1.  **Atualize o índice de pacotes e instale as dependências necessárias:**

    ```bash
    sudo apt update
    sudo apt install ca-certificates curl gnupg
    ```

2.  **Adicione a chave GPG oficial do Docker:**

    ```bash
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    ```

3.  **Configure o repositório do Docker:**

    ```bash
    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

4.  **Instale o Docker Engine, o CLI e o Docker Compose Plugin:**

    ```bash
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

5.  **Verifique a instalação:**

    ```bash
    docker --version
    docker compose version # Note que agora é 'docker compose'
    sudo docker run hello-world
    ```

6.  **(Opcional) Execute o Docker sem `sudo`:**

    Este passo é altamente recomendado para evitar digitar `sudo` a cada comando.

    ```bash
    sudo usermod -aG docker $USER
    # Faça logout e login novamente para que as alterações entrem em vigor
    ```
---

## 2️⃣ Puxando uma Imagem do Docker Hub (Pull)

Se você estiver em uma máquina que não construiu a imagem, você deve baixá-la do Docker Hub antes de executar:

*Substitua `yourusername` pelo nome do repositório de onde você fará o download.*

```bash
docker pull sadsjr/app-streamlit:latest
```

## 3️⃣ Executando a Aplicação com Scripts

Para executar a aplicação Streamlit em contêiner, use o script correspondente ao seu sistema operacional. Todos os scripts são configurados para montar um volume de dados.

*Após realizar o pull da Imagem.*

### Execução em Linux / macOS

**Basta executar o arquivo:**

```bash
run_app.sh (linnux)
run_app_windows.sh (WSL2 com volume para acessar os dados no windows)
run_app_windows.ps1 (Powersehll com volume para acessar os dados no windows)
```

[run_app.sh](https://github.com/SidneyJunior01234/ShrimpFeeder/blob/main/run_app.sh)

[run_app_windows.sh](https://github.com/SidneyJunior01234/ShrimpFeeder/blob/main/run_app_windows.sh)

[run_app_windows.ps1](https://github.com/SidneyJunior01234/ShrimpFeeder/blob/main/run_app_windows.ps1)
