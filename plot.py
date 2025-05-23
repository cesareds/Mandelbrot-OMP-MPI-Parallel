import numpy as np
import matplotlib.pyplot as plt

file_in = "times.txt"
file_out_all = "graphics/all.png"

with open(file_in, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

mpi_times = []
omp_times = []

mode = None
for line in lines:
    if line == "mpi":
        mode = "mpi"
    elif line == "omp":
        mode = "omp"
    else:
        try:
            time_value = float(line)
            if mode == "mpi":
                mpi_times.append(time_value)
            elif mode == "omp":
                omp_times.append(time_value)
        except ValueError:
            continue

def trunc(x, n=2):
    factor = 10.0 ** n
    return np.trunc(x * factor) / factor

# Construir dados da tabela
def build_metrics_table(mpi, omp):
    return [
        ["Métrica", "MPI Times", "OMP Times"],
        ["Tamanho", len(mpi), len(omp)],
        ["Média", f"{trunc(np.mean(mpi)):.2f}", f"{trunc(np.mean(omp)):.2f}"],
        ["Total", f"{trunc(np.sum(mpi)):.2f}", f"{trunc(np.sum(omp)):.2f}"],
        ["Desvio", f"{trunc(np.std(mpi)):.2f}", f"{trunc(np.std(omp)):.2f}"],
        ["Mín", f"{trunc(np.min(mpi)):.2f}", f"{trunc(np.min(omp)):.2f}"],
        ["Máx", f"{trunc(np.max(mpi)):.2f}", f"{trunc(np.max(omp)):.2f}"],
        ["Variação", f"{trunc(np.var(mpi)):.2f}", f"{trunc(np.var(omp)):.2f}"],
        ["Mediana", f"{trunc(np.median(mpi)):.2f}", f"{trunc(np.median(omp)):.2f}"],
        ["Q1", f"{trunc(np.percentile(mpi, 25)):.2f}", f"{trunc(np.percentile(omp, 25)):.2f}"],
        ["Q3", f"{trunc(np.percentile(mpi, 75)):.2f}", f"{trunc(np.percentile(omp, 75)):.2f}"],
        ["IQR", f"{trunc(np.percentile(mpi, 75) - np.percentile(mpi, 25)):.2f}", f"{trunc(np.percentile(omp, 75) - np.percentile(omp, 25)):.2f}"],
        ["Skewness", f"{trunc((3 * (np.mean(mpi) - np.median(mpi))) / np.std(mpi)):.2f}",
         f"{trunc((3 * (np.mean(omp) - np.median(omp))) / np.std(omp)):.2f}"]
    ]

# Preparar métricas para gráfico de barras
mean_values = [np.mean(mpi_times), np.mean(omp_times)]
std_values = [np.std(mpi_times), np.std(omp_times)]

# Layout: 2 colunas (esquerda: tabela; direita: dois gráficos empilhados)
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, width_ratios=[2, 2], height_ratios=[1.5, 1])
ax_table = fig.add_subplot(gs[:, 0])  # Ocupa as duas linhas da coluna 0
ax_line = fig.add_subplot(gs[0, 1])
ax_bar = fig.add_subplot(gs[1, 1])

# Tabela de métricas
ax_table.axis('off')
table_data = build_metrics_table(mpi_times, omp_times)
table = ax_table.table(cellText=table_data,
                       cellLoc='center',
                       loc='center')
table.scale(0.5, 3)
table.auto_set_font_size(False)
table.set_fontsize(10)
ax_table.set_title("Tabela de Métricas", fontsize=12)

# Gráfico de linha
ax_line.plot(mpi_times, label="MPI Only", marker='o', linewidth=1, color='blue')
ax_line.plot(omp_times, label="MPI + OpenMP", marker='s', linewidth=1, color='lightblue')
ax_line.set_title("Tempo por Execução")
ax_line.set_xlabel("Execução")
ax_line.set_ylabel("Tempo (s)")
ax_line.legend()
ax_line.grid(True)

# Gráfico de barras
bar_width = 0.35
x = np.arange(2)
ax_bar.bar(x, mean_values, width=bar_width, label='Média', color=['lightblue', 'lightblue'])
ax_bar.bar(x + bar_width, std_values, width=bar_width, label='Desvio Padrão', color=['blue', 'blue'])

# Texto nas barras
for i, v in enumerate(mean_values):
    ax_bar.text(i, v, f"{v:.2f}", ha='center', va='bottom')
for i, v in enumerate(std_values):
    ax_bar.text(i + bar_width, v, f"{v:.2f}", ha='center', va='bottom', color='lightblue')

ax_bar.set_title("Média e Desvio Padrão")
ax_bar.set_xticks(x + bar_width / 2)
ax_bar.set_xticklabels(['MPI Only', 'MPI + OpenMP'])
ax_bar.legend()
ax_bar.grid(True)

plt.tight_layout()
plt.savefig(file_out_all)
print(f"Gráfico salvo em: '{file_out_all}'")
plt.close()
