<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson09" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson11/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 10: Using MEMFS to Store/Load Data

## Question

Write a C program that uses Emscripten's in-memory filesystem (MEMFS) to save and load simulation state data. Specifically:

1. Implement a function `void saveState(const char* filename, float* positions, int length);` that writes an array of positions to a file.
2. Implement a function `void loadState(const char* filename, float* positions, int length);` that reads the positions back into the array.
3. From JavaScript, trigger the save and load operations, and verify that the data is restored correctly.

**Learning Goals:**
- Learn how to use Emscripten's MEMFS for file I/O.
- Understand how to interact with the virtual filesystem from both C and JavaScript.

## Hints

1. Emscripten provides a virtual filesystem called MEMFS, which allows you to simulate file I/O in memory. By default, MEMFS is enabled.
2. Use standard C file I/O functions like `fopen`, `fwrite`, and `fread` to interact with MEMFS.
3. To compile the C code, use the `-s EXPORTED_FUNCTIONS="['_saveState', '_loadState']"` flag to export the functions for JavaScript usage.
4. In JavaScript, you can verify the saved and loaded data by comparing the original and restored arrays.
5. Use `Module.HEAPF32` to pass arrays between JavaScript and WebAssembly.

## Solution

### C Code (`bindings.c`)

```c
#include <stdio.h>
#include <emscripten/emscripten.h>

// Save the positions array to a file
EMSCRIPTEN_KEEPALIVE
void saveState(const char* filename, float* positions, int length) {
    FILE* file = fopen(filename, "wb");
    if (file == NULL) {
        printf("Error: Could not open file for writing\n");
        return;
    }
    fwrite(positions, sizeof(float), length, file);
    fclose(file);
    printf("State saved to %s\n", filename);
}

// Load the positions array from a file
EMSCRIPTEN_KEEPALIVE
void loadState(const char* filename, float* positions, int length) {
    FILE* file = fopen(filename, "rb");
    if (file == NULL) {
        printf("Error: Could not open file for reading\n");
        return;
    }
    fread(positions, sizeof(float), length, file);
    fclose(file);
    printf("State loaded from %s\n", filename);
}
```

### Compilation Command

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_saveState', '_loadState', '_malloc', '_free']" -o bindings.js
```

### HTML and JavaScript (`index.html`)

```html
<html>
  <body>
    <h2>Demo</h2>
    <p>Saving and Loading Simulation State:</p>
    <p id="result">Status: Waiting...</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        const positions = new Float32Array([1.0, 2.0, 3.0, 4.0, 5.0]);
        const length = positions.length;

        // Allocate memory for the positions array
        const ptr = Module._malloc(length * 4);
        Module.HEAPF32.set(positions, ptr >> 2);

        // Save the state to a file
        const filename = "state.bin";
        Module._saveState(filename, ptr, length);

        // Modify the array to simulate a state change
        for (let i = 0; i < positions.length; i++) {
          Module.HEAPF32[(ptr >> 2) + i] = 0.0;
        }

        // Load the state back from the file
        Module._loadState(filename, ptr, length);

        // Read the restored data
        const restoredPositions = new Float32Array(
          Module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + length)
        );

        // Free the allocated memory
        Module._free(ptr);

        // Display the result
        document.getElementById("result").innerHTML =
          `Restored Positions: [${restoredPositions.join(", ")}]`;
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

## Demo

Saving and Loading Simulation State:  
<span id="result">Status: Waiting...</span>

<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const positions = new Float32Array([1.0, 2.0, 3.0, 4.0, 5.0]);
    const length = positions.length;

    // Allocate memory for the positions array
    const ptr = Module._malloc(length * 4);
    Module.HEAPF32.set(positions, ptr >> 2);

    // Save the state to a file
    const filename = "state.bin";
    Module._saveState(filename, ptr, length);

    // Modify the array to simulate a state change
    for (let i = 0; i < positions.length; i++) {
      Module.HEAPF32[(ptr >> 2) + i] = 0.0;
    }

    // Load the state back from the file
    Module._loadState(filename, ptr, length);

    // Read the restored data
    const restoredPositions = new Float32Array(
      Module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + length)
    );

    // Free the allocated memory
    Module._free(ptr);

    // Display the result
    document.getElementById("result").innerHTML =
      `Restored Positions: [${restoredPositions.join(", ")}]`;
  };
</script>
<script src="bindings.js"></script>