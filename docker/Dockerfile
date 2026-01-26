FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/ .
COPY core/ .
COPY manage.py .
WORKDIR /
EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# La descripción de este archivo es:
    # 1️⃣ Definimos la imagen base de nuestra API
    # 2️⃣ Agregamos un comando para agregar y un usuario no root sin contraseña para
        # correr los comandos, solo por desarrollo.
    # 3️⃣ Copiamos dependencias
    # 4️⃣ Instalamos dependencias
    # 5️⃣ Copiamos elementos necesarios
    # 6️⃣ Nos movemos a la posición desde donde ejecutaremos comandos
    # 7️⃣ Ejecutamos los comandos (Por separado)
