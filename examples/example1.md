<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson02/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>



# Problem 1, addition with WASM

## Problem statement

Create a bindings.c file with a function implementation: `int addIntegers(int a, int b);`
Compile this to WASM using the command `emcc bindings.c -o bindings.js`. Then, in a file `index.html` 
create a page that loads the resulting javascript and calls `addIntegers(5,3)` and displays the result on the webpage. 

## Hints

You may find it useful to use the following code (inside index.html). emscripten will populate the other methods of Module after loading `bindings.js`.

``` javascript
<span id='result'></span>
<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    document.getElementById('result').innerHTML = `5 + 3 = ${your code here}`;
}
</script>
<script src="bindings.js"></script>
```

## Solution.


bindings.c:
``` C
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int addIntegers(int a, int b) {
    return a + b;
}
```

index.html:

``` html
<html><body>
  <h2>Demo</h2>
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

## Demo
Result of addition: <span id="result">Calculating...</span>
<script>
var Module = {};
Module.onRuntimeInitialized = function() {
    document.getElementById('result').innerHTML = `5 + 3 = ${Module._addIntegers(5, 3)}`;
};
</script>
<script src="bindings.js"></script>
