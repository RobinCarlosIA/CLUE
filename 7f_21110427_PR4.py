
# -*- coding: utf-8 -*-
"""
CLUE 

"""

import random
import sys
from textwrap import dedent

# ------------------------------------------------------------------
# Sospechosos 
# ------------------------------------------------------------------
SUSPECTOS = [
    {"nombre": "Robin",     "profesion": "Chef de partida"},
    {"nombre": "Fernanda",  "profesion": "Química farmacobióloga (QFB)"},
    {"nombre": "Luis",      "profesion": "Ingeniero de procesos"},
    {"nombre": "Emiliano",  "profesion": "Técnico de mantenimiento industrial"},
    {"nombre": "Juan",      "profesion": "Coordinador de seguridad privada"},
]

# ------------------------------------------------------------------
# Armas 
# ------------------------------------------------------------------
ARMAS = [
    "Cuchillo",
    "Pistola 9mm",
    "Cuerda",
    "Veneno",
    "Barra metálica",
]

# ------------------------------------------------------------------
# Locaciones 
# ------------------------------------------------------------------
LOCACIONES = [
    "Cocina del restaurante",        # Robin (chef)
    "Laboratorio de toxicología",    # Fernanda (QFB)
    "Línea de producción",           # Luis (procesos)
    "Taller de mantenimiento",       # Emiliano (mantenimiento)
    "Sala de monitoreo de seguridad" # Juan (seguridad)
]

# ------------------------------------------------------------------
# Pistas y detalles técnicos 
# ------------------------------------------------------------------
ARMAS_SILENCIOSAS = {"Cuchillo", "Cuerda", "Veneno"}

TWIST_ARMA = {
    "Cuchillo": "El corte es limpio y profundo; la hoja presenta restos hemáticos y huellas parciales.",
    "Pistola 9mm": "Balística confirmó estriado compatible y se detectó residuo de disparo (GSR) en la ropa.",
    "Cuerda": "Se hallaron fibras sintéticas en la escena y marcas de compresión compatibles con sujeción.",
    "Veneno": "El cromatógrafo (HPLC) detectó compuestos activos en la muestra de bebida/alimento.",
    "Barra metálica": "Las lesiones son por objeto contundente; la barra tiene microvirutas y óxido reciente.",
}

TWIST_LUGAR = {
    "Cocina del restaurante": "El circuito de CCTV registró movimientos fuera de turno y manipulación de cuchilleros.",
    "Laboratorio de toxicología": "Quedó traza de reactivos en bancada y el acceso biométrico marcó ingreso no autorizado.",
    "Línea de producción": "El sistema ANDON reportó una parada no programada cercana a la zona del incidente.",
    "Taller de mantenimiento": "Una herramienta faltante del inventario y una taquilla mal cerrada llamaron la atención.",
    "Sala de monitoreo de seguridad": "Los logs muestran cámaras deshabilitadas por 4 minutos usando credenciales internas.",
}

# ------------------------------------------------------------------
# Finales 
# ------------------------------------------------------------------
def final_robin(arma, lugar):
    return dedent(f"""
        FINAL • Turno de cierre
        -----------------------
        Robin, {SUSPECTOS[0]['profesion']}, conocía ritmos y puntos ciegos de la cocina.
        {TWIST_ARMA[arma]}
        En {lugar}, {TWIST_LUGAR[lugar]}
        Dijo que fue un arrebato por presión del servicio, pero las pruebas lo señalan directamente.
    """).strip()

def final_fernanda(arma, lugar):
    return dedent(f"""
        FINAL • Control de trazas
        -------------------------
        Fernanda, {SUSPECTOS[1]['profesion']}, dominaba protocolos de bioseguridad y registro.
        {TWIST_ARMA[arma]}
        En {lugar}, {TWIST_LUGAR[lugar]}
        La cadena de custodia y los cromatogramas cerraron cualquier duda: no fue un accidente.
    """).strip()

def final_luis(arma, lugar):
    return dedent(f"""
        FINAL • Ventana de proceso
        --------------------------
        Luis, {SUSPECTOS[2]['profesion']}, ubicó una ventana de tiempo durante un cambio de turno.
        {TWIST_ARMA[arma]}
        En {lugar}, {TWIST_LUGAR[lugar]}
        Admitió que quiso 'resolver' un conflicto operativo, cruzando una línea que no debía.
    """).strip()

def final_emiliano(arma, lugar):
    return dedent(f"""
        FINAL • Pasillo de servicio
        ---------------------------
        Emiliano, {SUSPECTOS[3]['profesion']}, conocía rutas internas y bloqueos mecánicos.
        {TWIST_ARMA[arma]}
        En {lugar}, {TWIST_LUGAR[lugar]}
        Alegó que pretendía intimidar, pero la traza de herramientas y tiempos lo compromete.
    """).strip()

def final_juan(arma, lugar):
    return dedent(f"""
        FINAL • Apagón selectivo
        ------------------------
        Juan, {SUSPECTOS[4]['profesion']}, tenía control de llaves y rondines.
        {TWIST_ARMA[arma]}
        En {lugar}, {TWIST_LUGAR[lugar]}
        El patrón de desactivación de cámaras y accesos lo vincula como autor material.
    """).strip()

