# Docker image `diegoferigo/devenv` ![](https://img.shields.io/docker/pulls/diegoferigo/devenv.svg?link=https://hub.docker.com/r/diegoferigo/devenv&logo=docker)

|                                                              | Base Image                                                   | Base image repo                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [![](https://images.microbadger.com/badges/version/diegoferigo/devenv.svg)](https://microbadger.com/images/diegoferigo/devenv) | [`ubuntu:bionic`](https://hub.docker.com/_/ubuntu/)          | [github@tianon/docker-brew-ubuntu-core](https://github.com/tianon/docker-brew-ubuntu-core) |
| [![](https://images.microbadger.com/badges/version/diegoferigo/devenv:intel.svg)](https://microbadger.com/images/diegoferigo/devenv) | [`ubuntu:bionic`](https://hub.docker.com/_/ubuntu/)          | [github@tianon/docker-brew-ubuntu-core](https://github.com/tianon/docker-brew-ubuntu-core) |
| [![](https://images.microbadger.com/badges/version/diegoferigo/devenv:nvidia.svg)](https://microbadger.com/images/diegoferigo/devenv) | [`nvidia/opengl:1.0-glvnd-runtime-ubuntu18.04`](https://hub.docker.com/r/nvidia/opengl/) | [gitlab@nvidia/opengl](https://gitlab.com/nvidia/opengl/)    |

- [Build the image](#build-the-image)
- [Download the image](#download-the-image)

## Build the image

From the current folder, execute:

```sh
# Intel GPUs: it creates the image diegoferigo/devenv:intel
make intel

# Nvidia GPUs: it creates the image diegoferigo/devenv:nvidia
make nvidia
```

## Download the image

The images can be found in my [dockerhub profile](https://hub.docker.com/r/diegoferigo):

```sh
# Download the intel image
docker pull diegoferigo/devenv:intel

# Download the nvidia image
docker pull diegoferigo/devenv:nvidia
```

## Notes on the Nvidia image

TODO
