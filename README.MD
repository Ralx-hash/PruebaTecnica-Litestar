<h1>Prueba Tecnica - README</h1>
<h2>Descripción</h2>
<p>WEB API en Litestar con Front en Angular - Funcion principal de servir datos de usuarios con autenticacion mediante JWT
</p>
<p>Para iniciar el proyecto en local hay que instalar las librerias que se encuentrar en requeriments.txt y tener un .env que tenga DATABASE_URL = postgresql+asyncpg://...(credenciales), JWT_KEY y JWT_ALGORITHM. Luego usar el comando litestar run --reload en consola (con el entorno virtual de python abierto, en este caso venv/scripts/activate)
</p>

<h2>Funcionalidades principales</h2>
La base de datos se trabajo en PostgreSQL, con una sola tabla con los siguientes atributos:

<ul>
<li>id: Incremental/int</li>
<li>nombre: varchar(255)</li>
<li>rol: varchar(50)</li>
<li>renta_mensual: numeric(12, 5)</li>
<li>email: varchar(255) //Comentario: Esto es basicamente el nombre sin espacios, seguido de un "@gmail.com"</li> 
<li>normalized_email: varchar(255) //Comentario: Esto es el email pero totalemnte en mayusculas (util para validaciones)</li>
<li>hashed_password: varchar(255)</li>
</ul>

<p>Por temas de comodidad (y para hacer la insersion de los usuarios en la bd mas facil) campos que DEBERIAN ser Not Null no lo son, tales como rol, email, normalized_email y hashed_password (renta_mensual es por default 0)</p>

<p>Es importante notar que el json de usuario no contaba con email ni contraseña, por lo cual, para hacer el login, se tomo el nombre del usuario, se le quito el espacio y se le agrego "gmail.com", <span>la contraseña de cada usuario vendira siendo el mismo correo (el normal, no el normalizado)</span></p>

<h3>Controlador</h3>
<p>El proyecto se trabajo con un solo controlador, el cual posteaba el login y servia los datos al usuario cuando entraba a la vista con lista. Se creo un metodo para ingresar los datos de los usuarios del json entregado, el cual solo se utilizo una vez. El controlador de users cuenta con 4 endpoints:
</p>

<ul>
<li>agregar-masivo: Usado para ingresar el json con los usuarios</li>
<li>all-dict: Usado mostrar la lista de todos los usuarios, utilizado principalmente para debbug</li>
<li>login: Como su nombre indica, se encarga de logear a los usuarios y de devolver el token</li>
<li>users-filtered: Version mejorada de all-dict para servir la lista en relacion al rol</li>
</ul>


<h3>Repositorio</h3>
<p>Repositorio es el principal intermediario entre el controlador, para servir los datos y la misma bd. Este cuenta con metodos con algunas validaciones y consultas que ayudan a que el controlador este mas limpio. Cuenta con 3 metodos:
</p>

<ul>
<li>agregar_usuarios_masivo: Encargado de enviar los usuarios del endpont agregar-masivo</li>
<li>obtener_usuarios_por_roles: Controla la consulta de la lista para los roles de usuario</li>
<li>usuario_existe: Como su nombre indica, verifica que el usuario exista para devolver un booleano</li>
</ul>

<h3>JWT</h3>
<p>Para configurar la autentificacion se usaron los modulos JWTAuth y token de la libreria de litestar security jwt.
La configuracion se encuentra en el controlador de usuario mientras que la clave del token y su algoritmo se encuentran en .env. El tiempo de expiracion del token puede ser cambiando default_token_expiration (se uso con un token de 1 hora de duracion para las pruebas). La funcion retrieve_user_handler, exportada desde utils es la encargada de confirmar que la id (sub) con la que cuenta el token se encuentra efectivamente dentro de la base de datos y para guardar los datos del usuario y consultarlos mas tarde.
JWTAuth tambien cuenta con exclude, para excluir rutas que no deben ser alteradas por la autenticacion, aunque en este proyecto no se uso directamente, ya que el auth no aplicaba generalmente para toda la app, solo a los que estaban configurados con el middleware de jwtath en el endpoint</p>

<h3>hashing de contraseña</h3>
<p>Se llevo a cabo a travez de bcrypt en una 2 funcion, una para hashear (que recibe la contraseña) y otra para deshashear (recibe la contraseña y la contraseña hasheada de la bd). Si bien la opcion para hashear no se utilizo mucho ya que no hay register en si, se utilizo para registrar en masa a todos los usuarios del json por medio del correo generado a partir de sus nombres</p>


<h3>Tests</h3>   
<p>El proyecto cuenta con un solo test que prueba la funcionalidad del hashing de contraseñas. La forma para probar los tests es:</p>   

```bash
pytest "directorio de las pruebas, en este caso:" 
pytest tests/unit/utils/test_hashearPassword.py
```
<h3>Cache</h3> 
<p>Se uso el cache (de una hora) integrado de litestar para las consultas de listas</p>