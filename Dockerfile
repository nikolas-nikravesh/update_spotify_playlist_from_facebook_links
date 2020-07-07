FROM centos:7

RUN yum -y update

RUN yum install -y \
    python3 \
    jq \
    vim 

RUN pip3 install \
    requests 

