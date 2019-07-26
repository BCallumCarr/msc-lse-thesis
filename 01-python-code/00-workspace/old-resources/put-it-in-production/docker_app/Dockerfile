FROM jupyter/scipy-notebook

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONBUFFEREED=1
WORKDIR /tmp

COPY predict.py ./predict.py
COPY utils.py ./utils.py
COPY train.py ./train.py

ADD dtypes.pkl ./dtypes.pkl
ADD training_listings.csv ./training_listings.csv

RUN python3 train.py
ENTRYPOINT ["python3", "predict.py"]
