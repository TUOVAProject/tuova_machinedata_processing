
def transform(opts={}, data=None):
    # accept: {"from_data": [{}], "to_data": [{}]}
    # return: [{}]
    print("data_processor - transform...")

    if len(data["from_data"]) <= 0 or len(data["to_data"]) <= 0:
        print("data_processor - transform: no data")
        return None

    updated_rows = []

    # loop erp rows
    for from_row in data["from_data"]:
        fs = from_row["start_at"]
        fe = from_row["end_at"]

        # loop machine event rows
        for to_row in data["to_data"]:
            s = to_row["start_at"]
            e = to_row["end_at"]

            # check if the whole event is supposed to be withing stamping, or start only
            check = False
            if opts["check_start_only"] == True:
                check = s >= fs and s < fe
            else:
                check = s >= fs and e < fe

            if check:
                # pick fields from erp row
                newdata = {
                    "workphase_id": from_row["workphase_id"],
                    "work_number": from_row["work_number"],
                    "work_id": from_row["work_id"],
                    "article_id": from_row["article_id"],
                    "user_id": from_row["user_id"],
                    "machine_event_id": to_row["machine_event_id"], # machine event id for update WHERE
                }
                updated_rows.append(to_row | newdata)

    # return updated machine data rows
    return updated_rows
