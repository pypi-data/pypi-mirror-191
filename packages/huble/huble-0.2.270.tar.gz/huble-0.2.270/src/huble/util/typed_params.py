def get_typed_params(params: dict) -> dict:

    for param in params:
        if params[param] == "True":
            params[param] = True
            continue
        elif params[param] == "False":
            params[param] = False
            continue
        elif params[param] == "None":
            params[param] = None
            continue
        elif type(params[param]) == list:
            for i in params[param]:
                i = str(i)
                continue
        elif type(params[param]) == tuple:
            for i in params[param]:
                i = float(i)
            continue
        if (
            type(params[param]) is not list
            and type(params[param]) is not tuple
            and type(params[param]) is not dict
            and type(params[param]) is not bool
            and params[param] is not None
        ):
            try:
                params[param] = int(params[param])
            except:
                try:
                    params[param] = float(params[param])
                except:
                    try:
                        params[param] = str(params[param])
                    except:
                        print("Error generating type for parameter: ", param)

    return params
