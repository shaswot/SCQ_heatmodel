FROM ubuntu:24.04

# Set bash as the default shell
ENV SHELL=/bin/bash

# Combine update, repository management, and core utilities into one cached layer
RUN apt-get update -yqq && apt-get install -yqq --no-install-recommends \
    apt-utils \
    software-properties-common \
    curl \
    wget \
    git \
    vim \
    screen \
    htop \
    net-tools \
    cmake \
    swig \
    patchelf \
    python3-pip \
    python3-venv \
    fontconfig \
    tini \
    xpra \
    xserver-xorg-dev \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-pictures \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Enable multiverse repo, accept MS Fonts EULA, and install fonts
RUN add-apt-repository multiverse && \
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt-get update && apt-get install -yqq ttf-mscorefonts-installer \
    && rm -rf /var/lib/apt/lists/*

# Update font cache (fontconfig package ensures fc-cache is available)
RUN fc-cache -f -v

# --- VIRTUAL ENVIRONMENT SETUP ---
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python packages inside the venv
# Note: numpy < 2.0 to prevent breaking changes for stim/sinter
RUN pip install --upgrade pip && \
    pip install \
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
    "numpy<2.0"

EXPOSE 8888

# Using Tini installed via apt-get
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--notebook-dir=/"]