import ast
from typing import List, Tuple

from .constants import CODE_PREFIX, PACKAGES
from .utils import generate_message


# Based on:
# - https://github.com/asottile/flake8-2020/blob/v1.7.0/flake8_2020.py#L36
# - https://github.com/marcgibbons/flake8-datetime-import/blob/0.1.0/src/flake8_datetime_import.py#L34  # noqa: E501
# - https://flake8.pycqa.org/en/5.0.0/internal/utils.html
class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # print(ast.dump(node, include_attributes=True))
        # and run: `flake8 flake8_import_as_module/`

        # from flake8 import utils
        # print(utils)

        # Examples:

        # ImportFrom(
        #     module="typing",
        #     names=[alias(name="List", asname=None), alias(name="Tuple", asname=None)],
        #     level=0,
        #     lineno=2,
        #     col_offset=0,
        # )

        # ImportFrom(
        #     module="flake8",
        #     names=[alias(name="utils", asname=None)],
        #     level=0,
        #     lineno=4,
        #     col_offset=0,
        # )

        if node.module in PACKAGES:
            code_number = PACKAGES.index(node.module) + 1
            msg = generate_message(CODE_PREFIX, code_number, node.module)
            self.errors.append((node.lineno, node.col_offset, msg))

        self.generic_visit(node)
