/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* TypeDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_TYPEDEF_LIST
#undef GET_TYPEDEF_LIST

::mlir::tf_type::ControlType,
::mlir::tf_type::OpaqueTensorType

#endif  // GET_TYPEDEF_LIST

#ifdef GET_TYPEDEF_CLASSES
#undef GET_TYPEDEF_CLASSES

static ::mlir::OptionalParseResult generatedTypeParser(::mlir::AsmParser &parser, ::llvm::StringRef mnemonic, ::mlir::Type &value) {
  if (mnemonic == ::mlir::tf_type::ControlType::getMnemonic()) {
    value = ::mlir::tf_type::ControlType::get(parser.getContext());
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::tf_type::OpaqueTensorType::getMnemonic()) {
    value = ::mlir::tf_type::OpaqueTensorType::get(parser.getContext());
    return ::mlir::success(!!value);
  }
  return {};
}

static ::mlir::LogicalResult generatedTypePrinter(::mlir::Type def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Type, ::mlir::LogicalResult>(def)    .Case<::mlir::tf_type::ControlType>([&](auto t) {
      printer << ::mlir::tf_type::ControlType::getMnemonic();
      return ::mlir::success();
    })
    .Case<::mlir::tf_type::OpaqueTensorType>([&](auto t) {
      printer << ::mlir::tf_type::OpaqueTensorType::getMnemonic();
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace tf_type {
} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::ControlType)
namespace mlir {
namespace tf_type {
} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::OpaqueTensorType)

#endif  // GET_TYPEDEF_CLASSES

