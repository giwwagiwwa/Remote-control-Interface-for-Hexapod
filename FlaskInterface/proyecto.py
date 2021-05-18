from flask import Flask, url_for, request
from flask.templating import render_template
import bluetooth

app = Flask(__name__)
#con esto le decimos al flask que puede buscar las templates y static en las carpetas por defecto

#estado bt
pos_estado_bt = {
    '0': 'Desconectado',
    '1': 'Conectando',
    '2': 'Conectado'
}
estado_bt = pos_estado_bt['0']

#lista de los posts de la web (diccionarios)
offsets_servos = [
    {
        'id': 1,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    },{
        'id': 2,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    },{
        'id': 3,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    },{
        'id': 4,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    },{
        'id': 5,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    },{
        'id': 6,
        'Femur': 0,
        'Coxa': 0,
        'Tibia': 0
    }
]

#listas de articulaciones y servos
artic = ['Coxa','Femur','Tibia']
servos = [1,2,3,4,5,6]

#mensaje de error
err_msg = ''

#selecciones
articselected = ''
servoselected = 0

def conectar_bt():
    global estado_bt
    estado_bt = pos_estado_bt['1']

#modifica la función ruta con parametros nuestros sin tener que reescribir (decorator)
@app.route("/")#rutas del browser
@app.route("/home")#ambas rutas llevan a la misma función hello()
def home():
    return render_template('home.html',title='Hexapod Web Server', offsets=offsets_servos) #le pasamos las variables a la plantilla

@app.route("/servoffset",methods=['POST','GET'])#ambas rutas llevan a la misma función hello()
def servoffset():
    #lista articulaciones
    if request.method == 'POST':
        if "conectarbt" in request.form:
            conectar_bt()
    return render_template('servoffset.html', 
                            title='Control offsets',
                            offsets=offsets_servos, 
                            estadobt=estado_bt,
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)

@app.route("/incdec",methods=['POST','GET'])
def incdec():
    if "inc5" in request.form:
        incrementar_offset()
    elif "dec5" in request.form:
        decrementar_offset()
    return render_template('servoffset.html', 
                            title='Control offsets',
                            offsets=offsets_servos, 
                            estadobt=estado_bt,
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)     

def incrementar_offset():
    print("inc")
    global articselected, servoselected
    offsets_servos[servoselected-1][articselected] +=5


def decrementar_offset():
    print("dec")
    global articselected, servoselected
    offsets_servos[servoselected-1][articselected] -=5

@app.route("/about")#rutas del browser
def about(): #hay que cambiar la función
    return render_template('about.html', title='About')

@app.route("/selectservo", methods=['GET','POST'])
def recogerdato():
    #recoger datos del formulario
    global articselected, servoselected
    articselected = request.form.get('articulacion')
    servoselected = int(request.form.get('numservo'))
    #enviar al puerto serie
    print("enviar al puerto serie servo+articulacion")
    return render_template('servoffset.html', 
                    title='Control offsets',
                    offsets=offsets_servos, 
                    estadobt=estado_bt,
                    artic=artic,
                    servos=servos,
                    articselected=articselected,
                    servoselected=servoselected) 


@app.route("/cambiardato", methods=['GET','POST'])
def cambiardato():
    print("cambiardato")
    if request.method=='POST':
        #actualizar datos locales
        offsets_servos[servoselected-1][articselected] = int(request.form.get('useroffset'))
        #enviar al puerto serie
        print("actualizar puerto serie")
    return render_template('servoffset.html', 
                            title='Control offsets',
                            offsets=offsets_servos, 
                            estadobt=estado_bt,
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)  
       

#si lo ejecutamos con Python directamente el __name__ es igual a __main__ por lo que hará el .run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')