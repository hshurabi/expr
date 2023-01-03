# expr
Experiment versioning

To use the package, project should be organized into a combination of local files (which includes outputs and data and data dictionary) and code (which is your cloned git repo for the project).

Here is an example:

.
├── project xyz
├── Data                    # data for the project
├── xyz                     # Cloned git repo for the project codes
│   ├── cleaning            # Cleaning step
│   ├── model_evaluation    # Model evaluation
│   ├── Tuning              # Tuning step
│   └── ...
├── Dictionary              # data dictionary for the project data
└── Results                 # Results folder for the outputs of experiments
