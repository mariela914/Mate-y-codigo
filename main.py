import os
from datetime import datetime
from carga import cargar_telemetria
from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(DIRECTORIO_BASE, "gamesec_logs.csv")
RUTA_REPORTE = os.path.join(DIRECTORIO_BASE, "reporte_gamesec.txt")

fecha = datetime.now().strftime("%d/%m/%Y")

def exportar_reporte(sesiones: list[dict], ruta_salida: str) -> None:
    """Consigna 5 y 6: Exporta el informe estructurado a reporte_gamesec.txt."""
    glob = calcular_estadisticas_globales(sesiones)
    regionales = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)
    total = glob["total_sesiones"]

    with open(ruta_salida, mode="w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("              REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC\n")
        f.write("=" * 70 + "\n")
        f.write(f"Fecha de generación: {fecha}\n\n")
        

        f.write("[1] RESUMEN GLOBAL OPERATIVO\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total de sesiones procesadas: {glob['total_sesiones']}\n")
        f.write(f"Ping promedio global: {glob['ping_promedio']:.2f} ms\n")
        f.write(f"Duración media de partida: {glob['duracion_promedio']:.2f} min\n")
        f.write(f"Partidas de alta competencia (Ranked/Torneo): {glob['porcentaje_competitivas']:.2f}%\n\n")

        f.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio':<12}\n")
        f.write("-" * 70 + "\n")
        for srv, d in regionales.items():
            f.write(f"{srv:<18} | {d['cantidad']:<8} | {d['ping_promedio']:>6.2f} ms    | {d['fps_promedio']:>6.2f} fps\n")
        f.write("\n")

        f.write("[3] AUDITORÍA DE SEGURIDAD E INCIDENTES\n")
        f.write("-" * 70 + "\n")
        f.write("Distribución de estados de seguridad:\n")
        for estado in ["Normal", "Sospechoso", "Crítico"]:
            cant = frecuencias[estado]
            pct = (cant / total) * 100 if total > 0 else 0
            f.write(f"  • {estado + 'es' if estado == 'Normal' else estado + 's':<13} {cant:>4} sesiones ({pct:>6.2f}%)\n")
        f.write("\nDetalle de Sesiones Críticas Detectadas:\n")
        for c in criticos:
            f.write(f"  [!] Sesión #{c['id_sesion']} | Jugador: {c['jugador_id']} | Servidor: {c['servidor']}\n")
            f.write(f"      Motivo: {c['motivo']}\n")
        f.write("\n")

        f.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
        f.write("-" * 70 + "\n")
        f.write("1. La infraestructura sudamericana (SA-BuenosAires y SA-SaoPaulo) ofrece la mejor experiencia de usuario con latencias menores a 80 ms, mientras que nodos transoceánicos como NA-Virginia y EU-Frankfurt concentran la mayor cantidad de alertas por lag switching.\n")
        f.write("2. El 53.33% de las partidas corresponde a modalidades competitivas y torneos, lo cual justifica endurecer los filtros automáticos sobre jugadores que acumulan denuncias por trampas.\n")
        f.write("3. La detección de un 6.67% de sesiones críticas con patrones de fuerza bruta evidencia la necesidad de implementar bloqueos temporales por IP o verificación en dos pasos en el subsistema de login.\n")
        f.write("=" * 70 + "\n")
        f.write("                    FIN DEL REPORTE GAMESEC\n")
        f.write("=" * 70 + "\n")

def main():
    sesiones = []
    while True:
        print("\n=========================================")
        print("      GAMESEC MONITOR - PANEL DE CONTROL")
        print("=========================================")
        print("1. Cargar y validar dataset")
        print("2. Ver estadísticas globales de servidores")
        print("3. Ver rendimiento por región de servidor")
        print("4. Auditar incidentes de seguridad (Críticos y Sospechosos)")
        print("5. Exportar reporte consolidado (reporte_gamesec.txt)")
        print("6. Salir")
        print("=========================================")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                sesiones = cargar_telemetria(RUTA_CSV)
                print(f"\n[OK] Dataset cargado exitosamente. Se leyeron {len(sesiones)} sesiones.")
            except Exception as e:
                print(f"\n[ERROR] Falló la carga: {e}")
        elif opcion == "2":
            if not sesiones:
                print("\n[!] Primero debe cargar el dataset (Opción 1).")
                continue
            glob = calcular_estadisticas_globales(sesiones)
            print("\n--- ESTADÍSTICAS GLOBALES ---")
            print(f"Total de sesiones: {glob['total_sesiones']}")
            print(f"Ping promedio global: {glob['ping_promedio']} ms")
            print(f"Duración media de partida: {glob['duracion_promedio']} min")
            print(f"Partidas de alta competencia: {glob['porcentaje_competitivas']}%")
        elif opcion == "3":
            if not sesiones:
                print("\n[!] Primero debe cargar el dataset (Opción 1).")
                continue
            regionales = analizar_por_servidor(sesiones)
            print("\n--- RENDIMIENTO POR SERVIDOR ---")
            for servidorees, d in regionales.items():
                print(f"• {servidorees}: {d['cantidad']} partidas | Ping: {d['ping_promedio']} ms | FPS: {d['fps_promedio']}")
        elif opcion == "4":
            if not sesiones:
                print("\n[!] Primero debe cargar el dataset (Opción 1).")
                continue
            frec, crit = clasificar_incidentes(sesiones)
            print("\n--- DISTRIBUCIÓN DE SEGURIDAD ---")
            for estado, cant in frec.items():
                print(f"• {estado}: {cant} sesiones")
            print(f"\nSe detectaron {len(crit)} sesiones CRÍTICAS. (Ver detalle completo en reporte TXT).")
        elif opcion == "5":
            if not sesiones:
                print("\n[!] Primero debe cargar el dataset (Opción 1).")
                continue
            exportar_reporte(sesiones, RUTA_REPORTE)
            print(f"\n[OK] Reporte exportado exitosamente en: {RUTA_REPORTE}")
        elif opcion == "6":
            print("\nSaliendo del monitor. ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción inválida. Ingrese un número del 1 al 6.")

if __name__ == "__main__":
    main()