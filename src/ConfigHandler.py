#This will be generalized later.
def getPath():
    config_file = open('Config.txt')
    relative_path = config_file.readline().strip()
    config_file.close()
    return relative_path