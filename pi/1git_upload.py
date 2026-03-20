import os

def git_push():
    os.system("git add .")
    os.system('git commit -m "Auto image upload"')
    os.system("git push")