FINALES = {
    "Robin": final_robin,
    "Fernanda": final_fernanda,
    "Luis": final_luis,
    "Emiliano": final_emiliano,
    "Juan": final_juan,
}

# ------------------------------------------------------------------
#  Juego
# ------------------------------------------------------------------
def titulo():
    print(dedent("""
        =====================================================
                               C L U E
        =====================================================
        • 5 sospechosos (con profesión), 5 armas, 5 locaciones.
        • El caso (culpable, arma, locación) se elige al azar.
        • Tienes UNA acusación. Puedes pedir hasta 2 pistas.
        • Escribe 'q' o 'salir' en cualquier momento para terminar.
        =====================================================
    """).strip())

def listar_opciones(etiqueta, opciones):
    print(f"\n{etiqueta}")
    print("-" * len(etiqueta))
    for i, o in enumerate(opciones, 1):
        if isinstance(o, dict):
            print(f"{i}. {o['nombre']} — {o['profesion']}")
        else:
            print(f"{i}. {o}")

def pedir_indice(mensaje, total):
    while True:
        s = input(mensaje).strip()
        if s.lower() in {"q", "salir"}:
            print("Saliendo del juego...")
            sys.exit(0)
        if not s.isdigit():
            print("⚠️  Ingresa un número.")
            continue
        n = int(s)
        if not (1 <= n <= total):
            print(f"⚠️  Elige entre 1 y {total}.")
            continue
        return n - 1

def generar_caso():
    culpable = random.choice(SUSPECTOS)["nombre"]
    arma = random.choice(ARMAS)
    lugar = random.choice(LOCACIONES)
    return (culpable, arma, lugar)

def pista(caso, usadas):
    culpable, arma, lugar = caso
    if usadas == 0:
        tipo = "silenciosa" if arma in ARMAS_SILENCIOSAS else "ruidosa"
        return f"Pista 1 → El arma parece {tipo}."
    elif usadas == 1:
        return f"Pista 2 → Hay un registro anómalo en: {lugar}."
    else:
        iniciales = "".join([p[0] for p in culpable.split()])
        return f"Pista extra → Las iniciales del sospechoso son '{iniciales}'."

def acusar():
    listar_opciones("SOSPECHOSOS", SUSPECTOS)
    i_s = pedir_indice("Elige # del SOSPECHOSO: ", len(SUSPECTOS))
    listar_opciones("ARMAS", ARMAS)
    i_a = pedir_indice("Elige # del ARMA: ", len(ARMAS))
    listar_opciones("LOCACIONES", LOCACIONES)
    i_l = pedir_indice("Elige # de la LOCACIÓN: ", len(LOCACIONES))
    return (SUSPECTOS[i_s]["nombre"], ARMAS[i_a], LOCACIONES[i_l])

def mostrar_final(caso):
    culpable, arma, lugar = caso
    fn = FINALES.get(culpable)
    if fn:
        print("\n" + fn(arma, lugar))
    else:
        print(f"\nFINAL • {culpable} con {arma} en {lugar}.")

def exportar_caso(caso, victoria):
    culpable, arma, lugar = caso
    contenido = dedent(f"""
        Caso resuelto: {'ÉXITO' if victoria else 'FALLO'}
        Culpable: {culpable}
        Arma: {arma}
        Locación: {lugar}
    """).strip()
    with open("reporte_caso.txt", "w", encoding="utf-8") as f:
        f.write(contenido)
    print("Se guardó 'reporte_caso.txt' en la carpeta actual.")

def main():
    random.seed()
    titulo()
    caso = generar_caso()
    pistas_usadas = 0

    while True:
        print(dedent("""
            ------------------
            MENÚ
            1) Ver listas (sospechosos/armas/locaciones)
            2) Pedir pista
            3) Hacer acusación (una oportunidad)
            4) Salir
        """))
        op = input("Opción (1-4): ").strip()

        if op == "1":
            listar_opciones("SOSPECHOSOS", SUSPECTOS)
            listar_opciones("ARMAS", ARMAS)
            listar_opciones("LOCACIONES", LOCACIONES)

        elif op == "2":
            if pistas_usadas < 2:
                print(pista(caso, pistas_usadas))
                pistas_usadas += 1
            else:
                print("Ya usaste tus 2 pistas.")

        elif op == "3":
            eleccion = acusar()
            if eleccion == caso:
                print("\n✅ ¡ACERTASTE! Resolviste el caso.")
                mostrar_final(caso)
                exportar_caso(caso, True)
                break
            else:
                c, a, l = caso
                print("\n❌ Acusación incorrecta.")
                print(f"La solución correcta era: {c} con {a} en {l}.")
                mostrar_final(caso)
                exportar_caso(caso, False)
                break

        elif op == "4" or op.lower() in {"q", "salir"}:
            print("¡Gracias por jugar!")
            break

        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
