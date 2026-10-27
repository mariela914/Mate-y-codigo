# =====================================================================
# PARTE INTEGRANTE 2: Analista de Métricas (Consignas 2 y 3)
# =====================================================================

def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    """Consigna 2: Calcula métricas consolidadas de operación."""
    total = len(sesiones)
    if total == 0:
        return {
            "total_sesiones": 0,
            "ping_promedio": 0.0,
            "duracion_promedio": 0.0,
            "porcentaje_competitivas": 0.0
        }

    acum_ping = 0
    acum_duracion = 0.0
    conteo_competitivas = 0

    for s in sesiones:
        acum_ping += s["ping_promedio"]
        acum_duracion += s["duracion_minutos"]
        if s["tipo_partida"] in ("Competitiva", "Torneo"):
            conteo_competitivas += 1

    return {
        "total_sesiones": total,
        "ping_promedio": round(acum_ping / total, 2),
        "duracion_promedio": round(acum_duracion / total, 2),
        "porcentaje_competitivas": round((conteo_competitivas / total) * 100, 2)
    }


def analizar_por_servidor(sesiones: list[dict]) -> dict:
    """Consigna 3: Agrupación dinámica por región con diccionario acumulador."""
    if not sesiones:
        return {}

    acumuladores = {}
    for s in sesiones:
        srv = s["servidor"]
        if srv not in acumuladores:
            acumuladores[srv] = {
                "cantidad": 0,
                "acum_ping": 0,
                "acum_fps": 0
            }
        acumuladores[srv]["cantidad"] += 1
        acumuladores[srv]["acum_ping"] += s["ping_promedio"]
        acumuladores[srv]["acum_fps"] += s["fps_promedio"]

    resumen = {}
    for srv, datos in acumuladores.items():
        cant = datos["cantidad"]
        resumen[srv] = {
            "cantidad": cant,
            "ping_promedio": round(datos["acum_ping"] / cant, 2),
            "fps_promedio": round(datos["acum_fps"] / cant, 2)
        }
    return resumen


# =====================================================================
# PARTE INTEGRANTE 3: Auditor de Seguridad (Consigna 4)
# =====================================================================

def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    """
    Consigna 4: Motor heurístico determinístico de seguridad.
    Retorna (frecuencias, lista_de_criticos).
    """
    frecuencias = {"Normal": 0, "Sospechoso": 0, "Crítico": 0}
    eventos_criticos = []

    for s in sesiones:
        rep = s["reportes_trampa"]
        intentos = s["intentos_fallidos"]
        ping = s["ping_promedio"]

        # Regla 1: Crítico
        if rep >= 3 or intentos >= 4:
            frecuencias["Crítico"] += 1
            if rep >= 3 and intentos >= 4:
                motivo = f"Exceso de reportes por trampa ({rep}) e intentos fallidos ({intentos})"
            elif rep >= 3:
                motivo = f"Exceso de reportes por trampa ({rep})"
            else:
                motivo = f"Ataque de fuerza bruta en login ({intentos} intentos fallidos)"

            eventos_criticos.append({
                "id_sesion": s["id_sesion"],
                "jugador_id": s["jugador_id"],
                "servidor": s["servidor"],
                "motivo": motivo
            })

        # Regla 2: Sospechoso
        elif (ping > 200 and intentos >= 2) or (rep == 2):
            frecuencias["Sospechoso"] += 1

        # Regla 3: Normal
        else:
            frecuencias["Normal"] += 1

    return frecuencias, eventos_criticos