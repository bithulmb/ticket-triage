import runpy

runpy.run_path("main.py", run_name="__main__")
print(open("results.json").read())
print("--- run.log ---")
print(open("run.log").read())