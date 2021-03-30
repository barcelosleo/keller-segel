import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import time

logical_dict = {"S":True, "s":True,"N":False, "n":False, "sim":True, "nao":False}

print("\n")
def FTCS(p,m,k1,k2,l,k3,v):
    N = p.shape[0]
    
    p_ = np.zeros(N)
    m_ = np.zeros(N)
    
    for j in np.arange(0,N):
        back = (j-1)%N
        forward = (j+1)%N
        p_[j] = (1 - 2*k1 - k2*(m[back] - m[j]))*p[j] + k1*(p[back]+p[forward]) - k2*(m[forward] - m[j])*p[forward]
        m_[j] = (1 - l - k3)*m[j] + k3*(m[back] + m[forward]) + v*p[j]
    return p_,m_

def plot_gif(p,m,t,images, p_max = True, m_max = True):
    fig,ax = plt.subplots(1,2,figsize=(10,5))
    if not p_max:
        p_max = p.max()
        ax[0].set_ylim(-0.05,100*p_max+0.55)
    if not m_max:
        m_max = m.max()
        ax[1].set_ylim(-0.02,m_max+0.05)
    ax[0].set_title("Population, t = {}".format(round(t,1)))
    ax[0].plot(100*p,color='purple')
    
    ax[0].set_ylabel("%")
    ax[0].grid(False)
    ax[1].set_title("Money, t = {}".format(round(t,1)))
    ax[1].plot(m,color='darkgreen')
    ax[1].fill_between(np.arange(m.shape[0]),m,color='green',alpha=0.5,label="Total money: $ {}".format(round(np.sum(m),2)))
    
    ax[1].set_ylabel("$")
    ax[1].grid(False)
    ax[1].legend()
    
    plt.tight_layout()
    plt.savefig(imgname)
    plt.close()
    
    images.append(imageio.imread(imgname))
    os.remove(imgname)
    time.sleep(0.5)

def plot_grid(fig,p,m,i,t,nrows=2,ncols=5):
    #Population
    ax_p = fig.add_subplot(nrows,ncols,i+1)
    ax_p.set_title("t = {}".format(t),fontsize=18)
    ax_p.plot(100*p,color='purple')
    ax_p.fill_between(np.arange(N),100*p,color='purple',alpha=0.5)
    
    #Money
    ax_m = fig.add_subplot(nrows,ncols,i+1+ncols)
    ax_m.set_title("t = {}".format(t),fontsize=18)
    ax_m.plot(m,color='darkgreen')
    ax_m.fill_between(np.arange(N),m,color='green',alpha=0.5,label="Renda líquida: $ {}".format(round(np.sum(m),2)))
    ax_m.legend(fontsize=10)
    
    if i == 0:
        ax_p.set_ylabel("%",fontsize=15)
        ax_m.set_ylabel("$", fontsize=15)

##########################################################################################
"""DECLARAÇÃO DE CONSTANTES"""
gif = True
global N
N = 100
dx = 1
dt = 0.3
Dn = 1.0
Dp = 1.0
gamma = 1.0
alpha = 1.0
beta = 1.0

k1 = Dp*dt/(dx**2)
k2 = gamma*k1/Dp
k3 = Dn*dt/(dx**2)
v = alpha*dt
l = beta*dt

imgname = "aux.png"
##########################################################################################
print("=================================================================================")
print("Caso 1: População e dinheiro em pontos separados")
print("População começa totalmente concentrada em 1 ponto da rede.")
print("Dinheiro começa totalmente focado em 1 ponto da rede longe do ponto da população.")
simulate = logical_dict[input("Deseja essa simulação?(S/N)\n")]
print("=================================================================================")
if simulate:
    gif = logical_dict[input("Gif? (S/N)\n")]
    print("=================================================================================")
N = 100
dx = 1
dt = 0.3
Dn = 1.0
Dp = 1.0
gamma = 1.0
alpha = 1.0
beta = 1.0

