<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson01" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson03/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>
# Problem 2: Returning a Floating-Point Average

## Problem Statement

Create a C function `float averageArray(float* arr, int length);` that returns the average of all elements passed in. Pass a javascript array to this function and display the result.

## Hints

To deal with variable sized arrays, make sure to add the argument `-s EXPORTED_FUNCTIONS="['_averageArray', '_malloc', '_free']"` to ensure that malloc and free are exported correctly. 

When constructing the array, use js's `Float32Array` to create a typed array.

Allocating memory can be done with `Module._malloc()` once malloc has been correctly exported.

Finally, setting memory can be accomplished with `Module.HEAPF32.set`.

## Solution

Compile `bindings.c` with `emcc bindings.c -s EXPORTED_FUNCTIONS="['_averageArray', '_malloc', '_free']" -o bindings.js`.


```C
// bindings.c
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
float averageArray(float* arr, int length) {
    float sum = 0;
    for(int i = 0; i < length; i++) {
        sum += arr[i];
    }
    return sum / length;
}
```

index.html:
```html
<html><body>
  <h2>Demo</h2>
  <p>Average of [1, 2, 3, 4, 5, 6]:</p>
  <p id="result">Calculating...</p>

  <script>
    var Module = {};
    Module.onRuntimeInitialized = function() {
        const numbers = new Float32Array([1, 2, 3, 4, 5, 6]);

        const ptr = Module._malloc(numbers.length * 4);
        Module.HEAPF32.set(numbers, ptr >> 2);
        const result = Module._averageArray(ptr, numbers.length);
        Module._free(ptr);

        document.getElementById('result').innerHTML = `Average = ${result}`;
    };
  </script>
  <script src="bindings.js"></script>
</body></html>
```

## Demo
Average of [1, 2, 3, 4, 5, 6]: <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    const numbers = new Float32Array([1, 2, 3, 4, 5, 6]);
    const ptr = Module._malloc(numbers.length * 4);
    Module.HEAPF32.set(numbers, ptr >> 2);
    const result = Module._averageArray(ptr, numbers.length);
    Module._free(ptr);
    document.getElementById('result').innerHTML = `Average = ${result}`;
};
</script>
<script src="bindings.js"></script>

