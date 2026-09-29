import psycopg
import logging

def get_data(opts={}):
    # return: {"from_data": [], "to_data": []}
    print("postgres - get_data...")

    # use client from opts
    pg_client:psycopg.Connection = opts["pg_client"]

    with pg_client.cursor() as cur:
        # guess this handles the timezone weirdness
        cur.execute("SET timezone TO 'Europe/Helsinki'")

        # fetch erp rows
        from_data = cur.execute("""
            SELECT 
                source_id,
                event_type_id,
                workcenter_id,
                start_at,
                end_at,
                workphase_id,
                work_number,
                work_id,
                article_id,
                user_id
            FROM fact_machine_events WHERE
                source_id = ANY(%s) AND
                event_type_id = ANY(%s) AND
                workcenter_id = ANY(%s) AND
                start_at >= %s AND
                end_at < %s
            ORDER BY start_at ASC
        """,(
                opts["from_source_ids"], # namely the ERP source_id
                opts["from_event_type_ids"], # namely the stamping events
                opts["workcenter_ids"],
                opts["start_at"],
                opts["end_at"]
            )
        ).fetchall()

        # fetch machine events that are missing erp info (work_number)
        to_data = cur.execute("""
            SELECT
                machine_event_id,
                source_id,
                event_type_id,
                workcenter_id,
                start_at,
                end_at,
                workphase_id,
                work_number,
                work_id,
                article_id,
                user_id
            FROM fact_machine_events WHERE
                work_number IS NULL AND
                source_id = ANY(%s) AND
                start_at >= %s AND
                end_at < %s AND
                NOT (event_type_id = ANY(%s))
            ORDER BY start_at ASC
        """,(
            opts["to_source_ids"], # namely the sensors and machine APIs
            opts["start_at"],
            opts["end_at"],
            opts["excluded_to_event_types"] # namely the daily summaries
        )).fetchall()

        print(f"postgres - get_data: {len(to_data)} rows to update from {len(from_data)} rows")

        # return erp rows and machine event rows
        return {"from_data": from_data, "to_data": to_data}


def update_data(opts={}, newdata=None, dry_run=False):
    # accept: [{}]
    # return: true|false
    print("postgres - update_data")

    if newdata == None or len(newdata) <= 0:
        print("postgres - update_data: no newdata")
        return False
    
    # use client from opts 
    pg_client:psycopg.Connection = opts["pg_client"]

    print(f'postgres - update_data: update {len(newdata)} rows...')

    if dry_run is not True:
        with pg_client.cursor() as cur:
            # guess this is not needed here but hey
            cur.execute("SET timezone TO 'Europe/Helsinki'")
        
            # bulk update
            cur.executemany("""
                UPDATE fact_machine_events SET
                    workphase_id = %(workphase_id)s,
                    work_number = %(work_number)s,
                    work_id = %(work_id)s,
                    article_id = %(article_id)s,
                    user_id = %(user_id)s
                WHERE
                    machine_event_id = %(machine_event_id)s
            """, newdata)
            print(f"postgres - update_data: db says that {cur.rowcount} rows were updated, sound about right?")

    else:
        print(f"postgres - update_data: pretending to update {len(newdata)} rows...")
        # print first row to see if update would make sense
        print(newdata[0])

    return True
