<div align="center"> 
    <h1>
        Question Answering kit
    </h1>
</div>

## Requirements

    - python >= 3.7

```bash
# python environment
which python3
python3 -m venv nanoEnv
source ./nanoEnv/bin/activate

# m1 chip, problem shooting pyserini installation
# CFLAGS="-mavx -DWARN(a)=(a)" pip install nmslib 

# pip3 upgrade
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

    - Elasticsearch

```bash
# run elasticsearch in a docker container
docker run -d -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.9.2
# after creation of the container, run the following command to start the container
docker start <container_id>
```

## Todos

- [X] Migrate/Re-Implement full QA functions
- [X] Implementation of pdf conversion.
- [X] Implementation of file extraction.
- [X] Implementation of Retriever via ElasticSearch
- [X] Implementation of fine-tuning the reader with adapter
- [X] Put tests
