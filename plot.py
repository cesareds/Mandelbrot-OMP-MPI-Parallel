import matplotlib.pyplot as plt

file_in = "times.txt"
file_out = "graphic.png"

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

# Geração do gráfico
plt.figure(figsize=(10, 6))
plt.plot(mpi_times, label="MPI Only", marker='o')
plt.plot(omp_times, label="MPI + OpenMP", marker='s')
plt.title("Tempo de Execução (segundos)")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.close()

# Salva o gráfico
plt.savefig(file_out)
print(f"Gráfico salvo como '{file_out}'")

# boxplots:
plt.figure(figsize=(10, 6))
plt.boxplot(mpi_times, label="MPI Only", marker='o')
plt.boxplot(omp_times, label="MPI + OpenMP", marker='s')
plt.title("Tempo de Execução (segundos)")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid(True)
# plt.tight_layout()
plt.close()
