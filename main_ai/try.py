i = int(input("Number : "))

def is_one(n):

    def is_one_sub(n):
        # Now n is accessed and used in the function
        print("is_one_sub called with n =", n)

    if n == 1:
        return True
    elif n < 1:
        is_one_sub(n)

dat = is_one(i)

print(dat)