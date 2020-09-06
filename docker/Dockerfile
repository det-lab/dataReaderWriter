FROM ubuntu:latest
USER root

ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ENV TZ=America/Denver

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt update -y && apt upgrade -y && \
    apt install -y git sudo gnupg cmake wget gcc g++ && \
    echo "Set disable_coredump false" >> /etc/sudo.conf

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O /opt/anaconda.sh && /bin/bash /opt/anaconda.sh -b -p /opt/anaconda3

RUN . /opt/anaconda3/etc/profile.d/conda.sh && conda activate base && \
    git clone --recursive https://github.com/scikit-hep/awkward-1.0.git /opt/awkward-1.0 && cd /opt/awkward-1.0 && python setup.py install --user

RUN cd ~ && \
    git clone https://github.com/det-lab/dataReaderWriter.git && \
    echo "source /opt/anaconda3/etc/profile.d/conda.sh && conda activate base" > /root/.bashrc 
