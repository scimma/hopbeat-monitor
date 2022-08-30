###
### Author: rdt12@psu.edu
### Date:   Jun 29, 2020
### Desc:   Build a container that sends a heartbeat message every 30 seconds
###         using the hop library.
###
FROM scimma/client:0.7.1
RUN  mkdir -p /usr/local/src
RUN yum -y install git unzip python3-pytz.noarch python38-pytz.noarch
RUN cd /usr/local/src && \
    curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws
ADD scripts/hopbeatMon /root/hopbeatMon
ADD scripts/Utils.py       /root/Utils.py
ADD scripts/HeartUtils.py /root/HeartUtils.py
ADD scripts/runHopbeatMon.py /root/runHopbeatMon.py
RUN chmod ugo+rx /root/hopbeatMon
RUN chmod ugo+rx /root/runHopbeatMon.py
WORKDIR /tmp
ENTRYPOINT ["/root/runHopbeatMon.py"]
