from invoke import run, task


@task
def build(context, folder_mode=False):
    run(
        f'pyinstaller \
--name=exp \
--noconfirm {"--onefile" if not folder_mode else ""} \
--icon NONE \
"./exp.py"'
    )
