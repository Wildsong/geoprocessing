# This image is based on Ubuntu.
FROM osgeo/gdal:latest

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#ENV PIP_TARGET=/usr/local/share/pip-global
#ENV PYTHONPATH=${PYTHONPATH}:${PIP_TARGET}
#ENV PATH=${PATH}:${PIP_TARGET}/bin

ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get install -y --no-install-recommends sudo git python3-pip python3-setuptools pylint3 python3-wheel \
    && apt-get install -y --no-install-recommends python3-pylint-flask python3-flask-restful python3-flask-script \
    # Clean up
    && apt-get autoremove -y
# These make the container smaller for production but are a pain in development
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    #
    # Create alternate global install location that both uses have rights to access
    && mkdir -p /usr/local/share/pip-global \
    && chown ${USERNAME}:root /usr/local/share/pip-global

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
