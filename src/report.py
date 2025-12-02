import json
import pathlib as p
import subprocess
import sys

from utils import TestCase, TestSuiteConfig

ARGS = sys.argv
SUITE = None
TESTS = []
if len(ARGS) >= 2:
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

        for k, v in config.__dict__.items():
            md += f"* {k}: {v}\n"
            md += "\n"

        for test_dir in suite_dir.iterdir():
            if not test_dir.is_dir():
                continue
            subprocess.run(["rm", "-r", str(test_dir / "output")])
            output_dir = (test_dir / "output").mkdir(parents=True, exist_ok=True)
            test_name = test_dir.stem
            if test_name not in TESTS:
                continue
            title = f"\n## {' '.join(test_name.capitalize().split('-'))}\n"
            print(f"Testing {test_name} in {suite_name}")

            scm_expected = (test_dir / "expect.scm").read_text() or "_no scheme_"
            mei_expected = (test_dir / "expect.mei").read_text() or "_no mei_"

            output_ly_dir = test_dir / "output" / "ly"
            output_early_dir = test_dir / "output" / "early"
            # output_mei_dir = test_dir / "output" / "mei"

            lilypond = f'\\version "{config.lilypond}"\n'
            # lilypond += macra
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

            ly_img_path = f"{p.Path(*output_ly_dir.parts[1:])}.{FORMAT}"
            ly_img = f'<img src="{ly_img_path}" width="100">'

            early = f'\\version "{config.lilypond}"'
            early = f'\\include "releases/early-{config.early}.ly"'
            # early += macra
            early += LY_PAPER
            early += (test_dir / "early.ly").read_text()
            early += r"\bookpart { \actual }" + "\n"
            early += '#(display "SCHEME")\n'
            early += r"\void \displayMusic \actual" + "\n"
            early += '#(display "MEI")\n'
            early += r"%(# ly->mei test)"  # uncheck when ready.

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

            early_img_path = f"{p.Path(*output_early_dir.parts[1:])}.{FORMAT}"
            early_img = f'<img src="{early_img_path}" width="100">'

            test = TestCase()
            test.add("lilypond", ly_img, early_img)
            test.add(
                "scheme",
                scm_expected,
                scm_actual,
                format=["code", "pre"],
            )
            # test.add("verovio", img, img) # UNCOMMENT when ready.
            test.add("mei", mei_expected, mei_actual)

            md += title
            md += test.table()
            md += "\n"

    (DIR / "../report.md").write_text(md)
