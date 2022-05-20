def my_sum(*args):
    running_sum = 0
    for arg in args:
        running_sum += arg
    return running_sum

if __name__ == "__main__":
    print('HEllo!')