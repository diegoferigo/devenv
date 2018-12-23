ARG from=ubuntu:bionic
FROM ${from}

# Build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=0.9
LABEL \
    maintainer="Diego Ferigo <dgferigo@gmail.com>" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="devenv" \
    org.label-schema.description="Base for docker-based development environments" \
    org.label-schema.url="https://github.com/diegoferigo/devenv" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/diegoferigo/devenv" \
    # org.label-schema.vendor="" \
    org.label-schema.version=$VERSION \
    org.label-schema.schema-version="1.0"

# Support of nvidia-docker 2.0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

# Setup an additional entrypoint script
COPY setup.sh /usr/sbin/setup_devenv.sh
COPY entrypoint.sh /usr/sbin/entrypoint_devenv.sh
RUN chmod 755 /usr/sbin/setup_devenv.sh
RUN chmod 755 /usr/sbin/entrypoint_devenv.sh
ENTRYPOINT ["/usr/sbin/entrypoint_devenv.sh"]
CMD ["bash"]
