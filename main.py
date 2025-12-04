import pathlib as p
import subprocess

PREV = ""

if __name__ == "__main__":
    if not p.Path("./tests/main.py").is_file():
        print("NOTE: run this script from the top directory of your Early project.")
        exit()

    while True:
        print("\n🌺 Welcome to Early Testing Suite.\n")
        print("* type 'add' followed by suite-name and test name (or many test names);")
        print(
            "* type 'test' (and optional suite and tests names) to generate a report of your test outcome."
        )
        print("* type 'quit' to exit.\n")
        inp = input("mode: ") or PREV
        PREV = inp

        if inp.startswith("add "):
            cmd = ["python3", "./tests/src/add.py"] + inp.split(" ")[1:]
            o = subprocess.run(cmd, capture_output=True)

            if o.returncode == 0:
                print("Created test suite.")

            elif o.returncode == 1:
                err = o.stderr.decode("utf-8")
                if "ValueError" in err:
                    msg = err.split("ValueError: ")[1]
                    print(msg)
                else:
                    print(err)

            else:
                raise Exception(o)

            continue

        elif inp.startswith("test"):
            subprocess.run(["clear"])
            print("...running early tests.")
            args = inp.split(" ")
            suite_name = None
            tests = []

            if len(args) == 2:
                print("Please provide at least one test name.")
                continue
            if len(args) > 2:
                suite_name = args[1]
                tests = args[2:]

            o = subprocess.run(
                ["python3", "./tests/src/report.py", suite_name or ""] + tests,
                capture_output=True,
            )
            print(o.stdout.decode("utf-8"))
            print(o.stderr.decode("utf-8"))

            if o.returncode == 0:
                print(
                    "Successfully generated report. To exit press 'control+c' (unix only).\n"
                )
                continue
            else:
                print("* * * * * * Cannot create report. * * * * * *")
                print(o.stderr.decode("utf-8"))
                continue

        elif inp == "quit":
            break

        else:
            print("Invalid input, try again\n")
            continue
