# UHSLC tide gauge station tools
### Set of tools for loading, processing and saving sea level data

**Note:** This is still in development and certain pieces of code were ported directly from Matlab, 
so there might be awkward naming conventions and non-pythonic code.

## Running the software
First step is to install the python package built based on the source code in this repo:

```
pip install uhslc-station-tools
```

This will give you a set of tools that you can use to load, process and save sea level data directly from your python script.

### Loading legacy sea level data (.dat format)
```python
from uhslc_station_tools.extractor import load_station_data
station_data = load_station_data([input_filename])
```


`input_filename` is the path to the .dat file you want to load. You can load multiple months of data by passing a list of file paths to the `load_station_data` function.
The data files have to be ordered by date (from oldest to most recent) and months must be consecutive, and must belong to the same station. The object returned by the `load_station_data` function is a `Station` object. The `Station` class is defined [here](https://github.com/uhsealevelcenter/station_tools/blob/master/uhslc_station_tools/sensor.py). 

### Saving sea level data (.dat and .mat format)
Several attributes of the `Station` object are available to you. The most important ones are:
* `save_fast_delivery`
* `save_mat_high_fq`
* `save_to_annual_file`

You can call `save_fast_delivery` attribute on the station instance:
```python
station_data.save_fast_delivery(din_path: str, path: str, is_test_mode=False, callback: Callable = None)
```

`din_path` is the path to the .din file that lists primary sensors for each station

`path` is the path to the folder where you want to save the fast delivery output files (daily and hour data in both .mat and .dat format). 

`is_test_mode` is a boolean that determines whether you want to save the file in a directory named `test_data` (if `True`) or `production_data` (if `False`)

`callback` is a function that will be called after all the files are saved. The function takes two arguments: the first one is the success message and the second is the failure (in case any exception is raised).

You can also call `save_mat_high_fq` attribute on the station instance:
```python
station_data.save_mat_high_fq(path: str, is_test_mode=False, callback: Callable = None)
```

`path` is the path to the folder where you want to save the high frequency output files (high frequency data in both .mat and .dat formats). 

`is_test_mode` is a boolean that determines whether you want to save the file in a directory named `test_data` (if `True`) or `production_data` (if `False`)

`callback` is a function that will be called after all the files are saved. The function takes two arguments: the first one is the success message and the second is the failure (in case any exception is raised).


You can also call `save_to_annual_file` attribute on the station instance:
```python
station_data.save_to_annual_file(path: str, is_test_mode=False, callback: Callable = None)
```
`path` is the path to the folder where you want to save the annual output files (annual data .mat format). 

`is_test_mode` is a boolean that determines whether you want to save the file in a directory named `test_data` (if `True`) or `production_data` (if `False`)

`callback` is a function that will be called after all the files are saved. The function takes two arguments: the first one is the success message and the second is the failure (in case any exception is raised). This function only appends the already existing high frequency monthly files (produced by `save_mat_high_fq`), so to produce an annual file it is necessary to either produce the monthly high
frequency files first or to call the annual function on a folder where the monthly high frequency files are already present.


### Data processing (hourly)

To process arbitrary sea level data (data independent of the UHSLC .dat format) in order to produce hourly data, you can use the `hr_process` function:
(all the filtering tools were rewritten based on the research quality Matlab scripts)
```python
from uhslc_station_tools.filtering import hr_process
data_hr = hr_process(data_object, datetime_start, datetime_end)
```
`datetime_start` and `datetime_end` are `datetime` objects that define the time interval you want to process:
```python
from datetime import datetime
datetime_start = datetime(2019, 1, 1, 0, 0, 0)
datetime_end = datetime(2019, 2, 1, 0, 0, 0)
```
`data_object` is a json-like object that has a key describing the sensor that data belongs to (a three letter string, lower case; e.g. 'prs')
inside of that key is time vector and high frequency sea level data, and optional station ID (three digit string):

```json
{
    "prs": {
        "time": [matlab_epoch1, matlab_epoch2, ...],
        "data": [3456, 3211, ...],
        "station": '014'
    }
}
```

`"time"`: a list of matlab epoch timestamps (floats) that correspond to the high frequency data points in `"data"` key.

`"data"`: a list of high frequency sea level data points.

`"station"`: a three digit string that represents the station ID. It must be defined, but it can be any string.

To convert a list of datetime objects to matlab epoch timestamps, you can use the `datenum2` function in `utils.py`.

The `hr_process` function returns a json-like object that has time, sealevel, and station id keys nested inside of the sensor name key:
```json
{
    "prs": {
        "time": [matlab_epoch1, matlab_epoch2, ...],
        "data": [3456, 3211, ...],
        "station": '014'
    }
}
```

`"time"`: a list of matlab epoch timestamps (floats) that correspond to the hourly data points in `"data"` key.

`"data"`: a list of hourly sea level data points.

`"station"`: a three digit string that represents the station ID. It must be defined, but it can be any string.

To convert matlab epoch timestamps to datetime objects, you can use the `matlab2datetime` function in `utils.py`.

### Data processing (daily)
To filter the high freqeuncy data to produce daily data, you can use the `day_119filt` function. The data will first needed 
to be processed to hourly data using the `hr_process` function. The `day_119filt` function takes the hourly data as input:
```python
from uhslc_station_tools.filtering import day_119filt
data_day = day_119filt(hourly_merged, latitude)
```

`hourly_merged` is produced by supplying the hourly data (`data_hr` from above) to the `channel_merge` function:
```python
from uhslc_station_tools.filtering import channel_merge
ch_params = [{'prs': 0}]
hourly_merged = channel_merge(data_hr, ch_params)
```

`ch_params`: for more details, see [channel_merge function](https://github.com/uhsealevelcenter/station_tools/blob/master/uhslc_station_tools/filtering.py)
UHSLC fast delivery product does not actually merge channels (we only use the primary channel). This is different from Research Quality, where 
the channels are actually merged (filling in the missing data by using a different channel). But we still need to run the data through the merge function, even though we are only using one channel
in order to get the correct output data format suitable for the daily filter.

`data_day` returns a json-like object that has `time`, `sealevel`, `channel`, and `residual` values.


## Command Line interface
Under construction

## Development

If you would like to contribute to this project, please fork (or make a new branch) the repository and submit a pull request.
Below is a set of requirements for contributing to this project.
### Requirements
* Python 3.6.7 (to match the version used to build the GUI tool for data cleaning. It might work on other versions of Python but not tested)
* The remaining requirements are listed in the requirements.txt file. To install the requirements run the following command from the command line:
```
pip install -r requirements.txt
```
