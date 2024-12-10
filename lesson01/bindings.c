#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int addIntegers(int a, int b){
    return a+b;
}
