

def key_with_max_val(d: dict):
    """This function takes as input a dict and returns the key with the max value by
    a) creating a list of the dict's keys and values;
    b) returning the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def main():
    pass


if __name__ == '__main__':
    main()
