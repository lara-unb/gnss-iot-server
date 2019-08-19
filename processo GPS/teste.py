def read(filename):
    with open(filename) as file_object:
        for line in file_object:
            print(line)

read('logfile.txt')