k1 = Dp*dt/(dx**2)
k2 = gamma*k1/Dp
k3 = Dn*dt/(dx**2)
v = alpha*dt
l = beta*dt

if simulate:
    N_simulations = 500
    T = N_simulations * dt
    
    #Setting population for t = 0
    p = np.zeros(N)
    p[20] = 1
    p_max = p.max()
    
    #Setting money for t = 0
    m = np.zeros(N)
    m[80] = 1
    m_max = m.max()
    
    if gif:
        path1 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/split_money_pop.gif"
        #Generate gif
        images = []
        for i,t in enumerate(np.arange(0,T,dt)):
            if gif:
                if m.max() > m_max:
                    m_max = m.max()
            if i % 10 == 0:
                print("Building gif for iteration {}".format(i))
                plot_gif(p,m,t,images,p_max = 1,m_max = m_max)
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        imageio.mimsave(path1, images,fps=3)
    else:
        ncols = 6
        snapshots = np.array([int(r*N_simulations) for r in np.arange(0,1,1/ncols)])
        print("Image will be formed with t = [{}]".format(snapshots*dt))
        #Adjusting figure
        fig, big_axes = plt.subplots(nrows=2,ncols=1,figsize=(20,6),sharey=True)
        titles = ["População (%)","Renda ($)"]
        count = 0
        for row,big_ax in enumerate(big_axes):
            big_ax.set_title(titles[row],fontsize=22,y=1.15)
            big_ax.axis('off')
        #Figure adjusted
        path2 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/split_money_pop.png"
        #Generate .png
        for i,t in enumerate(np.arange(0,T,dt)):
            if i in snapshots:
                print("Grid for {} is being build.".format(i))
                plot_grid(fig,p,m,count,round(t,2),ncols=ncols)
                count += 1
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        fig.subplots_adjust(hspace=0.55)
        plt.savefig(path2)
    print("Image generated!")
    print("#########################")
    show = logical_dict[input("Quer abrir o arquivo? (S/N)\n")]
    
    if show:
        if gif:
            os.system("xdg-open {}".format(path1))
        else:
            os.system("xdg-open {}".format(path2))

##########################################################################################
print("=================================================================================")
print("Caso 2: Sem dinheiro p/ t = 0")
print("População começa totalmente concentrada em 1 ponto da rede.")
print("Dinheiro começa zerado")
simulate = logical_dict[input("Deseja essa simulação?(S/N)\n")]
print("=================================================================================")
if simulate:
    gif = logical_dict[input("Gif? (S/N)\n")]
    print("=================================================================================")
N = 100
dx = 1
dt = 0.3
Dn = 1.0
Dp = 1.0
gamma = 1.0
alpha = 1.0
beta = 1.0

k1 = Dp*dt/(dx**2)
k2 = gamma*k1/Dp
k3 = Dn*dt/(dx**2)
v = alpha*dt
l = beta*dt

if simulate:
    N_simulations = 500
    T = N_simulations * dt
    #Setting population for t = 0
    p1 = np.random.rand(N)
    p = p1 / np.sum(p1)
    p_max = 0.05
    #p[50] = 1
    #Setting money for t = 0
    m = np.zeros(N)
    m_max = 1
    if gif:
        path1 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/m0.gif"
        #Generate gif
        images = []
        for i,t in enumerate(np.arange(0,T,dt)):
            if m.max() > m_max:
                m_max = m.max()
            if p.max() > p_max:
                p_max = p.max()
            if i % 10 == 0:
                print("Building gif for iteration {}".format(i))
                plot_gif(p,m,t,images,p_max = p_max,m_max = m_max)
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        imageio.mimsave(path1, images,fps=3)
    else:
        ncols = 6
        snapshots = np.array([int(r*N_simulations) for r in np.arange(0,1,1/ncols)])
        print("Image will be formed with t = [{}]".format(snapshots*dt))
        #Adjusting figure
        fig, big_axes = plt.subplots(nrows=2,ncols=1,figsize=(20,6),sharey=True)
        titles = ["População (%)","Renda ($)"]
        count = 0
        for row,big_ax in enumerate(big_axes):
            big_ax.set_title(titles[row],fontsize=22,y=1.15)
            big_ax.axis('off')
        #Figure adjusted
        path2 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/m0.png"
        #Generate .png
        for i,t in enumerate(np.arange(0,T,dt)):
            if i in snapshots:
                print("Grid for {} is being build.".format(i))
                plot_grid(fig,p,m,count,round(t,2),ncols=ncols)
                count += 1
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        fig.subplots_adjust(hspace=0.55)
        plt.savefig(path2)
    print("Image generated!")
    print("#########################")
    show = logical_dict[input("Quer abrir o arquivo? (S/N)\n")]
    
    if show:
        if gif:
            os.system("xdg-open {}".format(path1))
        else:
            os.system("xdg-open {}".format(path2))

 ####################################################################

