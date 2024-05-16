import datetime
from flask import Flask, render_template, request, redirect, url_for, render_template_string, make_response
import pymysql
from io import StringIO

app = Flask(__name__)

conexion = pymysql.connect(
    host="34.133.88.203",
    user="tecnologico",
    password="123456789",
    database="CONSULTAS_MEDICAS",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conexion.cursor()

# Ruta para la página de inicio de sesión y procesamiento del formulario de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    # HTML para la página de inicio de sesión
    inicio_sesion_html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inicio de Sesión</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #3498db; /* Color de fondo azul */
            }
            .container {
                width: 400px;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h2 {
                text-align: center;
                color: #333;
            }
            form {
                margin-top: 20px;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"],
            input[type="password"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                width: 100%;
                background-color: #4caf50; /* Color de fondo verde para el botón */
                color: #fff;
                font-weight: bold;
                padding: 10px 0;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049; /* Color de fondo verde oscuro cuando se pasa el mouse sobre el botón */
            }
            .error-message {
                color: red;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Bienvenido</h2>
            <form action="/" method="POST">
                <label for="username">Nombre de Usuario:</label>
                <input type="text" id="username" name="username">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password">
                <input type="submit" value="Iniciar Sesión">
            </form>
            {% if mensaje %}
            <p class="error-message">{{ mensaje }}</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']

        if username and password:  # Verificar si se ingresaron tanto el nombre de usuario como la contraseña
            # Consulta SQL para verificar las credenciales
            consulta = "SELECT nom_usuario FROM sesion WHERE nom_usuario=%s AND contra=%s"
            cursor.execute(consulta, (username, password))
            usuario = cursor.fetchone()

            if usuario:
                # Inicio de sesión exitoso, redireccionar al index
                
                return redirect(url_for('index', user=username))
            else:
                # Nombre de usuario o contraseña incorrectos, renderizar la página de inicio de sesión con un mensaje de error
                return render_template_string(inicio_sesion_html, mensaje="Nombre de usuario o contraseña incorrectos.")
        else:
            # Si falta el nombre de usuario o la contraseña, simplemente renderizar la página de inicio de sesión sin mensaje de error
            return render_template_string(inicio_sesion_html, mensaje="")
    else:
        # Método GET, mostrar página de inicio de sesión sin mensaje de error
        return render_template_string(inicio_sesion_html, mensaje="")



@app.route('/index')
def index():
    username = request.args.get('user')
    cursor.execute("SELECT Num_Doc FROM sesion WHERE nom_usuario=%s", (username,))
    NDoc = cursor.fetchone()
    NDoc = NDoc['Num_Doc']
    cursor.execute("SELECT concat(NombreD, ' ', SNombreD, ' ', ApellidoP, ' ', ApellidoM) AS Nombre FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (NDoc,))
    nom_doctor = cursor.fetchone()
    nom_doctor = nom_doctor['Nombre']  # Convertir a cadena de texto
    cursor.execute("SELECT Espec FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (NDoc,))
    Esp = cursor.fetchone()
    Esp = Esp['Espec']  # Convertir a cadena de texto
    cursor.execute("SELECT CEDProf FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (NDoc,))
    Ced = cursor.fetchone()
    Ced = Ced['CEDProf']  # Convertir a cadena de texto
    cursor.execute("SELECT Turno FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (NDoc,))
    Tur = cursor.fetchone()
    Tur = Tur['Turno']  # Convertir a cadena de texto
    html_content ='''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registro de Consultas Médicas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f0f0;
            }
            .container {
                display: flex;
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: #f2f2f2; /* Color de fondo para el área del doctor */
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .doctor-info {
                flex: 1;
                padding: 20px;
                background-color: #3498db; /* Color de fondo para el área del doctor */
                color: #fff; /* Color del texto */
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
                margin-top: 20px;
            }
            .button-container {
                text-align: center;
                margin-top: 20px;
            }
            .button-container a {
                display: inline-block;
                margin: 0 10px;
                padding: 15px 30px;
                background-color: #4caf50; /* Color de fondo para los botones */
                color: #fff; /* Color del texto */
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            }
            .button-container a:hover {
                background-color: #45a049; /* Color de fondo cuando se pasa el mouse sobre los botones */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="doctor-info">
                <h2>Bienvenido <b>Dr(a). <i>
    '''
    html_content += nom_doctor if nom_doctor else ""
    html_content += '''</i></b>
                </h2>
                <h3>Datos del doctor:</h3>
                <p><b>Especialidad:</b> <i>'''
    html_content += Esp if Esp else ""
    html_content += '''</i></p>
                <p><b>Cédula Profesional: </b><i>'''
    html_content += Ced if Ced else ""
    html_content += '''</i></p>
                <p><b>Turno:</b><i> '''
    html_content += Tur if Tur else ""
    html_content += '''</i></p>
            </div>
            <div class="button-container">
                <a href="/nueva_consulta/'''
    html_content += str(NDoc) if str(NDoc) else ""
    html_content += '''">Nueva Consulta</a>
                <!--<a href="/consultar_consultas/'''
    html_content += str(NDoc) if str(NDoc) else ""
    html_content += '''">Consultar Recetas</a> -->
            </div>
        </div>
    </body>
    </html>
    '''

    return html_content
# Función para obtener el valor de la base de datos
def obtener_ultimo_numero_consulta():    
    # Ejecutar una consulta SQL para obtener el último número de consulta
    cursor.execute("SELECT NumCons+1 AS Cons FROM CONSULTAS_MEDICAS.consulta ORDER BY NumCons DESC LIMIT 1")
    consulta_actual = cursor.fetchone()
    consulta_actual = str(consulta_actual['Cons'])
    # Retornar el último número de consulta
    return consulta_actual

@app.route('/nueva_consulta/<int:NDoc>', methods=['GET', 'POST'])
def nueva_consulta(NDoc):
    # Inicializar NumCons
    cursor.execute("SELECT concat(NumMed,' ', DenGen, ' ', FormaFar, ' ', Dosis) AS Medicamento FROM CONSULTAS_MEDICAS.medi")
    valores = cursor.fetchall()
    NumConsA = obtener_ultimo_numero_consulta()
    if request.method == 'POST':
        cursor.execute("SELECT NumCons+1 FROM CONSULTAS_MEDICAS.consulta ORDER BY NumCons DESC LIMIT 1")
        consulta_actual = cursor.fetchone()
        NumConsA = consulta_actual['NumCons+1']
        Fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Num_D = NDoc
        NombreP = request.form['NombreP']
        Edad = request.form['Edad']
        Peso = request.form['peso']
        Alergias = request.form['Alergias']
        Diag = request.form['Diag']
        
        # Insertar datos en la tabla 'consulta'
        consulta_sql_consulta = "INSERT INTO consulta (Fecha, Num_D, NombreP, Edad, Peso, Alergias, Diag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        datos_consulta = (Fecha, Num_D, NombreP, Edad, Peso, Alergias, Diag)

        cursor.execute(consulta_sql_consulta, datos_consulta)
        conexion.commit()

        # Obtener el número de medicamentos ingresados
        num_medicamentos = int(request.form['numTratamientos'])
        
        # Iterar sobre los medicamentos ingresados
        for i in range(num_medicamentos):
            nombre_medicamento = request.form[f'medi_{i}']
            medi = nombre_medicamento[0]
            dosificacion = request.form[f'dosificacion_{i}']
            frecuencia = request.form[f'frecuencia_{i}']
            duracion = request.form[f'duracion_{i}']
            via_administracion = request.form[f'viaAdmin_{i}']
            
            # Insertar datos en la tabla 'tratam' con el número de consulta correspondiente
            consulta_sql_tratam = "INSERT INTO tratam (Num_Cons, Num_Med, Dosif, Frec, Durac, ViaAd) VALUES (%s, %s, %s, %s, %s, %s)"
            datos_tratam = (NumConsA, medi, dosificacion, frecuencia, duracion, via_administracion)

            cursor.execute(consulta_sql_tratam, datos_tratam)
            conexion.commit()

        # Redireccionar a la misma página después de ingresar los datos
        return redirect(url_for('nueva_consulta', NDoc=NDoc))

    html_content2 = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nueva Consulta</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            /* Estilos CSS aquí */
            body {
                background-color: #f8f9fa;
            }
            .container {
                margin-top: 50px;
            }
            .form-group {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Nueva Consulta</h2>
            <form method="POST">
                <div class="form-group">
                    <label for="NumCons">Número de Consulta:</label>
                    <input type="text" class="form-control" id="NumCons" value="  
    '''
    html_content2 += NumConsA if NumConsA else ""
    html_content2 += '''" readonly>
                </div>
                <div class="form-group">
                    <label for="NombreP">Nombre del Paciente:</label>
                    <input type="text" class="form-control" id="NombreP" name="NombreP" required>
                </div>
                <div class="form-group">
                    <label for="Edad">Edad:</label>
                    <input type="number" class="form-control" id="Edad" name="Edad" required>
                </div>
                <div class="form-group">
                    <label for="peso">Peso:</label>
                    <input type="number" class="form-control" id="peso" name="peso" required>
                </div>
                <div class="form-group">
                    <label for="Alergias">Alergias:</label>
                    <input type="text" class="form-control" id="Alergias" name="Alergias" required>
                </div>
                <div class="form-group">
                    <label for="Diag">Diagnóstico:</label>
                    <input type="text" class="form-control" id="Diag" name="Diag" required>
                </div>
                <!-- Agregar campos para datos de tratamiento -->
                <div class="form-group">
                    <label for="numTratamientos">Número de Tratamientos:</label>
                    <input type="number" class="form-control" id="numTratamientos" name="numTratamientos" required>
                </div>
                <div id="tratamientos">
                </div>
                <button type="submit" class="btn btn-primary">Guardar Consulta</button>
                <a href="/itinerario/'''
    html_content2 += str(NDoc) if str(NDoc) else ""
    html_content2 += '''" class="btn btn-secondary">Itinerario</a>
            </form>
        </div>

        <script>
            // Script para agregar campos de tratamiento dinámicamente
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('numTratamientos').addEventListener('input', function() {
                    var numTratamientos = parseInt(this.value);
                    var tratamientosDiv = document.getElementById('tratamientos');
                    tratamientosDiv.innerHTML = '';

                    for (var i = 0; i < numTratamientos; i++) {
                        var tratamientoHTML = `
                            <div class="form-group">
                                <label for="nombreMedicamento_${i}">Nombre del Medicamento:  </label>
                                <select id="medi_${i}" name="medi_${i}">
    '''
    for valor in valores:
        html_content2 += f"<option value='{valor['Medicamento']}'>{valor['Medicamento']}</option>"

    html_content2 += ''' 
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="dosificacion_${i}">Dosificación:</label>
                                <input type="text" class="form-control" id="dosificacion_${i}" name="dosificacion_${i}" required>
                            </div>
                            <div class="form-group">
                                <label for="frecuencia_${i}">Frecuencia (en horas):</label>
                                <input type="number" class="form-control" id="frecuencia_${i}" name="frecuencia_${i}" required>
                            </div>
                            <div class="form-group">
                                <label for="duracion_${i}">Duración (en días):</label>
                                <input type="number" class="form-control" id="duracion_${i}" name="duracion_${i}" required>
                            </div>
                            <div class="form-group">
                                <label for="viaAdmin_${i}">Vía de Administración:  </label>
                                <select id="viaAdmin_${i}" name="viaAdmin_${i}">
                                    <option value="ORAL" selected>ORAL</option>
                                    <option value="SUBLINGUAL">SUBLINGUAL</option>
                                    <option value="RECTAL">RECTAL</option>
                                    <option value="TÓPICA">TÓPICA</option>
                                    <option value="INHALATORIA">INHALATORIA</option>
                                    <option value="INTRAVENOSA">INTRAVENOSA</option>
                                    <option value="INTRAMUSCULAR">INTRAMUSCULAR</option>
                                    <option value="SUBCUTÁNEA">SUBCUTÁNEA</option>
                                    <option value="INTRADÉRMICA">INTRADÉRMICA</option>
                                </select>
                                <input type="hidden" id="viaAdmin_${i}" name="viaAdmin_${i}">
                            </div>
                        `;
                        tratamientosDiv.innerHTML += tratamientoHTML;
                    }
                });
            });

        function updateHiddenInput(select) {
            var hiddenInputId = select.id.replace('viaAd_', 'viaAdmin_');
            var hiddenInput = document.getElementById(hiddenInputId);
            hiddenInput.value = select.value;
        }
        </script>
    </body>
    </html>
    '''
    return html_content2

'''@app.route('/consultar_consultas/<int:NDoc>', methods=['GET', 'POST'])
def consultar_consultas(NDoc):
    if request.method == 'POST':
        paciente = request.form['paciente']
        cursor.execute("SELECT * FROM consulta WHERE NombreP LIKE %s AND Num_D = %s", (f"%{paciente}%", NDoc))
        consulta = cursor.fetchall()
        return render_template('consulta.html', consulta=consulta)
    else:
        cursor.execute("SELECT * FROM consulta WHERE Num_D = %s",(NDoc))
        consulta = cursor.fetchall()
        return render_template('consulta.html', consulta=consulta)'''
    
@app.route('/itinerario/<int:NDoc>', methods=['GET', 'POST'])
def itinerario(NDoc):
    # Escribir los resultados en un archivo HTML
    # Usar StringIO para almacenar temporalmente los datos HTML
    f = StringIO()
    f.write('<html>')
    f.write('<head>')
    f.write('<meta charset="UTF-8">')
    f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    f.write('<style> .tab { text-indent: 40px; }</style>')
    f.write('<title>Itinerario de toma de medicamentos</title></head>')
    f.write('<body>')

    # Aquí va tu código para generar el contenido HTML
    cursor = conexion.cursor()
    # Traer los datos con la consultas
    # Datos necesarios para delimitar que registros corresponden a las consultas
    cursor.execute("SELECT Num_D FROM CONSULTAS_MEDICAS.consulta ORDER BY NumCons DESC LIMIT 1")
    a = cursor.fetchone()
    doctor = a['Num_D']

    cursor.execute("SELECT NumCons FROM CONSULTAS_MEDICAS.consulta WHERE Num_D = %s ORDER BY NumCons DESC LIMIT 1", (doctor,))
    b = cursor.fetchone()
    consulta_actual = b['NumCons']

    cursor.execute("SELECT concat('Dr(a). ', NombreD, ' ', SNombreD, ' ', ApellidoP, ' ', ApellidoM) AS NDoctor FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (doctor,))
    c = cursor.fetchone()
    nom_doctor = c['NDoctor']

    cursor.execute("SELECT Espec FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (doctor,))
    d = cursor.fetchone()
    esp = d['Espec']

    cursor.execute("SELECT CEDProf FROM CONSULTAS_MEDICAS.doctor WHERE NumD = %s;", (doctor,))
    e = cursor.fetchone()
    ced = e['CEDProf']

    f.write(f'<h1>Receta m&eacute;dica #{consulta_actual}</h1>')
    f.write(f'<h2>Doctor: {nom_doctor}</h2>')
    f.write(f'<h2>Especialidad: {esp}<br>CED. PROF. {ced}<br></h2>')

    
    # Variable que necesita la fecha desde una consulta que especifique el Numero de Consulta
    cursor.execute("SELECT Fecha FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    f1 = cursor.fetchone()
    Fecha = f1['Fecha']

    cursor.execute("SELECT NombreP FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    g = cursor.fetchone()
    nomP = g['NombreP']

    cursor.execute("SELECT Edad FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    h = cursor.fetchone()
    edad = h['Edad']

    cursor.execute("SELECT Peso FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    i1 = cursor.fetchone()
    peso = i1['Peso']

    cursor.execute("SELECT Alergias FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    q = cursor.fetchone()
    alergias = q['Alergias']

    cursor.execute("SELECT Diag FROM CONSULTAS_MEDICAS.consulta WHERE NumCons = %s", (consulta_actual,))
    k = cursor.fetchone()
    diag = k['Diag']

    f.write(f'<h2>Fecha y hora de elaboraci&oacute;n: {Fecha}<br><br>Datos del paciente:</h2>')
    
    f.write(f'<h3><br>Paciente: {nomP}<br>Edad: {edad} a&ntilde;os<br>Peso: {peso}<br>Alergias: {alergias}<br>Diagn&oacute;stico: {diag}</h3>')

    # Variable que necesita la hora de Inicio para la consulta que haremos
    # Se suma 1, para determinar que una hora después de la consulta se toma los medicamentos
    InicioT = Fecha
    InicioT += datetime.timedelta(hours=1)
    # Variable que almacena la cantidad de medicantos que se recetaron
    cursor.execute("SELECT count(*) AS CantM FROM CONSULTAS_MEDICAS.tratam WHERE Num_Cons = %s", (consulta_actual,))
    l = cursor.fetchone()
    med = l['CantM']

    # Variables necesarias para los valores
    n = 0
    m = 0
    x = ''

    # Lista de datos que obtiene todos los datos de los medicamentos del tratamiento
    ListaMed = []

    cursor.execute("SELECT Num_Med FROM CONSULTAS_MEDICAS.tratam WHERE Num_Cons = %s", (consulta_actual,))
    resultados = cursor.fetchall()
    lista_valores = []
    for resultado in resultados:
        lista_valores.append(resultado['Num_Med'])

    consulta_sql = "SELECT concat(a.DenGen ,' ', a.DenDist) as Medicamento FROM (SELECT DenGen, DenDist FROM medi WHERE NumMed IN (%s)) as a"
    valores_str = ', '.join(['%s'] * len(lista_valores))
    consulta_sql = consulta_sql % valores_str
    cursor.execute(consulta_sql, lista_valores)

    
    for i in range(med):
        x = cursor.fetchone()
        ListaMed.append(x['Medicamento'])


    # Lista de datos que obtiene todos las duraciones de los medicamentos del tratamiento
    ListaDuracion = []

    cursor.execute("SELECT Durac FROM tratam WHERE Num_Cons = %s",(consulta_actual,))

    for o in range(med):
        n = cursor.fetchone()
        ListaDuracion.append(n['Durac']*24)


    # Lista de datos que obtiene todas las FRECUENCIAS de los medicamentos del tratamiento
    ListaFrecuencia = []

    cursor.execute("SELECT Frec FROM tratam WHERE Num_Cons = %s",(consulta_actual,))

    for p in range(med):
        m = cursor.fetchone()
        ListaFrecuencia.append(m['Frec'])

    f.write(f'<h2>Itinerario de autoadministraci&oacute;n de medicamento(s)</h2>')

    HrsMax = max(ListaDuracion)
    q = 1
    HoraItinerario = InicioT
    while q <= HrsMax:
        # Incremento de la variable que recorrera la cantidad de días del tratamiento
        # Condicional para imprimir la fecha de inicio y cuando se cambie de día
        if q == 1 or (Fecha != HoraItinerario and HoraItinerario.hour == 00):
            titulof = f'\n\nFECHA\n{HoraItinerario.strftime("%d de %B de %Y")}'
            f.write(f'<h3>{titulof}</h3>')
            f.write(f'<h3>HORARIO&emsp;MEDICAMENTO(S)</h3>')
        # Ciclo For que recorre los valores de la DataFrame
        # Se inicializa el indice para decidir si es el primer medicamento que se receta
        dec = 0
        indice = 0
        
        while indice < med:
            # Se asignan los valores al medicamento que se verificara en ese valor del indice
            medicamento = ListaMed[indice]
            duracion = ListaDuracion[indice]
            frecuencia = ListaFrecuencia[indice]
            
            # Condicional para saber si es el inicio del tratamiento o un multiplo de la frecuencia
            if q == 1 and dec == 0:
                horaiti = f'\n\t{HoraItinerario.strftime("%I:%M %p")}'
                f.write(f'<p>{horaiti}&emsp;&emsp;&emsp;{medicamento}</p>')
                dec = dec + 1
            elif q == 1 and dec > 0:
                f.write(f'<p>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;{medicamento}</p>')
            elif q < duracion:
                if q % frecuencia == 0:
                    if dec == 0:
                        Himpresa = HoraItinerario
                        Himpresa += datetime.timedelta(hours=1)
                        horaiti = f'\n\t{Himpresa.strftime("%I:%M %p")}'
                        f.write(f'<p>{horaiti}&emsp;&emsp;&emsp;{medicamento}</p>')
                        dec = dec + 1
                    else:
                        f.write(f'<p>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;{medicamento}</p>')
            indice = indice + 1

        # Aumento de la hora en una hora
        HoraItinerario += datetime.timedelta(hours=1)
        q = q + 1
    
    f.write('</body>')
    f.write('</html>')

    # Crear una respuesta con el contenido HTML
    response = make_response(f.getvalue())

    # Configurar las cabeceras para indicar que es un archivo HTML
    response.headers['Content-Type'] = 'text/html'

    return response
    

if __name__ == '__main__':
    app.run(debug=True)