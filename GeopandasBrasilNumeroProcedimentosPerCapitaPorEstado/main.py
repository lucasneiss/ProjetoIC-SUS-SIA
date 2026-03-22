import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

# atribuir os estados as capitais
df = pd.read_csv('Taxa_Per_Capita_Por_Ano.csv', sep=';')
capitais_para_estados = {
    'Aracaju': 'Sergipe', 'Belo Horizonte': 'Minas Gerais', 'Belém': 'Pará',
    'Boa Vista': 'Roraima', 'Brasília': 'Distrito Federal', 'Campo Grande': 'Mato Grosso do Sul',
    'Cuiabá': 'Mato Grosso', 'Curitiba': 'Paraná', 'Florianópolis': 'Santa Catarina',
    'Fortaleza': 'Ceará', 'Goiânia': 'Goiás', 'João Pessoa': 'Paraíba',
    'Macapá': 'Amapá', 'Maceió': 'Alagoas', 'Manaus': 'Amazonas', 'Natal': 'Rio Grande do Norte',
    'Palmas': 'Tocantins', 'Porto Alegre': 'Rio Grande do Sul', 'Porto Velho': 'Rondônia',
    'Recife': 'Pernambuco', 'Rio Branco': 'Acre', 'Rio de Janeiro': 'Rio de Janeiro',
    'Salvador': 'Bahia', 'São Luís': 'Maranhão', 'São Paulo': 'São Paulo',
    'Teresina': 'Piauí', 'Vitória': 'Espírito Santo'
}
df['nome_estado'] = df['Capital'].map(capitais_para_estados)
anos = ['PerCapita_2018', 'PerCapita_2019', 'PerCapita_2020', 'PerCapita_2023', 'PerCapita_2024'] # anos analizados

# carregar mapa
url_estados = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
gdf_final = gpd.read_file(url_estados).merge(df, left_on='name', right_on='nome_estado')

# configuração da Figura
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(bottom=0.25) # espaço para o slider

# limites de escala
vmin, vmax = df[anos].min().min(), df[anos].max().max()

# plot inicial
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
cbar = fig.colorbar(sm, ax=ax, label="Procedimentos Per Capita")

def plotar_mapa(ano_idx):
    ax.clear()
    coluna = anos[int(ano_idx)]
    gdf_final.plot(column=coluna, cmap='YlOrRd', ax=ax, edgecolor='black',
                   linewidth=0.5, vmin=vmin, vmax=vmax)
    ax.set_axis_off()
    ano_texto = coluna.split('_')[1]
    ax.set_title(f'Taxa Per Capita em {ano_texto}', fontsize=16)

# primeiro ano
plotar_mapa(0)

# configurar slider
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
# configurar que a escala pule de 1 em 1 ano
slider = Slider(ax_slider, 'Ano (Arraste)', 0, len(anos)-1, valinit=0, valstep=1)

# Mapear os números do slider para os nomes dos anos reais na tela
slider.valtext.set_text(anos[0].split('_')[1])

def update(val):
    idx = int(slider.val)
    plotar_mapa(idx)
    # atualizar texto
    slider.valtext.set_text(anos[idx].split('_')[1])
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
