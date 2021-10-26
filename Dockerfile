FROM python:3-alpine
WORKDIR /seleniumpytest
COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt"]
COPY . .
ENTRYPOINT ["pytest"]
CMD ["-v"]