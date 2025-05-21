import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

file_in = "times.txt"
file_out_line = "graphic.png"
file_out_box = "boxplot.png"

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
            continue  # ignora linhas inválidas

# Gráfico de linha (tempo por execução)
plt.figure(figsize=(10, 6))
plt.plot(mpi_times, label="MPI Only", marker='o')
plt.plot(omp_times, label="MPI + OpenMP", marker='s')
plt.title("Tempo de Execução (segundos)")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(file_out_line)
print(f"Gráfico de linha salvo como '{file_out_line}'")
plt.close()

# Boxplot
plt.figure(figsize=(10, 6))
box = plt.boxplot([mpi_times, omp_times], patch_artist=True)
colors = ['lightblue', 'lightgreen']

# Colorir caixas
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Título, eixos e legenda
plt.title("Tempo de Execução - Boxplot")
plt.ylabel("Tempo (s)")
plt.xticks([1, 2], ['MPI Only', 'MPI + OpenMP'])
plt.grid(True)

# Legenda manual
plt.legend(
    [mpatches.Patch(color=colors[0]), mpatches.Patch(color=colors[1])],
    ['MPI Only', 'MPI + OpenMP']
)

plt.tight_layout()
plt.savefig(file_out_box)
print(f"Boxplot salvo como '{file_out_box}'")
plt.close()
