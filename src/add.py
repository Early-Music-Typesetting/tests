import pathlib as p
import sys
from warnings import warn

DIR = p.Path("./tests/suites")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError(
            "Provide two or more arguments:\n1) testing suite name\n2) test name (or names)."
        )

    suite = sys.argv[1]

    suite_dir = DIR / suite

    if not suite_dir.is_dir():
        suite_dir.mkdir(parents=True, exist_ok=True)
        config = (DIR.parent / "src/config.json").read_text()
        print("KURWAAAA", config)
        (suite_dir / "config.json").write_text(config)

    tests = sys.argv[2:]

    for test in tests:
        test_dir = DIR / suite / test

        try:
            test_dir.mkdir(parents=True)
        except FileExistsError:
            warn(f'Test "{test}" in "{suite}" testing suite already exits.')

        """
        Create expect files.
        """
        (test_dir / "expect.ly").write_text("expected = \\relative g' { g a b }\n")
        (test_dir / "expect.scm").write_text("")
        (test_dir / "expect.mei").write_text("")

        """
        Create tested case of early snippet.
        """
        (test_dir / "early.ly").write_text("actual = \\early \\relative g' {}\n")
