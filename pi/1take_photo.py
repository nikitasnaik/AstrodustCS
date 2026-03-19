def take_photo():
    """
    Automatically takes a photo every 5 seconds and saves
    it to the SAME location as defined by REPO_PATH + FOLDER_PATH
    """

    print("Starting automatic capture every 5 seconds...")

    picam2.start()  # start camera once

    while True:
        name = "TeamAstrodust"
        img_path = img_gen(name)

        picam2.capture_file(img_path)
        print(f"Photo saved: {img_path}")

        # OPTIONAL: push to GitHub
        # git_push()

        time.sleep(5)