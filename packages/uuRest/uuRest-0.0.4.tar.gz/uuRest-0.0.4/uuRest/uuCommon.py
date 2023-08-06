

def dict_to_str(value: dict) -> str:
    return ""


def get_raw_str_payload(value) -> str:
    if type(value) == str:
        return str
    if type(value) == dict:
        return dict_to_str(value)


def linearize_dictionary(dictionary: dict, parent_path: str = "") -> dict:
    """
    From dict structure of {"level1": {"level2": {"variable1": "value1", "variable2": "value2"}}} creates dictionary
    {"level1.level2.variable1": "value1", "level1.level2.variable2": "value2"}
    :param dictionary:
    :param parent_path:
    :return:
    """
    result = {}
    for key, value in dictionary.items():
        if type(value) == str or type(value) == int:
            result.update({f'{parent_path}{key}': value})
        else:
            sub_dictionary = linearize_dictionary(value, f'{parent_path}{key}.')
            for skey, svalue in sub_dictionary.items():
                result.update({skey: svalue})
    return result


def substitute_variables(value: str, variables_dict: dict, var_begin: str = "${", var_end: str = "}") -> str:
    """
    Substitutes variables in string from dictionary
    For example 'This ${value1} is ${value2}' where variables_dict is {'value1': 'code', 'value2': 'quite long'}
    :param value:
    :param variables_dict:
    :param var_begin:
    :param var_end:
    :return:
    """
    if type(value) != str:
        return value
    result = ""
    remaining = value
    len_begin = len(var_begin)
    len_end = len(var_end)
    pos_begin = value.find(var_begin)
    while pos_begin >= 0:
        result += remaining[:pos_begin]
        remaining = remaining[pos_begin + len_begin:]
        pos_end = remaining.find(var_end)
        if pos_end <= 0:
            raise Exception(f"Cannot find \"{var_end}\" in string: {remaining}")
        variable_name = remaining[:pos_end]
        if variable_name not in variables_dict.keys():
            raise Exception(f'Variable with name "{variable_name}" in string "{value}" cannot be substituted because it  is not in dictionary {variables_dict}')
        result += variables_dict[variable_name]
        remaining = remaining[pos_end + len_end:]
        pos_begin = remaining.find(var_begin)
    result += remaining
    return result