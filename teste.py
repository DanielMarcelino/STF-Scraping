class Teste:
    def __init__(self) -> None:
        print('init')

    def __call__(cls, *args, **kwds) -> None:
        print('call')


a = Teste()
a()