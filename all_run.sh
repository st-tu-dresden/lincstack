#!/bin/bash

source enabled_services.sh

function snapshot() {
    function create() {
        mkdir snapshots
        cd snapshots
        git init .
        cd ..
    }
    [ -d snapshots ] || create
    ./run.sh "$1" config > "snapshots/$1.yml"
    echo "./run.sh $1 config > snapshots/$1.yml"
}

if [[ "$1" == "config2" ]]; then rm config.log; fi

for i in $ENABLED_S; do
    case "$1" in 
        snapshot) snapshot "$i";;
        config2)
            echo "$i:" | tee -a config.log
            ./run.sh "$i" "$1" 2>&1 | tee -a config.log || exit 1
            if grep -qv ":$" config.log ; then
                exit 1
            fi
        ;;
        *)
            ./run.sh "$i" "$1" || exit 1
    esac
done
