import os

def create_class_folders(class_name, path, weeks):
    try:
        class_dir_path = os.path.join(path, class_name)
        os.mkdir(class_dir_path)
        for i in range(1, weeks + 1):
            week_dir_path = os.path.join(class_dir_path, 'W{i}'.format(i=i)) 
            os.mkdir(week_dir_path)
            os.mkdir(os.path.join(week_dir_path, 'resources'))
            os.mkdir(os.path.join(week_dir_path, 'activities'))
    except OSError as error:
        print(error)


def create_classes():
    path = input('Enter the path in which you want to create the folders: ')
    amount = input('Enter the amount of classes you want to create: ')
    weeks = input('Enter the amount of weeks that you want to create for each class: ')

    for c in range(int(amount)):
        class_name = input('Write the class name: ').lower().rstrip().replace(' ', '_')
        create_class_folders(class_name, path, int(weeks))

