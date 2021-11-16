# Import in data, do some processing and break up the file
from authentication import ws
from azureml.core import Dataset
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.data import OutputFileDatasetConfig
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
from azureml.core.runconfig import DockerConfiguration

# Set up resources and run configuration
compute_target = ComputeTarget(workspace=ws, name='newcluster1')
experiment = Experiment(ws, 'experiment1')
docker_config = DockerConfiguration(use_docker=True)
run_config = RunConfiguration()
#run_config.environment.docker.enabled = True
run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE
run_config.docker = docker_config
run_config.environment.python.user_managed_dependencies = False
run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['pandas', 'pip'])

# Pipeline step 1: Cleanup file
def_blob_store = ws.get_default_datastore()
ds = Dataset.get_by_name(workspace=ws, name='HPI_file_dataset')
intermediate_source = OutputFileDatasetConfig(destination=(def_blob_store,'/inter/')).as_mount()
intermediate_filename = 'solution.csv'
cleanup_step = PythonScriptStep(
    name="cleanup_step",
    source_directory=".",
    script_name="cleanse.py",
    compute_target=compute_target,
    arguments=[
        "--input_file_path", ds.as_named_input('starting_input').as_mount(),
        "--output_file_path", intermediate_source,
        "--filename", intermediate_filename
        ],
    runconfig=run_config,
    allow_reuse=False
    )

# Pipeline step 2: Break up file, and store results to blob
final_source = OutputFileDatasetConfig(destination=(def_blob_store,'/inter/')).as_mount()
breakup_step = PythonScriptStep(
    name="breakup_step",
    source_directory=".",
    script_name="breakup.py",
    compute_target=compute_target,
    arguments=[
        "--input_file_path", intermediate_source.as_input(),
        "--output_file_path", final_source,
        "--filename", intermediate_filename
        ],
    runconfig=run_config,
    allow_reuse=False
)

# Actual pipeline integration
steps = [ cleanup_step, breakup_step ]
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline_run = experiment.submit(pipeline)
pipeline_run.wait_for_completion()

# Publish the pipeline
published_pipeline = pipeline.publish('Final_pipeline')
