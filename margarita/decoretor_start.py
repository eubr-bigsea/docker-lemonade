

def print_hello(f):
    def print_here():
        print('hello world')

    return print_here


@print_hello
def decorator_test():
    print("decorator test")


f_lista = []


def adiciona_lista(f):
    print(f'adicionando função {f}')
    f_lista.append(f)
    return f


@adiciona_lista
def a():
    print("função: a")


def b():
    print("função: b")


@adiciona_lista
def c():
    print("função: c")


def main():
    print("começo main")
    print(f'f_lista: {f_lista}')
    a()
    b()
    c()


if __name__ == '__main__':
    main()

