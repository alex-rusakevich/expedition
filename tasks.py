import os
from io import StringIO

from invoke import run, task


@task
def build(context, folder_mode=False):
    run(
        f'pyinstaller \
--name=exp \
--noconfirm {"--onefile" if not folder_mode else ""} \
--icon NONE \
--add-data "./expedition/VERSION.txt;expedition/" \
--collect-data grapheme \
"./exp.py"'
    )


@task
def update_version_txt(context):
    EXP_VERSION = (
        open(os.path.join("expedition", "VERSION.txt"), "r", encoding="utf8")
        .read()
        .strip()
    )

    latest_commit_msg = StringIO()
    run("git log -1 --pretty=%B", out_stream=latest_commit_msg)
    latest_commit_msg = latest_commit_msg.getvalue().strip()

    major, minor, patch = (int(i) for i in EXP_VERSION.split("."))

    if "#patch" in latest_commit_msg:
        patch += 1
    elif "#minor" in latest_commit_msg:
        patch = 0
        minor += 1
    elif "#major" in latest_commit_msg:
        patch, minor = 0, 0
        major += 1

    NEW_VER = ".".join([str(i) for i in (major, minor, patch)])

    if NEW_VER == EXP_VERSION:
        print("No new version marker, skipping")
    else:
        open(os.path.join("expedition", "VERSION.txt"), "w", encoding="utf8").write(
            NEW_VER
        )
        print(f"New version is {NEW_VER}")
        run(f'git add -A . && git commit -m "#bump to {NEW_VER}"')


@task(pre=(update_version_txt,))
def tag(context):
    """Auto add tag to git commit depending on version"""

    EXP_VERSION = (
        open(os.path.join("expedition", "VERSION.txt"), "r", encoding="utf8")
        .read()
        .strip()
    )

    latest_tag = StringIO()

    run("git describe --abbrev=0 --tags", out_stream=latest_tag, warn=True)
    latest_tag = latest_tag.getvalue().strip()

    if f"v{EXP_VERSION}" != latest_tag:
        run(f"git tag v{EXP_VERSION}")
        run(f"git push --tags")
    else:
        print("No new version, skipping")
