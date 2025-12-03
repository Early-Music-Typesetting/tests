import json
import pathlib as p
import subprocess
import sys

from utils import TestCase, TestSuiteConfig

ARGS = sys.argv
SUITE = None
TESTS = []
if len(ARGS) >= 2 and ARGS[1]:
    SUITE = ARGS[1]
if len(ARGS) > 2:
    TESTS = ARGS[2:]

DIR = p.Path("./tests/suites")
FORMAT = "svg"

LY_PAPER = r"""
\include "lilypond-book-preamble.ly"
% (set-default-paper-size '(cons (* 100 mm) (* 20 mm)))
#(ly:set-option 'warning-as-error #t)
\paper {
    page-breaking = #ly:one-line-breaking
    indent=0\mm
    line-width=120\mm
    oddFooterMarkup=##f
    oddHeaderMarkup=##f
    bookTitleMarkup = ##f
    scoreTitleMarkup = ##f
}
\header {
    tagline = ""
}
\layout {
    indent = 0
}
"""

if __name__ == "__main__":
    md = ""

    for suite_dir in DIR.iterdir():
        if not suite_dir.is_dir() or suite_dir.stem.startswith("__"):
            continue
        suite_name = suite_dir.stem
        if SUITE and SUITE != suite_name:
            continue
        md += f"\n# {suite_name.capitalize()}\n\n"
        config = TestSuiteConfig(**json.loads((suite_dir / "config.json").read_text()))
        macra = (suite_dir / "macra.ly").read_text()
        extractors = (DIR / "../src/extractors.ly").read_text()

        for k, v in config.__dict__.items():
            md += f"* {k}: {v}\n"
            md += "\n"

        for test_dir in suite_dir.iterdir():
            if not test_dir.is_dir():
                continue
            subprocess.run(["rm", "-r", str(test_dir / "output")])
            output_dir = test_dir / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            test_name = test_dir.stem
            if TESTS and test_name not in TESTS:
                continue
            title = f"\n## {' '.join(test_name.capitalize().split('-'))}\n"
            print(f"Testing {test_name} in {suite_name}")
            output = (
                (suite_dir / "output.ly").read_text()
                if (suite_dir / "output.ly").is_file()
                else ""
            )

            scm_expected = (test_dir / "expect.scm").read_text() or "_no scheme_"
            mei_expected = (test_dir / "expect.mei").read_text() or "_no mei_"

            output_ly_dir = test_dir / "output" / "ly"
            output_early_dir = test_dir / "output" / "early"
            # output_mei_dir = test_dir / "output" / "mei"

            lilypond = f'\\version "{config.lilypond}"\n'
            # lilypond += macra
            lilypond += extractors
            lilypond += output
            lilypond += LY_PAPER
            lilypond += (test_dir / "expect.ly").read_text()
            lilypond += r"\bookpart { \expected }"

            ly_cmd = [
                "lilypond",
                f"--{FORMAT}",
                "-o",
                output_ly_dir,
                "-",
            ]

            ly_out = subprocess.run(
                ly_cmd,
                input=lilypond.encode("utf-8"),
                capture_output=True,
            )

            if ly_out.returncode == 1:  # parsing not correct
                raise Exception(
                    f"Could not parse Lilypond:\n{ly_out.stderr.decode('utf-8')}"
                )
                ...  # handle.

            early = f'\\version "{config.lilypond}"'
            early = (
                f'\\include "releases/early-{config.early}.ly"'
                if config.early
                else r'\include "early/early.ly"'
            )
            early += (suite_dir / "macra.ly").read_text()
            early += extractors
            early += LY_PAPER
            early += (test_dir / "early.ly").read_text()
            early += output
            early += r"\bookpart { \actual }" + "\n"
            # early += '#(display "SCHEME")\n'
            # early += r"\void \displayMusic \actual" + "\n"
            early += '#(display "MEI")\n'
            early += r"%(# ly->mei actual)"  # uncheck when ready.

            early_cmd = [
                "lilypond",
                f"--{FORMAT}",
                "-o",
                output_early_dir,
                "-",
            ]

            early_out = subprocess.run(
                early_cmd,
                input=early.encode("utf-8"),
                capture_output=True,
            )

            if early_out.returncode == 1:  # parsing not correct
                raise Exception(
                    f"Could not parse Early Lilypond testing file:\n{early_out.stderr.decode('utf-8')}",
                )
                ...  # handle.

            scm_actual, mei_actual = early_out.stdout.decode("utf-8").split("\n\n")

            """Remove all non-scheme content"""
            scm_actual = "\n".join(
                [
                    line
                    for line in scm_actual.splitlines()
                    if line.startswith(("(", " "))
                ]
            )

            ly_img = ""
            early_img = ""
            for img_dir in output_dir.iterdir():
                if img_dir.suffix[1:] != FORMAT:
                    continue
                elif img_dir.stem.startswith("ly"):
                    ly_img_path = p.Path(*img_dir.parts[1:])
                    ly_img += f'<img src="{ly_img_path}" width="250">\n'
                elif img_dir.stem.startswith("early"):
                    early_img_path = p.Path(*img_dir.parts[1:])
                    early_img += f'<img src="{early_img_path}" width="250">\n'

            test = TestCase(suite_name, test_name)
            test.add("lilypond", ly_img, early_img, unittest_ignore=True)
            test.add(
                "scheme",
                scm_expected,
                scm_actual,
                format=["code", "pre"],
            )
            # test.add("verovio", img, img) # UNCOMMENT when ready.
            test.add("mei", mei_expected, mei_actual, format=["code", "pre"])

            md += title
            md += test.table()
            md += "\n"

            test.run()

    (DIR / "../report.md").write_text(md)
