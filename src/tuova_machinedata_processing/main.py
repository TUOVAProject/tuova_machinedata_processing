import json
from datetime import datetime, timedelta
import psycopg
from tuova_machinedata_processing import postgres
from tuova_machinedata_processing import data_processor

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("psycopg").setLevel(logging.DEBUG)

def main():
    opts = None
    with open("./config.json") as f:
        opts = json.loads(f.read())
    if opts is None:
        print("main - err: no opts")
        return -1

    # connect client
    p = opts["postgres"]
    pg_client = psycopg.connect(row_factory=psycopg.rows.dict_row, conninfo=f'host={p["host"]} port={p["port"]} user={p["user"]} password={p["password"]} dbname={p["dbname"]}')
    opts["pg_client"] = pg_client

    # create dates
    start_at = (datetime.now() + timedelta(days=-1)).date().isoformat()
    end_at = (datetime.now()).date().isoformat()
    opts["start_at"] = start_at
    opts["end_at"] = end_at

    # LOGIK!
    
    # fetch
    data = postgres.get_data(opts=opts)
    # transform
    newdata = data_processor.transform(opts=opts, data=data)
    # update
    postgres.update_data(opts=opts, newdata=newdata)


if __name__ == "__main__":
    main()
