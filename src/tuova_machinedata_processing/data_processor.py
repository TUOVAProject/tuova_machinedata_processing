from datetime import datetime, timedelta

def transform(opts={}, data=None):
    # return [{}]
    print("data_processor - transform...")

    if len(data["from_data"]) <= 0 or len(data["to_data"]) <= 0:
        print("data_processor - transform: no data")
        return None


    # TODO:
    # here's the plan:
    # 1. for each from_data row:
    # 2.    for each to_data row:
    #           update those that don't have work_number
    # 3. return

    for from_row in data["from_data"]:
        print(f'{from_row["start_at"]} - {from_row["end_at"]}')

    print("---")

    for to_row in data["to_data"]:
            print(f'{to_row["start_at"]} - {to_row["end_at"]}')
