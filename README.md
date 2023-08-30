# BookApi

- Guide complete in _./doc_

## Proyecto de API

Este es un proyecto de API desarrollado en Python que utiliza el framework FastAPI. El proyecto tiene la siguiente estructura de directorios y archivos:

```plaintext
.
├── api/
│   ├── app.py
│   ├── connections/
│   │   ├── db.py
│   │   ├── instace.py
│   │   └── ...
│   ├── controllers/
│   │   ├── controller_url.py
│   │   ├── controller_users.py
│   │   └── ...
│   ├── docs/
│   │   ├── api_documentation.md
│   │   └── api_guide.md
│   ├── models/
│   │   ├── model.py
│   │   └── ...
│   ├── modules/
│   │   ├── crud_postgresql/
│   │   ├── crud_reddis/
│   │   ├── logger_modify.py
│   │   ├── redis_conf/
│   │   └── ...
│   ├── routers/
│   │   ├── url_routers.py
│   │   ├── user_routers.py
│   │   └── ...
│   ├── tests/
│   │   └── test_database.py
│   └── utils/
│       └── access_token.py
```

Este proyecto está organizado en módulos y directorios que representan diferentes partes de la aplicación, incluyendo la configuración de la base de datos, controladores, rutas de la API, modelos de datos, módulos de utilidad y pruebas unitarias.

### Uso

Para ejecutar la API, asegúrate de tener Python instalado y las dependencias
requeridas instaladas. Luego, puedes ejecutar el archivo app.py o seguir la instrucciones en la pagina fastapi con uvicorn.

### Documentación

La documentación de la API se encuentra en los archivos api*documentation.md y api_guide.md en el directorio \_docs/*.

### Contribuciones

Si deseas contribuir a este proyecto, ¡estamos abiertos a colaboraciones! Puedes enviar pull requests con mejoras, correcciones de errores y nuevas características.

Si deseas contribuir a este proyecto, ¡estamos abiertos a colaboraciones! Puedes enviar pull requests con mejoras, correcciones de errores y nuevas características.
