###
### Author: rdt12@psu.edu
### Date:   Jun 29, 2020
### Desc:   Build a container that sends a heartbeat message every 30 seconds
###         using the hop library.
###
FROM scimma/client:0.2.0
RUN  mkdir -p /usr/local/src
RUN yum -y install git unzip
RUN cd /usr/local/src && \
    curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws
ADD scripts/hopBeatMon /root/hopBeatMon
ADD scripts/Utils.py       /root/Utils.py
ADD scripts/runHopBeatMon.py /root/runHopBeaMont.py
RUN chmod ugo+rx /root/hopBeatMon
RUN chmod ugo+rx /root/runHopBeatMon.py
WORKDIR /tmp
#ENTRYPOINT ["/root/runHopBeat.py"]
