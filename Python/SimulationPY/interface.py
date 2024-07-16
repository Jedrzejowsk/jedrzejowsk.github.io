#Grzegorz Jędrzejowski 428515 29.01.2024
import os
import tkinter as tk
from particle import Particle
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#umożliwienie pisania przecinka
def convert_to_float(value):
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None

# Nowa funkcja pomocnicza do wykonania pojedynczego kroku symulacji
def perform_simulation_step():
    global running, particle, lines, ax, canvas, iteration_count
    if running and iteration_count < 1000:  # Ustaw limit iteracji na 1000
        particle.runge_kutta_step(0.001)  # Przykładowy krok czasowy
        x, y = particle.get_position()
        update_plot(x, y, current_color)
        iteration_count += 0  # jak na 1 to jest limit iteracji
        root.after(1, perform_simulation_step)  # szybkość rysowania, im mniejsza 1 liczba tym szybciej
    else:
        running = False  # Zatrzymaj symulację po osiągnięciu limitu iteracji


# Funkcja rozpoczynająca symulację
def start_simulation():
    global running, current_color, lines, initial_conditions_text, particle, iteration_count

     #WARUNKI
    
    # Sprawdzenie, czy wszystkie pola są wypełnione
    if not all([central_charge_entry.get(), q_entry.get(), B_entry.get(), m_entry.get(), vx_entry.get(), vy_entry.get()]):
        messagebox.showerror("Input Error", "Please fill in all fields to start the simulation.")
        return
    
    # Pobiera wartości z pól wprowadzania
    central_charge = convert_to_float(central_charge_entry.get())
    q = convert_to_float(q_entry.get())
    B = convert_to_float(B_entry.get())
    m = convert_to_float(m_entry.get())
    vx = convert_to_float(vx_entry.get())
    vy = convert_to_float(vy_entry.get())

    #nieujemna masa
    try:
        m = convert_to_float(m_entry.get())
        if m < 0:
            messagebox.showerror("Value Error", "Mass needs to be greater or equal to 0.")
            return
    except ValueError:
        messagebox.showerror("Value Error", "Invalid input for mass.")
        return
    
    running = True
    lines.set_xdata([])
    lines.set_ydata([])
    current_color ="#ff0000"
     

    # Aktualizacja tekstu z wartościami początkowymi
    initial_conditions_text.set_text(
        f"Q: {central_charge}e\n"
        f"B: {B}  nT\n"
        f"q: {q}e\n"
        f"m: {m} MeV/c^2\n"
        f"[vx,vy]: [{vx}, {vy}] m/s"
    )

    # Tworzy obiekt Particle i ustawia początkowe warunki
    particle = Particle(q, B, m, central_charge)
    particle.set_initial_conditions([0, 0], [vx, vy])
    iteration_count = 0  # Inicjalizacja licznika iteracji


    # Rozpoczęcie aktualizacji wykresu w czasie rzeczywistym

    perform_simulation_step()
    


# Funkcja do aktualizacji wykresu
def update_plot(x, y, color):
    lines.set_xdata(list(lines.get_xdata()) + [x])
    lines.set_ydata(list(lines.get_ydata()) + [y])
    lines.set_color(color)
    ax.relim()
    ax.autoscale_view(True, True, True)
    canvas.draw()


# Flagi i konfiguracja początkowa interfacu
running = False

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Simulation of charged particle in the magnetic field (Runge-Kutta Method)")

# Konfiguracja kolumn i wierszy dla lepszego dopasowania 
for i in range(10):  # Dla 10 kolumn
    root.grid_columnconfigure(i, weight=1)

for i in range(20):  # Dla 20 wierszy (podwójna liczba wierszy)
    root.grid_rowconfigure(i, weight=1)


# Tworzenie etykiet i pól wprowadzania dla parametrów
central_charge_label = tk.Label(root, text="Central Charge (e) - Q:")
central_charge_label.grid(row=0, column=1)
central_charge_entry = tk.Entry(root)
central_charge_entry.grid(row=0, column=2)

B_label = tk.Label(root, text="Magnetic Field (nT) - B:")
B_label.grid(row=1, column=1)
B_entry = tk.Entry(root)
B_entry.grid(row=1, column=2)

q_label = tk.Label(root, text="Particle's Charge (e) - q:")
q_label.grid(row=0, column=3)
q_entry = tk.Entry(root)
q_entry.grid(row=0, column=4)

m_label = tk.Label(root, text="Particle's mass (MeV/c^2) - m:")
m_label.grid(row=1, column=3)
m_entry = tk.Entry(root)
m_entry.grid(row=1, column=4)

vx_label = tk.Label(root, text="Initial Velocity X (m/s) - vx:")
vx_label.grid(row=0, column=5)
vx_entry = tk.Entry(root)
vx_entry.grid(row=0, column=6)

vy_label = tk.Label(root, text="Initial Velocity Y (m/s) - vy:")
vy_label.grid(row=1, column=5)
vy_entry = tk.Entry(root)
vy_entry.grid(row=1, column=6)

# Tworzenie obszaru wykresu z Matplotlib
fig, ax = plt.subplots(figsize=(4, 4)) #proba zmiany rozmiaru, bug tkinter?
lines, = ax.plot([], [], 'o', markersize=1)  # rozmiar punktow
ax.set_xlim(-1000, 1000)
ax.set_ylim(-1000, 1000)
ax.set_title("Trajectory of a charged particle")
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
plt.axis('equal')
ax.grid(True)


# Dodanie obszaru na tekst z wartościami początkowymi
initial_conditions_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top')


# Integracja z Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.grid(row=4, column=1, columnspan=7, rowspan=3, sticky="nsew")




# Tworzenie przycisków do sterowania symulacją
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.grid(row=0, column=7)


def stop_simulation():
    global running
    running = False  # Zatrzymanie symulacji

stop_button = tk.Button(root, text="Stop Simulation", command=stop_simulation)
stop_button.grid(row=1, column=7)


# Funkcja do zapisywania wykresu
def save_plot():
    folder_name = "plots"
    base_file_name = "particle_trajectory"  # Podstawowa nazwa pliku

    # tworzenie folderu i warunek
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # nienadpisywanie plikow
    existing_files = [f for f in os.listdir(folder_name) if f.startswith(base_file_name)]
    new_file_number = len(existing_files) + 1
    file_name = f"{base_file_name}_{new_file_number}.png"
    file_path = os.path.join(folder_name, file_name)

    # zapis wykresu
    try:
        fig.savefig(file_path)
        messagebox.showinfo("Success", f"Plot saved successfully in {file_path}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving plot: {e}")

save_button = tk.Button(root, text="Save Plot", command=save_plot)
save_button.grid(row=9, column=7)

#petla zdarzen
root.mainloop()