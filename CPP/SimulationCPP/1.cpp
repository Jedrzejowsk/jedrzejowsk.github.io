#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

// Funkcja dla symulacji atraktora Lorenza
void simulateLorenz(double x0, double y0, double z0, double sigma, double rho, double beta, double dt, double tMax, std::vector<double>& x, std::vector<double>& y, std::vector<double>& z) {
    size_t numSteps = static_cast<size_t>(tMax / dt) + 1;
    x.resize(numSteps);
    y.resize(numSteps);
    z.resize(numSteps);

    double xTemp, yTemp, zTemp;
    x[0] = x0;
    y[0] = y0;
    z[0] = z0;

    for (size_t i = 1; i < numSteps; i++) {
        //układ Lorentza
        xTemp = x[i - 1] + sigma * (y[i - 1] - x[i - 1]) * dt;
        yTemp = y[i - 1] + (x[i - 1] * (rho - z[i - 1]) - y[i - 1]) * dt;
        zTemp = z[i - 1] + (x[i - 1] * y[i - 1] - beta * z[i - 1]) * dt;

        x[i] = xTemp;
        y[i] = yTemp;
        z[i] = zTemp;
    }
}

// Funkcja dla symulacji podwójnego wahadła
void simulateDoublePendulum(double theta1_0, double theta2_0, double omega1_0, double omega2_0, double L1, double L2, double g, double dt, double tMax, std::vector<double>& theta1, std::vector<double>& theta2) {
    size_t numSteps = static_cast<size_t>(tMax / dt) + 1;
    theta1.resize(numSteps);
    theta2.resize(numSteps);

    double theta1Temp, theta2Temp, omega1Temp, omega2Temp;
    theta1[0] = theta1_0;
    theta2[0] = theta2_0;

    for (size_t i = 1; i < numSteps; i++) {
        theta1Temp = theta1[i - 1] + omega1_0 * dt;
        theta2Temp = theta2[i - 1] + omega2_0 * dt;

        omega1Temp = omega1_0 - (g / L1) * std::sin(theta1Temp - theta2Temp) * dt;
        omega2Temp = omega2_0 - (g / L2) * std::sin(theta2Temp - theta1Temp) * dt;

        theta1[i] = theta1Temp;
        theta2[i] = theta2Temp;

        omega1_0 = omega1Temp;
        omega2_0 = omega2Temp;
    }
}

int main() {
    const double dt = 0.01;
    const double tMax = 5.0;

    // Symulacja atraktora Lorenza
    std::vector<double> x1, y1, z1;
    simulateLorenz(1.0, 0.0, 0.0, 10.0, 28.0, 8.0 / 3.0, dt, tMax, x1, y1, z1);
    std::ofstream lorenz1File("lorenz1.txt");
    for (size_t i = 0; i < x1.size(); i++) {
        lorenz1File << x1[i] << " " << y1[i] << " " << z1[i] << "\n";
    }
    lorenz1File.close();

    std::vector<double> x2, y2, z2;
    simulateLorenz(1.0, 0.0, 0.0, 10.0, 25.0, 8.0 / 3.0, dt, tMax, x2, y2, z2);
    std::ofstream lorenz2File("lorenz2.txt");
    for (size_t i = 0; i < x2.size(); i++) {
        lorenz2File << x2[i] << " " << y2[i] << " " << z2[i] << "\n";
    }
    lorenz2File.close();

    // Symulacja podwójnego wahadła
    std::vector<double> theta1, theta2, theta3, theta4;
    simulateDoublePendulum(0, 0.0, 1.0, 0.1, 1.0, 1.0, 9.81, 10*dt, 4*tMax, theta1, theta2);
    std::ofstream pendulum1File("pendulum1.txt");
    for (size_t i = 0; i < theta1.size(); i++) {
        pendulum1File << theta1[i] << " " << theta2[i] << "\n";
    }
    pendulum1File.close();


    simulateDoublePendulum(0.0, 0.0, 0.90, 0.0, 1.0, 1.0, 9.81, 10*dt, 4*tMax, theta3, theta4);
    std::ofstream pendulum3File("pendulum3.txt");

    for (size_t i = 0; i < theta3.size(); i++) {
        pendulum3File << theta3[i] << " " << theta4[i] << "\n";
    }
    pendulum3File.close();


    // Skrypt Gnuplot
    std::ofstream gnuplotScript("gnuplot_script.plt");
    gnuplotScript << "set term gif animate\n";
    gnuplotScript << "set output 'lorenz.gif'\n";
    gnuplotScript << "set view 60, 30, 1, 1\n";  // Ustawienie perspektywy widoku
    gnuplotScript << "set xrange [-30:30]\n";
    gnuplotScript << "set yrange [-30:30]\n";
    gnuplotScript << "set zrange [0:60]\n";
    gnuplotScript << "set size square\n";  // Ustawienie kwadratowych proporcji
    gnuplotScript << "do for [i=1:" << x1.size() << "] {\n";
    gnuplotScript << "    splot 'lorenz1.txt' every ::1::i using 1:2:3 with lines title 'Lorenz 1', ";
    gnuplotScript << "'lorenz2.txt' every ::1::i using 1:2:3 with lines title 'Lorenz 2'\n";
    gnuplotScript << "}\n";
    gnuplotScript.close();

    // Skrypt Gnuplot
    std::ofstream gnuplotScript2("gnuplot_script2.plt");
    gnuplotScript2 << "set term gif animate\n";
    gnuplotScript2 << "set output 'pendulum.gif'\n";
    gnuplotScript2 << "set xrange [0:5]\n";
    gnuplotScript2 << "set yrange [0:5]\n";
    gnuplotScript2 << "set size square\n";

    // Dodanie zmiennych przechowujących rozmiary wektorów
    gnuplotScript2 << "theta1_size = " << theta1.size() << "\n";
    gnuplotScript2 << "theta3_size = " << theta3.size() << "\n";

    gnuplotScript2 << "do for [i=1:theta1_size] {\n";
    gnuplotScript2 << "    plot 'pendulum1.txt' every ::1::i with lines title 'Pendulum 1' lc rgb 'blue', \\\n";
    gnuplotScript2 << "         'pendulum3.txt' every ::1::i with lines title 'Pendulum 2' lc rgb 'green', \\\n";
    gnuplotScript2 << "}\n";
    gnuplotScript2.close();

    // Wykonanie skryptu Gnuplot
    std::string gnuplotCommand = "gnuplot gnuplot_script.plt";
    std::system(gnuplotCommand.c_str());

    std::string gnuplotCommand2 = "gnuplot gnuplot_script2.plt";
    std::system(gnuplotCommand2.c_str());

    return 0;
}
