FROM python:3

ADD generate_plots.py /

RUN pip install numpy && \
    pip install matplotlib

CMD [ "python", "./generate_plots.py" ]