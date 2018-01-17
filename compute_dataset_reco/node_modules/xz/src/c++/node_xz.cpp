#include <nan.h>

#include "lzma.h"

#include "engine.h"

void init(v8::Local<v8::Object> exports) {
  Engine::Init(exports);
}

NODE_MODULE(node_xz, init);
