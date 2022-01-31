#!/bin/bash
echo "Bring down environment for FTiP Simulator"
#podman-compose down
podman pod rm -a -f
podman image prune -a -f
podman rmi -a -f
