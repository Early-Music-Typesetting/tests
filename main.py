import pathlib as p
import subprocess

if __name__ == "__main__":
    print("\n🌺 Welcome to Early Testing Suite.\n")

    if not p.Path("./tests/main.py").is_file():
        print("NOTE: run this script from the top directory of your Early project.")
        exit()

    while True:
        print("* type 'add' followed by suite-name and test name (or many test names);")
        print("* type 'test' to generate a report of your test outcome.\n")
        inp = input("mode: ")

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
            o = subprocess.run(
                ["python3", "./tests/src/report.py"], capture_output=True
            )
            if o.returncode == 0:
                print(
                    "Successfully generated report. To exit press 'control+c' (unix only).\n"
                )
                continue

        else:
            print("Invalid input, try again\n")
            continue

        break
