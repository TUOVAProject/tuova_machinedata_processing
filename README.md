# tuova_machinedata_processing

> ## IMPORTANT!
>
> This repository was created as part of the TUOVA Project (see https://tuova.savonia.fi and https://tuovaproject.github.io/). Some of the information presented here might assume familiarity with other repositories created during the course of the project. For more details on those, see the "Additional Information" section at the bottom of this README.
>
> ### Author
>
> Mika Leskinen \<mika.leskinen@savonia.fi\>\
> R&D Specialist\
> Savonia University of Applied Sciences
>
> [![DOI](https://zenodo.org/badge/1394834167.svg)](https://doi.org/10.5281/zenodo.23395112)
>
> **Everything is provided as-is, use at your own risk.**
>
> TUOVA Project co-funded by the European Union / Etelä-Savon ELY-keskus.
>
> ![Co-funded by the EU](co-fundedbythe-eu.png)

## General

This thing does the following:

1. Fetch e.g. ERP stamping data and machine events from postgres database
2. Check which machine events happened during which stamping event
3. Create updated machine event rows with these fields appended from the stamping event data:

- `workphase_id`
- `work_number`
- `work_id`
- `article_id`
- `user_id`

4. Send the updated machine event rows back to the database.

An Apache Airflow DAG is included, but since the whole process is done in one go in `process.py`, the DAG is more like a wrapper of sorts.

## Prerequisites

- It is assumed that a PostgreSQL database with the data model schema is already deployed (see "Additional Information").

## Config

Create the file `./config.json` with the following (`cp ./config.example.json ./config.json`):

```json
{
    "postgres": {
        "host": "POSTGRES_HOST",
        "port": "POSTGRES_PORT",
        "user": "POSTGRES_USER",
        "password": "POSTGRES_PASS",
        "dbname": "POSTGRES_DBNAME"
    },
    "workcenter_ids": ["WORKCENTER_ID"],
    "from_event_type_ids": [1],
    "from_source_ids": [1],
    "to_source_ids": [2, 3],
    "excluded_to_event_types": [17],
    "check_start_only": false
}
```

- `workcenter_ids`: array of workcenter ids for which to apply the process
- `from_event_type_ids`: only get stamping rows where `event_type_id` is any of these (here it's assumed that `1` is for stamping entries)
- `from_source_ids`: only get stamping rows where `source_id` is any of these (here it's assumed that `1` is for stamping data source)
- `to_source_ids`: only update machine event rows where `source_id` is any of these (here `2` is for machine API data and `3` is for external sensor data)
- `excluded_to_event_types`: only update machine event rows where `event_type_id` is _*NOT*_ one of these (here `17` is for daily summary entries)
- `check_start_only`:
    - `true` = only update machine event rows where the whole event duration (from `start_at` to `end_at`) fits the stamping period
    - `false` = update machine event rows where `start_at` is within the ERP stamping period, don't care about `end_at`.

## Dev Setup

```bash
git clone
uv sync

# single run (defaults to the previous day, adjust date in the file as needed (use "YYYY-MM-DD")):
python3 ./do_the_thing.py
```

## Deployment

1. Run `./build.sh` and copy the resulting files to your server
2. SSH to your server and create the python virtual environment (e.g. `cd /whatever && python3 -m venv venv`)
3. Activate the venv (e.g. `source ./venv/bin/activate`)
4. Install the modules to the python venv (e.g. `pip install -e .`)

## DAG

_(this part assumes you have an Apache Airflow server running and able to access the venv path)_

5. Create an Airflow Variable (via GUI or CLI) called `MACHINEDATA_PROCESSING_PYTHON_EXEC_PATH` with path to the python executable in the venv, e.g. `/whatever/venv/bin/python`
6. Create another Airflow Variable called `MACHINEDATA_PROCESSING_CONFIG_PATH` with path to the `config.json` in the venv, e.g. `/whatever/config.json`
7. Copy the DAG file (`machinedata_processing_dag.py`) to your Airflow instance.
8. Profit.

## Notes

If nothing in this README (or the code) makes sense, feel free to improve.

## LICENSE

See [LICENSE](LICENSE)

## Additional Information

### The TUOVA Project

- https://tuova.savonia.fi
- https://tuovaproject.github.io/

### The data model ("Tuotantotiedon tietomalli")

- https://github.com/TUOVAProject/tuotantotiedon-tietomalli
- https://tuovaproject.github.io/tuotantotiedon-tietomalli/

### On-premises server environment

- https://github.com/TUOVAProject/tuova_on_prem_server

### Sensor data collection system

- https://github.com/TUOVAProject/tuova-iot

### Energy analyzer data collection system

- https://github.com/TUOVAProject/tuova_energymeter

### Sensor data ETL process

- https://github.com/TUOVAProject/tuova-sensor-etl

### Sensor data - further processing

- https://github.com/TUOVAProject/tuova_machinedata_processing
