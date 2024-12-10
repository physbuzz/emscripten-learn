#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
float computeAverage(float* arr, int length) {
    float sum = 0;
    for (int i = 0; i < length; i++) {
        sum += arr[i];
    }
    return sum / length;
}