##########################################################################################
print("=================================================================================")
print("Caso 3: Rede aleatória")
print("População começa distribuída aleatoriamente sobre a rede.")
print("Dinheiro começa totalmente focado em um ponto no meio da rede.")
simulate = logical_dict[input("Deseja essa simulação?(S/N)\n")]
print("=================================================================================")
if simulate:
    gif = logical_dict[input("Gif? (S/N)\n")]
    print("=================================================================================")

N = 100
dx = 1
dt = 0.3
Dn = 1.0
Dp = 1.0
gamma = 1.0
alpha = 1.0
beta = 1.0

k1 = Dp*dt/(dx**2)
k2 = gamma*k1/Dp
k3 = Dn*dt/(dx**2)
v = alpha*dt
l = beta*dt

if simulate:
    N_simulations = 500
    T = N_simulations * dt
    
    #Setting population for t = 0
    p1 = np.random.rand(N)
    p = p1 / np.sum(p1)
    p_max = p.max() + 0.05
    
    #Setting money for t = 0
    m = np.random.rand(N)
    m_max = m.max()
    if gif:
        path1 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/random_population.gif"
        #Generate gif
        images = []
        for i,t in enumerate(np.arange(0,T,dt)):
            if m.max() > m_max:
                m_max = m.max()
            if p.max() > p_max:
                p_max = p.max()
            if i % 10 == 0:
                print("Building gif for iteration {}".format(i))
                plot_gif(p,m,t,images,p_max = False,m_max = False)
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        imageio.mimsave(path1, images,fps=3)
        print("GIF generated!")
    else:
        ncols = 6
        snapshots = np.array([int(r*N_simulations) for r in np.arange(0,1,1/ncols)])
        print("Image will be formed with t = [{}]".format(snapshots*dt))
        #Adjusting figure
        fig, big_axes = plt.subplots(nrows=2,ncols=1,figsize=(20,6),sharey=True)
        titles = ["População (%)","Renda ($)"]
        count = 0
        for row,big_ax in enumerate(big_axes):
            big_ax.set_title(titles[row],fontsize=22,y=1.15)
            big_ax.axis('off')
        #Figure adjusted
        path2 = r"/home/rubens22/Desktop/MetCompC/Trabalho1/1D_Simulations/random_population.png"
        #Generate .png
        for i,t in enumerate(np.arange(0,T,dt)):
            if i in snapshots:
                print("Grid for {} is being build.".format(i))
                plot_grid(fig,p,m,count,round(t,2),ncols=ncols)
                count += 1
            p,m = FTCS(p,m,k1,k2,l,k3,v)
        fig.subplots_adjust(hspace=0.55)
        plt.savefig(path2)
        print("Image generated!")
    print("#########################")
    show = logical_dict[input("Quer abrir o arquivo? (S/N)\n")]
    
    if show:
        if gif:
            os.system("xdg-open {}".format(path1))
        else:
            os.system("xdg-open {}".format(path2))
       