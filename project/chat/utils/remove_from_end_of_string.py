def remove_from_end_of_string(input_string: str, substring_to_remove: str) -> str:
    if input_string.endswith(substring_to_remove):
        return input_string[: -len(substring_to_remove)]
    else:
        return input_string
