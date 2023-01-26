install:
	#conda create -n steps python=3.8 -y; conda activate steps
	pip install azure-ai-ml
	pip install azure-identity
	pip install python-dotenv
	pip install pandas
	pip install flake8

# Setup infrastructure
infra:
	./setup/create-resources.sh

# Setup clusters, 
create_cluster:
	python ./common/cluster.py

# Setup environment
create_env:
	python ./common/env.py --name "housing-env" --conda_file "./config/conda.yml"

# Manually upload the HPI_master.csv file in the data folder into the default blobstore

run_pipeline:
	python ./scripts/main.py
