""" Program to remove empty folders on a directory """
import os


def remove_empty_folders():
    dir_path = input('\nEnter the directory path in which you want to delete empty folders: ')

    folders_removed = 0
    folders_to_remove = []
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for dir in dirs:
            full_path = os.path.join(root, dir)
            if not os.listdir(full_path):
                folders_to_remove.append(full_path)
                folders_removed += 1

    for file in folders_to_remove:
        os.removedirs(file)
        print('{file}'.format(file=file))

    print('\n{files_removed} files removed'.format(files_removed=folders_removed))
    if (folders_removed == 0):
        print('There were no empty folders')
    