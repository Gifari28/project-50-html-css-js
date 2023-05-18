import numpy as np
import random

# Inisialisasi parameter
num_of_ants = 10
num_of_flights = 5
num_of_days = 7
num_of_time_slots = 24
evaporation_rate = 0.5
alpha = 1
beta = 2
Q = 1
pheromone_matrix = np.ones((num_of_days, num_of_time_slots))

# Inisialisasi jadwal pesawat secara acak
flight_schedule = np.zeros((num_of_flights, num_of_days, num_of_time_slots))
for f in range(num_of_flights):
    for d in range(num_of_days):
        for t in range(num_of_time_slots):
            if random.random() < 0.5:
                flight_schedule[f][d][t] = 1

# Fungsi fitness
def fitness(schedule):
    # Menghitung jumlah penerbangan pada setiap jam dalam seminggu
    flights_per_slot = np.sum(schedule, axis=(0, 1))
    # Menghitung selisih antara jumlah penerbangan pada setiap jam dan rata-rata
    mean_flights = num_of_flights * num_of_days / num_of_time_slots
    deviation = np.abs(flights_per_slot - mean_flights)
    # Mengembalikan nilai fitness sebagai kebalikan dari selisih
    return 1 / (1 + deviation)

# Fungsi memilih waktu penerbangan berikutnya
def select_time_slot(f, d, schedule):
    time_slots = np.arange(num_of_time_slots)
    # Menghitung probabilitas untuk setiap waktu
    probabilities = []
    for t in time_slots:
        if schedule[f][d][t] == 0:
            numerator = pheromone_matrix[d][t] ** alpha * fitness(schedule[:, :, t]) ** beta
            denominator = np.sum(pheromone_matrix[d][time_slots] ** alpha * fitness(schedule[:, :, time_slots]) ** beta)
            probability = numerator / denominator
            probabilities.append(probability)
        else:
            probabilities.append(0)
    # Memilih waktu dengan probabilitas tertinggi
    probabilities = np.array(probabilities)
    probabilities /= np.sum(probabilities)
    time_slot = np.random.choice(time_slots, p=probabilities)
    return time_slot

# Fungsi update pheromone
def update_pheromone(schedule):
    # Mengurangi pheromone pada semua jalur
    pheromone_matrix *= evaporation_rate
    # Menambah pheromone pada jalur yang dilewati semut
    for f in range(num_of_flights):
        for d in range(num_of_days):
            time_slot = np.where(schedule[f][d] == 1)[0][0]
            pheromone_matrix[d][time_slot] += Q

# Main loop
for iteration in range(100):
    # Membuat koloni semut
    for ant in range(num_of_ants):
        # Inisialisasi jadwal pesawat baru
        ant_schedule = np.zeros((num_of_flights, num_of_days, num_of_time_slots))
        # Memilih waktu penerbangan untuk setiap pesawat
        for f in range(num_of_flights):
            for d in range(num_of_days):
                time_slot = select_time_slot(f, d, ant_schedule)
                ant_schedule
