<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson15" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson17/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 16: FFT with an External Library

## Question

Use the KissFFT library to implement a function in C that performs a Fast Fourier Transform (FFT) on a time-domain signal passed from JavaScript. The function should return the frequency-domain data back to JavaScript. The goal is to integrate an external library, manage memory between C and JavaScript, and handle more advanced computational routines.

### Requirements:
1. Use KissFFT for the FFT computation.
2. Write a C function `void computeFFT(float* timeDomain, float* freqDomain, int length)` that takes a time-domain signal and outputs the frequency-domain data.
3. Pass a JavaScript array to the function, perform the FFT in C, and return the result back to JavaScript.

---

## Hints

1. **Installing KissFFT**:  
   Download the KissFFT library from its [GitHub repository](https://github.com/mborgerding/kissfft). Include the `kiss_fft.h` and `kiss_fft.c` files in your project directory.

2. **Compiling with KissFFT**:  
   Use the `-I` flag to include the KissFFT headers and link the library during compilation. For example:  
   ```bash
   emcc bindings.c kiss_fft.c -s EXPORTED_FUNCTIONS="['_computeFFT', '_malloc', '_free']" -o bindings.js
   ```

3. **Memory Management**:  
   - Allocate memory for the input and output arrays using `Module._malloc()` in JavaScript.  
   - Use `Module.HEAPF32` to transfer data between JavaScript and WebAssembly.  
   - Free the allocated memory using `Module._free()` after the computation is complete.

4. **Frequency-Domain Data**:  
   KissFFT outputs complex numbers in the frequency domain. You will need to handle the real and imaginary parts separately. Consider interleaving them in the output array (e.g., `[real1, imag1, real2, imag2, ...]`).

---

## Solution

### Step 1: C Code (`bindings.c`)
```c
#include <emscripten/emscripten.h>
#include "kiss_fft.h"

EMSCRIPTEN_KEEPALIVE
void computeFFT(float* timeDomain, float* freqDomain, int length) {
    // Allocate memory for KissFFT input and output
    kiss_fft_cpx* in = (kiss_fft_cpx*)malloc(sizeof(kiss_fft_cpx) * length);
    kiss_fft_cpx* out = (kiss_fft_cpx*)malloc(sizeof(kiss_fft_cpx) * length);

    // Initialize KissFFT configuration
    kiss_fft_cfg cfg = kiss_fft_alloc(length, 0, NULL, NULL);

    // Populate the input array (real part from timeDomain, imaginary part = 0)
    for (int i = 0; i < length; i++) {
        in[i].r = timeDomain[i];
        in[i].i = 0.0f;
    }

    // Perform the FFT
    kiss_fft(cfg, in, out);

    // Copy the output to freqDomain (interleaved real and imaginary parts)
    for (int i = 0; i < length; i++) {
        freqDomain[2 * i] = out[i].r;     // Real part
        freqDomain[2 * i + 1] = out[i].i; // Imaginary part
    }

    // Free allocated memory
    free(in);
    free(out);
    free(cfg);
}
```

---

### Step 2: HTML and JavaScript (`index.html`)
```html
<html>
  <body>
    <h2>FFT Demo</h2>
    <p>Frequency-domain data for the signal [1, 0, 0, 0, 0, 0, 0, 0]:</p>
    <p id="result">Calculating...</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function () {
        // Input time-domain signal
        const timeDomain = new Float32Array([1, 0, 0, 0, 0, 0, 0, 0]);
        const length = timeDomain.length;

        // Allocate memory for input and output arrays
        const timeDomainPtr = Module._malloc(length * 4); // 4 bytes per float
        const freqDomainPtr = Module._malloc(length * 2 * 4); // 2 floats (real + imag) per element

        // Copy time-domain data to WebAssembly memory
        Module.HEAPF32.set(timeDomain, timeDomainPtr >> 2);

        // Call the computeFFT function
        Module._computeFFT(timeDomainPtr, freqDomainPtr, length);

        // Retrieve the frequency-domain data
        const freqDomain = new Float32Array(Module.HEAPF32.buffer, freqDomainPtr, length * 2);

        // Display the result
        let resultText = "Frequency-domain data: ";
        for (let i = 0; i < length; i++) {
          resultText += `[${freqDomain[2 * i].toFixed(2)}, ${freqDomain[2 * i + 1].toFixed(2)}] `;
        }
        document.getElementById("result").innerText = resultText;

        // Free allocated memory
        Module._free(timeDomainPtr);
        Module._free(freqDomainPtr);
      };
    </script>
    <script src="bindings.js"></script>
  </body>
</html>
```

---

## Demo

Frequency-domain data for the signal [1, 0, 0, 0, 0, 0, 0, 0]:  
<span id="result">Calculating...</span>

<script>
  var Module = {};
  Module.onRuntimeInitialized = function () {
    const timeDomain = new Float32Array([1, 0, 0, 0, 0, 0, 0, 0]);
    const length = timeDomain.length;

    const timeDomainPtr = Module._malloc(length * 4);
    const freqDomainPtr = Module._malloc(length * 2 * 4);

    Module.HEAPF32.set(timeDomain, timeDomainPtr >> 2);

    Module._computeFFT(timeDomainPtr, freqDomainPtr, length);

    const freqDomain = new Float32Array(Module.HEAPF32.buffer, freqDomainPtr, length * 2);

    let resultText = "Frequency-domain data: ";
    for (let i = 0; i < length; i++) {
      resultText += `[${freqDomain[2 * i].toFixed(2)}, ${freqDomain[2 * i + 1].toFixed(2)}] `;
    }
    document.getElementById("result").innerText = resultText;

    Module._free(timeDomainPtr);
    Module._free(freqDomainPtr);
  };
</script>
<script src="bindings.js"></script>