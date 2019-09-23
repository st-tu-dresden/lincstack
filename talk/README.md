# Talk

https://github.com/RocketChat/Rocket.Chat

## Initial Setup

You have to login with the admin-accound and create a new OAuth with the name "Keycloak" - then it should fill in all the information
already automatically.

## Backup

`/var/lib/docker/volumes/$INSTANCE"taiga"*`

## Updating

No custom modifications by us.

```bash
docker-compose down
edit docker-compose.yml
docker-compose pull
docker-compose up -d
```
