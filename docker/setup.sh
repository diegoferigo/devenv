#!/bin/bash
set -e

create_user() {
	# If the home folder exists, set a flag.
	# Creating the user during container initialization often is anticipated
	# by the mount of a docker volume. In this case the home directory is already
	# present in the file system and adduser skips by default the copy of the
	# configuration files.
	HOME_FOLDER_EXISTS=0
	if [ -d /home/$USERNAME ] ; then HOME_FOLDER_EXISTS=1 ; fi

	# Create a group with USER_GID
	if ! getent group ${USERNAME} >/dev/null; then
		echo "Creating ${USERNAME} group"
		groupadd -f -g ${USER_GID} ${USERNAME} 2> /dev/null
	fi

	# Create a user with USER_UID
	if ! getent passwd ${USERNAME} >/dev/null; then
		echo "Creating ${USERNAME} user"
		adduser --quiet \
		        --disabled-login \
				  --uid ${USER_UID} \
				  --gid ${USER_GID} \
				  --gecos 'Workspace' \
				  ${USERNAME}
	fi

	# If configuration files have not been copied, do it manually
	if [ ! $HOME_FOLDER_EXISTS -eq 0 ] ; then
		chown ${USER_UID}:${USER_GID} /home/${USERNAME}
		install -m 644 -g ${USERNAME} -o ${USERNAME} /etc/skel/.bashrc /home/${USERNAME}
		install -m 644 -g ${USERNAME} -o ${USERNAME} /etc/skel/.bash_logout /home/${USERNAME}
		install -m 644 -g ${USERNAME} -o ${USERNAME} /etc/skel/.profile /home/${USERNAME}
	fi
	
	# Assign the user to the runtimeusers group
	gpasswd -a ${USERNAME} runtimeusers
}

# Create the user
echo "==> Creating the runtime user"
create_user

# Set a default root password
echo "==> Setting the default root password"
ROOT_PASSWORD="root"
echo "root:${ROOT_PASSWORD}" | chpasswd

# Set a default password
echo "==> Setting the default user password"
USER_PASSWORD=${USERNAME}
echo "${USERNAME}:${USER_PASSWORD}" | chpasswd
echo "${USERNAME}    ALL=(ALL:ALL) ALL" >> /etc/sudoers

# Add the user to video group for HW acceleration (Intel GPUs)
usermod -aG video ${USERNAME}

# Configure git
if [[ ! -z ${GIT_USER_NAME:+x} && ! -z ${GIT_USER_EMAIL:+x} ]] ; then
	echo "==> Setting up git"
	su -c "git config --global user.name ${GIT_USER_NAME}" $USERNAME
	su -c "git config --global user.email ${GIT_USER_EMAIL}" $USERNAME
	su -c "git config --global color.pager true" $USERNAME
	su -c "git config --global color.ui auto" $USERNAME
	su -c "git config --global push.default upstream" $USERNAME
	su -c "git config --global core.autocrlf input" $USERNAME
fi

# Adding matlab to PATH
if [[ ! -z ${Matlab_ROOT_DIR:+x} ]] ; then
    echo "==> Setting up matlab"
    echo 'PATH=$PATH:$Matlab_ROOT_DIR/bin' >> /etc/bash.bashrc
fi
