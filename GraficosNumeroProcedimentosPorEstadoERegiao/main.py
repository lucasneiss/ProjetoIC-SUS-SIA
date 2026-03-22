import pandas as pd
import matplotlib.pyplot as plt

# tira notacao cientifica
pd.options.display.float_format = '{:.2f}'.format

# limpeza dos dados
df = pd.read_csv(
    'dadosAnalise.csv',
    encoding='latin1',
    sep=';',
    skiprows=3,
    skipfooter=11,
    engine='python'
)

df['Capital'] = df['Capital'].str.replace(r'^\d+\s', '', regex=True).str.strip()
df = df[df['Capital'] != 'Total']

# mapeia regioes
regioes = {
    'Porto Velho': 'Norte', 'Rio Branco': 'Norte', 'Manaus': 'Norte', 'Boa Vista': 'Norte',
    'Belém': 'Norte', 'Macapá': 'Norte', 'Palmas': 'Norte',
    'São Luís': 'Nordeste', 'Teresina': 'Nordeste', 'Fortaleza': 'Nordeste', 'Natal': 'Nordeste',
    'João Pessoa': 'Nordeste', 'Recife': 'Nordeste', 'Maceió': 'Nordeste', 'Aracaju': 'Nordeste',
    'Salvador': 'Nordeste',
    'Belo Horizonte': 'Sudeste', 'Vitória': 'Sudeste', 'Rio de Janeiro': 'Sudeste', 'São Paulo': 'Sudeste',
    'Curitiba': 'Sul', 'Florianópolis': 'Sul', 'Porto Alegre': 'Sul',
    'Campo Grande': 'Centro-Oeste', 'Cuiabá': 'Centro-Oeste', 'Goiânia': 'Centro-Oeste', 'Brasília': 'Centro-Oeste'
}

# cria colunas com cores
df['Regiao'] = df['Capital'].map(regioes)

cores_map = {
    'Norte': '#27ae60',         # Verde
    'Nordeste': '#f39c12',      # Laranja
    'Sudeste': '#2980b9',       # Azul
    'Sul': '#c0392b',           # Vermelho
    'Centro-Oeste': '#8e44ad'   # Roxo
}

df['Cor'] = df['Regiao'].map(cores_map)

# ordena o grafico
df = df.sort_values(by='Qtd.aprovada', ascending=True)


plt.figure(figsize=(12, 10))

# plota as barras usando a coluna de cores
plt.barh(df['Capital'], df['Qtd.aprovada'], color=df['Cor'], edgecolor='black', alpha=0.8)

# informacoes
plt.suptitle('Produção Ambulatorial do SUS por Região', fontsize=16, fontweight='bold')
plt.title('Quantidade aprovada por Capital (2018-2024) | Fonte: DataSUS', fontsize=11, pad=15)

# legendas
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color=cor, lw=4, label=reg) for reg, cor in cores_map.items()]
plt.legend(handles=legend_elements, title="Regiões", loc='lower right', borderpad=1)

plt.xlabel('Quantidade Aprovada', fontweight='bold')
plt.grid(axis='x', linestyle='--', alpha=0.3)



plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# para salvar a figura no computador remova esse comentario plt.savefig('grafico_sus_capitais.png', dpi=300, bbox_inches='tight')

plt.show()
