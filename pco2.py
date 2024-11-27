!curl -O https://raw.githubusercontent.com/AngeloDev-New/rosangelaPublic/refs/heads/main/dados_carbono.csv
!curl -O https://raw.githubusercontent.com/AngeloDev-New/rosangelaPublic/refs/heads/main/Dados.csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


Populacao = []
with open("Dados.csv","r") as doc:
    for i,line in enumerate(doc):
        if(i==0):
            titulo1,titulo2 = line.split(",")
            continue
        _,Y = line.split(',')
        Populacao.append(float(Y.replace(".","")))

# Dados de exemplo (x e y)

CO2 = []
with open("dados_carbono.csv", "r") as doc:
    for i, line in enumerate(doc):
        if i == 0:
            titulo1, titulo2 = line.split(",")
            continue
        _, Y = line.split(",")
        CO2.append(float(Y))

x = Populacao
y = CO2


titulo = 'População vs. CO₂'

# Função para regressão exponencial: y = a * exp(b * x)
def exponencial(x, a, b):
    return a * np.exp(b * x)

# Função para regressão logarítmica: y = a * log(x) + b
def logaritmica(x, a, b):
    return a * np.log(x) + b

# Função para regressão potencial: y = a * x^b
def potencial(x, a, b):
    return a * x**b

# Ajuste das curvas (retorna os parâmetros otimizados a e b)
params_exp, _ = curve_fit(exponencial, x, y, maxfev=10000)
params_log, _ = curve_fit(logaritmica, x, y, maxfev=10000)
params_pot, _ = curve_fit(potencial, x, y, maxfev=10000)

# Ajuste linear
params_lin = np.polyfit(x, y, 1)  # Grau 1 para regressão linear
lin_fit = np.poly1d(params_lin)   # Função linear gerada

# Gerar valores ajustados
x_fit = np.linspace(min(x), max(x), 100)  # Valores de x para a curva
y_exp = exponencial(x_fit, *params_exp)
y_log = logaritmica(x_fit, *params_log)
y_pot = potencial(x_fit, *params_pot)
y_lin = lin_fit(x_fit)  # Valores ajustados para o linear

# Plot dos dados e das curvas ajustadas
plt.scatter(x, y, color='red', label='Dados reais')  # Dados reais
plt.plot(x_fit, y_exp, label=f'Exponencial: y = {params_exp[0]:.2f} * exp({params_exp[1]:.2f} * x)')
plt.plot(x_fit, y_log, label=f'Logarítmica: y = {params_log[0]:.2f} * log(x) + {params_log[1]:.2f}')
plt.plot(x_fit, y_pot, label=f'Potencial: y = {params_pot[0]:.2f} * x^{params_pot[1]:.2f}')
plt.plot(x_fit, y_lin, label=f'Linear: y = {params_lin[0]:.2f} * x + {params_lin[1]:.2f}', linestyle='--', color='black')

# Configuração do gráfico
plt.xlabel('x')
plt.ylabel('y')
plt.title(titulo)
plt.legend()
plt.grid(True)
plt.show()
