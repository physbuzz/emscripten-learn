<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson13" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson15/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 14: O(N²) Distance Calculation and Flags

## Question

Write a C function `float calculateDistances(float* points, int numPoints, float* results);` that computes the pairwise Euclidean distances between a set of 2D points. The input array `points` contains `numPoints` pairs of floats (x, y coordinates), and the output array `results` should store the distances in a flattened format. For example, if there are 3 points, the results array will contain 9 values (distance matrix).

Compile the code to WebAssembly using Emscripten, experimenting with flags like `-O3` and `-s WASM=1`. Compare the runtime and memory usage for different optimization levels.

## Hints

1. **Understanding the Input and Output**:
   - The `points` array is a flattened array of 2D coordinates: `[x1, y1, x2, y2, ..., xn, yn]`.
   - The `results` array will store the pairwise distances in a flattened format. For example, for 3 points:
     ```
     results[0] = distance(points[0], points[0])
     results[1] = distance(points[0], points[1])
     results[2] = distance(points[0], points[2])
     ...
     ```

2. **Memory Management**:
   - Use `Module._malloc()` to allocate memory for the input and output arrays in JavaScript.
   - Use `Module.HEAPF32` to set and retrieve data from the allocated memory.

3. **Compilation Flags**:
   - Use `-O3` for maximum optimization.
   - Use `-s WASM=1` to ensure WebAssembly output.
   - Use `-s EXPORTED_FUNCTIONS="['_calculateDistances', '_malloc', '_free']"` to export the required functions.

4. **Performance Observation**:
   - Measure runtime using `console.time()` and `console.timeEnd()` in JavaScript.
   - Use browser developer tools to monitor memory usage.

## Solution

### C Code (`bindings.c`)

```c
#include <emscripten/emscripten.h>
#include <math.h>

// Function to calculate pairwise distances
EMSCRIPTEN_KEEPALIVE
void calculateDistances(float* points, int numPoints, float* results) {
    for (int i = 0; i < numPoints; i++) {
        for (int j = 0; j < numPoints; j++) {
            float dx = points[2 * i] - points[2 * j];
            float dy = points[2 * i + 1] - points[2 * j + 1];
            results[i * numPoints + j] = sqrt(dx * dx + dy * dy);
        }
    }
}
```

### Compilation Command

```bash
emcc bindings.c -O3 -s WASM=1 -s EXPORTED_FUNCTIONS="['_calculateDistances', '_malloc', '_free']" -o bindings.js
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Pairwise distances for points [(0, 0), (3, 4), (6, 8)]:</p>
    <pre id="result">Calculating...</pre>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Define points as a flattened array: [(0, 0), (3, 4), (6, 8)]
        const points = new Float32Array([0, 0, 3, 4, 6, 8]);
        const numPoints = points.length / 2;

        // Allocate memory for input and output arrays
        const pointsPtr = Module._malloc(points.length * 4);
        const resultsPtr = Module._malloc(numPoints * numPoints * 4);

        // Copy points data to WebAssembly memory
        Module.HEAPF32.set(points, pointsPtr >> 2);

        // Call the WebAssembly function
        console.time("Distance Calculation");
        Module._calculateDistances(pointsPtr, numPoints, resultsPtr);
        console.timeEnd("Distance Calculation");

        // Retrieve results from WebAssembly memory
        const results = new Float32Array(numPoints * numPoints);
        results.set(Module.HEAPF32.subarray(resultsPtr >> 2, (resultsPtr >> 2) + numPoints * numPoints));

        // Free allocated memory
        Module._free(pointsPtr);
        Module._free(resultsPtr);

        // Display the results
        let output = "";
        for (let i = 0; i < numPoints; i++) {
          output += results.slice(i * numPoints, (i + 1) * numPoints).join(", ") + "\n";
        }
        document.getElementById("result").textContent = output;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

## Demo

Pairwise distances for points `[(0, 0), (3, 4), (6, 8)]`:

<pre id="result">Calculating...</pre>
<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const points = new Float32Array([0, 0, 3, 4, 6, 8]);
    const numPoints = points.length / 2;

    const pointsPtr = Module._malloc(points.length * 4);
    const resultsPtr = Module._malloc(numPoints * numPoints * 4);

    Module.HEAPF32.set(points, pointsPtr >> 2);

    console.time("Distance Calculation");
    Module._calculateDistances(pointsPtr, numPoints, resultsPtr);
    console.timeEnd("Distance Calculation");

    const results = new Float32Array(numPoints * numPoints);
    results.set(Module.HEAPF32.subarray(resultsPtr >> 2, (resultsPtr >> 2) + numPoints * numPoints));

    Module._free(pointsPtr);
    Module._free(resultsPtr);

    let output = "";
    for (let i = 0; i < numPoints; i++) {
      output += results.slice(i * numPoints, (i + 1) * numPoints).join(", ") + "\n";
    }
    document.getElementById("result").textContent = output;
  };
</script>
<script src="bindings.js"></script>