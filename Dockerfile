FROM python:2.7

RUN useradd -m inumuta
RUN mkdir -p /home/inumuta/.willie/ && chown inumuta /home/inumuta/.willie/
VOLUME /home/inumuta/.willie/

ENTRYPOINT ["/usr/local/bin/python", "/usr/local/bin/willie"]

ADD dev-requirements.txt /
RUN pip install -r /dev-requirements.txt && rm /dev-requirements.txt

ADD . /inumuta/

RUN cd inumuta && python setup.py install

USER inumuta
