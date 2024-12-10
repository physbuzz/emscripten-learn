<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson19/" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson21/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 20: Final Visualization and Analysis Page

## Question

Create a complete browser-based scientific workflow that integrates the following features:
1. **Real-time simulation**: Run a simulation in WebAssembly and control it via browser inputs.
2. **State management**: Save and load simulation states using MEMFS (Emscripten's in-memory file system).
3. **FFT-based analysis**: Perform a Fast Fourier Transform (FFT) on simulation data using an external library (e.g., FFTW or a JavaScript-based FFT library).
4. **Visualization**: Display simulation results and FFT analysis on an HTML5 canvas chart.
5. **Performance comparison**: Compare the performance of the simulation with and without optimization flags (`-O0` vs. `-O3`).

The final solution should demonstrate mastery of Emscripten features, memory management, and browser interactivity.

## Hints

1. **Real-time simulation**:
   - Use a simple simulation, such as a sine wave generator or a particle system.
   - Use `setInterval` or `requestAnimationFrame` in JavaScript to update the simulation in real-time.

2. **State management**:
   - Use Emscripten's MEMFS to save and load simulation states.
   - Use `FS.writeFile` and `FS.readFile` to interact with MEMFS.

3. **FFT-based analysis**:
   - Use an external FFT library. For simplicity, you can use a JavaScript-based library like [fft.js](https://github.com/dntj/jsfft) or compile a C-based FFT library with Emscripten.
   - Pass simulation data to the FFT function and display the frequency spectrum.

4. **Visualization**:
   - Use the HTML5 `<canvas>` element to draw charts.
   - Libraries like [Chart.js](https://www.chartjs.org/) can simplify the process.

5. **Performance comparison**:
   - Compile the simulation with `-O0` (no optimization) and `-O3` (maximum optimization).
   - Measure execution time using `performance.now()` in JavaScript.

## Solution

### Step 1: Simulation Code (`simulation.c`)

```c
#include <emscripten/emscripten.h>
#include <math.h>
#include <stdlib.h>

#define BUFFER_SIZE 1024

float simulation_data[BUFFER_SIZE];
int current_step = 0;

// Simple sine wave simulation
EMSCRIPTEN_KEEPALIVE
void run_simulation_step(float frequency, float amplitude) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        simulation_data[i] = amplitude * sinf(2.0f * M_PI * frequency * (current_step + i) / BUFFER_SIZE);
    }
    current_step += BUFFER_SIZE;
}

// Save simulation state to MEMFS
EMSCRIPTEN_KEEPALIVE
void save_state(const char* filename) {
    FILE* file = fopen(filename, "wb");
    fwrite(simulation_data, sizeof(float), BUFFER_SIZE, file);
    fclose(file);
}

// Load simulation state from MEMFS
EMSCRIPTEN_KEEPALIVE
void load_state(const char* filename) {
    FILE* file = fopen(filename, "rb");
    fread(simulation_data, sizeof(float), BUFFER_SIZE, file);
    fclose(file);
}

// Get simulation data pointer
EMSCRIPTEN_KEEPALIVE
float* get_simulation_data() {
    return simulation_data;
}
```

### Step 2: Compile the Simulation Code

Compile the simulation code with and without optimization:

```bash
emcc simulation.c -s EXPORTED_FUNCTIONS="['_run_simulation_step', '_save_state', '_load_state', '_get_simulation_data']" -o simulation.js
emcc simulation.c -O3 -s EXPORTED_FUNCTIONS="['_run_simulation_step', '_save_state', '_load_state', '_get_simulation_data']" -o simulation_optimized.js
```

### Step 3: HTML and JavaScript (`index.html`)

```html
<html>
<head>
    <title>Final Visualization and Analysis</title>
    <script src="simulation.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Final Visualization and Analysis</h1>
    <div>
        <label>Frequency: <input type="number" id="frequency" value="1" step="0.1"></label>
        <label>Amplitude: <input type="number" id="amplitude" value="1" step="0.1"></label>
        <button onclick="runSimulation()">Run Simulation</button>
        <button onclick="saveState()">Save State</button>
        <button onclick="loadState()">Load State</button>
    </div>
    <canvas id="simulationChart" width="800" height="400"></canvas>
    <canvas id="fftChart" width="800" height="400"></canvas>
    <p id="performance">Performance: <span id="executionTime">N/A</span> ms</p>

    <script>
        var Module = {};
        Module.onRuntimeInitialized = function() {
            console.log("WASM Module Loaded");
        };

        const BUFFER_SIZE = 1024;

        function runSimulation() {
            const frequency = parseFloat(document.getElementById('frequency').value);
            const amplitude = parseFloat(document.getElementById('amplitude').value);

            const start = performance.now();
            Module._run_simulation_step(frequency, amplitude);
            const end = performance.now();

            const executionTime = end - start;
            document.getElementById('executionTime').innerText = executionTime.toFixed(2);

            const dataPtr = Module._get_simulation_data();
            const simulationData = new Float32Array(Module.HEAPF32.buffer, dataPtr, BUFFER_SIZE);

            updateChart(simulationChart, simulationData);
            performFFT(simulationData);
        }

        function saveState() {
            Module._save_state("/state.bin");
            alert("State saved to MEMFS.");
        }

        function loadState() {
            Module._load_state("/state.bin");
            alert("State loaded from MEMFS.");
        }

        function performFFT(data) {
            const fft = new FFT(data.length);
            const spectrum = fft.forward(data);
            updateChart(fftChart, spectrum.map(Math.abs));
        }

        function updateChart(chart, data) {
            chart.data.datasets[0].data = data;
            chart.update();
        }

        const simulationChart = new Chart(document.getElementById('simulationChart'), {
            type: 'line',
            data: {
                labels: Array.from({ length: BUFFER_SIZE }, (_, i) => i),
                datasets: [{ label: 'Simulation Data', data: [], borderColor: 'blue', fill: false }]
            },
            options: { responsive: true }
        });

        const fftChart = new Chart(document.getElementById('fftChart'), {
            type: 'line',
            data: {
                labels: Array.from({ length: BUFFER_SIZE }, (_, i) => i),
                datasets: [{ label: 'FFT Spectrum', data: [], borderColor: 'red', fill: false }]
            },
            options: { responsive: true }
        });
    </script>
</body>
</html>
```

## Demo

1. Open `index.html` in a browser.
2. Adjust the frequency and amplitude, then click "Run Simulation" to see the sine wave and its FFT spectrum.
3. Save the simulation state, reload the page, and load the state to restore the data.
4. Compare performance by switching between `simulation.js` (unoptimized) and `simulation_optimized.js` (optimized). Observe the execution time in the "Performance" section.