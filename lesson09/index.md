```html
<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson08/" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson10/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 9: Canvas Drawing from a Shared Memory Buffer

## Question

Create a C program that allocates a buffer in the Emscripten heap to represent particle positions. Continuously update the particle positions in C, and use JavaScript to render these positions on an HTML `<canvas>` element. The particles should move in a simple pattern, such as a circular motion. The goal is to demonstrate how to share memory between C and JavaScript for real-time rendering.

## Hints

1. **Memory Allocation**: Use `malloc` in C to allocate a buffer for particle positions. Export the buffer pointer so JavaScript can access it.
2. **Data Structure**: Store particle positions as an array of `float` values, where each particle has an `x` and `y` coordinate. For example, `[x1, y1, x2, y2, ...]`.
3. **Updating Positions**: In C, update the particle positions in a loop to simulate movement. Use a simple formula like circular motion:  
   `x = centerX + radius * cos(angle)`  
   `y = centerY + radius * sin(angle)`
4. **Accessing Memory in JS**: Use `Module.HEAPF32` to read the particle positions from the shared buffer.
5. **Rendering on Canvas**: Use the `<canvas>` API in JavaScript to draw the particles on the screen. Continuously update the canvas in sync with the C updates.

## Solution

### C Code (`bindings.c`)

```c
#include <emscripten/emscripten.h>
#include <math.h>
#include <stdlib.h>

#define NUM_PARTICLES 100
#define PI 3.14159265358979323846

float* particleBuffer;
float angle = 0.0f;

EMSCRIPTEN_KEEPALIVE
void initializeParticles() {
    particleBuffer = (float*)malloc(NUM_PARTICLES * 2 * sizeof(float));
    for (int i = 0; i < NUM_PARTICLES; i++) {
        particleBuffer[i * 2] = 0.0f;     // x-coordinate
        particleBuffer[i * 2 + 1] = 0.0f; // y-coordinate
    }
}

EMSCRIPTEN_KEEPALIVE
void updateParticles() {
    float centerX = 250.0f; // Canvas center
    float centerY = 250.0f;
    float radius = 100.0f;

    for (int i = 0; i < NUM_PARTICLES; i++) {
        float particleAngle = angle + (2 * PI * i / NUM_PARTICLES);
        particleBuffer[i * 2] = centerX + radius * cos(particleAngle);     // x-coordinate
        particleBuffer[i * 2 + 1] = centerY + radius * sin(particleAngle); // y-coordinate
    }

    angle += 0.01f; // Increment the angle for animation
}

EMSCRIPTEN_KEEPALIVE
float* getParticleBuffer() {
    return particleBuffer;
}

EMSCRIPTEN_KEEPALIVE
void freeParticles() {
    free(particleBuffer);
}
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>Canvas Drawing from Shared Memory Buffer</h2>
    <p>Particles moving in a circular pattern:</p>
    <canvas id="particleCanvas" width="500" height="500" style="border:1px solid black;"></canvas>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Initialize particles in C
        Module._initializeParticles();

        const canvas = document.getElementById("particleCanvas");
        const ctx = canvas.getContext("2d");

        const numParticles = 100;
        const particleBufferPtr = Module._getParticleBuffer();
        const particleBuffer = Module.HEAPF32.subarray(
          particleBufferPtr / 4,
          particleBufferPtr / 4 + numParticles * 2
        );

        function drawParticles() {
          // Update particles in C
          Module._updateParticles();

          // Clear the canvas
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Draw particles
          for (let i = 0; i < numParticles; i++) {
            const x = particleBuffer[i * 2];
            const y = particleBuffer[i * 2 + 1];

            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI); // Draw a small circle for each particle
            ctx.fillStyle = "blue";
            ctx.fill();
          }

          // Request the next frame
          requestAnimationFrame(drawParticles);
        }

        // Start the animation
        drawParticles();
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

### Compilation Command

Compile the C code to WebAssembly using the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_initializeParticles', '_updateParticles', '_getParticleBuffer', '_freeParticles']" -o bindings.js
```

## Demo

Particles moving in a circular pattern:  
<canvas id="particleCanvas" width="500" height="500" style="border:1px solid black;"></canvas>

<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    Module._initializeParticles();

    const canvas = document.getElementById("particleCanvas");
    const ctx = canvas.getContext("2d");

    const numParticles = 100;
    const particleBufferPtr = Module._getParticleBuffer();
    const particleBuffer = Module.HEAPF32.subarray(
      particleBufferPtr / 4,
      particleBufferPtr / 4 + numParticles * 2
    );

    function drawParticles() {
      Module._updateParticles();

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < numParticles; i++) {
        const x = particleBuffer[i * 2];
        const y = particleBuffer[i * 2 + 1];

        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "blue";
        ctx.fill();
      }

      requestAnimationFrame(drawParticles);
    }

    drawParticles();
  };
</script>
<script src="bindings.js"></script>
```