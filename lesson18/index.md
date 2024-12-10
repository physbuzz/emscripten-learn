<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson17" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson19/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 18: NPT Ensemble Control from JS

## Question

Create a C simulation engine that exposes functions to dynamically set parameters like temperature, density, and pressure from JavaScript. These parameters should influence the simulation's behavior. Write a simple HTML interface to allow the user to input these values, run the simulation, and observe the system's evolution.

The goal is to connect user input from JavaScript to the C simulation engine and demonstrate how to manage dynamic parameter updates in a WebAssembly-based application.

## Hints

1. **C Functions to Expose**:  
   Create three functions in C to set temperature, density, and pressure:
   - `void setTemperature(float temp);`
   - `void setDensity(float density);`
   - `void setPressure(float pressure);`

   Additionally, create a function to run the simulation:
   - `void runSimulation();`

2. **Exporting Functions**:  
   Use the `-s EXPORTED_FUNCTIONS="['_setTemperature', '_setDensity', '_setPressure', '_runSimulation']"` flag when compiling with `emcc` to ensure these functions are accessible from JavaScript.

3. **JavaScript Integration**:  
   Use `Module._functionName()` to call the exported C functions from JavaScript. For example, `Module._setTemperature(300)` sets the temperature to 300.

4. **HTML Interface**:  
   Create an HTML form with input fields for temperature, density, and pressure, and a button to run the simulation. Use JavaScript to read the input values and call the corresponding C functions.

5. **Simulation Output**:  
   For simplicity, simulate the system's evolution by printing a message (e.g., "Simulation running with T=300, D=1.0, P=101.3") to the webpage.

## Solution

### C Code (`simulation.c`)

```c
#include <emscripten/emscripten.h>
#include <stdio.h>

// Global variables for simulation parameters
float temperature = 300.0; // Default temperature
float density = 1.0;       // Default density
float pressure = 101.3;    // Default pressure

// Function to set temperature
EMSCRIPTEN_KEEPALIVE
void setTemperature(float temp) {
    temperature = temp;
    printf("Temperature set to: %.2f\n", temperature);
}

// Function to set density
EMSCRIPTEN_KEEPALIVE
void setDensity(float dens) {
    density = dens;
    printf("Density set to: %.2f\n", density);
}

// Function to set pressure
EMSCRIPTEN_KEEPALIVE
void setPressure(float press) {
    pressure = press;
    printf("Pressure set to: %.2f\n", pressure);
}

// Function to run the simulation
EMSCRIPTEN_KEEPALIVE
void runSimulation() {
    printf("Running simulation with T=%.2f, D=%.2f, P=%.2f\n", temperature, density, pressure);
}
```

### Compilation Command

```bash
emcc simulation.c -s EXPORTED_FUNCTIONS="['_setTemperature', '_setDensity', '_setPressure', '_runSimulation']" -o simulation.js
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>NPT Ensemble Simulation</h2>
    <p>Set the simulation parameters and run the simulation:</p>

    <form id="simulationForm">
      <label for="temperature">Temperature (K):</label>
      <input type="number" id="temperature" value="300" step="0.1"><br><br>

      <label for="density">Density (g/cm³):</label>
      <input type="number" id="density" value="1.0" step="0.1"><br><br>

      <label for="pressure">Pressure (kPa):</label>
      <input type="number" id="pressure" value="101.3" step="0.1"><br><br>

      <button type="button" onclick="runSimulation()">Run Simulation</button>
    </form>

    <h3>Simulation Output:</h3>
    <pre id="output">Waiting for input...</pre>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function() {
        console.log("WebAssembly module loaded.");
      };

      function runSimulation() {
        // Get input values
        const temp = parseFloat(document.getElementById("temperature").value);
        const dens = parseFloat(document.getElementById("density").value);
        const press = parseFloat(document.getElementById("pressure").value);

        // Set parameters in the simulation
        Module._setTemperature(temp);
        Module._setDensity(dens);
        Module._setPressure(press);

        // Run the simulation
        Module._runSimulation();

        // Display output
        document.getElementById("output").innerText = `Simulation running with T=${temp}, D=${dens}, P=${press}`;
      }
    </script>

    <script src="simulation.js"></script>
  </body>
</html>
```

## Demo

### Example Usage:

1. Open the webpage in a browser.
2. Enter values for temperature, density, and pressure in the input fields.
3. Click the "Run Simulation" button.
4. Observe the output below the form, which displays the simulation parameters and confirms the simulation is running.

### Output Example:

```
Simulation running with T=300, D=1.0, P=101.3
```