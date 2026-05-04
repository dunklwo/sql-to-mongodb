def convert_where(where_clause):
    if not where_clause:
        return "{}"

    where_clause = where_clause.replace(";", "").lower()

    operator_map = {
        "=": "",
        ">": "$gt",
        "<": "$lt",
        ">=": "$gte",
        "<=": "$lte"
    }

    # Helper to process single condition
    def process_condition(cond):
        parts = cond.strip().split()

        field = parts[0]
        operator = parts[1]
        value = parts[2]

        # Convert value
        if value.isdigit():
            value = int(value)
        else:
            value = f'"{value}"'

        if operator == "=":
            return f'{{ "{field}": {value} }}'
        else:
            return f'{{ "{field}": {{ "{operator_map[operator]}": {value} }} }}'

    # Handle OR
    if " or " in where_clause:
        conditions = where_clause.split(" or ")
        mongo_conditions = [process_condition(c) for c in conditions]

        return '{ "$or": [' + ", ".join(mongo_conditions) + "] }"

    # Handle AND
    elif " and " in where_clause:
        conditions = where_clause.split(" and ")
        mongo_conditions = []

        for cond in conditions:
            processed = process_condition(cond)
            # remove outer {}
            processed = processed[1:-1]
            mongo_conditions.append(processed)

        return "{ " + ", ".join(mongo_conditions) + " }"

    # Single condition
    else:
        return process_condition(where_clause)


def convert_to_mongo(parsed):
    collection = parsed["from"]

    # Projection
    if parsed["select"] == ["*"]:
        projection = "{}"
    else:
        proj = {field: 1 for field in parsed["select"]}
        projection = str(proj).replace("'", '"')

    where_clause = convert_where(parsed["where"])

    query = f'db.{collection}.find({where_clause}, {projection})'

    if parsed["order_by"]:
        query += f'.sort({{ "{parsed["order_by"]}": 1 }})'

    return query