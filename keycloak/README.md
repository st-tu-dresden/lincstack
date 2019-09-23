# Keycloak

## Backup

`/var/lib/docker/volumes/$INSTANCE"keycloak_"*`

## Custom modifications

* preconfigured json, which is modified by env-variables
    -> will be loaded on the first start
* some modifications to the theme for the German/EU privacy law

Basically it would be possible to just mount these modifications as volumes..

## Updating

Inside the repository, modify the Dockerfile for the new version and hope that no
other modifications are necessary.
Applications like WOI and Fridolean reference specific js/java which has the keycloak-version in its name.. Maybe you want to update it too.

After committing do something like `git tag 5.0.0`, which is used to specify a version to a specific commit.
Then `git push; git push --tags`. When the CI is successfully building everything, you will see on dockerhub
the latest version: https://hub.docker.com/r/lincstack/keycloak/tags/.

After this you can update as normal:

```bash
docker-compose down
edit docker-compose.yml
docker-compose pull
docker-compose up -d
```
