install:
	#pip install --upgrade pip && pip install -r requirements.txt
	./create-workspace-sprbac.sh

setup_run:
	python clusters.py
	python datasets.py

pipeline_setup:
	python basic_pipeline.py

trigger_pipeline:
	python trigger_pipeline.py

all: install setup_run pipeline_setup trigger_pipeline 
