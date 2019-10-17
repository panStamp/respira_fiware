[< índice](INDEX.md)

# El reto

RESPIRA FIWARE es un dispositivo de medición de la calidad del aire diseñado para aplicaciones urbanas. Se trata de una evolución de versiones precedentes de RESPIRA, diseño llevado a cabo por la compañía [panStamp](http://www.panstamp.com) y en despliegue por parte de la comunidad desde el año 2013. Esta versión de RESPIRA ha sido creada en el marco del reto FIWARE IoT 2019 lanzado por la [Diputación de Badajoz](https://www.dip-badajoz.es/) y [Telefónica](https://www.telefonica.com/en/) por medio de [FIWARE Space](https://www.fiware.space/).

# FIWARE

FIWARE es un estándar internacional creado para convertirse en el núcleo de cualquier solución IoT y así asegurar interoperabilidad entre plataformas IoT. Está basado en tecnologías tan populares como HTTP y MongoDB y se apoya en una arquitectura M2M bien definida, donde el Orion Context Broker, la pieza central dentro de esta arquitectura, gestiona informaciones provenientes de múltiples sistemas IoT heterogéneos.

FIWARE ha sido desplegado en multitud de proyectos Smart City por todo el mundo y es compatible con docenas de tecnologías IoT y plataformas de gestión y análisis de datos. RESPIRA FIWARE es capaz de transmitir niveles de contaminación del aire a cualquier plataforma FIWARE por medio de un [agente HTTP UltraLight](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html).

Por favor, visite la [página oficial FIWARE](https://www.fiware.org/) para obtener más información acerca de esta tecnología.

# Estación RESPIRA

La composición de las estaciones RESPIRA es sencilla. El núcleo, un SoC ESP32, lee periodicamente temperatura, humedad, concentraciones de partículas y de NO2 de tres sensores distintos. Las lecturas son entonces almacenadas y procesadas en por el microcontrolador antes de ser transmitidas hacia la plataforma FIWARE. La configuración por defecto dentro de la programación del dispositivo RESPIRA está diseñada para transmitir contra la _plataforma IoT medioambiental RESPIRA_ aunque usuarios y desarrolladores pueden apuntar hacia cualquier otra plataforma compatible con FIWARE.

Este proyecto consta de todas las fuentes e instrucciones necesarias para construir, programar y desplegar estaciones RESPIRA. Pueden visitar [esta página](RESPIRA_STATION.md) para saber más acerca de la composición y funcionamiento del hardware RESPIRA y de cómo construir su propia estación.

# Plataforma IoT medioambiental RESPIRA

La _Plataforma IoT medioambiental RESPIRA_ es otra iniciativa abierta de [Diputación de Badajoz](https://www.dip-badajoz.es/) y de [Telefónica](https://www.telefonica.com/en/) basada en FIWARE y creada para recoger, representar y explotar datos provenientes de distintas fuentes de datos IoT mediambientales dentro de la provincia española de Badajoz. Esta plataforma on-line ha sido también desarrollada por la empresa [panStamp](http://www.panstamp.com) y forma parte del reto FIWARE IoT 2019 ganado por la compañía.

Visite [esta página](RESPIRA_PLATFORM.md) par saber más acerca de esta plataforma.

