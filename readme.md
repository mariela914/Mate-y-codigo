# GameSec Monitor — Telemetría de Servidores y Detección de Incidentes

Trabajo Práctico Integrador para la materia **Taller de Programación I** (Ciclo Lectivo 2026).  
Instituto de Tecnología e Ingeniería — **Universidad Nacional de Hurlingham (UNAHUR)**. \
![unahur](./unahur.jpeg)


---

## 👥 Presentación del Grupo

* **Nombre del Grupo:** `Mate y código`

### Integrantes del Equipo

| Rol | Nombre y Apellido | DNI | Carrera |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | *Mariela Alejandra Oberg* | *26591452* | *Tecnicatura Universitaria en Inteligencia Artificial* |
| **Integrante 2** | *Talia Rodrigues* | *37141532* | *Licenciatura en Desarrollo de Videojuegos y Simulaciones* |
| **Integrante 3** | *Esmeralda jimenez* | *94430052* | * Programación de videojuegos* |
| **Integrante 4** | *Lorena Olivella* | *31045365* | *Tecnicatura Universitaria en Inteligencia Artificial* |

---

## 📌 ¿Qué es este código y para qué sirve?

**GameSec Monitor** es una herramienta de auditoría desarrollada en Python estándar, diseñada para el análisis de telemetría de servidores multijugador y la detección temprana de incidentes operativos y de ciberseguridad.

En la industria de los videojuegos en línea y los servicios en la nube, los servidores generan continuamente registros (*logs*) de las partidas activas. Este sistema tiene como finalidad:

1. **Ingestar y sanear datos:** Leer registros brutos del dataset `gamesec_logs.csv`, validando su integridad física y convirtiendo los datos a tipos numéricos nativos (`int`, `float`).
2. **Medir la calidad de servicio (QoS):** Calcular métricas operativas globales de rendimiento, como el promedio general de latencia (`ping_promedio`), la duración media de las sesiones y la proporción de partidas de alto rendimiento (`Competitiva` y `Torneo`).
3. **Analizar la estabilidad regional:** Agrupar dinámicamente las sesiones por región de servidor (`SA-BuenosAires`, `SA-SaoPaulo`, `NA-Virginia`, `EU-Frankfurt`) mediante diccionarios acumuladores, monitoreando latencia y fluidez gráfica (`fps_promedio`).
4. **Detectar anomalías y ciberataques:** Implementar un **motor heurístico determinístico** basado en reglas de negocio para clasificar automáticamente las sesiones en tres niveles:
   * **Normal:** Comportamiento estándar sin indicadores de riesgo.
   * **Sospechoso:** Sesiones con indicios de *lag switching* (latencia $> 200\text{ ms}$ con intentos fallidos acumulados) o denuncias previas por trampas.
   * **Crítico:** Sesiones con alto volumen de reportes por trampas ($\ge 3$) o indicios de ataques de fuerza bruta en autenticación ($\ge 4$ intentos fallidos).
5. **Auditoría estructurada:** Exportar un reporte consolidado en archivo de texto (`reporte_gamesec.txt`) con conclusiones técnicas del equipo.

---

## 🏗️ Arquitectura Modular del Software

El proyecto respeta de forma estricta el principio de separación de responsabilidades y modularización en exactamente tres componentes:

```
mate_y_codigo/
│
├── gamesec_logs.csv          # Dataset provisto con 150 registros de telemetría
├── carga.py                  # Módulo de lectura, casteo y validación de precondiciones
├── procesamiento.py          # Módulo de lógica: estadísticas globales, servidor y motor heurístico
├── main.py                   # Interfaz de usuario (consola) y generación del reporte final
├── reporte_gamesec.txt       # Reporte consolidado exportable (generado por la Opción 5)
└── README.md                 # Documentación técnica y datos del equipo
```

### Funciones Principales

* **`carga.py`:**
  * `cargar_telemetria(ruta_archivo: str) -> list[dict]`: Abre el archivo con `csv.DictReader`, verifica que el archivo exista (`os.path.exists`) y contenga datos, casteando cada columna a su tipo primitivo.
* **`procesamiento.py`:**
  * `calcular_estadisticas_globales(sesiones: list[dict]) -> dict`: Totaliza registros y calcula promedios generales y tasa de partidas competitivas.
  * `analizar_por_servidor(sesiones: list[dict]) -> dict`: Implementa diccionarios acumuladores dinámicos para agrupar métricas por región sin prefijar listas fijas de servidores.
  * `clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]`: Evalúa la jerarquía de reglas de seguridad y retorna la frecuencia de estados junto a la lista detallada de incidentes críticos.
* **`main.py`:**
  * `exportar_reporte(sesiones, ruta_salida)`: Escribe el archivo estructurado con formato tabular.
  * `main()`: Ciclo interactivo `while True` con control de flujo y prevención de operaciones sin carga previa.

---

## ⚙️ Requisitos y Ejecución

### Requisitos Técnicos
* **Python 3.10** o superior.
* **Sin dependencias externas:** No utiliza `pandas`, `numpy` ni paquetes de terceros; utiliza únicamente librerías estándar nativas (`csv`, `os`, `sys`).

### Instrucciones de Ejecución

1. **Abrir la terminal** en la carpeta donde residen los archivos del proyecto.
2. Asegurarse de que el archivo `gamesec_logs.csv` esté ubicado en la misma carpeta que los scripts `.py`.
3. Ejecutar el script principal:

```bash
python3 main.py
```

### Opciones del Menú de Control

Al iniciar el programa se presentará el panel interactivo:
```
=========================================
      GAMESEC MONITOR - PANEL DE CONTROL
=========================================
1. Cargar y validar dataset
2. Ver estadísticas globales de servidores
3. Ver rendimiento por región de servidor
4. Auditar incidentes de seguridad (Críticos y Sospechosos)
5. Exportar reporte consolidado (reporte_gamesec.txt)
6. Salir
=========================================
```

* **Paso indispensable:** Seleccionar primero la **Opción 1** para cargar el dataset en memoria. Las opciones 2 a 5 cuentan con validaciones que impedirán su ejecución si los datos no han sido leídos previamente.
