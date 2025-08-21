import subprocess


def adb_action(action: list):
    """Executes a single ADB command on the connected device."""
    cmd = ["adb", "shell", *action]
    subprocess.run(cmd, capture_output=True, check=True)