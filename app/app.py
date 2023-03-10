from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

conexion=MySQL(app)

# Para realizar acciones antes de que se ejecute una peticion
@app.before_request
def before_request():
    print("Antes de la peticion")
    
    
# Para realizar acciones despues de que se ejecute una peticion    
@app.after_request
def after_request(response):
    print("Despues de la peticion")
    return response
    

@app.route("/")
def index():
    # return "<h1>Hola Mundooo</h1>"
    cursos = ['PHP','Python','Java','Kotlin','Dart','JS']
    data = {
        'titulo':'index',
        'bienvenida':'saludos',
        'cursos':cursos,
        'numero_cursos':len(cursos)
    }
    return render_template('index.html',data=data)


@app.route("/contacto/<nombre>/<int:edad>")
def contacto(nombre,edad):
    data = {
        'titulo':'Contacto',
        'nombre':nombre,
        'edad':edad
    }
    return render_template('contacto.html',data=data)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "OK"


@app.route('/cursos')
def listar_cursos():
    data={
        
    }
    try:
        cursor=conexion.connection.cursor()
        sql = "SELECT codigo,nombre,creditos from curso ORDER BY nombre ASC;"
        cursor.execute(sql)
        cursos=cursor.fetchall()
        # print(cursos)
        data['cursos'] = cursos
        data['mensaje']='Exito'
        
    except Exception as ex:
        data['mensaje']='Error...'
    return jsonify(data)


def pagina_no_encontrada(error):
    # return render_template('404.html'),404
    return redirect(url_for('index'))


if __name__=='__main__':
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True, port=5000)