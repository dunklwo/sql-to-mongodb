import re

def parse_sql(query):
    query = query.strip().lower()

    select_match = re.search(r"select (.+?) from", query)
    select_fields = select_match.group(1).split(",") if select_match else ["*"]
    select_fields = [f.strip() for f in select_fields]

    from_match = re.search(r"from (\w+)", query)
    table = from_match.group(1) if from_match else ""

    where_match = re.search(r"where (.+)", query)
    where_clause = where_match.group(1) if where_match else None

    order_match = re.search(r"order by (\w+)", query)
    order_field = order_match.group(1) if order_match else None

    return {
        "select": select_fields,
        "from": table,
        "where": where_clause,
        "order_by": order_field
    }