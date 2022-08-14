FROM python

WORKDIR /UFP

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt'

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]