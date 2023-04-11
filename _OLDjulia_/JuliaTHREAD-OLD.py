import numpy as np
import matplotlib.pyplot as plt
import threading
def Start():
    # Definir parâmetros da varredura do plano complexo
    xmin, xmax, ymin, ymax = -2, 2, -2, 2
    N = 500  # número de pontos na varredura
    max_iter = 100  # número máximo de iterações

    # Criar matriz de zeros para armazenar os valores de magnitude
    magnitude = np.zeros((N, N), dtype=np.int32)

    # Função para calcular a magnitude de um número complexo
    def calc_magnitude(z):
       c = complex(-0.7, 0.27)  # constante para o Conjunto de Julia
       n = 0
       while abs(z) < 2 and n < max_iter:
           z = z**2 + c
           n += 1
       return n

    # Função para processar uma região do plano complexo
    def process_region(row_start, row_end):
        for i in range(row_start, row_end):
            for j in range(N):
                x = xmin + j * (xmax - xmin) / N
                y = ymin + i * (ymax - ymin) / N
                z = complex(x, y)
                magnitude[i, j] = calc_magnitude(z)

    #  Dividir o plano complexo em regiões e processá-las em paralelo
    n_threads = 4  # número de threads
    step = N // n_threads
    threads = []
    for i in range(n_threads):
        row_start = i * step
        row_end = (i + 1) * step
        t = threading.Thread(target=process_region, args=(row_start, row_end))
        t.start()
        threads.append(t)

    # Aguardar o término das threads
    for t in threads:
        t.join()

    # Criar imagem do fractal
    colors = [(0, 0, 0), (255, 255, 255)]  # cores para cada faixa de valores de magnitude
    cmap = plt.get_cmap("Spectral", colors)
    plt.imshow(magnitude, cmap=cmap, extent=[xmin, xmax, ymin, ymax])
    plt.axis('off')

    # Salvar imagem em um arquivo
    plt.savefig('julia_fractal.png', dpi=300)