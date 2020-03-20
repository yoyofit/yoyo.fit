# YoYo.fit

## Установка & Настройка

Для развертывания портала на сервере используйте Docker:

```bash
$ docker pull docker.pkg.github.com/yoyofit/yoyo.fit/yoyo:1.0
```

или

```Dockerfile
FROM docker.pkg.github.com/yoyofit/yoyo.fit/yoyo:1.0
```

### Переменные

`DJANGO_CONFIGURATION=Prod`  
`POSTGRES_HOST=<postgres host>`  
`POSTGRES_USER=<postgres user>`  
`POSTGRES_PASSWORD=<postgres password>`  
`DJANGO_SECRET_KEY=<django secret key>`
`DJANGO_DEBUG=false`  

Вы можете вписать эти переменные в файл `docker-compose.yaml` или 
в отдельный файл и указать на него в том же файле.

## Зависимости

Для полноценной работы используются слелующие зависимости:

- PostgreSQL
