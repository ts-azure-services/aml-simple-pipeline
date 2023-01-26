from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import command, dsl, Input, Output
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.authenticate import ml_client

env = "housing-env:1"

# First component randomly selects a few cities
random_component = command(
    code="./",
    name="Random selection of cities",
    description="Randomly selecting cities and counties",
    inputs={"input_data": Input(type=AssetTypes.URI_FOLDER)},
    outputs={"output_data": Output(type=AssetTypes.URI_FOLDER)},
    command="python ./scripts/random_selection.py --input_data ${{inputs.input_data}} --output_data ${{outputs.output_data}}",
    environment=env,
    compute="cpu-cluster",
)

# Second component prepares the data for an ML training model
data_prep_component = command(
    code="./",
    name="Data Prep Component",
    description="Filtering for specific segments of the data",
    inputs={"input_data": Input(type=AssetTypes.URI_FOLDER)},
    outputs={"output_data": Output(type=AssetTypes.URI_FOLDER)},
    command="python ./scripts/data_prep.py --input_data ${{inputs.input_data}} --output_data ${{outputs.output_data}}",
    environment=env,
    compute="cpu-cluster",
)


# DEFINE THE PIPELINE
@dsl.pipeline(compute='cpu-cluster')
def seq_pipeline(pdf_inputs):
    random_selection_job = random_component(input_data=pdf_inputs,)
    data_prep_job = data_prep_component(input_data=random_selection_job.outputs.output_data)

    # A pipeline returns a dictionary of outputs
    # Keys will code for the pipeline output identifier
    return {
        "pipeline_random_job_output": random_selection_job.outputs.output_data,
        "pipeline_data_prep_job_output": data_prep_job.outputs.output_data,
    }


if __name__ == "__main__":
    # Instantiate the pipeline
    default_blob_path = "azureml://datastores/workspaceblobstore/paths/"
    random_job_path = "azureml://datastores/workspaceblobstore/paths/random_job/"
    data_prep_path = "azureml://datastores/workspaceblobstore/paths/data_prep/"
    pipeline = seq_pipeline(pdf_inputs=Input(type=AssetTypes.URI_FOLDER, path=default_blob_path))
    pipeline.outputs.pipeline_random_job_output = Output(type=AssetTypes.URI_FOLDER, path=random_job_path)
    pipeline.outputs.pipeline_data_prep_job_output = Output(type=AssetTypes.URI_FOLDER, path=data_prep_path)

    # Submit the pipeline job
    pipeline_job = ml_client.jobs.create_or_update(pipeline, experiment_name="sample-pipeline")
