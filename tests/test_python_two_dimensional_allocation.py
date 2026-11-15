import unittest

from atcodertools.codegen.code_generators.universal_code_generator import (
    UniversalCodeGenerator,
    get_builtin_code_generator_info_toml_path,
)
from atcodertools.codegen.code_style_config import CodeStyleConfig
from atcodertools.common.language import PYTHON
from atcodertools.fmtprediction.models.format import Format
from atcodertools.fmtprediction.models.index import Index
from atcodertools.fmtprediction.models.type import Type
from atcodertools.fmtprediction.models.variable import Variable


def make_index(maximum):
    index = Index()
    index.update("1")
    index.update(maximum)
    return index


class TestPythonTwoDimensionalAllocation(unittest.TestCase):
    """The Python templates for allocating a 2D array without reading it at
    the same time produce runnable code that builds an H x W grid."""

    def setUp(self):
        self.generator = UniversalCodeGenerator(
            Format(),
            CodeStyleConfig(lang=PYTHON.name),
            get_builtin_code_generator_info_toml_path(PYTHON.name),
        )
        self.var = Variable(
            "A", make_index("H"), make_index("W"), Type.int)

    def assert_allocates_h_by_w_grid(self, code):
        namespace = {"H": 2, "W": 3}
        exec(code, namespace)
        self.assertEqual([[0] * 3 for _ in range(2)], namespace["A"])

    def test_declare_and_allocate_2d_seq(self):
        code = self.generator._generate_declaration_and_allocation(self.var)

        self.assert_allocates_h_by_w_grid(code)
        self.assertIn("# type: list[list[int]]", code)

    def test_allocate_2d_seq(self):
        code = self.generator._generate_allocation(self.var)

        self.assert_allocates_h_by_w_grid(code)


if __name__ == "__main__":
    unittest.main()
