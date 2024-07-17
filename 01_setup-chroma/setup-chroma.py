import subprocess

print(subprocess.run(["sh 01_setup-chroma/setup-chroma.sh"], shell=True))