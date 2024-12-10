<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson02/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 1: Basic Integer Addition

## Problem Statement

Create a `bindings.c` file with a function `int addIntegers(int a, int b)`. Export this function to javascript using emscripten and call it using `Module._add`, displaying the result on the webpage.

## Hints

1. For the HTML webpage `demo.html`, you may find it useful to use the following template. Emscripten will populate the other methods of Module after loading `bindings.js`.

``` html
<span id='result'></span>
<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    document.getElementById('result').innerHTML = `5 + 3 = ${your code here}`;
}
</script>
<script src="bindings.js"></script>
```

2. To compile your C code, use `emcc bindings.c -s EXPORTED_FUNCTIONS="['_addIntegers']" -o add.js`

## Solution

* In the file `bindings.c`, we use the `EMSCRIPTEN_KEEPALIVE` macro to ensure our function isn't optimized away by the compiler.

``` c
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int addIntegers(int a, int b){
    return a+b;
}
```

* demo.html:
``` html
<html><body>
  <p>Result of addition:</p>
  <p id="result">Calculating...</p>

  <script>
    var Module = {};
    Module.onRuntimeInitialized = function() {
        document.getElementById('result').innerHTML = `5 + 3 = ${Module._addIntegers(5, 3)}`;
    };
  </script>
  <script src="bindings.js"></script>
</body></html>
```

* index.html will load the file bindings.js, which we compile via 

``` bash
emcc bindings.c -s EXPORTED_FUNCTIONS="['_addIntegers']" -o bindings.js
```

* The easiest way to run the code locally is to run a Python server, for example by running `python -m http.server` and then navigating to `http://0.0.0.0:8000/demo.html`.

## Demo

Demo.html iframe:

<div style="background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 15px; margin: 15px 0;">
    <iframe 
        src="demo.html" 
        style="width: 100%; height: 200px; border: none; overflow: hidden;"
        title="WebAssembly Addition Demo"
    ></iframe>
</div>

