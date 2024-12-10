<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson11" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson13/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 12: Prime Sieve Benchmark (No Optimization)

## Question

Implement a simple Sieve of Eratosthenes in C to find all prime numbers up to a given limit. Then, measure the execution time of this function from JavaScript using `performance.now()`. Display the list of primes and the time taken on a webpage.

**Learning Goals:**
- Learn how to benchmark WebAssembly code running in the browser.
- Understand baseline performance before applying optimizations.

## Hints

1. **Sieve of Eratosthenes Algorithm**:  
   - Create an array of booleans representing numbers from 2 to `n`.
   - Mark multiples of each prime as non-prime.
   - Collect all indices still marked as prime.

2. **Exporting Functions**:  
   Use the `-s EXPORTED_FUNCTIONS="['_sieve', '_malloc', '_free']"` flag when compiling with `emcc` to ensure the C function and memory management functions are accessible in JavaScript.

3. **Measuring Time**:  
   Use `performance.now()` in JavaScript to measure the time before and after calling the WebAssembly function.

4. **Memory Management**:  
   Allocate memory for the result array using `Module._malloc()` and free it after use with `Module._free()`.

5. **Returning Results**:  
   Return the number of primes found and store the primes in a memory buffer that JavaScript can access.

## Solution

Compile the C code with the following command:  
```bash
emcc sieve.c -s EXPORTED_FUNCTIONS="['_sieve', '_malloc', '_free']" -o sieve.js
```

### sieve.c
```c
#include <emscripten/emscripten.h>
#include <stdlib.h>
#include <stdbool.h>

EMSCRIPTEN_KEEPALIVE
int sieve(int limit, int* primes) {
    bool* is_prime = (bool*)malloc((limit + 1) * sizeof(bool));
    if (!is_prime) return 0;

    // Initialize all numbers as prime
    for (int i = 0; i <= limit; i++) {
        is_prime[i] = true;
    }
    is_prime[0] = is_prime[1] = false; // 0 and 1 are not prime

    // Sieve of Eratosthenes
    for (int i = 2; i * i <= limit; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = false;
            }
        }
    }

    // Collect primes into the output array
    int count = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            primes[count++] = i;
        }
    }

    free(is_prime);
    return count; // Return the number of primes found
}
```

### index.html
```html
<html>
  <body>
    <h2>Prime Sieve Benchmark</h2>
    <p>Find all primes up to a given limit and measure execution time.</p>
    <label for="limit">Enter limit:</label>
    <input type="number" id="limit" value="1000000">
    <button onclick="runSieve()">Run Sieve</button>
    <p id="result">Result will appear here.</p>
    <p id="time">Execution time will appear here.</p>

    <script>
      var Module = {};
      Module.onRuntimeInitialized = function() {
        console.log("WebAssembly module loaded.");
      };

      function runSieve() {
        const limit = parseInt(document.getElementById('limit').value);
        if (isNaN(limit) || limit < 2) {
          document.getElementById('result').innerHTML = "Please enter a valid limit (>= 2).";
          return;
        }

        // Allocate memory for the result array
        const maxPrimes = limit; // Worst case: all numbers are prime
        const ptr = Module._malloc(maxPrimes * 4); // Allocate memory for an int array

        // Measure execution time
        const start = performance.now();
        const count = Module._sieve(limit, ptr); // Call the C function
        const end = performance.now();

        // Read the primes from the memory buffer
        const primes = [];
        const heap = new Int32Array(Module.HEAP32.buffer, ptr, count);
        for (let i = 0; i < count; i++) {
          primes.push(heap[i]);
        }

        // Free the allocated memory
        Module._free(ptr);

        // Display results
        document.getElementById('result').innerHTML = `Found ${count} primes. Example: ${primes.slice(0, 10).join(", ")}...`;
        document.getElementById('time').innerHTML = `Execution time: ${(end - start).toFixed(2)} ms`;
      }
    </script>
    <script src="sieve.js"></script>
  </body>
</html>
```

## Demo

Enter a limit and click "Run Sieve" to find all primes up to that limit and measure the execution time.

Example:  
- **Input**: Limit = 1,000,000  
- **Output**: Found 78498 primes. Example: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...  
- **Execution Time**: ~50 ms (varies by system/browser).