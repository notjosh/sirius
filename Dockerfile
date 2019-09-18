FROM python:3.7.4-slim-buster

WORKDIR /sirius

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  curl \
  gnupg

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  python3 \
  python3-dev \
  python3-pip \
  libfreetype6-dev \
  libgstreamer1.0-dev \
  libjpeg-dev \
  libpq-dev \
  zlib1g-dev \
  fontconfig \
  fonts-dejavu \
  fonts-noto-color-emoji \
  gcc \
  google-chrome-stable \
  postgresql-11 \
  unzip \
  git && \
  apt-get autoremove -y

# Find the latest version for `chromedriver` that matches our installed `google-chrome` & install it to be available on $PATH
RUN COMMON_VERSION=$(google-chrome --version | sed -nre "s/.* ([0-9]+\.[0-9]+\.[0-9]+)/\1/p" | cut -d"." -f1-3) && \
  URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${COMMON_VERSION}" && \
  CHROMEDRIVER_VERSION=$(curl -Ss "${URL}") && \
  CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
  curl "${CHROMEDRIVER_URL}" -o "${HOME}/chromedriver_linux64.zip" && \
  unzip "${HOME}/chromedriver_linux64.zip" -d "${HOME}/" && \
  rm "${HOME}/chromedriver_linux64.zip" && \
  mv -f "${HOME}/chromedriver" /usr/local/bin/chromedriver && \
  chmod 0755 /usr/local/bin/chromedriver

RUN pip install --upgrade pip

ADD ./requirements.txt /sirius/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install honcho

EXPOSE 5000

ADD . .
