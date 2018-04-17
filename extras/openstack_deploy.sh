#!/bin/env bash
OS_PROJECT_DOMAIN_NAME=default
OS_USER_DOMAIN_NAME=default
OS_IDENTITY_API_VERSION=3
OS_AUTH_STRATEGY=keystone
OS_REGION_NAME=RegionOne

DEPLOY_USER=ubuntu
DEPLOY_KEY=$HOME/id_rsa

SSH_OPTS="-q -o PrintMotd=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

GIT_REF=${TRAVIS_PULL_REQUEST_BRANCH:-${TRAVIS_BRANCH}}
PROJECT=${TRAVIS_REPO_SLUG##eubr-bigsea/}

function setup_environment {
  STACK_NAME=`openstack stack list -f value -c ID --tags ${DEPLOY_ENV}`
  DEPLOY_SERVER=`openstack stack output show -f value -c output_value ${STACK_NAME} public_ip`

  #Ssh private key content to file
  openstack stack output show -f value -c output_value ${STACK_NAME} ssh_private_key 1> $DEPLOY_KEY && \
    chmod 600 ${DEPLOY_KEY}
}

function update_with_pull {
  PROJECT=${PROJECT:-${1}}
  ssh ${SSH_OPTS} -i ${DEPLOY_KEY} ${DEPLOY_USER}@${DEPLOY_SERVER} <<EOF
    cd /srv/docker-lemonade/
    sudo docker-compose pull ${PROJECT}
    sudo docker-compose up -d ${PROJECT}
EOF
}

function update_with_build {
  PROJECT=${PROJECT:-${1}}
  ssh ${SSH_OPTS} -i ${DEPLOY_KEY} ${DEPLOY_USER}@${DEPLOY_SERVER} <<EOF
    cd /srv/docker-lemonade/
    git submodule init
    git submodule update ${PROJECT}

    cd /srv/docker-lemonade/${PROJECT}
    git fetch -ap
    git checkout origin/${GIT_REF}
    cd ../
    sudo docker-compose up -d --build ${PROJECT}
EOF
}

case ${DOCKER_COMPOSE_METHOD} in
  build)
    setup_environment
    update_with_build
    ;;
  pull)
    setup_environment
    update_with_pull
    ;;
  *)
    echo 'nothing to do'
    ;;
esac
