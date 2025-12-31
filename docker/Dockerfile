FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/ .
COPY core/ .
COPY manage.py .
WORKDIR /
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# La descripción de este archivo es:
    # 1️⃣ Definimos la imagen base de nuestra API
    # 2️⃣ Copiamos dependencias
    # 3️⃣ Instalamos dependencias
    # 4️⃣ Copiamos elementos necesarios
    # 5️⃣ Nos movemos a la posición desde donde ejecutaremos comandos
    # 6️⃣ Ejecutamos los comandos (Por separado)