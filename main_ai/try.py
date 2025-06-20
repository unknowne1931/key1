

def one(i):
    print("one")
    def two(i):
        print("two")
        return True


def three(i):
    dat = one(i)
    if dat is True:
        print("True")
    else:
        print("False")

if __name__ == "__main__":
    three(1)