#!/bin/env bash
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_STRATEGY=keystone
export OS_REGION_NAME=RegionOne

DEPLOY_USER=ubuntu
DEPLOY_KEY=$HOME/id_rsa

SSH_OPTS="-q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

GIT_REF=${TRAVIS_PULL_REQUEST_BRANCH:-${TRAVIS_BRANCH}}
GIT_TAG=${TRAVIS_TAG:-notag}

openstack stack create \
  --wait \
  --template extras/docker_swarm_os.hot.yaml \
  --parameter git_ref=${GIT_REF} \
  --parameter travis_build_number=${TRAVIS_BUILD_NUMBER} \
  --tags ${GIT_TAG} \
  $STACK_NAME

DEPLOY_SERVER=`openstack stack output show -f value -c output_value ${STACK_NAME} public_ip`

# ssh private key content to file
openstack stack output show -f value -c output_value ${STACK_NAME} ssh_private_key 1> $DEPLOY_KEY && \
  chmod 600 ${DEPLOY_KEY}

wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && chmod +x wait-for-it.sh

./wait-for-it.sh -q -t 120 ${DEPLOY_SERVER}:22 -- \
  ssh ${SSH_OPTS} -i ${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_SERVER} cat /etc/hostname

