/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace kernel_gen {
namespace tf_framework {
::llvm::StringRef stringifyErrorCode(ErrorCode val) {
  switch (val) {
    case ErrorCode::OK: return "OK";
    case ErrorCode::CANCELLED: return "CANCELLED";
    case ErrorCode::UNKNOWN: return "UNKNOWN";
    case ErrorCode::INVALID_ARGUMENT: return "INVALID_ARGUMENT";
    case ErrorCode::DEADLINE_EXCEEDED: return "DEADLINE_EXCEEDED";
    case ErrorCode::NOT_FOUND: return "NOT_FOUND";
    case ErrorCode::ALREADY_EXISTS: return "ALREADY_EXISTS";
    case ErrorCode::PERMISSION_DENIED: return "PERMISSION_DENIED";
    case ErrorCode::UNAUTHENTICATED: return "UNAUTHENTICATED";
    case ErrorCode::RESOURCE_EXHAUSTED: return "RESOURCE_EXHAUSTED";
    case ErrorCode::FAILED_PRECONDITION: return "FAILED_PRECONDITION";
    case ErrorCode::ABORTED: return "ABORTED";
    case ErrorCode::OUT_OF_RANGE: return "OUT_OF_RANGE";
    case ErrorCode::UNIMPLEMENTED: return "UNIMPLEMENTED";
    case ErrorCode::INTERNAL: return "INTERNAL";
    case ErrorCode::UNAVAILABLE: return "UNAVAILABLE";
    case ErrorCode::DATA_LOSS: return "DATA_LOSS";
  }
  return "";
}

::llvm::Optional<ErrorCode> symbolizeErrorCode(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ErrorCode>>(str)
      .Case("OK", ErrorCode::OK)
      .Case("CANCELLED", ErrorCode::CANCELLED)
      .Case("UNKNOWN", ErrorCode::UNKNOWN)
      .Case("INVALID_ARGUMENT", ErrorCode::INVALID_ARGUMENT)
      .Case("DEADLINE_EXCEEDED", ErrorCode::DEADLINE_EXCEEDED)
      .Case("NOT_FOUND", ErrorCode::NOT_FOUND)
      .Case("ALREADY_EXISTS", ErrorCode::ALREADY_EXISTS)
      .Case("PERMISSION_DENIED", ErrorCode::PERMISSION_DENIED)
      .Case("UNAUTHENTICATED", ErrorCode::UNAUTHENTICATED)
      .Case("RESOURCE_EXHAUSTED", ErrorCode::RESOURCE_EXHAUSTED)
      .Case("FAILED_PRECONDITION", ErrorCode::FAILED_PRECONDITION)
      .Case("ABORTED", ErrorCode::ABORTED)
      .Case("OUT_OF_RANGE", ErrorCode::OUT_OF_RANGE)
      .Case("UNIMPLEMENTED", ErrorCode::UNIMPLEMENTED)
      .Case("INTERNAL", ErrorCode::INTERNAL)
      .Case("UNAVAILABLE", ErrorCode::UNAVAILABLE)
      .Case("DATA_LOSS", ErrorCode::DATA_LOSS)
      .Default(::llvm::None);
}
::llvm::Optional<ErrorCode> symbolizeErrorCode(uint32_t value) {
  switch (value) {
  case 0: return ErrorCode::OK;
  case 1: return ErrorCode::CANCELLED;
  case 2: return ErrorCode::UNKNOWN;
  case 3: return ErrorCode::INVALID_ARGUMENT;
  case 4: return ErrorCode::DEADLINE_EXCEEDED;
  case 5: return ErrorCode::NOT_FOUND;
  case 6: return ErrorCode::ALREADY_EXISTS;
  case 7: return ErrorCode::PERMISSION_DENIED;
  case 16: return ErrorCode::UNAUTHENTICATED;
  case 8: return ErrorCode::RESOURCE_EXHAUSTED;
  case 9: return ErrorCode::FAILED_PRECONDITION;
  case 10: return ErrorCode::ABORTED;
  case 11: return ErrorCode::OUT_OF_RANGE;
  case 12: return ErrorCode::UNIMPLEMENTED;
  case 13: return ErrorCode::INTERNAL;
  case 14: return ErrorCode::UNAVAILABLE;
  case 15: return ErrorCode::DATA_LOSS;
  default: return ::llvm::None;
  }
}

bool ErrorCodeAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 0)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 3)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 4)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 5)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 6)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 7)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 16)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 8)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 9)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 10)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 11)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 12)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 13)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 14)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 15)));
}
ErrorCodeAttr ErrorCodeAttr::get(::mlir::MLIRContext *context, ErrorCode val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<ErrorCodeAttr>();
}
ErrorCode ErrorCodeAttr::getValue() const {
  return static_cast<ErrorCode>(::mlir::IntegerAttr::getInt());
}
} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir

