import sys
import os
import threading
import time

# --- IMPORTACIÓN DE FLASK ---
from api.app import app 

# --- IMPORTACIÓN DE MODELOS ---
from api.models.paciente import Paciente
from api.models.medico import Medico
from api.models.cita import Cita

# --- IMPORTACIÓN DE SERVICIOS ---
from api.services.paciente_service import PacienteService
from api.services.medico_service import MedicoService
from api.services.cita_service import CitaService
from api.services.usuario_service import UsuarioService

# --- INSTANCIAS GLOBALES ---
paciente_service = PacienteService()
medico_service = MedicoService()
cita_service = CitaService()
usuario_service = UsuarioService()

# --- FUNCIÓN PARA CORRER LA API EN SEGUNDO PLANO ---
def ejecutar_api():
    app.run(port=5000, debug=False, use_reloader=False)

# --- UTILIDADES DE DISEÑO ---
def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def imprimir_titulo(texto):
    print("\n" + "═"*60)
    print(f" {texto.upper()} ")
    print("═"*60)

def pausa():
    input("\nPresione ENTER para continuar...")

# --- MENÚS ESPECÍFICOS ---

def menu_pacientes():
    while True:
        limpiar_pantalla()
        imprimir_titulo("Gestión de Pacientes")
        print("1. Registrar nuevo paciente")
        print("2. Listar todos los pacientes")
        print("3. Buscar paciente por RUT")
        print("4. Eliminar Paciente")
        print("5. Volver al menú principal")
        
        opcion = input("\n>> Seleccione una opción: ")

        if opcion == '1':
            try:
                print("\n[Ingrese datos del Paciente]")
                nombre = input("Nombre completo: ")
                rut = input("RUT: ")
                telefono = input("Teléfono: ")
                
                if nombre and rut:
                    nuevo_paciente = Paciente(None, nombre, rut, telefono)
                    paciente_service.crear_paciente(nuevo_paciente)
                else:
                    print(" Error: Nombre y RUT son obligatorios.")
            except Exception as e:
                print(f"Error: {e}")
            pausa()

        elif opcion == '2':
            lista = paciente_service.listar_pacientes()
            print(f"\n--- Listado ({len(lista)} encontrados) ---")
            for p in lista:
                print(p.mostrar_info())
            pausa()

        elif opcion == '3':
            rut_buscar = input("\nIngrese el RUT a buscar: ")
            paciente = paciente_service.buscar_por_rut(rut_buscar)
            if paciente:
                print("\n PACIENTE ENCONTRADO:")
                print(paciente.mostrar_info())
            else:
                print(" No se encontró ningún paciente con ese RUT.")
            pausa()

        elif opcion == '4':
            try:
                id_p = int(input("\nIngrese ID del paciente a eliminar: "))
                print(" ADVERTENCIA: Esto borrará también el historial de citas de este paciente.")
                conf = input("¿Está seguro? (s/n): ")
                if conf.lower() == 's':
                    paciente_service.eliminar_paciente(id_p)
            except ValueError:
                print(" El ID debe ser un número.")
            pausa()

        elif opcion == '5':
            break
        else:
            print(" Opción no válida.")
            pausa()

def menu_medicos():
    while True:
        limpiar_pantalla()
        imprimir_titulo("Gestión de Médicos")
        print("1. Registrar nuevo médico")
        print("2. Listar médicos disponibles")
        print("3. Eliminar Médico")
        print("4. Volver al menú principal")
        
        opcion = input("\n>> Seleccione una opción: ")

        if opcion == '1':
            nombre = input("\nNombre del Médico: ")
            especialidad = input("Especialidad: ")
            if nombre:
                nuevo_medico = Medico(None, nombre, especialidad)
                medico_service.crear_medico(nuevo_medico)
            else:
                print(" El nombre es obligatorio.")
            pausa()
        
        elif opcion == '2':
            lista = medico_service.listar_medicos()
            print("\n--- Staff Médico ---")
            for m in lista:
                print(m.mostrar_info())
            pausa()

        elif opcion == '3':
            try:
                id_m = int(input("\nIngrese ID del médico a eliminar: "))
                conf = input("¿Está seguro? (s/n): ")
                if conf.lower() == 's':
                    medico_service.eliminar_medico(id_m)
            except ValueError:
                print(" El ID debe ser un número.")
            pausa()

        elif opcion == '4':
            break
        else:
            print(" Opción no válida.")
            pausa()

def menu_citas():
    while True:
        limpiar_pantalla()
        imprimir_titulo("Agenda de Citas Médicas")
        print("1. Agendar nueva cita")
        print("2. Ver reporte completo (Detallado)")
        print("3. Modificar cita")
        print("4. Cancelar/Eliminar cita")
        print("5. Volver al menú principal")
        
        opcion = input("\n>> Seleccione una opción: ")

        if opcion == '1':
            try:
                print("\n[ Nueva Cita ]")
                print("--- Pacientes (Últimos) ---")
                for p in paciente_service.listar_pacientes()[-5:]: print(f"ID {p.id}: {p.nombre}")
                
                print("\n--- Médicos Disponibles ---")
                for m in medico_service.listar_medicos(): print(f"ID {m.id}: {m.nombre} ({m.especialidad})")
                print("-" * 30)

                id_paciente = int(input("Ingrese ID del Paciente: "))
                id_medico = int(input("Ingrese ID del Médico: "))
                fecha = input("Fecha (YYYY-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                motivo = input("Motivo: ")
                
                nueva_cita = Cita(None, id_paciente, id_medico, fecha, hora, motivo)
                cita_service.agendar_cita(nueva_cita)
            except ValueError:
                print(" Error: Los ID deben ser números enteros.")
            except Exception as e:
                print(f" Error inesperado: {e}")
            pausa()

        elif opcion == '2':
            reporte = cita_service.obtener_reporte_citas()
            print("\n--- CALENDARIO DE ATENCIONES ---")
            if not reporte:
                print("No hay citas registradas.")
            for r in reporte:
                print(f"#{r['id_cita']} | {r['fecha']} {r['hora']} | Px: {r['paciente']} | Dr: {r['medico']} | [{r['estado']}]")
            pausa()

        elif opcion == '3':
            try:
                id_cita = int(input("\nID de la cita a modificar: "))
                n_fecha = input("Nueva Fecha (YYYY-MM-DD): ")
                n_hora = input("Nueva Hora: ")
                n_estado = input("Nuevo Estado (Agendada/Realizada/Cancelada): ")
                cita_service.modificar_cita(id_cita, n_fecha, n_hora, n_estado)
            except ValueError:
                print(" El ID debe ser numérico.")
            pausa()

        elif opcion == '4':
            try:
                id_cita = int(input("\nID de la cita a eliminar: "))
                conf = input("¿Seguro? (s/n): ")
                if conf.lower() == 's':
                    cita_service.eliminar_cita(id_cita)
            except ValueError:
                print(" El ID debe ser numérico.")
            pausa()

        elif opcion == '5':
            break
        else:
            print(" Opción no válida.")
            pausa()

def menu_usuarios():
    while True:
        limpiar_pantalla()
        imprimir_titulo("Gestión de Usuarios (Admin)")
        print("1. Listar Usuarios")
        print("2. Eliminar Usuario")
        print("3. Volver")
        
        opcion = input("\n>> Seleccione una opción: ")
        
        if opcion == '1':
            usuarios = usuario_service.listar_usuarios()
            print("\n--- Usuarios del Sistema ---")
            for u in usuarios:
                print(f"ID: {u['id_usuario']} | Nombre: {u['nombre']} | Correo: {u['correo']}")
            pausa()

        elif opcion == '2':
            try:
                id_u = int(input("\nIngrese ID del usuario a eliminar: "))
                if id_u == 1:
                    print(" No se recomienda eliminar al administrador principal.")
                
                conf = input("¿Está seguro? (s/n): ")
                if conf.lower() == 's':
                    usuario_service.eliminar_usuario(id_u)
            except ValueError:
                print(" El ID debe ser numérico.")
            pausa()

        elif opcion == '3':
            break
        else:
            print(" Opción no válida.")
            pausa()

# --- LOGICA PRINCIPAL ---

def main():
    while True:
        limpiar_pantalla()
        imprimir_titulo("Sistema Clínico 'Salud Python' v4.0")
        print(" API ESTADO: Ejecutándose en segundo plano (Puerto 5000)")
        
        # === 1. BLOQUE DE LOGIN ===
        usuario_autenticado = False
        
        while not usuario_autenticado:
            print("\n ACCESO RESTRINGIDO")
            print("1. Iniciar Sesión")
            print("2. Registrar Nuevo Usuario")
            print("3. Salir")
            
            opcion = input("\n>> Seleccione: ")
            
            if opcion == '1':
                correo = input("Correo: ")
                password = input("Contraseña: ")
                if usuario_service.login(correo, password):
                    usuario_autenticado = True
                    pausa()
                else:
                    pausa()
            
            elif opcion == '2':
                print("\n[Registro de Administrador]")
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                password = input("Contraseña: ")
                usuario_service.registrar_usuario(nombre, correo, password)
                pausa()
                
            elif opcion == '3':
                print("Cerrando sistema...")
                sys.exit()
            else:
                print("Opción inválida.")
                pausa()

        # === 2. MENÚ PRINCIPAL ===
        while usuario_autenticado:
            limpiar_pantalla()
            imprimir_titulo("Menú Principal")
            
            # --- PANEL DE URLS ---
            print("API REST ACTIVA (JSON ENDPOINTS):")
            print("   Pacientes: http://localhost:5000/api/pacientes")
            print("   Médicos:   http://localhost:5000/api/medicos")
            print("   Citas:     http://localhost:5000/api/citas")
            print("-" * 50)
            
            print("1. Gestionar Pacientes")
            print("2. Gestionar Médicos")
            print("3. Gestionar Citas")
            print("4. Gestionar Usuarios (Cuentas)")
            print("5. Cerrar Sesión")
            
            opcion = input("\n>>> Ingrese su opción: ")

            if opcion == '1':
                menu_pacientes()
            elif opcion == '2':
                menu_medicos() 
            elif opcion == '3':
                menu_citas()
            elif opcion == '4':
                menu_usuarios()
            elif opcion == '5':
                print("Cerrando sesión actual...")
                usuario_autenticado = False 
            else:
                print(" Opción no válida.")
                pausa()

if __name__ == "__main__":
    try:
        # ---------------------------------------------------------
        #  LANZAMIENTO DEL HILO DE LA API
        # ---------------------------------------------------------
        print(" Iniciando servidor API en segundo plano...")
        api_thread = threading.Thread(target=ejecutar_api, daemon=True)
        api_thread.start()
        
        time.sleep(1) 
        
        main()
        
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit()