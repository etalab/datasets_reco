#include <node.h>
#include <node_buffer.h>
#include <nan.h>

#include "lzma.h"

#include "engine.h"

#define MODE_ENCODE 0
#define MODE_DECODE 1
#define ENCODE_FINISH 1

Nan::Persistent<v8::FunctionTemplate> Engine::constructor;

static lzma_stream blank_stream = LZMA_STREAM_INIT;

static const char *lzma_perror(lzma_ret err) {
  switch (err) {
    case LZMA_MEM_ERROR: return "Memory allocation failed";
    case LZMA_MEMLIMIT_ERROR: return "Memory usage limit reached";
    case LZMA_FORMAT_ERROR: return "File format not recognized";
    case LZMA_OPTIONS_ERROR: return "Compression options not supported";
    case LZMA_DATA_ERROR: return "Data is corrupt";
    case LZMA_BUF_ERROR: return "No progress is possible (internal error)";
    case LZMA_UNSUPPORTED_CHECK: return "Check type not supported";
    case LZMA_PROG_ERROR: return "Invalid arguments";
    default: return "?";
  }
}


Engine::Engine(void) : _active(false) {
  _stream = blank_stream;
}

Engine::~Engine() {
  if (_active) lzma_end(&_stream);
}

void Engine::Init(v8::Local<v8::Object> exports) {
  Nan::HandleScope scope;

  // constructor template
  v8::Local<v8::FunctionTemplate> ctor = Nan::New<v8::FunctionTemplate>(Engine::New);
  constructor.Reset(ctor);
  ctor->SetClassName(Nan::New<v8::String>("Engine").ToLocalChecked());
  ctor->InstanceTemplate()->SetInternalFieldCount(1);

  // prototype methods
  // v8::Local<v8::ObjectTemplate> proto = ctor->PrototypeTemplate();
  Nan::SetPrototypeMethod(ctor, "close", Engine::Close);
  Nan::SetPrototypeMethod(ctor, "feed", Engine::Feed);
  Nan::SetPrototypeMethod(ctor, "drain", Engine::Drain);

  exports->Set(Nan::New<v8::String>("Engine").ToLocalChecked(), ctor->GetFunction());
  exports->Set(Nan::New<v8::String>("MODE_ENCODE").ToLocalChecked(), Nan::New<v8::Integer>(MODE_ENCODE));
  exports->Set(Nan::New<v8::String>("MODE_DECODE").ToLocalChecked(), Nan::New<v8::Integer>(MODE_DECODE));
  exports->Set(Nan::New<v8::String>("ENCODE_FINISH").ToLocalChecked(), Nan::New<v8::Integer>(ENCODE_FINISH));
}

// new Engine(MODE_DECODE or MODE_ENCODE, [ preset ]);
// "preset" is the compression level (0 - 9)
NAN_METHOD(Engine::New) {
  Nan::HandleScope scope;

  if (!info.IsConstructCall()) {
    Nan::ThrowError("Must be called as constructor");
  }

  int mode = (info.Length() > 0) ? info[0]->IntegerValue() : 0;
  int preset = (info.Length() > 1) ? info[1]->IntegerValue() : 6;

  Engine *obj = new Engine();
  obj->Wrap(info.This());

  lzma_ret ret;
  if (mode == MODE_DECODE) {
    ret = lzma_stream_decoder(&obj->_stream, UINT64_MAX, 0);
  } else {
    ret = lzma_easy_encoder(&obj->_stream, preset, LZMA_CHECK_NONE);
  }
  if (ret != LZMA_OK) {
    delete obj;
    Nan::ThrowError(lzma_perror(ret));
  }

  obj->_active = true;
  info.GetReturnValue().Set(info.This());
}

NAN_METHOD(Engine::Close) {
  Nan::HandleScope scope;

  Engine *obj = Nan::ObjectWrap::Unwrap<Engine>(info.This());
  if (!obj->_active) Nan::ThrowError("Engine has already been closed");

  lzma_end(&obj->_stream);
  obj->_active = false;
  return;
}

// prep next "Drain" by setting up the input buffer.
// you may not let the buffer leave scope before draining!
NAN_METHOD(Engine::Feed) {
  Nan::HandleScope scope;

  Engine *obj = Nan::ObjectWrap::Unwrap<Engine>(info.This());
  if (!obj->_active) Nan::ThrowError("Engine has already been closed");

  if (info.Length() != 1) Nan::ThrowTypeError("Requires 1 argument: <buffer>");

  v8::Local<v8::Object> buffer = info[0]->ToObject();
  if (!node::Buffer::HasInstance(buffer)) Nan::ThrowTypeError("Argument must be a buffer");
  obj->_stream.next_in = (const uint8_t *) node::Buffer::Data(buffer);
  obj->_stream.avail_in = node::Buffer::Length(buffer);

  info.GetReturnValue().Set(Nan::New<v8::Integer>((int) obj->_stream.avail_in));
}

// run the encoder, filling as much of the buffer as possible, returning the amount used.
// negative value means you need to run it again.
// if "finished" is true, tell the encoder there will be no more data, and to wrap it up.
NAN_METHOD(Engine::Drain) {
  Nan::HandleScope scope;

  Engine *obj = Nan::ObjectWrap::Unwrap<Engine>(info.This());
  if (!obj->_active) Nan::ThrowError("Engine has already been closed");
  if (info.Length() < 1 || info.Length() > 2) Nan::ThrowTypeError("Requires 1 or 2 arguments: <buffer> [<flags>]");

  v8::Local<v8::Object> buffer = info[0]->ToObject();
  if (!node::Buffer::HasInstance(buffer)) Nan::ThrowTypeError("Argument must be a buffer");

  int flags = (info.Length() > 1) ? info[1]->IntegerValue() : 0;

  lzma_action action = (flags & ENCODE_FINISH) ? LZMA_FINISH : LZMA_RUN;

  obj->_stream.next_out = (uint8_t *) node::Buffer::Data(buffer);
  obj->_stream.avail_out = node::Buffer::Length(buffer);
  lzma_ret ret = lzma_code(&obj->_stream, action);
  if (ret != LZMA_OK && ret != LZMA_STREAM_END) Nan::ThrowError(lzma_perror(ret));

  int used = node::Buffer::Length(buffer) - obj->_stream.avail_out;
  if (obj->_stream.avail_in > 0 || (action == LZMA_FINISH && ret != LZMA_STREAM_END)) {
    // try more.
    info.GetReturnValue().Set(Nan::New<v8::Integer>(-used));
  } else {
    info.GetReturnValue().Set(Nan::New<v8::Integer>(used));
  }
}
