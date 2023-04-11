from PIL import Image
import threading

c = complex(-0.5, 0.25)
it = 10
W = 600
H = 600
MAXREAL = 2
MINREAL = -2
MAXIMAG = 2
MINIMAG = -2
AJUSTE = 0.005
NUM_THREADS = 4 # Defina o número de threads que deseja utilizar

img = Image.new('RGB', (W, H+1), color = 'black')
lock = threading.Lock() # Cria um lock para garantir acesso exclusivo à imagem

def process_part(start_x, end_x, start_y, end_y):
    global img
    for a in range(start_x, end_x):
        for b in range(start_y, end_y):
            z = complex(a * AJUSTE + MINREAL, b * AJUSTE + MINIMAG)
            i = 0
            while i < it:
                z = z*z + c
                if abs(z) > 2:
                    break
                i += 1
            if i < it:
                with lock:
                    # Mapeamento das coordenadas complexas para as coordenadas da imagem
                    x = int(W*(a-MINREAL)/(MAXREAL - MINREAL))
                    y = int(H*(b-MINIMAG)/(MAXIMAG - MINIMAG))
                    y = H-y
                    img.putpixel((x,y), (255,0,0))

# Lista de threads
threads = []

# Cada thread processa uma parte da imagem
for i in range(NUM_THREADS):
    start_x = int(i * W / NUM_THREADS)
    end_x = int((i+1) * W / NUM_THREADS)
    t = threading.Thread(target=process_part, args=(start_x, end_x, 0, H))
    threads.append(t)

# Inicia as threads
for t in threads:
    t.start()

# Aguarda o término de todas as threads
for t in threads:
    t.join()

img.save('res.png')
