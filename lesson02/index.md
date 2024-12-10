<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson01/" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson03/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 2: Averaging a Float32 Array

## Problem Statement

Inside `bindings.c`, write a function `float computeAverage(float* arr, int length)` computes the average of an array. Export this function to javascript using emscripten and compute the average of a javascript `Float32Array` using it. 

The intent of this problem is to use `Module.HEAPF32.set`, `_malloc`, and `_free`.

## Hints

1. You'll want to use the `emcc` argument `-s EXPORTED_FUNCTIONS="['_computeAverage', '_malloc', '_free']"`

2. Use `Module._malloc()` to allocate memory for the array in the WebAssembly heap. Remember to calculate the size of the memory block in bytes (e.g., `array.length * 4` for a `Float32Array`).

3. Use `Module.HEAPF32.set()` to copy the JavaScript `Float32Array` into the allocated memory. The pointer returned by `malloc` must be divided by 4 (since `HEAPF32` is a 32-bit view of the memory).

4. Remember to free the allocated memory using `Module._free()`

## Solution


* `bindings.c` has a simple implementation using `EMSCRIPTEN_KEEPALIVE`.

```c
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
float computeAverage(float* arr, int length) {
    float sum = 0;
    for (int i = 0; i < length; i++) {
        sum += arr[i];
    }
    return sum / length;
}
```

* Inside the javascript of `demo.html`, we have a bit more work to do. We again use `Module.onRuntimeInitialized`, but now we have to carefully construct and set the arrays.

``` html
<html><body>
  <p>Average of the array [1,2,3,4,5,6]:</p>
  <p id="result">Calculating...</p>

  <script>
    var Module={};
    Module.onRuntimeInitialized=function() {
        const numbers=new Float32Array([1,2,3,4,5,6]);
        const ptr=Module._malloc(numbers.length*4); // 4 bytes per float
        // >>2 divides by four to get the correct index.
        Module.HEAPF32.set(numbers,ptr>>2); 

        const result=Module._computeAverage(ptr,numbers.length);

        Module._free(ptr);
        document.getElementById('result').innerHTML = `Average = ${result}`;
    };
  </script>
  <script src="bindings.js"></script>
</body></html>
```

Compile the C code to WebAssembly using the following command:

```bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_computeAverage', '_malloc', '_free']" -o bindings.js
```


## Demo

Demo.html iframe:

<div style="background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 15px; margin: 15px 0;">
    <iframe 
        src="demo.html" 
        style="width: 100%; height: 200px; border: none; overflow: hidden;"
        title="WebAssembly Addition Demo"
    ></iframe>
</div>
