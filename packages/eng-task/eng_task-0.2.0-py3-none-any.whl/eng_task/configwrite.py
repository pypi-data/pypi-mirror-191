from configparser import ConfigParser

config = ConfigParser()

config["DEFAULT"] = {
    "output_dir":"/Users/jedmundson",
    "filenamme" : "raw.csv",
    "clean_data" : "_clean_data",
    "data_profiling" : "_data_profiling",
    "data_consistency" : "_data_consistency",
}

with open("configure.ini","w") as f:
    config.write(f)