FROM debian:sid

# use mirrors.ocf.berkeley.edu
RUN sed -i 's|httpredir\.debian\.org|mirrors.ocf.berkeley.edu|g; \
        s|security\.debian\.org|mirrors.ocf.berkeley.edu/debian-security|g' \
        /etc/apt/sources.list


RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
         ca-certificates  curl  htop  net-tools  sudo  vim-tiny  \
    && rm -rf /var/lib/apt/lists/*



RUN curl -sLo /tmp/dumb-init.deb \
        https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64.deb \
    && dpkg -i /tmp/dumb-init.deb \
    && rm /tmp/dumb-init.deb \
    && apt-get clean
ENTRYPOINT ["/usr/bin/dumb-init", "-c", "--"]




# add deb-src entries
RUN sed 's/^deb /deb-src /' /etc/apt/sources.list >> /etc/apt/sources.list

# vim: ft=jinja
