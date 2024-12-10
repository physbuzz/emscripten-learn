<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson12" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson14/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 13: Re-Compile with -O3

## Question

Recompile a prime sieve algorithm written in C using the `-O3` optimization flag in Emscripten. Measure the performance difference between the unoptimized and optimized versions when running in the browser. Observe how the `-O3` optimization affects the WebAssembly output and runtime performance.

**Learning Goals:**
- Understand the impact of compiler optimization flags, specifically `-O3`, on performance.
- Learn how Emscripten translates typical C optimizations into WebAssembly.
- Gain experience measuring and comparing performance in a browser environment.

## Hints

1. **Prime Sieve Algorithm**: Use the Sieve of Eratosthenes to find all prime numbers up to a given limit. If you don't already have a sieve implementation, you can use the one provided in the solution.
   
2. **Compilation**: Compile the C code twice:
   - Without optimization: `emcc sieve.c -o sieve.js`
   - With `-O3` optimization: `emcc sieve.c -O3 -o sieve_optimized.js`

3. **Measuring Performance**: Use JavaScript's `performance.now()` to measure the time taken to execute the sieve function in both versions.

4. **WebAssembly Functions**: Ensure the sieve function is exported by adding `EMSCRIPTEN_KEEPALIVE` to its declaration and using the `-s EXPORTED_FUNCTIONS` flag during compilation.

5. **Browser Setup**: Create an HTML file that loads both versions of the WebAssembly module and compares their execution times.

## Solution

### Step 1: Write the Prime Sieve in C

```c
// sieve.c
#include <emscripten/emscripten.h>
#include <stdlib.h>
#include <stdbool.h>

EMSCRIPTEN_KEEPALIVE
int* sieve(int limit, int* primeCount) {
    bool* isPrime = (bool*)malloc((limit + 1) * sizeof(bool));
    for (int i = 0; i <= limit; i++) {
        isPrime[i] = true;
    }

    isPrime[0] = isPrime[1] = false; // 0 and 1 are not prime numbers
    for (int i = 2; i * i <= limit; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                isPrime[j] = false;
            }
        }
    }

    // Count primes and store them in an array
    *primeCount = 0;
    for (int i = 2; i <= limit; i++) {
        if (isPrime[i]) {
            (*primeCount)++;
        }
    }

    int* primes = (int*)malloc((*primeCount) * sizeof(int));
    int index = 0;
    for (int i = 2; i <= limit; i++) {
        if (isPrime[i]) {
            primes[index++] = i;
        }
    }

    free(isPrime);
    return primes;
}
```

### Step 2: Compile the Code

Compile the code twice:

1. Without optimization:
   ```bash
   emcc sieve.c -s EXPORTED_FUNCTIONS="['_sieve', '_malloc', '_free']" -o sieve.js
   ```

2. With `-O3` optimization:
   ```bash
   emcc sieve.c -O3 -s EXPORTED_FUNCTIONS="['_sieve', '_malloc', '_free']" -o sieve_optimized.js
   ```

### Step 3: Create the HTML File

```html
<html>
  <body>
    <h2>Prime Sieve Performance Comparison</h2>
    <p>Limit: <span id="limit">100000</span></p>
    <p>Unoptimized Time: <span id="unoptimized-time">Calculating...</span> ms</p>
    <p>Optimized Time: <span id="optimized-time">Calculating...</span> ms</p>

    <script>
      const limit = 100000;

      function measurePerformance(modulePath, resultElementId) {
        return new Promise((resolve) => {
          const Module = {};
          Module.onRuntimeInitialized = function () {
            const start = performance.now();
            const ptr = Module._malloc(4); // Allocate memory for prime count
            Module._sieve(limit, ptr); // Run the sieve
            Module._free(ptr); // Free memory
            const end = performance.now();
            document.getElementById(resultElementId).innerText = (end - start).toFixed(2);
            resolve();
          };
          const script = document.createElement("script");
          script.src = modulePath;
          document.body.appendChild(script);
        });
      }

      async function runComparison() {
        await measurePerformance("sieve.js", "unoptimized-time");
        await measurePerformance("sieve_optimized.js", "optimized-time");
      }

      runComparison();
    </script>
  </body>
</html>
```

## Demo

Limit: <span id="limit">100000</span>  
Unoptimized Time: <span id="unoptimized-time">Calculating...</span> ms  
Optimized Time: <span id="optimized-time">Calculating...</span> ms  

<script>
  const limit = 100000;

  function measurePerformance(modulePath, resultElementId) {
    return new Promise((resolve) => {
      const Module = {};
      Module.onRuntimeInitialized = function () {
        const start = performance.now();
        const ptr = Module._malloc(4); // Allocate memory for prime count
        Module._sieve(limit, ptr); // Run the sieve
        Module._free(ptr); // Free memory
        const end = performance.now();
        document.getElementById(resultElementId).innerText = (end - start).toFixed(2);
        resolve();
      };
      const script = document.createElement("script");
      script.src = modulePath;
      document.body.appendChild(script);
    });
  }

  async function runComparison() {
    await measurePerformance("sieve.js", "unoptimized-time");
    await measurePerformance("sieve_optimized.js", "optimized-time");
  }

  runComparison();
</script>