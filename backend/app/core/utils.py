def schema_or_dict_to_dict(obj_in):
    if isinstance(obj_in, dict):
        obj_in_data = {k.name: v for k, v in obj_in.items()}
    else:
        obj_in_data = obj_in.dict(exclude_unset=True)
    return obj_in_data
