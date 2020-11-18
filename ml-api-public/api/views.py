# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
)
import middleware

router = Blueprint('app_name',
                   __name__,
                   template_folder='templates')


@router.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'text': None,
        'prediction': None,
        'score': None,
        'success': False
    }
    # Obtiene la sentencia ingresada por el usuario en el frontend
    text_data = request.form.get('text_data')

    if text_data:
        prediction, score = middleware.model_predict(text_data)
        context = {
        'text': text_data,
        'prediction': prediction,
        'score': score,
        'success': True
        }
        #################################################################
        # COMPLETAR AQUI: Envie el texto ingresado para ser procesado
        # por nuestra función middleware.model_predict.
        # Luego con los resultados obtenidos, complete el diccionario
        # "context" para mostrar la predicción en el frontend.
        #################################################################
       #################################################################
    return render_template('index.html', context=context)


#@router.route('/feedback', methods=['GET', 'POST'])
#def feedback():
#    """
#    [Práctico 2 - No completar]
#    Esta función nos permitirá darle feedback a nuestra API
#    para los casos en los que clasificamos una oración
#    con un sentimiento erroneo.
#    """
#    context = {
#        'text': None,
#        'prediction': None,
#        'score': None,
#        'success': False
#    }
#return render_template('index.html', context=context)

@router.route('/predict', methods=['POST'])
def predict():

    # Respuesta inicial
    rpse = {
        'success': False,
        'prediction': None,
        'score': None
    }

    # Nos aseguramos que el método sea correcto y tengamos datos
    # para procesar
    if request.method == 'POST' and request.args.get('text'):
        text_data = request.args.get('text')
        prediction, score = middleware.model_predict(text_data)
        rpse = {
        'success': True,
        'prediction': prediction,
        'score': score
        }
        return jsonify(rpse)
        #################################################################
        # COMPLETAR AQUI: Extraiga la sentencia a procesar y utilice la
        # función middleware.model_predict para obtener el sentimiento
        # de la misma. Complete los campos de "rpse" con los valores
        # obtenidos.
        #################################################################
        #raise NotImplementedError
        #################################################################

    return jsonify(rpse), 400
