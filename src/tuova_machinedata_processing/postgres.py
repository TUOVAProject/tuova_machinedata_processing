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
                user_id,
                program_name,
                erp_id
            FROM fact_machine_events WHERE
                source_id = ANY(%s) AND
                event_type_id = ANY(%s) AND
                workcenter_id = ANY(%s) AND
                start_at >= %s AND
                end_at < %s
            ORDER BY start_at ASC
        """,(
                opts["from_source_ids"],
                opts["from_event_type_ids"],
                opts["workcenter_ids"],
                opts["start_at"],
                opts["end_at"]
            )
        ).fetchall()

        # fetch machine events that are missing erp info
        to_data = cur.execute("""
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
                user_id,
                program_name,
                erp_id
            FROM fact_machine_events WHERE
                work_number IS NULL AND
                source_id = ANY(%s) AND
                start_at >= %s AND
                end_at < %s
            ORDER BY start_at ASC
        """,(
            opts["to_source_ids"],
            opts["start_at"],
            opts["end_at"]
        )).fetchall()

        print(f"postgres - get_data: {len(to_data)} rows to update from {len(from_data)} rows")

        # return erp rows and machine event rows
        return {"from_data": from_data, "to_data": to_data}


def update_data(opts={}, newdata=None):
    # accept: [{}]
    # return: true|false
    print("postgres - update_data")

    # 
