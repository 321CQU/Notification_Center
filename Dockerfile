FROM python:3.11

COPY requirements.txt /src/

WORKDIR /src
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

EXPOSE 53210

CMD ["python", "main.py"]