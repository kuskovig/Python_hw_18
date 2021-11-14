FROM python:3-alpine
WORKDIR /seleniumpytest
COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt"]
COPY . .
RUN ["mkdir", "-p", "logs"]
ENTRYPOINT ["pytest"]
CMD ["-v"]