This folder is for the MODTRAN automation pipeline. The folders are as follows:

- complete_pipeline: has the entire pipeline complete and put together
- sub_steps: 
    - 1_parse_csv: the code to parse the giant dataset csv files into csv files of individual spectra
    - 2_csv_to_sli: the code to convert .csv to .sli, through the use of ENVI
    - 3_generate_json: the code to mass generate the json files which will be used to run MODTRAN
    - 4_loop_forward: the code to loop through the JSON files and perform forward propagation
    - 5_noise: all the functions to add noise to the generated spectra
    - 6_inversion: code to invert the simulated data and retreive the data. it also includes the code to put together all the data generated
- runs:
    the jupyter notebooks which we use to run all the processes

The sub-folders might have their own readme files. Make sure to read them.