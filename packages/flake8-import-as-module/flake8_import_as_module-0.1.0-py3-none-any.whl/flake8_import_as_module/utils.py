def generate_code(code_prefix: str, number: int) -> str:
    pad_number = str(number).zfill(3)

    return f"{code_prefix}{pad_number}"


def generate_description(package: str) -> str:
    description = (
        f"`from {package} import ...` is unconventional. "
        f"`{package}` should be imported as a module."
    )
    # print(description)

    return description


def generate_message(code_prefix: str, number: int, package: str) -> str:
    code = generate_code(code_prefix, number)
    description = generate_description(package)

    return f"{code} {description}"
