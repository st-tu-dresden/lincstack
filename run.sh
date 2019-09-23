#!/bin/bash

function start() {
    docker-compose up -d
    echo 'docker-compose up -d'
}

stop() {
    docker-compose down
    echo 'docker-compose down'
}
update() {
    docker-compose pull
    echo 'docker-compose pull'
}
logs() {
    docker-compose logs -f
    echo 'docker-compose logs -f'
}
config() {
    docker-compose config --resolve-image-digests
    echo 'docker-compose config --resolve-image-digests'
}
config2() {
    docker-compose config -q || exit 1
}

if [[ "$1" == "" || "$2" == "" ]]; then
    echo "usage: $0 talk|fridolean|woi|landing|taiga|md|landing start|stop|restart|update|logs|config " >&2
    exit 1
fi


(
cd "$1" || echo "Directory $1 does not exit" || exit 1
case "$2" in 
    start)   start ;;
    stop)    stop ;;
    update)  update;;
    pull)  update;;
    logs)  logs;;
    config)  config;;
    config2)  config2;;
    restart) stop; start ;;
    *)
        echo "usage: $0 talk|fridolean|woi|landing|taiga|md|landing start|stop|restart|update|logs " >&2
        exit 1 ;;
esac
)
