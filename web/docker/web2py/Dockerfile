# base dockerfile from git@github.com:cabildocl/web2py-docker.git
FROM nginx:latest
MAINTAINER VARIA "varia@varia.run"

ENV CERT_PASS web2py
ENV CERT_DOMAIN web2py.local
#password web2py admin
ENV PW admin
ARG BRANCH=master
ARG GITHUB_TOKEN

EXPOSE 443 80 8000

RUN apt-get update && \
    apt-get install wget -y && \
    apt-get install unzip -y && \
    apt-get -y install python3 python3-pip && \
    pip3 install gunicorn mysql-connector-python
RUN apt-get install -y supervisor unzip git

WORKDIR /root
RUN wget https://mdipierro.pythonanywhere.com/examples/static/web2py_src.zip && \
	unzip web2py_src.zip && \
	rm web2py_src.zip

WORKDIR /root/web2py
RUN python3 -c "from gluon.main import save_password; save_password('$PW',80)" && \
    python3 -c "from gluon.main import save_password; save_password('$PW',443)" && \
    python3 -c "from gluon.main import save_password; save_password('$PW',8000)"

RUN mkdir /certs
WORKDIR /certs
RUN openssl genrsa -passout pass:$CERT_PASS 2048 > web2py.key && \
    openssl req -new -x509 -nodes -sha1 -days 1780 -subj "/C=US/ST=Denial/L=Chicago/O=Dis/CN=$CERT_DOMAIN" -key web2py.key > web2py.crt && \
    openssl x509 -noout -fingerprint -text < web2py.crt > web2py.info

# add VARIA source and submodules, use /root as HOME
WORKDIR /root
RUN if [ -n "${GITHUB_TOKEN}" ]; then \
    git clone --recurse-submodules -b ${BRANCH} https://${GITHUB_TOKEN}:x-oauth-basic@github.com/theonlydude/RandomMetroidSolver.git; \
else \
    wget https://github.com/theonlydude/RandomMetroidSolver/archive/${BRANCH}.zip && unzip ${BRANCH}.zip && mv RandomMetroidSolver-${BRANCH} RandomMetroidSolver && rm -f ${BRANCH}.zip; \
    cd RandomMetroidSolver; \
    rm -rf varia_custom_sprites && wget https://github.com/theonlydude/varia_custom_sprites/archive/main.zip && unzip main.zip && mv varia_custom_sprites-main varia_custom_sprites && rm -f main.zip; \
    rm -rf super-metroid && wget https://github.com/chriscauley/super-metroid/archive/main.zip && unzip main.zip && mv super-metroid-main super-metroid && rm -f main.zip; \
fi

# fetch race mode, only through github because private repo
RUN if [ -n "${GITHUB_TOKEN}" ]; then git clone https://${GITHUB_TOKEN}:x-oauth-basic@github.com/theonlydude/varia-race-mode; fi

# add community presets
WORKDIR /root/web2py
RUN mkdir -p /root/web2py/varia_repository
RUN wget https://github.com/theonlydude/community_presets/archive/master.zip && unzip master.zip && mv community_presets-master community_presets && rm -f master.zip

# add symbolic links and other web2py customization
RUN ln -s /root/RandomMetroidSolver/rando_presets /root/web2py/rando_presets
RUN ln -s /root/RandomMetroidSolver/standard_presets /root/web2py/standard_presets
RUN rm -f /web2py/routes.py && ln -s /root/RandomMetroidSolver/web/static/routes.py /root/web2py/routes.py
RUN mkdir -p /root/web2py/plandository /root/web2py/roms /root/web2py/applications/solver

WORKDIR /root/web2py/applications/solver
RUN mkdir cache  controllers  cron  databases  errors  languages  models  modules  private  sessions  static  uploads  views
RUN mkdir -p views/solver_web && touch views/solver_web/__init__.py
WORKDIR /root/web2py/applications/solver/static
RUN mkdir -p js graph fonts images/sprite_sheets css


# install yarn
RUN apt-get install curl
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt install nodejs
RUN wget https://github.com/yarnpkg/yarn/releases/download/v1.22.19/yarn_1.22.19_all.deb && \
    apt-get remove -y cmdtest && \
    dpkg -i yarn_1.22.19_all.deb && \
    rm -f yarn_1.22.19_all.deb

# compile new tracker
WORKDIR /root/RandomMetroidSolver/super-metroid/client
RUN yarn install
RUN yarn build:varia

# varia install
RUN /root/RandomMetroidSolver/web/install.sh
RUN /root/RandomMetroidSolver/varia_custom_sprites/install.sh
RUN if [ -n "${GITHUB_TOKEN}" ]; then VARIA_DIR=/root/RandomMetroidSolver /root/varia-race-mode/install.sh; fi

# add db conf
RUN echo "dbParams = dict(host='varia-mysql', user='varia', database='varia', password='varia', port=3306)" > /root/RandomMetroidSolver/db_params.py

# add web conf
COPY nginx.conf /etc/supervisor/conf.d/nginx.conf
COPY web2py.conf /etc/supervisor/conf.d/web2py.conf

WORKDIR /
CMD ["supervisord", "-n"]