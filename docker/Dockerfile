FROM ubuntu:24.04
# Refer requirements.txt for environment packages
# Does not override jupyterlab defaults

# Set bash as the default shell
ENV SHELL=/bin/bash

# Build with some basic utilities
RUN apt-get -yqq update --fix-missing
RUN apt-get -yqq install \
	python3-pip \
	python3-venv \
	apt-utils \
	vim \
	git \
	screen \
	htop \
	wget \
	net-tools \
	cmake \
	swig \
    	patchelf \
   	curl \
    	software-properties-common \
    	xpra \
    	xserver-xorg-dev \
	texlive-latex-recommended \
	texlive-latex-extra \
	texlive-pictures poppler-utils\
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Accept the Microsoft Core Fonts EULA non-interactively
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections

# Install ttf-mscorefonts-installer
RUN apt-get update && apt-get install -y \
    ttf-mscorefonts-installer \
    && rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -f -v

# --- VIRTUAL ENVIRONMENT SETUP START ---

# Create the virtual environment in /opt/venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# PREPEND the venv bin directory to the PATH.
# This ensures that 'pip', 'python', and 'jupyter' commands
# automatically refer to the versions inside the virtual environment.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# --- VIRTUAL ENVIRONMENT SETUP END ---

# build with some basic python packages
# Because of the PATH change above, this now runs inside the venv
RUN pip install --upgrade pip
RUN pip install \
	jupyterlab \
	ipywidgets \
	ipynbname \
	autopep8 \
	gitpython \
	matplotlib \
	tqdm \
    scikit-learn \
    stim \
    sinter \
    pymatching \
    numpy<2.0 \
# numpy >= 2.0 has breaking changes for stim/sinter

# define the port number(s) the container should expose
# All running containers expose 8888 and 6006
# They are redirected to other ports using docker -p <machine_port>:8888
EXPOSE 8888
EXPOSE 6006

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION=v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# start jupyter lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--notebook-dir=/"]
