# start by pulling the python image
FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ python3-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# run the recommender
CMD ["python", "frontend/recommender/app.py"]
