# tuova_machinedata_processing

> ## IMPORTANT
>
> This repository was created as part of the TUOVA Project (see https://tuova.savonia.fi and https://tuovaproject.github.io/). Most of the information provided here assumes some familiarity with the data model ("Tuotantotiedon tietomalli") also developed during the TUOVA Project (see https://github.com/TUOVAProject/tuotantotiedon-tietomalli).
>
> **Repository provided as-is, use at your own risk.**
>
> TUOVA Project co-funded by the European Union / Etelä-Savon ELY-keskus.

## General

This thing does the following:

1. Fetch e.g. ERP stamping data and machine events from postgres database
2. Check which machine events happened during which stamping event
3. Create updated machine event rows with these fields appended from said stamping event:

- `workphase_id`
- `work_number`
- `work_id`
- `article_id`
- `user_id`

4. Update said machine event rows back to the database.

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

# single run:
python3 ./main.py
```

## DAG

TODO

## Deployment

TODO

## Licence

TODO
