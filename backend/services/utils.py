import time


def tempo_execucao(func):
    def wraper():
        inicio = time.time()
        func()
        fim = time.time()
        print(f"Tempo: {fim - inicio:.2f} segundos")

    return wraper


def fundir_csv(path1: str, path2: str):
    pass
