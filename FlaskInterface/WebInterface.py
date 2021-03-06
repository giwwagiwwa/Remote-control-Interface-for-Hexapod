#*******************
#Autor: Miquel EJ  *
#     2021         *
#*******************


import time, subprocess as sp, serial
from flask import Flask, request
from flask.templating import render_template


app = Flask(__name__)
#Carpetas templates y static por defecto


#parametros Bt
hc06_direccion = '00:20:12:08:42:2F'
#Configuración del Puerto Serie
serie_port = '/dev/rfcomm0'
serie_baud = 38400


#lista de los offsets iniciales
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


#listas de nombres de articulaciones y servos
artic = ['Coxa','Femur','Tibia']
servos = [1,2,3,4,5,6]


#selecciones
articselected = ''
servoselected = 0


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/preservoffset",methods=['POST','GET'])
def preservoffset():
    #comprobar conexion bluetooth
    stdoutdata = sp.getoutput("hcitool con")
    time.sleep(1)
    #si estamos conectados entramos modo offset
    if hc06_direccion in stdoutdata.split():
        print("Conectado a BT")
        #intentamos abrir el puerto serie
        try:
            ser= serial.Serial(port=serie_port, 
                               baudrate=serie_baud)
            #enviamos caracter para entrar al modo servo offset
            ser.write(b"O")
            time.sleep(1)
            bytes_recibidos = ser.readline() #linea cmd eok...
            #separar los valores por comas
            bytes_recibidos = ser.readline().decode('utf-8').strip().split(",")
            ser.close()
        except:
            print("Error abriendo puerto serie")

        #Guardamos los datos recibidos en la estructura local
        indice = 0
        for servo in offsets_servos:
            servo['Coxa'] = int(bytes_recibidos[indice])
            servo['Femur'] = int(bytes_recibidos[indice+1])
            servo['Tibia'] = int(bytes_recibidos[indice+2])
            indice +=3
        #Cargamos la pagina
        return render_template('servoffset.html', 
                                title='Control offsets',
                                offsets=offsets_servos,
                                artic=artic,
                                servos=servos,
                                articselected=articselected,
                                servoselected=servoselected)
    #si no estamos conectados cargamos la página de preservooffset
    return render_template('preservoffset.html', title='Control offsets')


@app.route("/saliroffset",methods=['POST','GET'])
def saliroffset():
    try:
        ser= serial.Serial(port=serie_port, baudrate=serie_baud)
        ser.write(b"$")
    except:
        print("Error abriendo puerto serie")
    time.sleep(1)
    if "guardar" in request.form:
        print("Guardar offsets")
        try:
            ser.write(b"Y")
        except:
            print("Error enviando dato al puerto serie")
    elif "descartar" in request.form:
        print("Descartar offsets")
        try:
            ser.write(b"N")
        except:
            print("Error enviando dato al puerto serie")
    try:
        ser.close()
    except:
        print("Error cerrando puerto serie")
    return render_template('home.html',title='Hexapod Web Server', offsets=offsets_servos)


@app.route("/servoffset",methods=['POST','GET'])
def servoffset():
    #cargar lista articulaciones, servos y offsets locales obtenidos en preservoffset.
    return render_template('servoffset.html', 
                            title='Control offsets',
                            offsets=offsets_servos,
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)


@app.route("/incdec",methods=['POST','GET'])
def incdec():
    global articselected, servoselected
    #abrimos puerto serie
    try:
        ser= serial.Serial(port=serie_port, baudrate=serie_baud)   
    except:
        print("Error abriendo puerto serie")
    if "inc5" in request.form: #incrementar 5
        offsets_servos[servoselected-1][articselected] +=5
        try:
            ser.write(b"+") 
        except:
            print("Error enviando caracter")
    elif "dec5" in request.form: #decrementar 5
        offsets_servos[servoselected-1][articselected] -=5
        try:
            ser.write(b"-") 
        except:
            print("Error enviando caracter")
    try:
        ser.close()
    except:
        print("Error cerrando puerto serie")
    return render_template('servoffset.html', 
                            title='Control offsets',
                            offsets=offsets_servos,
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)     


@app.route("/about")#rutas del browser
def about():
    return render_template('about.html', title='About')


@app.route("/selectservo", methods=['GET','POST'])
def recogerdato():
    #recoger datos del formulario
    global articselected, servoselected
    articselected = request.form.get('articulacion')
    servoselected = int(request.form.get('numservo'))
    #String con la articulacion y el numero de servo para seleccionarlo
    dato = str(servoselected-1)+articselected[0]
    #enviar al puerto serie dato
    try:
        ser= serial.Serial(port=serie_port, baudrate=serie_baud)
        ser.write(bytes(dato,encoding='utf-8'))
        print(dato) #por la consola de flask
        ser.close()
    except:
        print("Error abriendo puerto serie")

    return render_template('servoffset.html', 
                    title='Control offsets',
                    offsets=offsets_servos,
                    artic=artic,
                    servos=servos,
                    articselected=articselected,
                    servoselected=servoselected)   
       


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')