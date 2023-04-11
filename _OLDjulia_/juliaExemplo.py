from PIL import Image #instalar com "pip install pillow"

c = complex(-0.5, 0.25)
it = 10
W = 600
H = 600
MAXREAL = 2
MINREAL = -2
MAXIMAG = 2
MINIMAG = -2
AJUSTE = 0.001

img = Image.new('RGB', (W, H+1), color = 'black') #imagem com +1 de altura para evitar erro na hora de desenhar pixeis na posição H
a = MINREAL
while a < MAXREAL:
    b = MINIMAG
    while b<MAXIMAG:
        z = complex(a,b)
        i = 0
        while i < it:
            z = z*z + c
            if(abs(z)>2):
                break
            i+=1

        if(i < it): #pinta se estoura
            #faz a mudança de escala (mapeamento) do plano complexo para as coordenadas da imagem
            x = int(W*(a-MINREAL)/(MAXREAL - MINREAL)) #converte a coordenada real complexa em coordenada x da imagem
            y = int(H*(b-MINIMAG)/(MAXIMAG - MINIMAG)) #converte a coordenada imaginária complexa em coordenada y da imagem
            y = H-y #inverte o y, pois na imagem o eixo Y cresce de cima pra baixo
            img.putpixel((x,y), (255,0,0))
        b+=AJUSTE
    a+=AJUSTE
img.save('res.png')