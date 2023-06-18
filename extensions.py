def rows_to_dict(rows, obj):
    if rows:
        objects_list = [obj(*row) for row in rows]
        objects_dicts = [obj.to_dict() for obj in objects_list]
        return objects_dicts
    else:
        return None