def generate_exception_fields_must_be_provided(fields: list[str]) -> dict[str, str]:
    return {"error": f"{'_or_'.join(fields)}_must_be_provided"}


def generate_exception_fields_cant_be_provided_at_once(
    fields: list[str],
) -> dict[str, str]:
    return {"error": f"{'_and_'.join(fields)}_cant_be_provided_at_once"}
