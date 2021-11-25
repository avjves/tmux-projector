import subprocess

debug = False

def run_command(command):
    # print("Running cmd:", command)
    if debug:
        print(f"Running command {command}")
    result = subprocess.run(command, capture_output=True, shell=True)
    return result.stdout.decode()


def debug_print(output):
    # print(output)
    pass
