# Iknelia API
Para correr localmente de manera correcta, necesitas tener instalado el SDK de Google Cloud y además un proyecto en la plataforma con la API de speech to text permitido, para hacer esto necesitas hacer (una vez que ya instalaste el SDK de GCP y ya tienes configurado tu proyecto dentro de tu terminal):

## Acceso a la API de Google
1. Crear la variabel de entorno `PROJECT_ID`, esto lo usa la API de google internamente:
```bash
export PROJECT_ID=$(gcloud config get-value core/project)
```

2. Crear un nuevo servicio para acceder a la API (Sólo la primera vez)
```bash
gcloud iam service-accounts create my-stt-sa \
  --display-name "my stt service account"
```

3. Crear las credenciales para el código de Python en un archivo (en mi caso estarán guardadas en `~/key.json`)
```bash
gcloud iam service-accounts keys create ~/key.json \
  --iam-account my-stt-sa@${PROJECT_ID}.iam.gserviceaccount.com
```

4. Y ahora solo tenemos que consumir las credenciales desde nuestro archivo y guardarlas en una variable de entorno. Siempre tienes que tener esta variable con la información correcta, por lo que, si cada que cierras tu terminal se borran las variables de entorno que creaste (como a mí), tendrás que escribir esto cada vez que abras la terminal y quieras correr la api:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json
```

## Ejecutar código de manera local
1. Crea un entorno de desarrollo y activarlo, por ejemplo:
```bash
python3 -m venv venv
./venv/bin/activate #WSL
```

2. Instalar los requerimientos del `requirements.txt`
```bash
pip install -r requirements.txt
```

3. Esto es un servidor de FastAPI que se puede ejecutar de la siguiente manera:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

4. Puedes acceder a la documentación interactiva en el siguiente link `http://127.0.0.1:8000/docs` y jugar con ella, nota que el código tiene un bandera casi al principio:
```python
requesting_key = False
```
que quiere decir que para usar la API necesitas o no cierta llave que asigné para producción, para obtener esta llave comunícate con: [Bubu](https://www.instagram.com/david_bubu73/). Pero si la dejas como False, no debería de haber ningún problema para local.


# Cliente
Agregué un archivo `client.py` para hacer tests sobre la API mientras corre, puedes ejecutar este código para probar que tu local funciona bien. Checando cambios