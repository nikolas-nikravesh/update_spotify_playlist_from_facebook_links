FROM centos:7

RUN yum -y update

RUN yum install -y \
    python3 \
    vim 

RUN pip3 install \
    requests 

