# Despliegue de FastAPI en Render

## Pasos para desplegar

### Incialmente:
Tenemos que crear el .gitignore donde dentro colocamos los archivos que no queremos subir a GitHub. Tales como:
```
.venv/
__pycache__/
*.pyc
.env
```
Además tenemos quue modificar unos aspectos de nuestro db.py para que funcione con Render. 


### 1. Subir el proyecto a GitHub
Darse de alta en GitHub, crear un repositorio y subir el proyecto.
Desde la terminal, ejecutar los siguientes comandos:
```powershell
git init
git add .
git commit -m "Proyecto FastAPI Mitologia"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```
### 2. Darse de alta en Render
Nos dirigimos la página web de Render y nos damos de alta y vinculamos nuestro GitHub. 
Pasos:
1. Crear una instancia PostgreSQL gestionada. Dashboard -> New -> PostgreSQL
   
    Configuramos dando el nombre, la base de datos y demás. Al terminar copiamos la URL interna proporcionada por Render.
2. Crear la app FastAPI en Render. Dashboard -> New -> Web Service

    Apuntamos a nuestro repositorio de GitHub, revisamos el branch, el runtime, root directory y el Dockerfile path.
    
    Importante ir al Environment -> Add variable. 

    DB_URL (la URL de PostgreSQL que copiamos en el paso anterior)

    Finalmente, pulsamos el botón Deploy.

### 3. Nos dirigimos a la página de la app
Con https://mitologia.onrender.com se nos redirige a la página de la app.

### 4. Hacer el cambio en index.html
En index.html, agregamos una línea que dice "Aplicación desplegada en Render 🚀"
Para subir el cambio entramos en terminal y ejecutamos:
```powershell
git add src/templates/index.html
git commit -m "Añadido mensaje en index.html"
git push
```
Reiniciamos la página de la app y vemos que ahora aparece el mensaje.

