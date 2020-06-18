from __future__ import print_function
import shutil
import os
import delete_old_files


EXTERNAL_HARD_DRIVE_NAME = "Tyler's External HD"


def main():
    source = "%s/Documents/Takeout/" % os.environ['HOME']
    dest = "/Volumes/%s/Takeout/" % EXTERNAL_HARD_DRIVE_NAME

    file_count = len([name for name in os.listdir(source)
                      if os.path.isfile(os.path.join(source, name))])

    if file_count > 0 and not os.path.exists(dest):
        os.system(
            """osascript -e 'display notification "Hook up your external drive to sync" with title "New backup ready"'""")
    elif file_count > 0 and os.path.exists(dest):
        files = os.listdir(source)

        for f in files:
            shutil.move(source + f, dest + f)

        os.system(
            """osascript -e 'display notification "You are good to go" with title "External Drive Synced"'""")

        delete_old_files.delete(dest + "*")


if __name__ == '__main__':
    try:
        main()
    except:
        os.system(
            """osascript -e 'display notification "Check it out" with title "Oh no! External Drive Sync Failed"'""")
