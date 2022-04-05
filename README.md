# Proyecto ClassVRoom

## Descripción de Proyecto
El proyecto trata de hacer una página web que gestione cursos para que profesores puedan colgar material para sus alumnos y los alumnos puedan subir ejercicios y ver el feedback de su profesor.

## Instalación y uso del proyecto

## Equipo
El equipo ha sido compuesto por 3 alumnos de DAW del instituto Esteve Terradas i Illa.

* Carlos Fernández
  * [Github](https://github.com/bycarlos28) 
  * [Discord: bycarlos28#9418]

* Adrián Gomez
  * [Github](https://github.com/AdrianOrea) 
  * [Github: Adgoor#0880]

* Carlos Valenzuela
  * [Github](https://github.com/carlosvalgar) 
  * [Discord: Carvagia#1404]

# Instalación docker
```
apt-get install docker.io docker-compose
```

Después tenemos que crear el archivo db.sqlite3 para poder hacer el migrate cuando hayamos levantado el docker.

```
touch db.sqlite3
```

Una vez hecho levantamos el docker-compose.

```
docker-compose up -d --build
```

Lo siguiente es entrar dentro del docker para ello necesitamos saber la ID de este lo hacemos así.

```
docker ps
```

Y ejecutamos el siguiente comando

```
docker exec -ti <primeros 3 letras/números del docker> bash
```

Una vez dentro hacemos ./manage.py migrate y ./manage.py creategroups.
