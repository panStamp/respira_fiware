[< índice](INDEX.md)

# Índice de contenidos

- [RESPIRA tool](#respira-tool)
- [Configuración inicial](#configuracion-inicial)
- [Corrección manual por factor-offset](#correccion-manual-por-factor-offset)
- [Corrección automática por nivel cero](#correccion-automatica-por-nivel-cero)
- [Reset de los parámetros de calibración](#reset-de-los-parametros-de-calibracion)
- [Lectura de los parámetros de calibración](#lectura-de-los-parametros-de-calibracion)

# RESPIRA tool

RESPIRA tool es un programa en línea de comandos (terminal) desarrollado en Python 3.7 para enviar configuración y parámetros de calibración a cualquier estación remota RESPIRA por medio de FIWARE. Ya explicamos en [esta otra sección](RESPIRA_CALIBRATION.md) dos estrategias distintas de calibración: corrección manual por factor-offset y calibración automática por nivel cero. Los siguientes apartados emplean cada uno de estos métodos por medio del correspondiente comando.

# Configuración inicial

Antes de usar RESPIRA tool necesitamos introducir nuestro service path FIWARE. A todo usuario de la plataforma RESPIRA IoT medioambiental se el proporciona un service path, una región específica dentro del Context-Broker FIWARE donde confluyen todas la sinformaciones IoT. Los usuarios pueden encontrar su service path bajo su perfil en la plataforma.

Con el service path en mano, basta con ejecutar el siguiente comando:

```
python3 respira_tool.py --set-service-path /my_service_path
```

Este comando almacena el service path en un fichero de configuración, de modo que no necesitaremos volver a ejecutar el comando salvo que que queramos cambiar a un service path distinto (distinto usuario). Podemos comprobar el service path vigente en todo momento mediante este otro comando:

```
python3 respira_tool.py --show-service-path
```

devolviendo el service path actualmente en curso:

```
/my_service_path
```

# Corrección manual por factor-offset

Asumiendo que ya se dispone de los parámetros de corrección (factor y offset), su transmisión a FIWARE sólo requiere de la ejecución de este comando:

```
python3 respira_tool.py --calibrate no2 -d RESPIRA_XXXXXXXXXXXX -f 1.0021 -o -12.687
```

Donde no2 es la lectura que deseamos corregir, RESPIRA_XXXXXXXXXXXX es el ID de la estación RESPIRA, 1.0021 el factor de corrección (o ganancia) y -12.687 es el offset de corrección. Los contaminantes soportados por esta versión del software son: no2, pm1.0, pm2.5, pm4.0 y pm10, de forma que podemso enviar calibraciones individuales para cada uno de los gases y diámetros de partículas.

```
python3 respira_tool.py --calibrate pm2.5 -d RESPIRA_XXXXXXXXXXXX -f 1.0016 -o 5.342
```

Las estaciones RESPIRA consultan el Context-Broker FIWARE de forma periódica cada hora con el fin de obtener los parámetros de configuración. Una vez obtenidos estos parámetros, la estación empieza a aplicar las correcciones sobre las siguientes lecturas, de forma que las correcciones se hacen visibles tras la siguiente transmisión una hora más tarde.

# Corrección automática por nivel cero

Esta estrategia permite a la estación restar un offset de nivel cero a cada lectura. Este nivel cero corresponde al valor mínimo detectado en el intervalo de los últimos 10 días. Podemos habilitar esta funcionalidad tanto para el sensor de NO2 como de partículas (SPS30). Es necesario reseñar que no es posible activar este tipo de compensación únicamente para un tipo de partícula sino que hay que hacerlo para todos los diámetros a los que el dispositivo SPS30 es sensible.

Estos comandos habilitan la calibración automática por nivel cero para cada sensor:

```
python3 respira_tool.py --enable-zero-calibration no2 -d RESPIRA_XXXXXXXXXXXX
python3 respira_tool.py --enable-zero-calibration pm -d RESPIRA_XXXXXXXXXXXX
```

y lo mismo para deshabilitar la funcionalidad:


```
python3 respira_tool.py --disable-zero-calibration no2 -d RESPIRA_XXXXXXXXXXXX
python3 respira_tool.py --disable-zero-calibration pm -d RESPIRA_XXXXXXXXXXXX
```

Tal y como se indica anteriormente, estos cambios surgen efecto a partir de la siguiente transmisión, una hora más tarde.

# Reset calibration settings

Digamos que queremos volver a los parámetros de configuración por defecto:

- Calibración automática por nivel cero deshabilitada para todos los sensores.
- Factor de corrección = 1 y offset = 0 para todos los contaminantes.

Podemos ejecutar este comando para volver a los valores por defecto:

```
python3 respira_tool.py --reset-calibration -d RESPIRA_XXXXXXXXXXXX
```

# Lectura de los parámetros de calibración

La opción _--read-calibration_ permite mostrarlos valores actuales de calibración de cualquier estación RESPIRA:

```
python3 respira_tool.py --read-calibration -d RESPIRA_XXXXXXXXXXXX
```

Respuesta de FIWARE:

```
Calibration settings for device :RESPIRA:RESPIRA_807D3AF39E18
NO2 automatic zero-calibration: enabled
NO2 correction factor (gain): 1
NO2 correction offset: 0
PM sensor automatic zero-calibration: enabled
PM1.0 correction factor (gain): 1
PM1.0 correction offset: 0
PM2.5 correction factor (gain): 1
PM2.5 correction offset: 0
PM4.0 correction factor (gain): 1
PM4.0 correction offset: 0
PM10 correction factor (gain): 1
PM10 correction offset: 0
```

