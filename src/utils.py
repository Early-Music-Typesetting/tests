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

    def __init__(self, name, expected, actual, format):
        self.name = name
        self.expected = expected
        self.actual = actual
        self.format: list[str] | None = format

    def result(self):
        passed = self.expected == self.actual
        return f"{'✅' if passed else '⭕'} {self.name}"

    def wrap(self, value: str):
        if not self.format:
            return value
        result = (
            "".join([f"<{f}>" for f in self.format])
            + value
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

    def __init__(self):
        self.tests: list[Test] = []

    def add(self, name, expected, actual, format: list[str] | None = None) -> None:
        test = Test(name, expected, actual, format)
        self.tests.append(test)

    def table(self) -> str:
        return (
            "<table>\n"
            + " <tr>\n  <td/>\n  <td>expected</td>\n  <td>actual</td>\n </tr>\n"
            + "\n".join([f" <tr>\n{test.row()}\n </tr>" for test in self.tests])
            # + f"<tr>\n{'\n'.join(['\n'.join([f'<td>{d}</td>\n' for d in test]) for test in self.tests])}\n</tr>"
            + "</table>\n"
        )
