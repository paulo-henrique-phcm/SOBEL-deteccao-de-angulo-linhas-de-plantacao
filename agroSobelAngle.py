import cv2 #to load image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.color import rgb2gray

#variaveis
amostra = 50; #quantidade de amostra no histograma, (melhor resultado quando proximo de 50)
#a imagem a ser analisada

img = cv2.imread("./aa70.jpg") #load image
gray = rgb2gray(img)
#filtros sobel
sobel_horizontal = np.array([
    [1,2,1],
    [0,0,0],
    [-1,-2,-1]
])

sobel_vertical = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]])
#convolução dos filtros com a imagem em preto e branco
imgH = ndimage.convolve(gray, sobel_horizontal)
imgV = ndimage.convolve(gray, sobel_vertical)
plt.subplot(131)
plt.imshow(imgH, cmap='gray')

plt.subplot(132)
plt.imshow(imgV, cmap='gray')

# imgA terá os gradientes das diferencias (sobel) verticais e horzontais
imgA = imgH

for i in range(imgH.shape[0]):
    for j in range(imgH.shape[1]):
        try: #try evita problemas quando posições inexistentes são acessadas
            #pega os 8 pexel ao redor para melhor distribuição diferencias. calculo da media entre eles
            HtoMean = (imgH[i-1,j-1], imgH[i-1,j], imgH[i-1,j+1], imgH[i,j-1], imgH[i,j+1], imgH[i+1,j-1], imgH[i+1,j], imgH[i+1,j+1], imgH[i,j])
            VtoMean = (imgV[i-1,j-1], imgV[i-1,j], imgV[i-1,j+1], imgV[i,j-1], imgV[i,j+1], imgV[i+1,j-1], imgV[i+1,j], imgV[i+1,j+1], imgV[i,j])
            HtoMean = np.mean(HtoMean)
            VtoMean = np.mean(VtoMean)
            if VtoMean != 0: # para que não haja divisão por zero
                imgA[i,j] = ((np.arctan(HtoMean/VtoMean))*2)/np.pi
        except IndexError as e:
            pass # resposta para posições inexistentes

imgA = ((imgA*(-1) + 1)/2)*np.pi #ajuste de (-1 á 1) para (0 á pi) para calcular angulo
plt.subplot(133)
plt.imshow(imgA, cmap='gray')
plt.show()

imgAd = imgA.ravel() #transforma a matriz em um vetor linear

fig = plt.figure()
ax = fig.add_subplot(121, polar=True)

ax.set_thetamin(0)
ax.set_thetamax(180)
a,_,_ = plt.hist(imgAd, amostra,range=(0,np.pi)) #histograma do vetor de angulos, com 50 amostras no intervalo de 0 á pi
plt.title("Approximate angle: [ " + str((np.argmax(a)/amostra)*180) + " º ]")
# (np.argmax(a)/amostra)*180 obtém a posição (entre as amostras) do angulo com maior frequencia e converte para angulos de 0 á 180 º
ax = fig.add_subplot(122, polar=False)
plt.imshow(img)

plt.show()
