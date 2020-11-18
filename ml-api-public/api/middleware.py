# -*- coding: utf-8 -*-
import redis
import uuid
import json
import time
########################################################################
# COMPLETAR AQUI: Crear conexion a redis y asignarla a la variable "db".
########################################################################
db = redis.Redis(host='redis', port=6379,db=0)
########################################################################


def model_predict(text_data):
    
    """
    Esta función recibe sentencias para analizar desde nuestra API,
    las encola en Redis y luego queda esperando hasta recibir los
    resultados, qué son entonces devueltos a la API.

    Attributes
    ----------
    text_data : str
        Sentencia para analizar.

    Returns
    -------
    prediction : str
        Sentimiento de la oración. Puede ser uno de: "Positivo",
        "Neutral" o "Negativo".
    score : float
        Valor entre 0 y 1 que especifica el grado de positividad
        de la oración.
    """
    prediction = None
    score = None

    #################################################################
    # COMPLETAR AQUI: Crearemos una tarea para enviar a procesar.
    # Una tarea esta definida como un diccionario con dos entradas:
    #     - "id": será un hash aleatorio generado con uuid4 o
    #       similar, deberá ser de tipo string.
    #     - "text": texto que se quiere procesar, deberá ser de tipo
    #       string.
    # Luego utilice rpush de Redis para encolar la tarea.
    #################################################################
    job_id = str(uuid.uuid4())
    job_data = {
            'id': job_id,
            'text': text_data
            }
    #################################################################
    db.rpush('service_queue',json.dumps(job_data))
    # Iterar hasta recibir el resultado
    while True:
        response = db.get(job_id)
        if response is not None:
            response = json.loads(response.decode('utf-8'))
            prediction = response['prediction']
            score = response['score']
        time.sleep(1)

    return prediction, score
