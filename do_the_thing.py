from tuova_machinedata_processing import process

# NOTE: this file is not used by the DAG

def do_the_thing(date=None, dry_run=False):
    process.run(date=date, dry_run=dry_run)

if __name__ == "__main__":
    do_the_thing(date=None, dry_run=True)
