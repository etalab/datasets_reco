#pragma once

#include <node.h>
#include <v8.h>

#include "lzma.h"

/**
 * This low-level wrapper is unpleasant, and isn't meant to be used directly.
 * It just provides access to the raw stream engine in xz.
 */
class Engine : public Nan::ObjectWrap {
public:
  static void Init(v8::Local<v8::Object> exports);

private:
  explicit Engine(void);
  ~Engine();

  static NAN_METHOD(New);
  static NAN_METHOD(Close);
  static NAN_METHOD(Feed);
  static NAN_METHOD(Drain);

  static Nan::Persistent<v8::FunctionTemplate> constructor;

  static v8::Local<v8::Object> NewInstance(v8::Local<v8::Value> info);

  lzma_stream _stream;
  bool _active;
};
