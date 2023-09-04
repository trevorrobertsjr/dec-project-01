FROM python:3.9 

WORKDIR /source 

COPY requirements.txt .

RUN pip install -q -r requirements.txt

COPY /source .

CMD ["python", "-m", "us_real_estate.pipelines.us_real_estate"]