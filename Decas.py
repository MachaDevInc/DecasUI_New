import subprocess

try:
    subprocess.run(["sudo", "/usr/bin/python3", "/home/decas/ui/DecasUI_New/Splash.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")