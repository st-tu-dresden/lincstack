# Docker for LINC

This is the main entrypoint if you want to have an easy LINC installation.

## LINC consists of following services

* Watch Our Ideas
* Fridolean
* Taiga
* A landing page
* Keycloak 
* Rocketchat
* Checkup 


# Installation

## Configuration

## Required Configuration

Run `install.py` from within this folder.

### Post-Setup

Some configurations can only be done manually currently. This includes setting up the reverse Proxy (apache, nginx, traefik) and
retrieving/setting some config options.

#### Reverse Proxy

Please have a look inside the `extra/reverse_proxy` directory. It contains example files for apache2.
If you have much time on your hand, you can look into https://traefik.io this is a reverse proxy which works very well together with docker.

I *think*, that you have to use https for everything, when you install it not on localhost. This is because of the browser settings in conjunction with keycloak. But a localhost setup is currently completely untested.

#### Manual steps needed

**Certificates and keys from Keycloak**
For taiga and hackmd you have to extract some certificates from keycloak, which have to be entered inside their respective `docker-compose.override` file or inside `keycloak/cert.pem`.

**Manual config**
To configure rocketchat, login with the admin and then create a custom oauth provider with the name `keycloak`.
Also create a user which can act as the bot with the same password as was defined inside the docker-compose.yml.

You have to change the admin-password of taiga: for this you log into taiga with the name "admin" and password "123123".

## Starting / Stopping the services

Easiest way is to use the `run.sh` script since a docker-compose command requires to set the correct compose-files first.
When running `./run.sh woi config` you will also see at the bottom what the command has to look like.
I.e., `docker-compose -p linc_woi -f docker-compose.woi.yml -f docker-compose.woi.override.yml config --resolve-image-digests`.

With `./all_run.sh` you can also run some commands on all services.. Most commands assume you have installed the systemd services.

### Snapshots

Please run from time to time `./all_run.sh snapshot` this will dump all the final configuration into a snapshots folder. With this, you
always can restore your current state.

## Location of all the docker containers:

* https://hub.docker.com/u/lincstack/

