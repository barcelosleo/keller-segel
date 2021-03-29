import os
import imageio
import numpy as np
import time
import matplotlib
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ParametrosKellerSegelModel():
    def __init__(self, L_x, L_y,D_p, D_m, ds, dt, alfa, beta, gamma):
        self.L_x = L_x # Tamanho em x
        self.L_y = L_y # Tamanho em y
        self.D_p = D_p # Coeficiente de difusão da população
        self.D_m = D_m # Coeficiente de difusão da economia
        self.ds = ds # Diferencial espacial
        self.dt = dt # Diferencial temporal
        self.alfa = alfa # taxa de produção de economia per capita
        self.beta = beta # taxa de decaimente da economia
        self.gamma = gamma # velocidade com que as pessoas migram em direção ao dinheiro

        self.k1 = D_p * dt / (ds ** 2)
        self.k2 = gamma * self.k1 / D_p
        self.k3 = D_m * dt / (ds ** 2)
        self.v = alfa * dt
        self.lamb = beta * dt

        self.N_x = int(np.ceil(L_x / ds)) # Arredonda pra cima
        self.N_y = int(np.ceil(L_y / ds)) # Arredonda pra cima

        self.x = np.arange(0, L_x, ds) # Lista dos x
        self.y = np.arange(0, L_y, ds) # Lista dos y

    def getParametros(self):
        return {
            'L_x' : self.L_x,
            'L_y' : self.L_y,
            'D_p' : self.D_p,
            'D_m' : self.D_m,
            'ds' : self.ds,
            'dt' : self.dt,
            'alfa' : self.alfa,
            'beta' : self.beta,
            'gamma' : self.gamma,
            'k1': self.k1,
            'k2': self.k2,
            'k3': self.k3,
            'v': self.v,
            'lamb': self.lamb,
            'x': self.x,
            'y': self.y,
        }

class KellerSegelModel():
    def __init__(self, parametros):
        self.parametros = parametros

        self.zeros = np.matrix(np.zeros((parametros.N_x, parametros.N_y)))

        self.tempo = 0

    def contagemPopulacao(self):
        return self.estado_populacao.sum()

    def contagemDinheiro(self):
        return self.estado_dinheiro.sum()

    def setEstadoInicial(self, matriz_populacao, matriz_dinheiro):
        self.estado_populacao = np.matrix(matriz_populacao)
        self.estado_dinheiro = np.matrix(matriz_dinheiro)

    def getEstado(self):
        return (self.estado_populacao, self.estado_dinheiro, self.tempo)

    def atualizaEstado(self):
        # Pega o estado atual da população e dinheiro
        pn = self.estado_populacao
        mn = self.estado_dinheiro

        # Inicializa as variáveis que receberão o estado seguinte
        pn1 = self.zeros.copy()
        mn1 = self.zeros.copy()

        k1 = self.parametros.k1
        k2 = self.parametros.k2
        k3 = self.parametros.k3
        lamb = self.parametros.lamb
        v = self.parametros.v

        # Realiza o FTCS
        for i in np.arange(0, self.parametros.N_x):
            i_previous = (i - 1) % self.parametros.N_x # Garante que em i == 0 o item anterior seja o último da lista
            i_next = (i + 1) % self.parametros.N_x # Garante que em i == N_x o item posterior seja o primeiro da lista

            for j in np.arange(0, self.parametros.N_y):
                j_previous = (j - 1) % self.parametros.N_y # Garante que em j == 0 o item anterior seja o último da lista
                j_next = (j + 1) % self.parametros.N_y # Garante que em j == N_y o item posterior seja o primeiro da lista

                pn1[(i, j)] = pn[(i, j)] * (1 - 4 * k1 - k2 * (mn[(i_previous, j)] - 2 * mn[(i, j)] + mn[(i, j_previous)])) \
                            + k1 * (pn[(i_previous, j)] + pn[(i, j_previous)] + pn[(i_next, j)] + pn[(i, j_next)]) \
                            - k2 * (pn[(i_next, j)] * (mn[(i_next, j)] - mn[(i, j)]) + pn[(i, j_next)] * (mn[(i, j_next)] - mn[(i, j)]))

                mn1[(i, j)] = mn[(i, j)] * (1 - 4 * k3 - lamb) + k3 * (mn[(i_previous, j)] + mn[(i, j_previous)] + mn[(i_next, j)] + mn[(i, j_next)]) + v * pn[(i, j)]

        self.estado_populacao = pn1 # Atualiza o estado da população
        self.estado_dinheiro = mn1 # Atualiza o estado do dinheiro
        self.tempo += self.parametros.dt # Atualiza o tempo decorrido no modelo

    def atualizaEstadoMultiplasVezes(self, n = 1):
        for _ in range(0, n):
            self.atualizaEstado()

