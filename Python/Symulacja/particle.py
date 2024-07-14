#Grzegorz Jędrzejowski 29.01.2024
import numpy as np

class Particle:
    def __init__(self, q, B, m, central_charge):
        self.central_charge = central_charge * 1.6e-19 #konwersja do SI
        self.q = q * 1.6e-19  # Konwersja ładunku do SI 
        self.B = B * 1e-9  # Konwersja pola magnetycznego do nanotesli
        self.m = m * 9.10938356e-31 / 0.511  # Konwersja masy do kilogramów (masa elektronu jako jednostka odniesienia)
        self.position = np.array([0.0, 0.0], dtype=np.longdouble)  # Inicjalizacja początkowej pozycji
        self.velocity = np.array([0.0, 0.0], dtype=np.longdouble)  # Inicjalizacja początkowej prędkości

    def set_initial_conditions(self, position, velocity):
        # warunki poczatkowe przed modyfikacja
        self.position = np.array(position, dtype=np.longdouble)
        self.velocity = np.array(velocity, dtype=np.longdouble)

    def calculate_lorentz_force(self):
        # sila lorentza
        force_x = self.q * self.velocity[1] * self.B
        force_y = -self.q * self.velocity[0] * self.B
        return np.array([force_x, force_y])


    def calculate_columb_force(self):
        
        distance = np.sqrt(self.position[0]**2 + self.position[1]**2)
        #b.mala odleglosc
        if distance < 1e-10:
            return np.zeros_like(self.position)

        #prawo columba
        force_magnitude = (8.987551787e9 * self.q * self.central_charge) / (distance ** 2)
       

        return force_magnitude 



    def runge_kutta_step(self, dt):
        def acceleration(velocity):
            lorentz_force = self.calculate_lorentz_force()
            columb_force = self.calculate_columb_force()
            total_force = lorentz_force + columb_force
            return total_force / self.m
            
            
        
        # Obliczenia kroków Rungego-Kutty
        k1_v = dt * acceleration(self.velocity)
        k1_x = dt * self.velocity

        k2_v = dt * acceleration(self.velocity + 0.5 * k1_v)
        k2_x = dt * (self.velocity + 0.5 * k1_v)

        k3_v = dt * acceleration(self.velocity + 0.5 * k2_v)
        k3_x = dt * (self.velocity + 0.5 * k2_v)

        k4_v = dt * acceleration(self.velocity + k3_v)
        k4_x = dt * (self.velocity + k3_v)

        # Aktualizacja prędkości i pozycji cząsteczki
        self.velocity += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6
        self.position += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6

    def get_position(self):
        # Zwraca aktualną pozycję cząsteczki
        return self.position