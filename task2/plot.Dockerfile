FROM python:3

ADD generate_plots.py /

RUN pip install pandas && \
    pip install matplotlib && \
    pip install seaborn

CMD [ "python", "./generate_plots.py" ]