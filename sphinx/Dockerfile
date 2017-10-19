FROM centurylink/sphinx

#RUN yum install -y python-pip; yum clean all
#RUN pip2 install lxml
RUN cd /opt
RUN wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz && tar xf Python-2.7.6.tar.xz && cd ./Python-2.7.6 && ./configure --prefix=/usr/local && make && make altinstall

RUN wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py 
#RUN /usr/local/bin/python2.7 ez_setup.py 
#RUN /usr/local/bin/easy_install-2.7 pip
COPY sphinx.conf /usr/local/etc/sphinx.conf
COPY sphinx-xmlpipe2.py /sphinx-xmlpipe2.py

RUN ls -ls /usr/local/etc
#RUN python2 sphinx-xmlpipe2.py

