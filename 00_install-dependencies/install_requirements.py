import subprocess

print(subprocess.run(["sh 00_install-dependencies/install_requirements.sh"], shell=True))