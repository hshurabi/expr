# expr
Experiment versioning

To use the package, project should be organized into a combination of local files (which includes outputs and data and data dictionary) and code (which is your cloned git repo for the project).

### An example top-level directory layout

    .
    ├── project xyz               # Porject directory in your local system
      ├── Data                    # Data for the project, includes all data files
      ├── xyz                     # Cloned git repo for the project codes, includes all the code
        ├── cleaning              # Cleaning step
        ├── model_evaluation      # Model evaluation
        ├── Tuning                # Tuning step
        └── ...
      ├── Dicionary               # data dictionary for the project data
      ├── Results                 # Results folder for the outputs of experiments, results of each run will be stored here.
      └── README.md

