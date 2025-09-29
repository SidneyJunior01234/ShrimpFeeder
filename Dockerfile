FROM python:3.11

# diretorio de trabalho
WORKDIR /app

# copiar requirements para instalar as bibliotecas
COPY requirements.txt .

# pip pode usar o arquivo que já esta no cache, em vez de baixa-lo novamente da internet
RUN pip install --no-cache-dir -r requirements.txt

# copiar os outros arquivos
COPY . .

# porta do streamlit exposta para uso
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]