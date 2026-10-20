import csv

def cargar_telemetria(ruta_archivo: str):

    lista_telemetria = []
    
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        dato = csv.DictReader(archivo)
        
        for jugador in dato:
            jugador["id_sesion"] = int(jugador["id_sesion"])
            jugador["ping_promedio"] = int(jugador["ping_promedio"])
            jugador["fps_promedio"] = int(jugador["fps_promedio"])
            jugador["duracion_minutos"] = float(jugador["duracion_minutos"])
            jugador["intentos_fallidos"] = int(jugador["intentos_fallidos"])
            jugador["reportes_trampa"] = int(jugador["reportes_trampa"])
            jugador["servidor"] = str(jugador["servidor"])
            jugador["jugador_id"] = str(jugador["jugador_id"])
            jugador["tipo_partida"] = str(jugador["tipo_partida"])

            lista_telemetria.append(jugador)
            
    if len(lista_telemetria) == 0:
        print("El archivo csv esta vacio y no tiene jugadores")
        
    return lista_telemetria


