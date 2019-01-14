FROM python:3-alpine

ARG SOPEL_GID=100000
ARG SOPEL_UID=100000

RUN set -ex \
  && apk add --no-cache \
      enchant \
  && addgroup -g ${SOPEL_GID} sopel \
  && adduser -u ${SOPEL_UID} -G sopel -h /home/sopel sopel -D

USER sopel
WORKDIR /home/sopel

COPY --chown=sopel:sopel . ./sopel-src
RUN set -ex \
  && cd ./sopel-src \
  && python setup.py install --user \
  && rm -rf /home/sopel/sopel-src

ENV PATH="/home/sopel/.local/bin:${PATH}"

# OS X users will crash with permission errors if they use a
#     volume over /home/sopel/.sopel - nothing we can do about it.
# Workaround: Don't use OS X
# https://github.com/boot2docker/boot2docker/issues/581
# https://github.com/docker/kitematic/issues/351
VOLUME [ "/home/sopel" ]
CMD [ "sopel" ]