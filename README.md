# Transferencias de Delegaciones

El script proporcionado realiza un análisis del historial de transferencias en la blockchain de Hive para uno o un conjunto de usuarios específicos. Utiliza la biblioteca Beem para interactuar con la blockchain y obtener los datos de transferencia. El script lee los nombres de usuario desde un archivo de texto, establece una conexión a la blockchain de Hive y recopila información sobre las transferencias de cada usuario, incluyendo la cantidad de HIVE y HBD enviados y recibidos. Luego, genera tablas y gráficas que resumen estos datos tanto a nivel de usuarios como mensualmente. Las tablas se guardan en archivos de texto, y las gráficas se guardan como imágenes. El script también utiliza la biblioteca dotenv para cargar variables de entorno desde un archivo .env y la biblioteca matplotlib para la generación de gráficas.

## Pasos de preparación del proyecto

Sigue estos pasos para preparar y ejecutar el proyecto:

1. Clona el repositorio en tu máquina local:

### Clonar con SSH:

```
git clone git@gitlab.com:alberto0torrealba/transfer-history.git
```

### Clonar con HTTPS:

```
git clone https://gitlab.com/alberto0torrealba/transfer-history.git
```

2. Entra a la carpeta del proyecto:

```
cd transfer-history
```

3. Crea un entorno virtual para el proyecto:

```
python -m venv env

ó

python3 -m venv env
```

4. Activa el entorno virtual:

- En Windows:

```
env\Scripts\activate
```

- En Linux o macOS:

```
source env/bin/activate
```

5. Instala las dependencias del proyecto desde el archivo `requirements.txt`:

```
pip install -r requirements.txt
```

6. Renombra el archivo `.env-example` a `.env` y configura las variables de entorno según tus necesidades. Asegúrate de proporcionar los valores correctos para las variables relacionadas con los nodos para hacer la conexión de la blockchain de Hive y la fecha a partir de la cual se extraeran los datos. Asegúrate de proporcionar la fecha de inicio en el formato correcto, en este caso, `YYYY-MM-DD`.

## Uso del proyecto

Una vez que hayas configurado el entorno y las variables de entorno, puedes ejecutar el proyecto. El archivo `main.py` contiene toda la lógica que extraeré de la blockchain de Hive todos los datos necesarios para analizar y generar las listas que contendrá la información del historial de transferencias.

Puedes ejecutar el proyecto de la siguiente manera:

```
python main.py
```

El resultado son las tablas y gráficas que resumen estos datos tanto a nivel de usuarios como mensualmente

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras errores, mejoras o nuevas características que se puedan agregar al proyecto, no dudes en enviar una solicitud de extracción.
También puedes dejar un comentario en mi blog, [ver aquí](https://ecency.com/hive-139531/@alberto0607/script-en-python-analisis-de)

## Licencia

Este proyecto se ofrece bajo los principios del código abierto, lo que significa que puedes utilizarlo, modificarlo y distribuirlo de acuerdo con las libertades que ofrece este tipo de licencias. Se proporciona sin garantía alguna, y la responsabilidad recae en el usuario que lo utilice. Te invitamos a aprovechar al máximo las ventajas del código abierto y a contribuir a su comunidad.
