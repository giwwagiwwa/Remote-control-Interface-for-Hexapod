import time, subprocess as sp, os, serial
from flask import Flask, request
from flask.templating import render_template


app = Flask(__name__)
#con esto le decimos al flask que puede buscar las templates y static en las carpetas por defecto

#parametros Bt
hc06_direccion = '00:20:12:08:42:2F'
#Configuración del Puerto Serie
serie_port = '/dev/rfcomm0'
serie_baud = 38400

#lista de los offsets iniciales (diccionarios)
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


#selecciones
articselected = ''
servoselected = 0


#modifica la función ruta con parametros nuestros sin tener que reescribir (decorator)
@app.route("/")#rutas del browser
@app.route("/home")#ambas rutas llevan a la misma función hello()
def home():
    return render_template('home.html',title='Hexapod Web Server', offsets=offsets_servos) #le pasamos las variables a la plantilla

@app.route("/preservoffset",methods=['POST','GET'])
def preservoffset():
    #comprobar conexión bluetooth
    stdoutdata = sp.getoutput("hcitool con")
    time.sleep(1)
    #si estamos conectados abrimos puerto serie, entramos modo offset y cargamos la pagina
    if hc06_direccion in stdoutdata.split():
        print("Conectado a BT")
        #intentamos abrir el puerto serie
        try:
            # ser= serial.Serial(port=serie_port, baudrate=serie_baud)
            # #enviamos caracter para entrar al modo servo offset
            # ser.write(b"O")
            # time.sleep(1)
            # bytes_recibidos = ser.readline() #linea cmd eok...
            # bytes_recibidos = ser.readline().decode('utf-8').strip().split(",") #datos
            # ser.close()
            bytes_recibidos = ['-1','-2','-3','-4','-5','-6','-7','-8','-9','-10','-11','-12','-13','-14','-15','-16','-17','-18',]
            #ponemos los datos recibidos en la estructura local
            indice = 0
            for servo in offsets_servos:
                servo['Coxa'] = int(bytes_recibidos[indice])
                servo['Femur'] = int(bytes_recibidos[indice+1])
                servo['Tibia'] = int(bytes_recibidos[indice+2])
                indice +=3
        except:
            print("error abriendo puerto serie")
        #cargamos la pagina
        return render_template('servoffset.html', 
                                title='Control offsets',
                                offsets=offsets_servos,
                                artic=artic,
                                servos=servos,
                                articselected=articselected,
                                servoselected=servoselected)
    #si no estamos conectados cargamos la página de preservooffset
    return render_template('preservoffset.html', title='Control offsets', estado='Error conectando')


@app.route("/saliroffset",methods=['POST','GET'])
def saliroffset():
    ser= serial.Serial(port=serie_port, baudrate=serie_baud)
    ser.write(b"$")
    time.sleep(1)
    if "guardar" in request.form:
        print("Guardar offsets")
        ser.write(b"S")
    elif "descartar" in request.form:
        print("Descartar offsets")
        ser.write(b"N")
    ser.close()
    return render_template('home.html',title='Hexapod Web Server', offsets=offsets_servos)


@app.route("/servoffset",methods=['POST','GET'])
def servoffset():
    #lista articulaciones
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
    # ser= serial.Serial(port=serie_port, baudrate=serie_baud)   
    if "inc5" in request.form: #incrementar 5
        offsets_servos[servoselected-1][articselected] +=5
        # ser.write(b"+") 
    elif "dec5" in request.form: #decrementar 5
        offsets_servos[servoselected-1][articselected] -=5
        # ser.write(b"-")
    # ser.close()
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
    #String con la articulación y el numero de servo
    dato = str(servoselected-1)+articselected[0]
    #enviar al puerto serie dato
        # ser= serial.Serial(port=serie_port, baudrate=serie_baud)
        # ser.write(b"$")
        #---------------------
        # only an example, you can choose a different encoding
        #bytes('example', encoding='utf-8')
        # ser.close()
    print(dato)
    return render_template('servoffset.html', 
                    title='Control offsets',
                    offsets=offsets_servos,
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
                            artic=artic,
                            servos=servos,
                            articselected=articselected,
                            servoselected=servoselected)  
       

#si lo ejecutamos con Python directamente el __name__ es igual a __main__ por lo que hará el .run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')