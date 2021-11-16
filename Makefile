install:
	pip install --upgrade pip && pip install -r requirements.txt
	./scripts/create-workspace-sprbac.sh

setup_run:
	python ./scripts/clusters.py
	python ./scripts/datasets.py

pipeline_setup:
	python ./scripts/basic_pipeline.py

trigger_pipeline:
	python ./scripts/trigger_pipeline.py

all: install setup_run pipeline_setup trigger_pipeline 
