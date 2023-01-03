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

## Usage
To start, import the package, and define an experiment. 
First, get the name of the notebook you're working with by running:
```
curr_notebook =  re.search('(.+).ipynb',os.path.basename(globals()['__vsc_ipynb_file__']))[1]
```
Alternatively, you can directly use the name of the file you're working with.

Next, use experiment class to define a new class for your experiment (run) by:
```
expr = experiments.experiment(curr_notebook, overwrite_existing=False)
```

To log a message, use:
expr.log("This is a logged message.")

To wirte a file (image, excel, etc.) you'll need to log the file first by using log_file function:
```
FileName_excel = expr.log_file('Test_excel_file.xlsx')
```
Then, you can use the FileName_excel variable in the ExcelWriter:
```
writer = pd.ExcelWriter(FileName_excel)
```
