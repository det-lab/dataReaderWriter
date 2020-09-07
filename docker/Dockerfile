FROM ubuntu:latest
USER root
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ENV TZ=America/Denver

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    echo "Set disable_coredump false" >> /etc/sudo.conf && \
    apt update -y && apt upgrade -y && \
    apt install -y sudo gnupg cmake gcc g++ wget git vim

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O /opt/anaconda.sh && \
    /bin/bash /opt/anaconda.sh -b -p /opt/anaconda3

RUN . /opt/anaconda3/etc/profile.d/conda.sh && conda activate base && \
    git clone --recursive https://github.com/scikit-hep/awkward-1.0.git /opt/awkward-1.0 && \ 
    cd /opt/awkward-1.0 && \
    python setup.py install --user

RUN cd ~ && \
    git clone https://github.com/det-lab/dataReaderWriter.git && \
    git clone https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime.git && \
    mv -f kaitai_struct_cpp_stl_runtime/ dataReaderWriter/kaitai/awkward_example && \
    git clone https://gitlab.com/glass-ships/bash-env.git && \
    echo "source /root/bash-env/main" >> /root/.bashrc && \
    echo "source /opt/anaconda3/etc/profile.d/conda.sh && conda activate base" >> /root/.bashrc
