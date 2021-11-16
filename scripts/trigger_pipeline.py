from authentication import ws
from azureml.pipeline.core import Pipeline, PublishedPipeline
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule


def main():
    # List out published pipelines (should only be one)
    published_pipelines = PublishedPipeline.list(ws)
    for published_pipeline in published_pipelines:
        pipeline_name = published_pipeline.name
        pipeline_id = published_pipeline.id
        print(f"{published_pipeline.name},'{published_pipeline.id}'")

    # Triggering through a REST CALL
    #from azureml.pipeline.core import PublishedPipeline
    # import requests
    # response = requests.post(published_pipeline.endpoint, #headers=aad_token,json={"ExperimentName": "experiment1"})

    # Triggering through a schedule
    recurrence = ScheduleRecurrence(frequency="Minute", interval=5)
    recurring_schedule = Schedule.create(ws, name="Trigger_every_5_minutes",
                                description="Based on every 5 minutes",
                                pipeline_id= pipeline_id,
                                experiment_name='experiment1', 
                                recurrence=recurrence)

if __name__ == "__main__":
    main()
