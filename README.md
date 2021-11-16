# Intent
- Showcase a simple Azure ML pipeline with two python script steps
- Sample dataset taken from [Federal Housing Finance Agency
  datasets](https://www.fhfa.gov/DataTools/Downloads/Pages/House-Price-Index-Datasets.aspx#mpo) stored in the ./input-data folder

# Steps
- In the ./scripts folder, create a ```sub.env``` file with the following line: ```SUB_ID=<your subscription id>```
- The `Makefile` contains a general flow of the steps needed to run this basic pipeline. Added notes:
	- Run the ```create-workspace-sprbac.sh``` shell script to provision the AML workspace.
	- Create a cluster through the ```clusters.py``` script.
	- Upload the dataset in the ./input-data folder through the ```datasets.py``` script.
	- Run the ```basic_pipeline.py``` script which runs two Python Script steps and publishes the
	  pipeline.
	- Run the `trigger_pipeline.py` script to see how to query the published pipeline and then trigger it
	  based on a timed cadence.
- The two Python Script steps run in the ```basic_pipeline.py``` correspond to the ```cleanse.py``` and the
  ```breakup.py``` file respectively. These are simple data transformations on the uploaded dataset just to highlight
  inputs and outputs between pipeline steps.
- As part of the ```create-workspace-sprbac.sh``` provisioning, two environment specific files get created:
	- ```config.json``` This is the standard workspace configuration file.
	- ```variables.env``` This captures service principal info, used in the ```authentication``` script.
- As part of the ```create-workspace-sprbac.sh``` script, names are derived based upon a random choice
  combining the ```nouns.txt``` and the ```adjectives.txt``` file, implemented in the ```random_name.py``` script.

