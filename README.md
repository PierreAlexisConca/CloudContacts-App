# CloudContacts – Agenda de Contactos en la Nube

Este proyecto implementa una aplicación web sencilla para gestionar contactos, desplegada en **AWS** bajo una arquitectura de **dos servidores EC2**: uno para el servidor web (**Flask + Gunicorn + Nginx**) y otro para la base de datos (**MySQL**).

---

## 🧩 1. Objetivo del Proyecto

Diseñar, construir y desplegar una aplicación web que permita registrar contactos y almacenarlos en una base de datos MySQL ubicada en un servidor separado. La arquitectura debe seguir buenas prácticas de seguridad, despliegue y modularización del código.

---

## 🏗️ 2. Arquitectura en AWS

La aplicación utiliza **dos instancias EC2 independientes**, cada una con responsabilidades específicas:

```
┌────────────────────┐       Puerto 3306        ┌──────────────────────┐
│    EC2 WEB         │────────────────────────►│      EC2 DB          │
│  Flask + Gunicorn  │                          │     MySQL Server     │
│  Nginx (puerto 80) │◄────────── ninguna ◄────│   Sin acceso público  │
└────────────────────┘                          └──────────────────────┘
        ▲
        │
        │ Internet (solo puerto 80)
```

### 🔐 Aislamiento de Servidores
- **EC2-WEB**: Único servidor expuesto a internet (solo puerto 80).
- **EC2-DB**: Sin acceso público; solo acepta conexiones del grupo de seguridad de EC2‑WEB en el puerto 3306.

---

## 🧪 3. Tecnologías Utilizadas

- **Python 3 / Flask**
- **MySQL Server 8**
- **Tailwind CSS** (CDN)
- **Gunicorn** como servidor de producción
- **Nginx** como reverse proxy
- **Systemd** para ejecución automática
- **AWS EC2** (Ubuntu 22.04)

---

## ⭐ 4. Funcionalidades de la Aplicación

### Página Principal `/`
Formulario responsivo para ingresar:
- Nombre Completo
- Correo Electrónico
- Teléfono (opcional)

### Página `/contacts`
- Tabla responsiva mostrando todos los contactos almacenados.
- Visualización de:
  - ID
  - Nombre
  - Correo
  - Teléfono
  - Fecha y hora de registro

### Manejo de Errores
- Error de conexión a MySQL
- Error de correo duplicado
- Mensajes informativos usando `flash()`

---

## 📂 5. Estructura de Directorios

```
CloudContacts-App/
│── app.py
│── database.py
│── .env               (no se sube a GitHub)
│── README.md
│── requirements.txt
│── venv/
│── templates/
│     ├── index.html
│     └── contacts.html
└── static/
      └── styles.css
```

---

## 🔑 6. Configuración del Servidor DB (EC2-DB)

### 1. Instalar MySQL
```bash
sudo apt update
sudo apt install mysql-server -y
```

### 2. Crear base de datos y tabla
```sql
CREATE DATABASE IF NOT EXISTS cloudcontacts;
USE cloudcontacts;

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Crear usuario seguro
```sql
CREATE USER 'clouduser'@'%' IDENTIFIED BY 'TuPasswordSeguro';
GRANT ALL PRIVILEGES ON cloudcontacts.* TO 'clouduser'@'%';
FLUSH PRIVILEGES;
```

---

## 🔐 7. Variables de Entorno (.env)

Este archivo **no se sube al repositorio**.

```
DB_HOST=IP_PRIVADA_EC2_DB
DB_USER=clouduser
DB_PASSWORD=TuPasswordSeguro
DB_NAME=cloudcontacts
```

---

## 🚀 8. Instalación en EC2-WEB

### 1. Clonar repositorio
```bash
git clone https://github.com/tuusuario/CloudContacts-App.git
cd CloudContacts-App
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Probar la app antes del despliegue
```bash
python3 app.py
```

---

## 🔥 9. Configurar Gunicorn

Archivo systemd:

```
[Unit]
Description=CloudContacts Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/CloudContacts-App
EnvironmentFile=/home/ubuntu/CloudContacts-App/.env
ExecStart=/home/ubuntu/CloudContacts-App/venv/bin/gunicorn -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudcontacts
sudo systemctl start cloudcontacts
```

---

## 🌍 10. Configurar Nginx (Reverse Proxy)

```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Reiniciar:

```bash
sudo systemctl restart nginx
```

---

## 📦 11. Requirements.txt

```
Flask
gunicorn
mysql-connector-python
python-dotenv
```

---

## 📝 12. Entrega (Classroom)

El entregable debe incluir:

- Enlace al repositorio GitHub del proyecto.
- La **IP Elástica** donde funciona la aplicación.
- Captura o video demostrando `/` y `/contacts`.

---

## ✔️ Proyecto completado

Este README cumple **todos los requisitos solicitados** para la entrega oficial del proyecto CloudContacts.

---

Si deseas incluir **diagramas, capturas, GIFs** o que adapte este README exactamente al formato de tu profesor, puedo ajustarlo.

