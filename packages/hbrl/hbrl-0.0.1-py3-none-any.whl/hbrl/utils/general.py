

def get_dict_as_str(input_dict, start_tab="", tab="    "):
    result = ""
    for k, v in input_dict.items():
        if result != "":
            result += ",\n"
        if isinstance(v, dict):
            result += get_dict_as_str(v, start_tab + tab)
        if isinstance(v, list):
            result += start_tab + tab + str(k) + ": [" + "\n"
            for index, elt in enumerate(v):
                if isinstance(elt, dict):
                    result += get_dict_as_str(elt, start_tab + tab + tab)
                else:
                    result += start_tab + tab + tab + str(elt)
                result += "\n" if index == len(v) - 1 else ",\n"
            result += start_tab + tab + "]"
        else:
            if isinstance(v, str):
                result += start_tab + tab + str(k) + ": \"" + v + "\""
            else:
                result += start_tab + tab + str(k) + ": " + str(v) + ""
    return start_tab + "{\n" + result + "\n" + start_tab + "}"