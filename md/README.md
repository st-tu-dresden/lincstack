# CodiMD

https://github.com/hackmdio/codimd

## Initial Setup

You have to login to keycloak as admin and get the cert which you put into this folder.

## Backup

`/var/lib/docker/volumes/$INSTANCE"md_"*`

## Updating

No custom modifications by us.

```bash
docker-compose down
edit docker-compose.yml
docker-compose pull
docker-compose up -d
```
