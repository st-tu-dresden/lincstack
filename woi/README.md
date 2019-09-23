# WOI - Watch our Ideas

## Backup

`/var/lib/docker/volumes/$INSTANCE"woi"*`

## Updating

Inside the repository, write the code you want.
After committing do something like `git tag 2019_04_10`, which is used to specify a version to a specific commit.
Then `git push; git push --tags`. When the CI is successfully building everything, you will see on dockerhub
the latest version: https://hub.docker.com/r/lincstack/woi/tags/. I.e., `backend_2019_04_10` and
`frontend_2019_04_10`.

After this you can update as normal:

```bash
docker-compose down
edit docker-compose.yml
docker-compose pull
docker-compose up -d
```
