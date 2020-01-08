FROM ubuntu:latest
USER root

ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

RUN apt update -y && apt upgrade -y && \
    apt install -y  git gnupg make g++

RUN mkdir ~/.gnupg && echo "disable-ipv6" >> ~/.gnupg/dirmngr.conf

# add repository for kaitai-struct-compiler (unstable) 
RUN apt-key adv --keyserver hkp://pool.sks-keyservers.net --recv 379CE192D401AB61 && \
    echo "deb https://dl.bintray.com/kaitai-io/debian_unstable jessie main" | tee /etc/apt/sources.list.d/kaitai.list

RUN apt update -y && apt install -y kaitai-struct-compiler

RUN git clone https://github.com/det-lab/dataReaderWriter.git
RUN cd dataReaderWriter && \
    git checkout develop && \
    cd kaitai/simple_example && \
    kaitai-struct-compiler -t cpp_stl ../ksy/animal.ksy && \
    mv animal.* src/ && \
    make -f makefile && \ 
    mkdir bin && mv kaitaiAnimalExample bin/ && \
    rm *.o  
