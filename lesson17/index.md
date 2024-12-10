<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson16" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson18/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 17: Monte-Carlo Simulation with Periodic Boundaries

## Question

Implement a Monte-Carlo step in C that updates particle positions in a 2D box with periodic boundary conditions. The function should take an array of particle positions, the number of particles, the box size, and a maximum displacement (`delta`) as inputs. It should randomly displace each particle within the range `[-delta, delta]` and apply periodic boundary conditions to ensure particles remain inside the box. Use WebAssembly to expose this functionality to JavaScript, where you will visualize the updated particle positions.

## Hints

1. **Periodic Boundary Conditions**:  
   Use the modulo operator to ensure particles stay within the box. For example, if a particle's position exceeds the box size, wrap it around using:  
   ```c
   position = fmod(position + box_size, box_size);
   ```

2. **Random Number Generation**:  
   Use `rand()` in C to generate random displacements. Scale the random value to the range `[-delta, delta]` using:  
   ```c
   displacement = ((float)rand() / RAND_MAX) * 2 * delta - delta;
   ```

3. **Memory Management**:  
   Export `malloc` and `free` to allocate memory for the particle array in JavaScript. Use `Module.HEAPF32` to interact with the array in WebAssembly memory.

4. **Compilation**:  
   Compile the C code with:  
   ```bash
   emcc monte_carlo.c -s EXPORTED_FUNCTIONS="['_monteCarloStep', '_malloc', '_free']" -o monte_carlo.js
   ```

5. **Visualization**:  
   Use JavaScript to create a simple HTML canvas to display the particle positions.

## Solution

### C Code (`monte_carlo.c`)

```c
#include <emscripten/emscripten.h>
#include <stdlib.h>
#include <math.h>

// Function to perform a Monte-Carlo step with periodic boundary conditions
EMSCRIPTEN_KEEPALIVE
void monteCarloStep(float* positions, int num_particles, float box_size, float delta) {
    for (int i = 0; i < num_particles; i++) {
        // Random displacement in x and y directions
        float dx = ((float)rand() / RAND_MAX) * 2 * delta - delta;
        float dy = ((float)rand() / RAND_MAX) * 2 * delta - delta;

        // Update positions with periodic boundary conditions
        positions[2 * i] = fmod(positions[2 * i] + dx + box_size, box_size);
        positions[2 * i + 1] = fmod(positions[2 * i + 1] + dy + box_size, box_size);
    }
}
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>Monte-Carlo Simulation with Periodic Boundaries</h2>
    <canvas id="simulation" width="500" height="500" style="border:1px solid black;"></canvas>
    <p>Click the canvas to perform a Monte-Carlo step.</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        const canvas = document.getElementById("simulation");
        const ctx = canvas.getContext("2d");

        const boxSize = 100.0; // Box size in simulation units
        const delta = 5.0; // Maximum displacement
        const numParticles = 100; // Number of particles
        const scale = canvas.width / boxSize; // Scale for visualization

        // Initialize particle positions
        const positions = new Float32Array(numParticles * 2);
        for (let i = 0; i < numParticles; i++) {
          positions[2 * i] = Math.random() * boxSize;
          positions[2 * i + 1] = Math.random() * boxSize;
        }

        // Allocate memory in WebAssembly
        const ptr = Module._malloc(positions.length * 4);
        Module.HEAPF32.set(positions, ptr >> 2);

        // Function to draw particles
        function drawParticles() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.fillStyle = "blue";
          for (let i = 0; i < numParticles; i++) {
            const x = Module.HEAPF32[(ptr >> 2) + 2 * i] * scale;
            const y = Module.HEAPF32[(ptr >> 2) + 2 * i + 1] * scale;
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
          }
        }

        // Initial draw
        drawParticles();

        // Perform a Monte-Carlo step on click
        canvas.addEventListener("click", () => {
          Module._monteCarloStep(ptr, numParticles, boxSize, delta);
          drawParticles();
        });

        // Free memory when the page is unloaded
        window.addEventListener("unload", () => {
          Module._free(ptr);
        });
      };
    </script>
    <script src="monte_carlo.js"></script>
  </body>
</html>
```

## Demo

Click on the canvas below to perform a Monte-Carlo step. The particles will move randomly within the box, and their positions will wrap around due to periodic boundary conditions.

<canvas id="simulation" width="500" height="500" style="border:1px solid black;"></canvas>
<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const canvas = document.getElementById("simulation");
    const ctx = canvas.getContext("2d");

    const boxSize = 100.0;
    const delta = 5.0;
    const numParticles = 100;
    const scale = canvas.width / boxSize;

    const positions = new Float32Array(numParticles * 2);
    for (let i = 0; i < numParticles; i++) {
      positions[2 * i] = Math.random() * boxSize;
      positions[2 * i + 1] = Math.random() * boxSize;
    }

    const ptr = Module._malloc(positions.length * 4);
    Module.HEAPF32.set(positions, ptr >> 2);

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "blue";
      for (let i = 0; i < numParticles; i++) {
        const x = Module.HEAPF32[(ptr >> 2) + 2 * i] * scale;
        const y = Module.HEAPF32[(ptr >> 2) + 2 * i + 1] * scale;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      }
    }

    drawParticles();

    canvas.addEventListener("click", () => {
      Module._monteCarloStep(ptr, numParticles, boxSize, delta);
      drawParticles();
    });

    window.addEventListener("unload", () => {
      Module._free(ptr);
    });
  };
</script>
<script src="monte_carlo.js"></script>