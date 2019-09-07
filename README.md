<p align="center">
    <h1 align="center">devenv</h1>
</p>

<p align="center">
<b><a href="https://github.com/diegoferigo/devenv#why">Why</a></b>
•
<b><a href="https://github.com/diegoferigo/devenv#solutions">Solutions</a></b>
•
<b><a href="https://github.com/diegoferigo/devenv#features">Features</a></b>
•
<b><a href="https://github.com/diegoferigo/devenv#setup">Setup</a></b>
•
<b><a href="https://github.com/diegoferigo/devenv#example">Example</a></b>
</p>

<p align="center">
    <a href="https://github.com/diegoferigo/devenv/actions">
    <img src="https://github.com/diegoferigo/devenv/workflows/Continuous%20Integration/badge.svg" alt="Build Status (master)" />
    </a>
    <a href="https://www.codacy.com/app/diegoferigo/devenv?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=diegoferigo/devenv&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/dc64ae76526a49c6af2205c798a9e69d" alt="Codacy Badge" />
    </a>
</p>

## Why?

Software development does not only consist of improving and maintaining code. Developers spend a considerable amount of time and effort in keeping the entire development environment enough updated, complete, robust, and clean. Moreover, these environments are like living organisms, they need to be maintained and evolve with the same pace of the projects that spring from them.

Due to these reasons, development environments should be treated similarly to regular software projects. For both power users and new team members, configuring from scratch a fresh setup is often seen as a tedious task. In most cases a big number of components need to interact and communicate between each other, everyone coming with its own configuration. All the effort to achieve a complete and functional result is rarely shared among users, each of them need to start again from scratch and find their own way.

## Solutions

The usual and canonical solution are **virtual machines**. They are portable and can provide an isolated setup that can be pre-configured and shared with others. However, many problems arise when there is the need to interact to particular hardware devices, when a direct access to the machine features is not entirely possible, or when the virtualization overhead becomes a bottleneck. Last but not least, customising VMs and porting the modifications to an updated image is very difficult, if not impossible.

The proposed solution to all such problems is **shipping an entire development environment as a docker image**. This image works as system inside a system, it shares and directly accesses all the host resources, providing an isolation that can be fully customized depending on the particular requirements. On the contrary of VMs, the docker stack introduces only an imperceptible overhead. More in detail, this approach allows achieving the following aims:

- Minimize the setup time of new machines
- Optimize the trade-off between isolation and performance
- Develop the development environment as a software project
- Generate a reproducible development environment
- Obtain a clean environment with just few keystrokes (recreating the container)
- Run in parallel multiple independent development environments
- Share a common environment with other developers
- Customize the environment and port easily the modifications to an updated base
- Apply Continuos Integration (CI) approach to the entire environment
- Apply Continuous Delivery (CD) through CI deployment

In short, is like maintaining a fancy bash script that allows creating and configuring from scratch a new machine. With the pro that, once ready, it can be wiped and recreated with minimal effort.

## Features

`devenv` provides the following features:

- Runtime user matching the host's user
- Easy access to persistent resources from the host system
- Intel and Nvidia GPUs support
- X11 authentication for GUIs
- Debugger support
- Matlab support
- Git configuration
- Systemd support

All these features are already natively supported by docker. In order to simplify their setup, `devenv` provides two components:

1. A python wrapper around `docker-compose`
1. A docker image with the support of these features

Once installed, you can use the provided docker image as a base for installing the preferred tools that suit your development needs. Access to the `devenv` features are possible through an extended docker-compose `yaml` configuration containing high-level options loaded by the python script ([example conf](.ci/devenv.yml)).

## Setup

### Python script

To install the `devenv` script, execute:

```sh
pip3 install git+https://github.com/diegoferigo/devenv.git
```

You will find the `devenv` executable in your local binary folder (usually `~/.local/bin`). In order to use it, make sure that this folder is part of your system path.

```
$ devenv -h
usage: devenv [-h] [-f FILE] [-G] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  the configuration file (default: devenv.yml)
  -G, --generate        generate output compose file and exit, do not run
                        docker-compose
  -o OUTPUT, --output OUTPUT
                        specify an alternate output compose file (default:
                        devenv-docker-compose.yml)
```

### Docker image

You can either build the image locally or download it from [dockerhub](https://hub.docker.com/r/diegoferigo/devenv). This repository exploits the CI pipeline to push weekly new images, they are always updated and built on top of the latest version of the `ubuntu:bionic` image.

Read the [docker/README.md](docker/README.md) for further information.

## Example

You can find a simple application in the [example](example/) folder. It shows a minimal setup for forwarding a popup to the host X server. Execute the following commands:

```sh
# Clone this repository
git clone https://github.com/diegoferigo/devenv
cd devenv

# Install the script if you didn't install it before
pip3 install .

# Build the base docker image
cd docker
make intel

# Build the example image with X11
cd ../example
docker build --build-arg from=diegoferigo/devenv:intel -t devenv_example .
devenv -f devenv.yml -o devenv-docker-compose.yml up # Or just "devenv up"
```

A popup will appear on your display.

The python script processes the [`devenv.yml`](example/devenv.yml) file and creates an intermediate [`devenv-docker-compose.yml`](example/devenv-docker-compose.yml) file which is later used by `docker-compose`. All the extra arguments passed to the `devenv` script which are not recognized are passed to `docker-compose`, such as `up` in this example. If you want to only generate the `docker-compose` configuration out of the `devenv` yaml, use the `-G` option.

---

### History

Ancestors of this project were born in the beginning of 2017 during my early experiments with [docker](https://github.com/diegoferigo/dockerfiles). I quickly realized that these development images had to be treated differently than the other images instantiated in the idiomatic docker way (ephemeral containers), and were separated to a [new repository](https://github.com/diegoferigo/development-iit). When I realized that this pipeline could be generalized and customized arbitrarily, `devenv` was split and became a standalone project, reaching a third level of meta-development:

> A project to develop development environments to develop software projects
