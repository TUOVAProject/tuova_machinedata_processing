import psycopg
import logging

def get_data(opts={}):
    # return {"from_data": [], "to_data": []}
    print("postgres - get_data...")

    pg_client:psycopg.Connection = opts["pg_client"]

    # fetch all [from] events as per config
    with pg_client.cursor() as cur:
        cur.execute("SET timezone TO 'Europe/Helsinki'")
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

        # fetch all [to] events that are missing specific info as per config
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
        return {"from_data": from_data, "to_data": to_data}


def update_data(opts={}, new_data=None):
    print("postgres - update_data: TODO")
