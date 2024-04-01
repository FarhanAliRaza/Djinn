import shutil


def remove_dotgithub_folder():
    shutil.rmtree(".github")


if __name__ == "__main__":
    if "{{ cookiecutter.use_github_actions }}".lower() == "y":
        remove_dotgithub_folder()
