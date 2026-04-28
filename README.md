# 🏥 Salud Python v4.0 – Sistema de Gestión Clínica

Sistema de escritorio y API REST para la administración de **pacientes**, **médicos** y **citas médicas**.  
Desarrollado en Python con Flask y MySQL.

---

## 🚀 Funcionalidades

- ✅ Registro, listado, búsqueda y eliminación de **pacientes**.
- ✅ Registro, listado y eliminación de **médicos**.
- ✅ **Agenda de citas**: creación, modificación, cancelación y reporte con unión de tablas (detallado).
- ✅ Gestión de **usuarios** (administradores) con inicio de sesión.
- ✅ Interfaz de consola interactiva (CLI) y **API REST** en segundo plano.
- ✅ Reporte de citas con nombres reales de paciente y médico.

---

## 📦 Tecnologías

| Componente       | Herramienta          |
|------------------|----------------------|
| Lenguaje         | Python 3.10+         |
| Framework Web    | Flask                |
| Base de datos    | MySQL                |
| Conexión BD      | `mysql-connector-python` |
| Interfaz consola | Módulos nativos `os`, `sys`, `threading` |

---

## ⚙️ Requisitos previos

- Python 3.8 o superior.
- MySQL (o MariaDB) con una base de datos creada.
- Git (para clonar el repositorio).

## Creación de Tablas en MySQL

CREATE TABLE JF_usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE JF_Paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE JF_Medico (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL
);

CREATE TABLE JF_Citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE,
    hora VARCHAR(10),
    motivo TEXT,
    estado VARCHAR(20) DEFAULT 'Agendada',
    CONSTRAINT fk_paciente FOREIGN KEY (id_paciente) REFERENCES JF_Paciente(id_paciente),
    CONSTRAINT fk_medico FOREIGN KEY (id_medico) REFERENCES JF_Medico(id_medico)
);

CREATE TABLE JF_Log_Externo (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    origen VARCHAR(50),
    datos_json TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE Table JF_Recetas (
    id_receta INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT NOT NULL,
    medicamento VARCHAR(100) NOT NULL,
    dosis VARCHAR(50),
    instrucciones TEXT,
    CONSTRAINT fk_cita FOREIGN KEY (id_cita) REFERENCES JF_Citas(id_cita)
);
