from PIL import Image 
import concurrent.futures
import time

c = complex(-0.5, 0.25)
it = 10
nthreads=1024
W = 600
H = 600
MAXREAL = 2
MINREAL = -2
MAXIMAG = 2
MINIMAG = -2
AJUSTE = 0.001


def process_vertical_strip(x_range, thread_id):
    start_time = time.time()
    for x in x_range:
        for y in range(H):
            a = x_range.start / W * (MAXREAL - MINREAL) + MINREAL
            b = y / H * (MAXIMAG - MINIMAG) + MINIMAG
            z = complex(a,b)
            i = 0
            while i < it:
                z = z*z + c
                if(abs(z)>2):
                    break
                i+=1

            if(i < it): #pinta se estoura
                #faz a mudança de escala (mapeamento) do plano complexo para as coordenadas da imagem
                x_img = x
                y_img = H - y - 1 # inverte o eixo y
                img.putpixel((x_img, y_img), (255,0,0))
    end_time = time.time()
    thread_time = end_time - start_time
    print(f"Thread {thread_id} finalizada em {thread_time:.3f} segundos")

img = Image.new('RGB', (W, H), color = 'black')
def call():
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
        # divide a imagem em 16 faixas verticais e processa cada uma em uma thread
        x_ranges = [
            range(int(W/nthreads*i), int(W/nthreads*(i+1)))
            for i in range(nthreads)
        ]
        futures = []
        for i, x_range in enumerate(x_ranges):
            futures.append(executor.submit(process_vertical_strip, x_range, i))
    
        # espera todas as threads terminarem
        for future in futures:
            future.result()
    img.save('res.png')
    total_time = time.time() - start_time
    print(f"Tempo total: {total_time:.3f} segundos")

if __name__ == "__main__":
    call()