class AnimacaoTool():
    def __init__(self, nome_gif):
        self.nome_gif = nome_gif
        self.temp_img_name = 'tmp.jpeg'
        self.images = []

    def plotSuperficie(self, ax, x, y, z, cmap, title): # Método para fazer o plot da superfície
        X, Y = np.meshgrid(x, y)
        ax.set_title(title, fontsize = 15)
        ax.grid(False)
        plot = ax.plot_surface(X, Y, z, cmap=cmap, edgecolor='none', rstride=1, cstride=1, shade=True)
        return plot

    def __plotDuasSuperficies(self, x, y, populacao, dinheiro): # Método para fazer um plot para população e dinheiro separadamente
        f = plt.figure(figsize=(10, 6))
        ax = f.add_subplot(1, 2, 1, projection = '3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.plotSuperficie(ax, x, y, populacao, 'cool', 'População')

        ax = f.add_subplot(1, 2, 2, projection = '3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.plotSuperficie(ax, x, y, dinheiro, 'winter', 'Dinheiro')

    def __plotUmaSuperficie(self, x, y, populacao, dinheiro): # Método para fazer um plot para população com o dinheiro sendo uma 4ª dimensão na forma de mapa de cor
        X, Y = np.meshgrid(x, y)
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('População')
        ax.set_title('População-Economia', fontsize = 15)

        # fourth dimention - colormap
        # create colormap according to x-value (can use any 50x50 array)
        color_dimension = dinheiro # change to desired fourth dimension
        minn, maxx = color_dimension.min(), color_dimension.max()
        norm = matplotlib.colors.Normalize(minn, maxx)
        m = plt.cm.ScalarMappable(norm=norm, cmap='viridis')
        m.set_array([])
        fcolors = m.to_rgba(color_dimension)


        plot = ax.plot_surface(X, Y, populacao, edgecolor='none', rstride=1, cstride=1, facecolors=fcolors, vmin=minn, vmax=maxx, shade=True)

        fig.colorbar(plot)

        return plot

    def plotEstadoModelo(self, x, y, populacao, dinheiro): # Método que seleciona o tipo de plot
        self.__plotDuasSuperficies(x, y, populacao, dinheiro)
        # self.__plotUmaSuperficie(x, y, populacao, dinheiro)

    def __erro(self, pn, pn10): # Cálculo do erro
        dif_p = pn - pn10
        erro = dif_p.max()
        return erro

    def salvaFrame(self): # Salva o frame em uma lista
        plt.savefig(self.temp_img_name)
        plt.close()
        self.images.append(imageio.imread(self.temp_img_name))
        os.remove(self.temp_img_name)

    def geraGif(self, modelo, epsilon = 1e-6): # Método que gera o gif animado. Recebe como parâmetro o modelo, e uma tolerância epsilon
        print(f"Iniciando processamento...")
        start = time.time() # Salva o tempo inicial de processamento do modelo

        x = modelo.parametros.x
        y = modelo.parametros.y
        populacao, dinheiro, _ = modelo.getEstado()

        self.plotEstadoModelo(x, y, populacao, dinheiro) # Plota o estado inicial
        self.salvaFrame() # Salva o frame

        erro = 999

        print(f"População: {modelo.contagemPopulacao()}") # Esse trecho de código serve para acompanhar se a população está se mantendo fixa, em consonância com o modelo
        print(f"Dinheiro: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido inicial

        while erro >= epsilon:
            modelo.atualizaEstadoMultiplasVezes(n = 10) # Intera dez vezes o estado do modelo
            p, d, _ = modelo.getEstado() # Pega os valores da população e dinheiro

            self.plotEstadoModelo(x, y, p, d) # Plota o estado atual
            self.salvaFrame() # Salva o frame

            erro = self.__erro(dinheiro, d) # Calcula o erro
            dinheiro = d # atualiza a variável de comparação

            print(f"Erro atual: {erro}") # Mostra o erro para verificar se o modelo está convergindo
            print(f"População Atual: {modelo.contagemPopulacao()}") # Verifica a população
            print(f"Dinheiro Atual: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido

        elapsed = time.time() - start # Calcula o tempo de processamento
        print(f"Fim do processamento: {elapsed}s")

        print(f"Iniciando render...")
        start = time.time() # Salva o tempo inicial de render

        imageio.mimsave(f'{self.nome_gif}.gif', self.images, fps=20) # Gera um gif com as imagens geradas. Deve-se tomar cuidado com o número de interações, pois muitas imagens podem lotar facilmente a memória RAM

        elapsed = time.time() - start # Calcula o tempo de render do gif
        print(f"Fim do render: {elapsed}s")

class JpegTool():
    def __init__(self, nome_imagem):
        self.nome_imagem = nome_imagem

    def plotSuperficie(self, ax, x, y, z, cmap, title): # Método que faz um plot da superfície
        X, Y = np.meshgrid(x, y)
        ax.set_title(title, fontsize = 15)
        ax.grid(False)
        plot = ax.plot_surface(X, Y, z, cmap=cmap, edgecolor='none', rstride=1, cstride=1, shade=True)
        return plot

    def __plotDuasSuperficies(self, f, x, y, populacao, dinheiro, tempo, n): # Método que plota as superfícies da população e dinheiro, uma acima da outra, na n-ésima coluna de 6
        ax = f.add_subplot(2, 6, n, projection = '3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.plotSuperficie(ax, x, y, populacao, 'cool', f'População (t = {round(tempo)}s)')

        ax = f.add_subplot(2, 6, n + 6, projection = '3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.plotSuperficie(ax, x, y, dinheiro, 'winter', f'Dinheiro (t = {round(tempo)}s)')

    def plotEstadosModelo(self, x, y, estados): # Intera sobre os estados de evolução do modelo e plot
        f = plt.figure(figsize=(20, 7), dpi=290)
        for i in range(len(estados)):
            self.__plotDuasSuperficies(f, x, y, estados[i][0], estados[i][1], estados[i][2], i + 1)

    def salvaJpeg(self, sufixo = ''): # salva as 12 superfícies em uma imagem
        plt.savefig(f"{self.nome_imagem}{sufixo}.png")
        plt.close()

    def geraJpeg(self, modelo): # Método que gera uma imagem com 6 estados de evolução do modelo. Recebe como parâmetro o modelo
        print(f"Iniciando processamento...")
        start = time.time() # Salva o tempo inicial de processamento do modelo

        m = [] # lista de estados da evolução do modelo

        x = modelo.parametros.x
        y = modelo.parametros.y
        m.append(modelo.getEstado()) # Salva o estado inicial

        self.plotEstadosModelo(x, y, estados = m) # Plota o estado
        self.salvaJpeg() # Salva para visualização prévia

        print(f"População: {modelo.contagemPopulacao()}") # Verifica a população
        print(f"Dinheiro: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido

        modelo.atualizaEstadoMultiplasVezes(n = int(15 / modelo.parametros.dt)) # 15s
        m.append(modelo.getEstado())

        self.plotEstadosModelo(x, y, estados = m) # Plota o estado
        self.salvaJpeg() # Salva para visualização prévia

        print(f"População: {modelo.contagemPopulacao()}") # Verifica a população
        print(f"Dinheiro: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido

        modelo.atualizaEstadoMultiplasVezes(n = int(30 / modelo.parametros.dt)) # 30s
        m.append(modelo.getEstado())

        self.plotEstadosModelo(x, y, estados = m) # Plota o estado
        self.salvaJpeg() # Salva para visualização prévia

        print(f"População: {modelo.contagemPopulacao()}") # Verifica a população
        print(f"Dinheiro: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido

        modelo.atualizaEstadoMultiplasVezes(n = int(45 / modelo.parametros.dt)) # 45s
        m.append(modelo.getEstado())

        self.plotEstadosModelo(x, y, estados = m) # Plota o estado
        self.salvaJpeg() # Salva para visualização prévia

        print(f"População: {modelo.contagemPopulacao()}") # Verifica a população
        print(f"Dinheiro: {modelo.contagemDinheiro()}\n") # Mostra o dinheiro líquido

        modelo.atualizaEstadoMultiplasVezes(n = int(200 / modelo.parametros.dt)) # 200s
        m.append(modelo.getEstado())

        self.plotEstadosModelo(x, y, estados = m) # Plota o estado
        self.salvaJpeg() # Salva para visualização prévia

        elapsed = time.time() - start # Calcula o tempo de processamento
        print(f"Fim do processamento: {elapsed}s")


if __name__ == "__main__":
    L = 100 # Tamanho do Grid
    D_p = 0.5 # Coeficiente de difusão de pessoas
    D_m = 0.5 # Coeficiente de difusão de dinheiro
    ds = 1 # Diferencial Espacial
    dt = 0.3 # Diferencial Temporal
    alfa = 1.2 # Taxa de produção de economia per capita
    beta = 0.03 # Taxa de decaimente da economia
    gamma = 1 # Taxa de velocidade com que as pessoas migram em direção ao dinheiro

    # CRIA OBJETO DE PARÂMETROS PARA O MODELO #
    parametros = ParametrosKellerSegelModel(L, L, D_p, D_m, ds, dt, alfa, beta, gamma)

    # INICIALIZA O MODELO COM OS PARÂMETROS #
    modelo = KellerSegelModel(parametros)

    # GERA CONDIÇÕES INICIAIS A SEREM ESTUDADAS #
    condicao_inicial_populacao = np.matrix(np.full((parametros.N_x, parametros.N_x), 1 / (L ** 2)))
    condicao_inicial_dinheiro = np.matrix(np.full((parametros.N_y, parametros.N_y), 1 / (L ** 2)))

    # condicao_inicial_dinheiro[(0, 0)] = 0.125
    # condicao_inicial_dinheiro[(0, 99)] = 0.125
    # condicao_inicial_dinheiro[(99, 99)] = 0.125
    # condicao_inicial_dinheiro[(99, 0)] = 0.125
    # condicao_inicial_dinheiro[(49, 49)] = 0.5
    # condicao_inicial_dinheiro[(49, 69)] = 1
    # condicao_inicial_dinheiro[(49, 29)] = 2
    # condicao_inicial_dinheiro[(69, 49)] = 3
    # condicao_inicial_dinheiro[(29, 49)] = 4

    condicao_inicial_dinheiro[(24, 24)] = 1
    condicao_inicial_dinheiro[(74, 74)] = 1

    # SETA AS CONDIÇÕES INICIAIS DO MODELO #
    modelo.setEstadoInicial(condicao_inicial_populacao, condicao_inicial_dinheiro)

    # # GERA O OBJETO DE GRÁFICO ESTÁTICO
    # jpeg = JpegTool(nome_imagem = 'comparacao_tempos_pop_uniforme_sem_dinheiro')

    # # GERA GRÁFICOS
    # jpeg.geraJpeg(modelo)

    # # REINICIALIZA MODELO
    # modelo = KellerSegelModel(parametros)

    # # SETA AS CONDIÇÕES INICIAIS DO MODELO #
    # modelo.setEstadoInicial(condicao_inicial_populacao, condicao_inicial_dinheiro)

    # GERA O OBJETO DE ANIMACAO #
    ani = AnimacaoTool(nome_gif = 'dinamica_pop_eco_2d_pop_uniforme_sem_dinheiro')

    # GERA GIF COM A EVOLUCAO DO MODELO #
    ani.geraGif(modelo)


