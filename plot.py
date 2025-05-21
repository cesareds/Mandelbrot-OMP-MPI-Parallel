import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_in = "times_dynamic.txt"
file_out_all = "graphics/all.png"

# Leitura e separação dos dados
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

# Função para truncar sem arredondar
def trunc(x, n=2):
    factor = 10.0 ** n
    return np.trunc(x * factor) / factor

# Impressão das métricas com alinhamento
print(f"{'Métrica':<12} {'MPI Times':>12} {'OMP Times':>12}")
print(f"{'Média':<12} {trunc(np.mean(mpi_times)):>12.2f} {trunc(np.mean(omp_times)):>12.2f}")
print(f"{'Total':<12} {trunc(np.sum(mpi_times)):>12.2f} {trunc(np.sum(omp_times)):>12.2f}")
print(f"{'Desvio':<12} {trunc(np.std(mpi_times)):>12.2f} {trunc(np.std(omp_times)):>12.2f}")
print(f"{'Mín':<12} {trunc(np.min(mpi_times)):>12.2f} {trunc(np.min(omp_times)):>12.2f}")
print(f"{'Máx':<12} {trunc(np.max(mpi_times)):>12.2f} {trunc(np.max(omp_times)):>12.2f}")
print(f"{'Variação':<12} {trunc(np.var(mpi_times)):>12.2f} {trunc(np.var(omp_times)):>12.2f}")
print(f"{'Mediana':<12} {trunc(np.median(mpi_times)):>12.2f} {trunc(np.median(omp_times)):>12.2f}")
print(f"{'Q1':<12} {trunc(np.percentile(mpi_times, 25)):>12.2f} {trunc(np.percentile(omp_times, 25)):>12.2f}")
print(f"{'Q3':<12} {trunc(np.percentile(mpi_times, 75)):>12.2f} {trunc(np.percentile(omp_times, 75)):>12.2f}")
print(f"{'IQR':<12} {trunc(np.percentile(mpi_times, 75) - np.percentile(mpi_times, 25)):>12.2f} {trunc(np.percentile(omp_times, 75) - np.percentile(omp_times, 25)):>12.2f}")
print(f"{'Skewness':<12} {trunc((3 * (np.mean(mpi_times) - np.median(mpi_times))) / np.std(mpi_times)):>12.2f} {trunc((3 * (np.mean(omp_times) - np.median(omp_times))) / np.std(omp_times)):>12.2f}")

# ========= VISUALIZAÇÕES ORIGINAIS =========

# Gráfico de linha
plt.figure(figsize=(10, 6))
plt.plot(mpi_times, label="MPI Only", marker='o')
plt.plot(omp_times, label="MPI + OpenMP", marker='s')
plt.title("Tempo por Execução")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid(True)
plt.savefig("graphics/line_plot.png")
plt.close()

# Boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([mpi_times, omp_times], labels=["MPI Only", "MPI + OpenMP"])
plt.title("Boxplot dos Tempos")
plt.ylabel("Tempo (s)")
plt.grid(True)
plt.savefig("graphics/boxplot.png")
plt.close()

# ========= NOVOS GRÁFICOS ADICIONAIS =========

# Preparar métricas para gráfico de barras
mean_values = [np.mean(mpi_times), np.mean(omp_times)]
std_values = [np.std(mpi_times), np.std(omp_times)]
skew_values = [
    (3 * (np.mean(mpi_times) - np.median(mpi_times))) / np.std(mpi_times),
    (3 * (np.mean(omp_times) - np.median(omp_times))) / np.std(omp_times)
]

# Gráfico composto
fig, axs = plt.subplots(2, 2, figsize=(16, 10))

# Repetição do gráfico de linha no subplot
axs[0, 0].plot(mpi_times, label="MPI Only", marker='o')
axs[0, 0].plot(omp_times, label="MPI + OpenMP", marker='s')
axs[0, 0].set_title("Tempo por Execução")
axs[0, 0].set_xlabel("Execução")
axs[0, 0].set_ylabel("Tempo (s)")
axs[0, 0].legend()
axs[0, 0].grid(True)

# Boxplot no subplot
box = axs[0, 1].boxplot([mpi_times, omp_times], patch_artist=True)
colors = ['lightblue', 'lightgreen']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
axs[0, 1].set_title("Boxplot dos Tempos")
axs[0, 1].set_xticks([1, 2])
axs[0, 1].set_xticklabels(['MPI Only', 'MPI + OpenMP'])
axs[0, 1].grid(True)

# Histograma com KDE
sns.histplot(mpi_times, kde=True, color='lightblue', label='MPI Only', ax=axs[1, 0])
sns.histplot(omp_times, kde=True, color='lightgreen', label='MPI + OpenMP', ax=axs[1, 0])
axs[1, 0].set_title("Distribuição dos Tempos")
axs[1, 0].set_xlabel("Tempo (s)")
axs[1, 0].legend()
axs[1, 0].grid(True)

# Gráfico de barras com valores
bar_width = 0.25
x = np.arange(2)
axs[1, 1].bar(x, mean_values, width=bar_width, label='Média', color=['lightblue', 'lightgreen'])
axs[1, 1].bar(x + bar_width, std_values, width=bar_width, label='Desvio Padrão', color=['blue', 'green'])
axs[1, 1].bar(x + 2*bar_width, skew_values, width=bar_width, label='Assimetria', color=['darkblue', 'darkgreen'])

# Texto nas barras
for i, v in enumerate(mean_values):
    axs[1, 1].text(i, v, f"{v:.2f}", ha='center', va='bottom')
for i, v in enumerate(std_values):
    axs[1, 1].text(i + bar_width, v, f"{v:.2f}", ha='center', va='bottom', color='white')
for i, v in enumerate(skew_values):
    axs[1, 1].text(i + 2*bar_width, v, f"{v:.2f}", ha='center', va='bottom', color='white')

axs[1, 1].set_title("Média, Desvio Padrão e Assimetria")
axs[1, 1].set_xticks(x + bar_width)
axs[1, 1].set_xticklabels(['MPI Only', 'MPI + OpenMP'])
axs[1, 1].legend()
axs[1, 1].grid(True)

plt.tight_layout()
plt.savefig(file_out_all)
print(f"Gráficos salvos: 'graphics/line_plot.png', 'graphics/boxplot.png', e '{file_out_all}'")
plt.close()
