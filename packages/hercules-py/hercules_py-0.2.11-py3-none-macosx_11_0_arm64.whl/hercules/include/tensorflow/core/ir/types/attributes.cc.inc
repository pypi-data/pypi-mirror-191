/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_LIST
#undef GET_ATTRDEF_LIST

::mlir::tf_type::FuncAttr,
::mlir::tf_type::PlaceholderAttr,
::mlir::tf_type::ShapeAttr,
::mlir::tf_type::VersionAttr

#endif  // GET_ATTRDEF_LIST

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES

static ::mlir::OptionalParseResult generatedAttributeParser(::mlir::AsmParser &parser, ::llvm::StringRef mnemonic, ::mlir::Type type, ::mlir::Attribute &value) {
  if (mnemonic == ::mlir::tf_type::FuncAttr::getMnemonic()) {
    value = ::mlir::tf_type::FuncAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::tf_type::PlaceholderAttr::getMnemonic()) {
    value = ::mlir::tf_type::PlaceholderAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::tf_type::ShapeAttr::getMnemonic()) {
    value = ::mlir::tf_type::ShapeAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::tf_type::VersionAttr::getMnemonic()) {
    value = ::mlir::tf_type::VersionAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  return {};
}

static ::mlir::LogicalResult generatedAttributePrinter(::mlir::Attribute def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Attribute, ::mlir::LogicalResult>(def)    .Case<::mlir::tf_type::FuncAttr>([&](auto t) {
      printer << ::mlir::tf_type::FuncAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::tf_type::PlaceholderAttr>([&](auto t) {
      printer << ::mlir::tf_type::PlaceholderAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::tf_type::ShapeAttr>([&](auto t) {
      printer << ::mlir::tf_type::ShapeAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::tf_type::VersionAttr>([&](auto t) {
      printer << ::mlir::tf_type::VersionAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace tf_type {
namespace detail {
struct FuncAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<SymbolRefAttr, DictionaryAttr>;
  FuncAttrStorage(SymbolRefAttr name, DictionaryAttr attrs) : ::mlir::AttributeStorage(), name(name), attrs(attrs) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (name == std::get<0>(tblgenKey)) && (attrs == std::get<1>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static FuncAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto name = std::get<0>(tblgenKey);
    auto attrs = std::get<1>(tblgenKey);
    return new (allocator.allocate<FuncAttrStorage>()) FuncAttrStorage(name, attrs);
  }

  SymbolRefAttr name;
  DictionaryAttr attrs;
};
} // namespace detail
FuncAttr FuncAttr::get(::mlir::MLIRContext *context, SymbolRefAttr name, DictionaryAttr attrs) {
  return Base::get(context, name, attrs);
}

FuncAttr FuncAttr::get(::mlir::MLIRContext *context, StringRef name, DictionaryAttr attr) {
  return Base::get(context, SymbolRefAttr::get(context, name), attr);
}

SymbolRefAttr FuncAttr::getName() const {
  return getImpl()->name;
}

DictionaryAttr FuncAttr::getAttrs() const {
  return getImpl()->attrs;
}

} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::FuncAttr)
namespace mlir {
namespace tf_type {
namespace detail {
struct PlaceholderAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::StringRef>;
  PlaceholderAttrStorage(::llvm::StringRef value) : ::mlir::AttributeStorage(), value(value) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static PlaceholderAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    value = allocator.copyInto(value);
    return new (allocator.allocate<PlaceholderAttrStorage>()) PlaceholderAttrStorage(value);
  }

  ::llvm::StringRef value;
};
} // namespace detail
PlaceholderAttr PlaceholderAttr::get(::mlir::MLIRContext *context, ::llvm::StringRef value) {
  return Base::get(context, value);
}

::llvm::StringRef PlaceholderAttr::getValue() const {
  return getImpl()->value;
}

} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::PlaceholderAttr)
namespace mlir {
namespace tf_type {
namespace detail {
struct ShapeAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, bool>;
  ShapeAttrStorage(::llvm::ArrayRef<int64_t> shape, bool unranked) : ::mlir::AttributeStorage(), shape(shape), unranked(unranked) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (shape == std::get<0>(tblgenKey)) && (unranked == std::get<1>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static ShapeAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto shape = std::get<0>(tblgenKey);
    auto unranked = std::get<1>(tblgenKey);
    shape = allocator.copyInto(shape);
    return new (allocator.allocate<ShapeAttrStorage>()) ShapeAttrStorage(shape, unranked);
  }

  ::llvm::ArrayRef<int64_t> shape;
  bool unranked;
};
} // namespace detail
ShapeAttr ShapeAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> shape, bool unranked) {
  return Base::get(context, shape, unranked);
}

::llvm::ArrayRef<int64_t> ShapeAttr::getShape() const {
  return getImpl()->shape;
}

bool ShapeAttr::getUnranked() const {
  return getImpl()->unranked;
}

} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::ShapeAttr)
namespace mlir {
namespace tf_type {
namespace detail {
struct VersionAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<int32_t, int32_t, ::llvm::ArrayRef<int32_t>>;
  VersionAttrStorage(int32_t producer, int32_t minConsumer, ::llvm::ArrayRef<int32_t> badConsumers) : ::mlir::AttributeStorage(), producer(producer), minConsumer(minConsumer), badConsumers(badConsumers) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (producer == std::get<0>(tblgenKey)) && (minConsumer == std::get<1>(tblgenKey)) && (badConsumers == std::get<2>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey));
  }

  static VersionAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto producer = std::get<0>(tblgenKey);
    auto minConsumer = std::get<1>(tblgenKey);
    auto badConsumers = std::get<2>(tblgenKey);
    badConsumers = allocator.copyInto(badConsumers);
    return new (allocator.allocate<VersionAttrStorage>()) VersionAttrStorage(producer, minConsumer, badConsumers);
  }

  int32_t producer;
  int32_t minConsumer;
  ::llvm::ArrayRef<int32_t> badConsumers;
};
} // namespace detail
VersionAttr VersionAttr::get(::mlir::MLIRContext *context, int32_t producer, int32_t minConsumer, ::llvm::ArrayRef<int32_t> badConsumers) {
  return Base::get(context, producer, minConsumer, badConsumers);
}

int32_t VersionAttr::getProducer() const {
  return getImpl()->producer;
}

int32_t VersionAttr::getMinConsumer() const {
  return getImpl()->minConsumer;
}

::llvm::ArrayRef<int32_t> VersionAttr::getBadConsumers() const {
  return getImpl()->badConsumers;
}

} // namespace tf_type
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_type::VersionAttr)

#endif  // GET_ATTRDEF_CLASSES

