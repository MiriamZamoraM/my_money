# 💰 My Money API

API de finanzas personales diseñada con enfoque en producción, seguridad y buenas prácticas backend + DevOps.

## 🧩 Descripción

My Money API es una API REST que permite a los usuarios gestionar sus finanzas personales de forma estructurada y segura.

El sistema modela el dinero como lo hace el mundo real:
el dinero vive en distintos lugares y se mueve constantemente.

Esta API permite crear usuarios, administrar múltiples tipos de cuentas financieras y registrar ingresos y egresos con balances claros por usuario.

El proyecto está preparado para ejecución en contenedores, con una arquitectura limpia y lista para escalar.

---

## ✨ Funcionalidades
* 👤 **Usuarios**
  * Registro y autenticación
  * Autenticación basada en JWT
  * Aislamiento de datos por usuario

* 🏦 **Cuentas financieras**
  * Crédito
  * Débito
  * Ahorro
  * Wallet
  * Efectivo

* 📊 **Movimientos**
  * Ingresos
  * Egresos
  * Balance por cuenta

* 🔐 **Seguridad**
  * Autenticación con tokens
  * Variables sensibles desacopladas del código
  * Ejecución de la aplicación con usuario no root
---


## 🛠️ **Stack tecnológico**
**Backend**
* Python
* Django
* Django REST Framework
* Gunicorn (producción)

**Base de datos**
* PostgreSQL

**Infraestructura**
* Docker
* Docker Compose
* Separación de entornos (desarrollo / producción)
---
## 🐳 Arquitectura

La aplicación se ejecuta en contenedores independientes:

* API Django ejecutándose con Gunicorn
* PostgreSQL como base de datos relacional
* Persistencia de datos mediante volúmenes Docker
* Configuración gestionada mediante variables de entorno

Esta arquitectura permite:

* despliegues reproducibles
* aislamiento de responsabilidades
* base sólida para migrar a Kubernetes
---

## ▶️ Ejecución (entorno tipo producción)

**Requisitos:**
* Docker
* Docker Compose

**Construir y levantar servicios**
```
docker-compose up --build
```

La API estará disponible en:
```
http://localhost:8000
```
---
## ⚙️ Configuración

Las variables de entorno se gestionan mediante archivos .env, excluidos del repositorio.

* Ejemplos de variables utilizadas:
* Credenciales de base de datos
* Configuración de Django
* Secret keys

Ninguna variable sensible vive en el código fuente.

## 📈 Estado del proyecto

El proyecto se encuentra funcional y estable, con una base sólida para continuar evolucionando.

Próximos pasos:
* Metas de ahorro
* Reportes financieros
* Observabilidad y logging
* Preparación para Kubernetes
* Hardening de seguridad

### 👩‍💻 Autor

***Miriam Zamora Morales**
**Backend / DevOps Engineer***

Este proyecto refleja mi forma de trabajar:

* decisiones técnicas conscientes
* enfoque en producción desde etapas tempranas
* aprendizaje continuo aplicado en código real

## 📌 Nota

> *La producción no empieza cuando se despliega,*
> *empieza cuando el diseño se toma en serio.*