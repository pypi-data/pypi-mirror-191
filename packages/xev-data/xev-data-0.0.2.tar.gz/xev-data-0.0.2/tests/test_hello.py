#!usr/bin/env python3

######## Functions ########
def print_hello_world():
    print("Hello World!")

def touch_hello():
    import os
    os.system("touch HelloWorld.txt")

######## Main ########

def main():
    print_hello_world()
    touch_hello()
    return

######## Execution ########
if __name__ == "__main__":
    main()
