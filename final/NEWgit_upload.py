import os

def git_push(crater_id):
    os.system("git add images logs")

    commit_message = f"Add images for {crater_id} (4-image batch)"
    os.system(f'git commit -m "{commit_message}" || echo "No changes to commit"')

    os.system("git push")

# def git_push(crater_id):
#     """
#     Pushes a batch of images for a crater to GitHub.
#     """
#     os.system("git add .")

#     commit_message = f"Add images for {crater_id} (All 4 images)"
    
#     os.system(f'git commit -m "{commit_message}" || echo "No changes to commit"')
#     os.system("git push")