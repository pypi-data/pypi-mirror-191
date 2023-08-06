class HelloWorld:
    def __init__(self, val=0):
        self.val = val

    def show_hello_world(self):
        print("Hello World " + str(self.val))

def user_exposed_function(val=0):
    my_hello_world = HelloWorld(val)
    my_hello_world.show_hello_world()