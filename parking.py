import argparse
import functools

from cmd2 import with_argparser, Cmd

from sc_handler import SCHandler


def set_args(*key_args, description=""):
    argparser = argparse.ArgumentParser(description=description)
    for key_arg in key_args:
        argparser.add_argument(f'--{key_arg}', dest=key_arg, required=True)

    def decorator_repeat(func):
        @functools.wraps(func)
        @with_argparser(argparser)
        def wrapper_repeat(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper_repeat

    return decorator_repeat


class VoyageFinanceHW(Cmd):
    prompt = 'parking> '
    intro = "Welcome! Type ? to list commands"

    def __init__(self, *args, **kwargs):
        self.sc_handler = SCHandler()
        super().__init__(*args, **kwargs)

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        super().do_help(inp)

    do_EOF = do_exit
    help_EOF = help_exit

    @set_args("url", "key", description="create NFT car")
    def do_create(self, args):
        key = args.key
        url = args.url
        self.sc_handler.create_car(url=url, key=key)

    @set_args("key")
    def do_status(self, args):
        key = args.key
        print(self.sc_handler.status(key=key))

    @set_args("car_id", "key")
    def do_deposit(self, args):
        key = args.key
        car_id = int(args.car_id)
        self.sc_handler.deposit(car_id=car_id, key=key)

    @set_args("car_id", "key")
    def do_retrieve(self, args):
        key = args.key
        car_id = int(args.car_id)
        self.sc_handler.retrieve(car_id=car_id, key=key)

    def do_free_lots(self, args):
        print(f"Available lots: {self.sc_handler.free_lots()}")

    @set_args("key")
    def do_retrieve_all(self, args):
        key = args.key
        for car_id in self.sc_handler.parked_car_ids(key=key):
            self.sc_handler.retrieve(car_id=car_id, key=key)


if __name__ == '__main__':
    VoyageFinanceHW().cmdloop()
