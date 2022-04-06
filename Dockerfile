FROM debian:buster
RUN apt-get update
RUN apt-get install -y python3 python3-pip libzbar0 libidn2-dev locales traceroute git libcairo2-dev wget
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
RUN git clone https://github.com/YukariChiba/tgbot /code
RUN mkdir -p /code/data/Dress && wget https://raw.githubusercontent.com/YukariChiba/DressMeta/data/dress.json -O /code/data/Dress/dress.json
RUN mkdir -p /code/data/Dress && wget https://raw.githubusercontent.com/YukariChiba/DressMeta/data/dress.lite.json -O /code/data/Dress/dress.lite.json
RUN pip3 install -r /code/requirements.txt
WORKDIR /code
CMD python3 main.py
