
# 💰 My Money API

> **Una API de finanzas personales diseñada con mentalidad de producto, buenas prácticas de backend y fundamentos DevOps.**

---

## 🚀 Visión del proyecto

**My Money API** es una API REST para la gestión de finanzas personales. Permite a cada usuario controlar su dinero de forma clara y estructurada: cuentas, ingresos, egresos y balances.

Este proyecto **no nace como un simple CRUD**, sino como un **laboratorio de aprendizaje real** donde aplico:

* Diseño de APIs con Django REST Framework
* Autenticación segura con JWT
* Modelado relacional con PostgreSQL
* Contenerización con Docker
* Separación clara de entornos (desarrollo / producción)
* Criterio DevOps desde etapas tempranas

> El objetivo no es solo que funcione, sino que **esté bien pensado**.

---

## 🧠 Problema que resuelve

Muchas aplicaciones de finanzas personales:

* son rígidas
* no representan la realidad financiera del usuario
* mezclan conceptos (cuentas, efectivo, tarjetas)

**My Money API** parte de una idea simple:

> *El dinero vive en distintos lugares y se mueve constantemente.*

Por eso el sistema permite:

* múltiples tipos de cuentas
* control de ingresos y egresos
* balances claros por usuario

---

## ✨ Funcionalidades principales

* 👤 **Usuarios**

  * Registro y autenticación con JWT
  * Acceso aislado por usuario

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

  * Autenticación basada en tokens
  * Variables sensibles fuera del código

---

## 🛠️ Stack tecnológico

**Backend**

* Python
* Django
* Django REST Framework

**Base de datos**

* PostgreSQL

**Infraestructura / DevOps**

* Docker
* Docker Compose
* Separación de entornos (dev / prod)

---

## 🐳 Arquitectura con Docker

El proyecto está preparado para ejecutarse en contenedores desde el inicio:

* API Django en un contenedor
* PostgreSQL en un contenedor independiente
* Persistencia de datos mediante volúmenes
* Configuración desacoplada mediante variables de entorno

Esto permite:

* reproducibilidad
* facilidad de onboarding
* base sólida para escalar a Kubernetes

---

## ▶️ Ejecución en desarrollo

Requisitos:

* Docker
* Docker Compose

```bash
docker-compose up --build
```

La API quedará disponible en:

```
http://localhost:8000
```

---

## 🌱 Estado del proyecto

Este es un **proyecto en evolución**.

Próximos pasos planeados:

* 🎯 Metas de ahorro
* 📈 Reportes y métricas
* ⚙️ Configuración de producción
* ☸️ Preparación para Kubernetes
* 🔍 Observabilidad y logging

---

## 👩‍💻 Sobre mí

Este proyecto forma parte de mi proceso de crecimiento como **Backend / DevOps Engineer**.

No pretende demostrar que ya lo sé todo, sino que:

* pienso en arquitectura
* entiendo los fundamentos
* tomo decisiones conscientes
* y construyo con visión de producción

---

## 📌 Nota final

> *El buen software no empieza en producción.
> Empieza con decisiones correctas desde el primer commit.*

Si este proyecto te resulta interesante, cualquier feedback es bienvenido 🚀


***Aprendido y aplicado por Miriam Zamora Morales***
