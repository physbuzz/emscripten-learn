<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson18" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson20/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 19: Compute Pair Correlation Functions and FFT

## Question

Write a C function `void computeCorrelation(float* data, int length, float* output);` that computes the pair correlation function for a given dataset. Then, use an integrated FFT library (such as the one provided by Emscripten) to process the correlation data. Pass the processed results back to JavaScript for visualization. 

The task involves:
1. Computing the pair correlation function in C.
2. Applying an FFT to the correlation data using Emscripten's FFTW integration.
3. Returning the processed results to JavaScript for rendering.

## Hints

1. **Pair Correlation Function**: This function measures how particle density varies as a function of distance. For simplicity, assume the input data is a 1D array of particle positions.

2. **Using FFTW with Emscripten**:
   - Emscripten provides bindings for the FFTW library. You can use the `fftwf_plan_dft_r2c_1d` function for real-to-complex FFT.
   - Include the FFTW library during compilation with the `-s USE_FFTW=1` flag.

3. **Memory Management**:
   - Allocate memory for the input and output arrays using `Module._malloc()` in JavaScript.
   - Use `Module.HEAPF32` to transfer data between JavaScript and WebAssembly.

4. **Compilation Command**:
   Use the following command to compile your C code:
   ```bash
   emcc bindings.c -s USE_FFTW=1 -s EXPORTED_FUNCTIONS="['_computeCorrelation', '_malloc', '_free']" -o bindings.js
   ```

5. **JavaScript Integration**:
   - Use `Module.HEAPF32` to pass the input data to WebAssembly.
   - Retrieve the processed FFT results from the output array in WebAssembly.

## Solution

### bindings.c
```c
#include <emscripten/emscripten.h>
#include <fftw3.h>
#include <math.h>
#include <stdlib.h>

// Compute the pair correlation function
EMSCRIPTEN_KEEPALIVE
void computeCorrelation(float* data, int length, float* output) {
    // Initialize the output array to zero
    for (int i = 0; i < length; i++) {
        output[i] = 0.0f;
    }

    // Compute pair correlation function
    for (int i = 0; i < length; i++) {
        for (int j = i + 1; j < length; j++) {
            int distance = abs(i - j);
            output[distance] += 1.0f;
        }
    }

    // Normalize the correlation function
    for (int i = 0; i < length; i++) {
        output[i] /= length;
    }

    // Perform FFT on the correlation data
    fftwf_complex* fft_output = (fftwf_complex*)fftwf_malloc(sizeof(fftwf_complex) * (length / 2 + 1));
    fftwf_plan plan = fftwf_plan_dft_r2c_1d(length, output, fft_output, FFTW_ESTIMATE);

    fftwf_execute(plan);

    // Copy the FFT results back to the output array (real part only)
    for (int i = 0; i < length / 2 + 1; i++) {
        output[i] = sqrtf(fft_output[i][0] * fft_output[i][0] + fft_output[i][1] * fft_output[i][1]);
    }

    // Clean up
    fftwf_destroy_plan(plan);
    fftwf_free(fft_output);
}
```

### index.html
```html
<html>
  <body>
    <h2>Demo</h2>
    <p>FFT of Pair Correlation Function:</p>
    <p id="result">Calculating...</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Input data: particle positions (1D array)
        const data = new Float32Array([1.0, 2.0, 3.5, 5.0, 6.5, 8.0]);
        const length = data.length;

        // Allocate memory for input and output arrays
        const dataPtr = Module._malloc(data.length * 4);
        const outputPtr = Module._malloc(data.length * 4);

        // Copy input data to WebAssembly memory
        Module.HEAPF32.set(data, dataPtr >> 2);

        // Call the computeCorrelation function
        Module._computeCorrelation(dataPtr, length, outputPtr);

        // Retrieve the output data
        const output = new Float32Array(Module.HEAPF32.buffer, outputPtr, length);

        // Display the FFT results
        document.getElementById('result').innerHTML = `FFT Results: ${Array.from(output).slice(0, length / 2 + 1).join(', ')}`;

        // Free allocated memory
        Module._free(dataPtr);
        Module._free(outputPtr);
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

## Demo

FFT of Pair Correlation Function: <span id="result">Calculating...</span>
<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const data = new Float32Array([1.0, 2.0, 3.5, 5.0, 6.5, 8.0]);
    const length = data.length;

    const dataPtr = Module._malloc(data.length * 4);
    const outputPtr = Module._malloc(data.length * 4);

    Module.HEAPF32.set(data, dataPtr >> 2);

    Module._computeCorrelation(dataPtr, length, outputPtr);

    const output = new Float32Array(Module.HEAPF32.buffer, outputPtr, length);

    document.getElementById('result').innerHTML = `FFT Results: ${Array.from(output).slice(0, length / 2 + 1).join(', ')}`;

    Module._free(dataPtr);
    Module._free(outputPtr);
  };
</script>
<script src="bindings.js"></script>