import pathlib as p
import unittest


class TestSuiteConfig:
    """
    This class represents a correct config object shape.
    """

    def __init__(self, lilypond, mei_mensural, early):
        self.lilypond = lilypond
        self.mei_mensural = mei_mensural
        self.early = early


class Test:
    """
    This class handles comparison between expected
    and actual test report.
    """

    def __init__(
        self,
        name,
        expected: p.Path | str,
        actual: p.Path | str,
        format,
        unittest_ignore: bool,
    ):
        self.name = name
        self.expected: p.Path | str = expected
        self.actual: p.Path | str = actual
        self.format: list[str] | None = format
        self.unittest_ignore = unittest_ignore

    def resolve(self, value: str | p.Path) -> str:
        return value.read_text() if type(value) is p.Path else value

    def result(self):
        passed = self.resolve(self.expected) == self.resolve(self.actual)
        return f"{'✅' if passed else '⭕'} {self.name}"

    def comparison(self) -> tuple:
        expected_without_trailing_newline = self.resolve(self.expected)[:-1]
        actual = self.resolve(self.actual)
        return expected_without_trailing_newline, actual

    def wrap(self, value: str):
        """
        Wraps the value within tags
        provided in self.format.
        """
        if not self.format:
            return str(value)
        result = (
            "".join([f"<{f}>" for f in self.format])
            + str(value)
            + "".join([f"</{f}>" for f in reversed(self.format)])
        )
        return result

    def row(self) -> str:
        return (
            " <tr>\n"
            + f"  <td>{self.result()}</td>\n"
            + f"  <td>{self.wrap(self.expected)}</td>\n"
            + f"  <td>{self.wrap(self.actual)}</td>\n"
            + " </tr>"
        )


class TestCase:
    """
    This class handles formating test report output
    as a markdown table with links to generated images.
    """

    def __init__(self, suite_name: str, test_name: str):
        self.suite_name = suite_name
        self.test_name = test_name
        self.tests: list[Test] = []

    def add(
        self,
        name,
        expected,
        actual,
        format: list[str] | None = None,
        unittest_ignore=False,
    ) -> None:
        test = Test(name, expected, actual, format, unittest_ignore)
        self.tests.append(test)

    def table(self) -> str:
        return (
            "<table>\n"
            + " <tr>\n  <td/>\n  <td>expected</td>\n  <td>actual</td>\n </tr>\n"
            + "\n".join([f" <tr>\n{test.row()}\n </tr>" for test in self.tests])
            # + f"<tr>\n{'\n'.join(['\n'.join([f'<td>{d}</td>\n' for d in test]) for test in self.tests])}\n</tr>"
            + "</table>\n"
        )

    def run(self) -> None:
        tests = {
            f"test_{test.name}": lambda this, test=test: this.assertMultiLineEqual(
                *test.comparison()
            )
            for test in self.tests
            if not test.unittest_ignore
        } | {"maxDiff": None}
        suite = unittest.TestLoader().loadTestsFromTestCase(
            type(self.test_name, (unittest.TestCase,), tests)
        )
        unittest.TextTestRunner(verbosity=2).run(suite)
