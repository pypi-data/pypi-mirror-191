/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::kernel_gen::tf_framework::IsValidMemRefOp,
::mlir::kernel_gen::tf_framework::JITCompileFromStrOp,
::mlir::kernel_gen::tf_framework::JITCompileOp,
::mlir::kernel_gen::tf_framework::JITCompileYieldOp,
::mlir::kernel_gen::tf_framework::JITExecuteOp,
::mlir::kernel_gen::tf_framework::NullContextOp,
::mlir::kernel_gen::tf_framework::NullMemRefOp,
::mlir::kernel_gen::tf_framework::ReportErrorOp,
::mlir::kernel_gen::tf_framework::TFAllocOp,
::mlir::kernel_gen::tf_framework::TFAssertOp,
::mlir::kernel_gen::tf_framework::TFDeallocOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::MemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be memref of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isSignlessInteger(1)))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be 1-bit signless integer, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops2(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::kernel_gen::tf_framework::OpKernelContextType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be op_kernel_construction, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops3(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::kernel_gen::tf_framework::JITCallableType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be , but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops4(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((((type.isa<::mlir::UnrankedMemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType()))) || (((type.isa<::mlir::MemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType())))) || (((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be unranked.memref of any type values or memref of any type values or tensor of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops5(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((type.isa<::mlir::UnrankedMemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType()))) || (((type.isa<::mlir::MemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType()))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be unranked.memref of any type values or memref of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_framework_ops6(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::IndexType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be index, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::StringAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: string attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(attr.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); })))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 64-bit integer array attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 64-bit signless integer attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops3(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::BoolAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: bool attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops4(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: error code";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops5(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(attr.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); })))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit integer array attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_framework_ops6(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit signless integer attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_region_constraint_tf_framework_ops0(
    ::mlir::Operation *op, ::mlir::Region &region, ::llvm::StringRef regionName,
    unsigned regionIndex) {
  if (!((::llvm::hasNItems(region, 1)))) {
    return op->emitOpError("region #") << regionIndex
        << (regionName.empty() ? " " : " ('" + regionName + "') ")
        << "failed to verify constraint: region with 1 blocks";
  }
  return ::mlir::success();
}
} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::IsValidMemRefOp definitions
//===----------------------------------------------------------------------===//

IsValidMemRefOpAdaptor::IsValidMemRefOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

IsValidMemRefOpAdaptor::IsValidMemRefOpAdaptor(IsValidMemRefOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange IsValidMemRefOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> IsValidMemRefOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange IsValidMemRefOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value IsValidMemRefOpAdaptor::arg() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr IsValidMemRefOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult IsValidMemRefOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> IsValidMemRefOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range IsValidMemRefOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value IsValidMemRefOp::arg() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange IsValidMemRefOp::argMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> IsValidMemRefOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range IsValidMemRefOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value IsValidMemRefOp::result() {
  return *getODSResults(0).begin();
}

void IsValidMemRefOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value arg) {
  odsState.addOperands(arg);
  odsState.addTypes(result);
}

void IsValidMemRefOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value arg) {
  odsState.addOperands(arg);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void IsValidMemRefOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult IsValidMemRefOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops1(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<IsValidMemRefOp>(*this);
}

::mlir::ParseResult IsValidMemRefOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType argRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> argOperands(argRawOperands);  ::llvm::SMLoc argOperandsLoc;
  (void)argOperandsLoc;
  ::mlir::Type argRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> argTypes(argRawTypes);
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);
  if (parser.parseLParen())
    return ::mlir::failure();

  argOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(argRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseRParen())
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::MemRefType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    argRawTypes[0] = type;
  }
  if (parser.parseArrow())
    return ::mlir::failure();

  {
    ::mlir::IntegerType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  if (parser.resolveOperands(argOperands, argTypes, argOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void IsValidMemRefOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << "(";
  _odsPrinter << arg();
  _odsPrinter << ")";
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = arg().getType();
    if (auto validType = type.dyn_cast<::mlir::MemRefType>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::IntegerType>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::IsValidMemRefOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::JITCompileFromStrOp definitions
//===----------------------------------------------------------------------===//

JITCompileFromStrOpAdaptor::JITCompileFromStrOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

JITCompileFromStrOpAdaptor::JITCompileFromStrOpAdaptor(JITCompileFromStrOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange JITCompileFromStrOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> JITCompileFromStrOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange JITCompileFromStrOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileFromStrOpAdaptor::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::DictionaryAttr JITCompileFromStrOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr JITCompileFromStrOpAdaptor::code() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("code").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::ArrayAttr JITCompileFromStrOpAdaptor::tileSizes() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("tileSizes").cast<::mlir::ArrayAttr>();
  return attr;
}

::mlir::ArrayAttr JITCompileFromStrOpAdaptor::unrollFactors() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("unrollFactors").cast<::mlir::ArrayAttr>();
  return attr;
}

::mlir::IntegerAttr JITCompileFromStrOpAdaptor::maxSupportedRank() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::IntegerAttr attr = odsAttrs.get("maxSupportedRank").cast<::mlir::IntegerAttr>();
  return attr;
}

::mlir::BoolAttr JITCompileFromStrOpAdaptor::enableFtz() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::BoolAttr attr = odsAttrs.get("enableFtz").cast<::mlir::BoolAttr>();
  return attr;
}

::mlir::BoolAttr JITCompileFromStrOpAdaptor::cpuCodegen() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::BoolAttr attr = odsAttrs.get("cpuCodegen").cast<::mlir::BoolAttr>();
  return attr;
}

::mlir::LogicalResult JITCompileFromStrOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_code = odsAttrs.get("code");
    if (!tblgen_code)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'code'");

    if (tblgen_code && !((tblgen_code.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'code' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_tileSizes = odsAttrs.get("tileSizes");
    if (!tblgen_tileSizes)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'tileSizes'");

    if (tblgen_tileSizes && !(((tblgen_tileSizes.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_tileSizes.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'tileSizes' failed to satisfy constraint: 64-bit integer array attribute");
  }
  {
    auto tblgen_unrollFactors = odsAttrs.get("unrollFactors");
    if (!tblgen_unrollFactors)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'unrollFactors'");

    if (tblgen_unrollFactors && !(((tblgen_unrollFactors.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_unrollFactors.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'unrollFactors' failed to satisfy constraint: 64-bit integer array attribute");
  }
  {
    auto tblgen_maxSupportedRank = odsAttrs.get("maxSupportedRank");
    if (!tblgen_maxSupportedRank)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'maxSupportedRank'");

    if (tblgen_maxSupportedRank && !(((tblgen_maxSupportedRank.isa<::mlir::IntegerAttr>())) && ((tblgen_maxSupportedRank.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'maxSupportedRank' failed to satisfy constraint: 64-bit signless integer attribute");
  }
  {
    auto tblgen_enableFtz = odsAttrs.get("enableFtz");
    if (!tblgen_enableFtz)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'enableFtz'");

    if (tblgen_enableFtz && !((tblgen_enableFtz.isa<::mlir::BoolAttr>())))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'enableFtz' failed to satisfy constraint: bool attribute");
  }
  {
    auto tblgen_cpuCodegen = odsAttrs.get("cpuCodegen");
    if (!tblgen_cpuCodegen)
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""requires attribute 'cpuCodegen'");

    if (tblgen_cpuCodegen && !((tblgen_cpuCodegen.isa<::mlir::BoolAttr>())))
      return emitError(loc, "'tf_framework.jit_compile_from_str' op ""attribute 'cpuCodegen' failed to satisfy constraint: bool attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> JITCompileFromStrOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range JITCompileFromStrOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileFromStrOp::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::MutableOperandRange JITCompileFromStrOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> JITCompileFromStrOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range JITCompileFromStrOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileFromStrOp::result() {
  return *getODSResults(0).begin();
}

::mlir::StringAttr JITCompileFromStrOp::codeAttr() {
  return (*this)->getAttr(codeAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef JITCompileFromStrOp::code() {
  auto attr = codeAttr();
  return attr.getValue();
}

::mlir::ArrayAttr JITCompileFromStrOp::tileSizesAttr() {
  return (*this)->getAttr(tileSizesAttrName()).cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr JITCompileFromStrOp::tileSizes() {
  auto attr = tileSizesAttr();
  return attr;
}

::mlir::ArrayAttr JITCompileFromStrOp::unrollFactorsAttr() {
  return (*this)->getAttr(unrollFactorsAttrName()).cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr JITCompileFromStrOp::unrollFactors() {
  auto attr = unrollFactorsAttr();
  return attr;
}

::mlir::IntegerAttr JITCompileFromStrOp::maxSupportedRankAttr() {
  return (*this)->getAttr(maxSupportedRankAttrName()).cast<::mlir::IntegerAttr>();
}

uint64_t JITCompileFromStrOp::maxSupportedRank() {
  auto attr = maxSupportedRankAttr();
  return attr.getValue().getZExtValue();
}

::mlir::BoolAttr JITCompileFromStrOp::enableFtzAttr() {
  return (*this)->getAttr(enableFtzAttrName()).cast<::mlir::BoolAttr>();
}

bool JITCompileFromStrOp::enableFtz() {
  auto attr = enableFtzAttr();
  return attr.getValue();
}

::mlir::BoolAttr JITCompileFromStrOp::cpuCodegenAttr() {
  return (*this)->getAttr(cpuCodegenAttrName()).cast<::mlir::BoolAttr>();
}

bool JITCompileFromStrOp::cpuCodegen() {
  auto attr = cpuCodegenAttr();
  return attr.getValue();
}

void JITCompileFromStrOp::codeAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(codeAttrName(), attr);
}

void JITCompileFromStrOp::tileSizesAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(tileSizesAttrName(), attr);
}

void JITCompileFromStrOp::unrollFactorsAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(unrollFactorsAttrName(), attr);
}

void JITCompileFromStrOp::maxSupportedRankAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(maxSupportedRankAttrName(), attr);
}

void JITCompileFromStrOp::enableFtzAttr(::mlir::BoolAttr attr) {
  (*this)->setAttr(enableFtzAttrName(), attr);
}

void JITCompileFromStrOp::cpuCodegenAttr(::mlir::BoolAttr attr) {
  (*this)->setAttr(cpuCodegenAttrName(), attr);
}

void JITCompileFromStrOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, /*optional*/::mlir::Value ctx, ::mlir::StringAttr code, ::mlir::ArrayAttr tileSizes, ::mlir::ArrayAttr unrollFactors, ::mlir::IntegerAttr maxSupportedRank, ::mlir::BoolAttr enableFtz, ::mlir::BoolAttr cpuCodegen) {
  if (ctx)
    odsState.addOperands(ctx);
  odsState.addAttribute(codeAttrName(odsState.name), code);
  odsState.addAttribute(tileSizesAttrName(odsState.name), tileSizes);
  odsState.addAttribute(unrollFactorsAttrName(odsState.name), unrollFactors);
  odsState.addAttribute(maxSupportedRankAttrName(odsState.name), maxSupportedRank);
  odsState.addAttribute(enableFtzAttrName(odsState.name), enableFtz);
  odsState.addAttribute(cpuCodegenAttrName(odsState.name), cpuCodegen);
  odsState.addTypes(result);
}

void JITCompileFromStrOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value ctx, ::mlir::StringAttr code, ::mlir::ArrayAttr tileSizes, ::mlir::ArrayAttr unrollFactors, ::mlir::IntegerAttr maxSupportedRank, ::mlir::BoolAttr enableFtz, ::mlir::BoolAttr cpuCodegen) {
  if (ctx)
    odsState.addOperands(ctx);
  odsState.addAttribute(codeAttrName(odsState.name), code);
  odsState.addAttribute(tileSizesAttrName(odsState.name), tileSizes);
  odsState.addAttribute(unrollFactorsAttrName(odsState.name), unrollFactors);
  odsState.addAttribute(maxSupportedRankAttrName(odsState.name), maxSupportedRank);
  odsState.addAttribute(enableFtzAttrName(odsState.name), enableFtz);
  odsState.addAttribute(cpuCodegenAttrName(odsState.name), cpuCodegen);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void JITCompileFromStrOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, /*optional*/::mlir::Value ctx, ::llvm::StringRef code, ::mlir::ArrayAttr tileSizes, ::mlir::ArrayAttr unrollFactors, uint64_t maxSupportedRank, bool enableFtz, bool cpuCodegen) {
  if (ctx)
    odsState.addOperands(ctx);
  odsState.addAttribute(codeAttrName(odsState.name), odsBuilder.getStringAttr(code));
  odsState.addAttribute(tileSizesAttrName(odsState.name), tileSizes);
  odsState.addAttribute(unrollFactorsAttrName(odsState.name), unrollFactors);
  odsState.addAttribute(maxSupportedRankAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), maxSupportedRank));
  odsState.addAttribute(enableFtzAttrName(odsState.name), odsBuilder.getBoolAttr(enableFtz));
  odsState.addAttribute(cpuCodegenAttrName(odsState.name), odsBuilder.getBoolAttr(cpuCodegen));
  odsState.addTypes(result);
}

void JITCompileFromStrOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value ctx, ::llvm::StringRef code, ::mlir::ArrayAttr tileSizes, ::mlir::ArrayAttr unrollFactors, uint64_t maxSupportedRank, bool enableFtz, bool cpuCodegen) {
  if (ctx)
    odsState.addOperands(ctx);
  odsState.addAttribute(codeAttrName(odsState.name), odsBuilder.getStringAttr(code));
  odsState.addAttribute(tileSizesAttrName(odsState.name), tileSizes);
  odsState.addAttribute(unrollFactorsAttrName(odsState.name), unrollFactors);
  odsState.addAttribute(maxSupportedRankAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), maxSupportedRank));
  odsState.addAttribute(enableFtzAttrName(odsState.name), odsBuilder.getBoolAttr(enableFtz));
  odsState.addAttribute(cpuCodegenAttrName(odsState.name), odsBuilder.getBoolAttr(cpuCodegen));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void JITCompileFromStrOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult JITCompileFromStrOp::verify() {
  {
    auto tblgen_code = (*this)->getAttr(codeAttrName());
    if (!tblgen_code)
      return emitOpError("requires attribute 'code'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops0(*this, tblgen_code, "code")))
      return ::mlir::failure();
  }
  {
    auto tblgen_tileSizes = (*this)->getAttr(tileSizesAttrName());
    if (!tblgen_tileSizes)
      return emitOpError("requires attribute 'tileSizes'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops1(*this, tblgen_tileSizes, "tileSizes")))
      return ::mlir::failure();
  }
  {
    auto tblgen_unrollFactors = (*this)->getAttr(unrollFactorsAttrName());
    if (!tblgen_unrollFactors)
      return emitOpError("requires attribute 'unrollFactors'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops1(*this, tblgen_unrollFactors, "unrollFactors")))
      return ::mlir::failure();
  }
  {
    auto tblgen_maxSupportedRank = (*this)->getAttr(maxSupportedRankAttrName());
    if (!tblgen_maxSupportedRank)
      return emitOpError("requires attribute 'maxSupportedRank'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops2(*this, tblgen_maxSupportedRank, "maxSupportedRank")))
      return ::mlir::failure();
  }
  {
    auto tblgen_enableFtz = (*this)->getAttr(enableFtzAttrName());
    if (!tblgen_enableFtz)
      return emitOpError("requires attribute 'enableFtz'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops3(*this, tblgen_enableFtz, "enableFtz")))
      return ::mlir::failure();
  }
  {
    auto tblgen_cpuCodegen = (*this)->getAttr(cpuCodegenAttrName());
    if (!tblgen_cpuCodegen)
      return emitOpError("requires attribute 'cpuCodegen'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops3(*this, tblgen_cpuCodegen, "cpuCodegen")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    if (valueGroup0.size() > 1) {
      return emitOpError("operand group starting at #") << index
          << " requires 0 or 1 element, but found " << valueGroup0.size();
    }

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops3(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<JITCompileFromStrOp>(*this);
}

::mlir::ParseResult JITCompileFromStrOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> ctxOperands;
  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::StringAttr codeAttr;

  {
    ctxOperandsLoc = parser.getCurrentLocation();
    ::mlir::OpAsmParser::OperandType operand;
    ::mlir::OptionalParseResult parseResult =
                                    parser.parseOptionalOperand(operand);
    if (parseResult.hasValue()) {
      if (failed(*parseResult))
        return ::mlir::failure();
      ctxOperands.push_back(operand);
    }
  }
  if (!ctxOperands.empty()) {
  if (parser.parseComma())
    return ::mlir::failure();
  }

  if (parser.parseCustomAttributeWithFallback(codeAttr, parser.getBuilder().getType<::mlir::NoneType>(), "code",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::JITCallableType>();
  ::mlir::Type odsBuildableType1 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  result.addTypes(odsBuildableType0);
  if (parser.resolveOperands(ctxOperands, odsBuildableType1, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void JITCompileFromStrOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  if (ctx()) {
  _odsPrinter << ' ';
  if (::mlir::Value value = ctx())
    _odsPrinter << value;
  _odsPrinter << ",";
  }
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(codeAttr());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"code"});
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::JITCompileFromStrOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::JITCompileOp definitions
//===----------------------------------------------------------------------===//

JITCompileOpAdaptor::JITCompileOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

JITCompileOpAdaptor::JITCompileOpAdaptor(JITCompileOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange JITCompileOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> JITCompileOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange JITCompileOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileOpAdaptor::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::DictionaryAttr JITCompileOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::RegionRange JITCompileOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &JITCompileOpAdaptor::body() {
  return *odsRegions[0];
}

::mlir::LogicalResult JITCompileOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> JITCompileOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range JITCompileOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileOp::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::MutableOperandRange JITCompileOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> JITCompileOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range JITCompileOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileOp::result() {
  return *getODSResults(0).begin();
}

::mlir::Region &JITCompileOp::body() {
  return (*this)->getRegion(0);
}

void JITCompileOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, /*optional*/::mlir::Value ctx) {
  if (ctx)
    odsState.addOperands(ctx);
  (void)odsState.addRegion();
  odsState.addTypes(result);
}

void JITCompileOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value ctx) {
  if (ctx)
    odsState.addOperands(ctx);
  (void)odsState.addRegion();
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void JITCompileOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult JITCompileOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    if (valueGroup0.size() > 1) {
      return emitOpError("operand group starting at #") << index
          << " requires 0 or 1 element, but found " << valueGroup0.size();
    }

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops3(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_tf_framework_ops0(*this, region, "body", index++)))
        return ::mlir::failure();
  }
  return Verify<JITCompileOp>(*this);
}

::mlir::ParseResult JITCompileOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> ctxOperands;
  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  std::unique_ptr<::mlir::Region> bodyRegion = std::make_unique<::mlir::Region>();

  {
    ctxOperandsLoc = parser.getCurrentLocation();
    ::mlir::OpAsmParser::OperandType operand;
    ::mlir::OptionalParseResult parseResult =
                                    parser.parseOptionalOperand(operand);
    if (parseResult.hasValue()) {
      if (failed(*parseResult))
        return ::mlir::failure();
      ctxOperands.push_back(operand);
    }
  }

  if (parser.parseRegion(*bodyRegion))
    return ::mlir::failure();

  if (bodyRegion->empty()) bodyRegion->emplaceBlock();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  result.addRegion(std::move(bodyRegion));
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::JITCallableType>();
  ::mlir::Type odsBuildableType1 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  result.addTypes(odsBuildableType0);
  if (parser.resolveOperands(ctxOperands, odsBuildableType1, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void JITCompileOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  if (::mlir::Value value = ctx())
    _odsPrinter << value;
  _odsPrinter << ' ';
  _odsPrinter.printRegion(body());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::JITCompileOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::JITCompileYieldOp definitions
//===----------------------------------------------------------------------===//

JITCompileYieldOpAdaptor::JITCompileYieldOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

JITCompileYieldOpAdaptor::JITCompileYieldOpAdaptor(JITCompileYieldOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange JITCompileYieldOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> JITCompileYieldOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange JITCompileYieldOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileYieldOpAdaptor::result() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr JITCompileYieldOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult JITCompileYieldOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> JITCompileYieldOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range JITCompileYieldOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITCompileYieldOp::result() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange JITCompileYieldOp::resultMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> JITCompileYieldOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range JITCompileYieldOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void JITCompileYieldOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value result) {
  odsState.addOperands(result);
}

void JITCompileYieldOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value result) {
  odsState.addOperands(result);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void JITCompileYieldOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult JITCompileYieldOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<JITCompileYieldOp>(*this);
}

::mlir::ParseResult JITCompileYieldOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType resultRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> resultOperands(resultRawOperands);  ::llvm::SMLoc resultOperandsLoc;
  (void)resultOperandsLoc;
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  resultOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(resultRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  if (parser.resolveOperands(resultOperands, resultTypes, resultOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void JITCompileYieldOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << result();
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void JITCompileYieldOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::JITCompileYieldOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::JITExecuteOp definitions
//===----------------------------------------------------------------------===//

JITExecuteOpAdaptor::JITExecuteOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

JITExecuteOpAdaptor::JITExecuteOpAdaptor(JITExecuteOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange JITExecuteOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> JITExecuteOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  assert(odsAttrs && "missing segment size attribute for op");
  auto sizeAttr = odsAttrs.get("operand_segment_sizes").cast<::mlir::DenseIntElementsAttr>();

  const uint32_t *sizeAttrValueIt = &*sizeAttr.value_begin<uint32_t>();
  if (sizeAttr.isSplat())
    return {*sizeAttrValueIt * index, *sizeAttrValueIt};

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttrValueIt[i];
  return {start, sizeAttrValueIt[index]};
}

::mlir::ValueRange JITExecuteOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITExecuteOpAdaptor::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::Value JITExecuteOpAdaptor::callable() {
  return *getODSOperands(1).begin();
}

::mlir::ValueRange JITExecuteOpAdaptor::operands() {
  return getODSOperands(2);
}

::mlir::DictionaryAttr JITExecuteOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult JITExecuteOpAdaptor::verify(::mlir::Location loc) {
  {
    auto sizeAttr = odsAttrs.get("operand_segment_sizes").dyn_cast<::mlir::DenseIntElementsAttr>();
    if (!sizeAttr)
      return emitError(loc, "'tf_framework.jit_execute' op ""missing segment sizes attribute 'operand_segment_sizes'");
    auto numElements =
        sizeAttr.getType().cast<::mlir::ShapedType>().getNumElements();
    if (numElements != 3)
      return emitError(loc, "'tf_framework.jit_execute' op ""'operand_segment_sizes' attribute for specifying operand segments must have 3 "
                "elements, but got ") << numElements;
  }
    return ::mlir::success();
}

std::pair<unsigned, unsigned> JITExecuteOp::getODSOperandIndexAndLength(unsigned index) {
  auto sizeAttr =
      (*this)->getAttr(operand_segment_sizesAttrName()).cast<::mlir::DenseIntElementsAttr>();

  const uint32_t *sizeAttrValueIt = &*sizeAttr.value_begin<uint32_t>();
  if (sizeAttr.isSplat())
    return {*sizeAttrValueIt * index, *sizeAttrValueIt};

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttrValueIt[i];
  return {start, sizeAttrValueIt[index]};
}

::mlir::Operation::operand_range JITExecuteOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value JITExecuteOp::ctx() {
  auto operands = getODSOperands(0);
  return operands.empty() ? ::mlir::Value() : *operands.begin();
}

::mlir::Value JITExecuteOp::callable() {
  return *getODSOperands(1).begin();
}

::mlir::Operation::operand_range JITExecuteOp::operands() {
  return getODSOperands(2);
}

::mlir::MutableOperandRange JITExecuteOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(0u, *getOperation()->getAttrDictionary().getNamed(operand_segment_sizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange JITExecuteOp::callableMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(1u, *getOperation()->getAttrDictionary().getNamed(operand_segment_sizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange JITExecuteOp::operandsMutable() {
  auto range = getODSOperandIndexAndLength(2);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(2u, *getOperation()->getAttrDictionary().getNamed(operand_segment_sizesAttrName())));
  return mutableRange;
}

std::pair<unsigned, unsigned> JITExecuteOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range JITExecuteOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range JITExecuteOp::results() {
  return getODSResults(0);
}

void JITExecuteOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, /*optional*/::mlir::Value ctx, ::mlir::Value callable, ::mlir::ValueRange operands) {
  if (ctx)
    odsState.addOperands(ctx);
  odsState.addOperands(callable);
  odsState.addOperands(operands);
  odsState.addAttribute(operand_segment_sizesAttrName(odsState.name), odsBuilder.getI32VectorAttr({(ctx ? 1 : 0), 1, static_cast<int32_t>(operands.size())}));
  odsState.addTypes(results);
}

void JITExecuteOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() >= 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult JITExecuteOp::verify() {
  {
    auto sizeAttr = (*this)->getAttr(operand_segment_sizesAttrName()).dyn_cast<::mlir::DenseIntElementsAttr>();
    if (!sizeAttr)
      return emitOpError("missing segment sizes attribute 'operand_segment_sizes'");
    auto numElements =
        sizeAttr.getType().cast<::mlir::ShapedType>().getNumElements();
    if (numElements != 3)
      return emitOpError("'operand_segment_sizes' attribute for specifying operand segments must have 3 "
                "elements, but got ") << numElements;
  }
    {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    if (valueGroup0.size() > 1) {
      return emitOpError("operand group starting at #") << index
          << " requires 0 or 1 element, but found " << valueGroup0.size();
    }

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops4(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<JITExecuteOp>(*this);
}

::mlir::ParseResult JITExecuteOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> ctxOperands;
  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::OpAsmParser::OperandType callableRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> callableOperands(callableRawOperands);  ::llvm::SMLoc callableOperandsLoc;
  (void)callableOperandsLoc;
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> operandsOperands;
  ::llvm::SMLoc operandsOperandsLoc;
  (void)operandsOperandsLoc;
  ::mlir::SmallVector<::mlir::Type, 1> operandsTypes;
  ::mlir::SmallVector<::mlir::Type, 1> resultsTypes;
  if (succeeded(parser.parseOptionalKeyword("ctx"))) {
  if (parser.parseLParen())
    return ::mlir::failure();

  {
    ctxOperandsLoc = parser.getCurrentLocation();
    ::mlir::OpAsmParser::OperandType operand;
    ::mlir::OptionalParseResult parseResult =
                                    parser.parseOptionalOperand(operand);
    if (parseResult.hasValue()) {
      if (failed(*parseResult))
        return ::mlir::failure();
      ctxOperands.push_back(operand);
    }
  }
  if (parser.parseRParen())
    return ::mlir::failure();
  }

  callableOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(callableRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseLParen())
    return ::mlir::failure();

  operandsOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperandList(operandsOperands))
    return ::mlir::failure();
  if (parser.parseRParen())
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  if (parser.parseTypeList(operandsTypes))
    return ::mlir::failure();
  if (parser.parseArrow())
    return ::mlir::failure();

  if (parser.parseTypeList(resultsTypes))
    return ::mlir::failure();
  result.addAttribute("operand_segment_sizes", parser.getBuilder().getI32VectorAttr({static_cast<int32_t>(ctxOperands.size()), 1, static_cast<int32_t>(operandsOperands.size())}));
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  ::mlir::Type odsBuildableType1 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::JITCallableType>();
  result.addTypes(resultsTypes);
  if (parser.resolveOperands(ctxOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(callableOperands, odsBuildableType1, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(operandsOperands, operandsTypes, operandsOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void JITExecuteOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  if (ctx()) {
  _odsPrinter << ' ' << "ctx";
  _odsPrinter << "(";
  if (::mlir::Value value = ctx())
    _odsPrinter << value;
  _odsPrinter << ")";
  }
  _odsPrinter << ' ';
  _odsPrinter << callable();
  _odsPrinter << "(";
  _odsPrinter << operands();
  _odsPrinter << ")";
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"operand_segment_sizes", });
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  _odsPrinter << operands().getTypes();
  _odsPrinter << ' ' << "->";
  _odsPrinter << ' ';
  _odsPrinter << results().getTypes();
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::JITExecuteOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::NullContextOp definitions
//===----------------------------------------------------------------------===//

NullContextOpAdaptor::NullContextOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

NullContextOpAdaptor::NullContextOpAdaptor(NullContextOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange NullContextOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> NullContextOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange NullContextOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr NullContextOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult NullContextOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> NullContextOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range NullContextOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> NullContextOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range NullContextOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value NullContextOp::result() {
  return *getODSResults(0).begin();
}

void NullContextOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result) {
  odsState.addTypes(result);
}

void NullContextOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void NullContextOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult NullContextOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<NullContextOp>(*this);
}

::mlir::ParseResult NullContextOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  return ::mlir::success();
}

void NullContextOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void NullContextOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::NullContextOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::NullMemRefOp definitions
//===----------------------------------------------------------------------===//

NullMemRefOpAdaptor::NullMemRefOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

NullMemRefOpAdaptor::NullMemRefOpAdaptor(NullMemRefOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange NullMemRefOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> NullMemRefOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange NullMemRefOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr NullMemRefOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult NullMemRefOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> NullMemRefOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range NullMemRefOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> NullMemRefOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range NullMemRefOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value NullMemRefOp::result() {
  return *getODSResults(0).begin();
}

void NullMemRefOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result) {
  odsState.addTypes(result);
}

void NullMemRefOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void NullMemRefOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult NullMemRefOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops5(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<NullMemRefOp>(*this);
}

::mlir::ParseResult NullMemRefOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  return ::mlir::success();
}

void NullMemRefOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::NullMemRefOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::ReportErrorOp definitions
//===----------------------------------------------------------------------===//

ReportErrorOpAdaptor::ReportErrorOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ReportErrorOpAdaptor::ReportErrorOpAdaptor(ReportErrorOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ReportErrorOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ReportErrorOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange ReportErrorOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value ReportErrorOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr ReportErrorOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::kernel_gen::tf_framework::ErrorCodeAttr ReportErrorOpAdaptor::error_code() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::kernel_gen::tf_framework::ErrorCodeAttr attr = odsAttrs.get("error_code").cast<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>();
  return attr;
}

::mlir::StringAttr ReportErrorOpAdaptor::msg() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("msg").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::LogicalResult ReportErrorOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_error_code = odsAttrs.get("error_code");
    if (!tblgen_error_code)
      return emitError(loc, "'tf_framework.report_error' op ""requires attribute 'error_code'");

    if (tblgen_error_code && !((tblgen_error_code.isa<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>())))
      return emitError(loc, "'tf_framework.report_error' op ""attribute 'error_code' failed to satisfy constraint: error code");
  }
  {
    auto tblgen_msg = odsAttrs.get("msg");
    if (!tblgen_msg)
      return emitError(loc, "'tf_framework.report_error' op ""requires attribute 'msg'");

    if (tblgen_msg && !((tblgen_msg.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_framework.report_error' op ""attribute 'msg' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReportErrorOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ReportErrorOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value ReportErrorOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange ReportErrorOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> ReportErrorOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ReportErrorOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::kernel_gen::tf_framework::ErrorCodeAttr ReportErrorOp::error_codeAttr() {
  return (*this)->getAttr(error_codeAttrName()).cast<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>();
}

::mlir::kernel_gen::tf_framework::ErrorCode ReportErrorOp::error_code() {
  auto attr = error_codeAttr();
  return attr.getValue();
}

::mlir::StringAttr ReportErrorOp::msgAttr() {
  return (*this)->getAttr(msgAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef ReportErrorOp::msg() {
  auto attr = msgAttr();
  return attr.getValue();
}

void ReportErrorOp::error_codeAttr(::mlir::kernel_gen::tf_framework::ErrorCodeAttr attr) {
  (*this)->setAttr(error_codeAttrName(), attr);
}

void ReportErrorOp::msgAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(msgAttrName(), attr);
}

void ReportErrorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_code, ::mlir::StringAttr msg) {
  odsState.addOperands(ctx);
  odsState.addAttribute(error_codeAttrName(odsState.name), error_code);
  odsState.addAttribute(msgAttrName(odsState.name), msg);
}

void ReportErrorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_code, ::mlir::StringAttr msg) {
  odsState.addOperands(ctx);
  odsState.addAttribute(error_codeAttrName(odsState.name), error_code);
  odsState.addAttribute(msgAttrName(odsState.name), msg);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReportErrorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::kernel_gen::tf_framework::ErrorCode error_code, ::llvm::StringRef msg) {
  odsState.addOperands(ctx);
  odsState.addAttribute(error_codeAttrName(odsState.name), ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(odsBuilder.getContext(), error_code));
  odsState.addAttribute(msgAttrName(odsState.name), odsBuilder.getStringAttr(msg));
}

void ReportErrorOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::kernel_gen::tf_framework::ErrorCode error_code, ::llvm::StringRef msg) {
  odsState.addOperands(ctx);
  odsState.addAttribute(error_codeAttrName(odsState.name), ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(odsBuilder.getContext(), error_code));
  odsState.addAttribute(msgAttrName(odsState.name), odsBuilder.getStringAttr(msg));
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReportErrorOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ReportErrorOp::verify() {
  {
    auto tblgen_error_code = (*this)->getAttr(error_codeAttrName());
    if (!tblgen_error_code)
      return emitOpError("requires attribute 'error_code'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops4(*this, tblgen_error_code, "error_code")))
      return ::mlir::failure();
  }
  {
    auto tblgen_msg = (*this)->getAttr(msgAttrName());
    if (!tblgen_msg)
      return emitOpError("requires attribute 'msg'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops0(*this, tblgen_msg, "msg")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<ReportErrorOp>(*this);
}

::mlir::ParseResult ReportErrorOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType ctxRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> ctxOperands(ctxRawOperands);  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_codeAttr;
  ::mlir::StringAttr msgAttr;

  ctxOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(ctxRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseComma())
    return ::mlir::failure();

  {
    ::llvm::StringRef attrStr;
    ::mlir::NamedAttrList attrStorage;
    auto loc = parser.getCurrentLocation();
    if (parser.parseOptionalKeyword(&attrStr, {"OK","CANCELLED","UNKNOWN","INVALID_ARGUMENT","DEADLINE_EXCEEDED","NOT_FOUND","ALREADY_EXISTS","PERMISSION_DENIED","UNAUTHENTICATED","RESOURCE_EXHAUSTED","FAILED_PRECONDITION","ABORTED","OUT_OF_RANGE","UNIMPLEMENTED","INTERNAL","UNAVAILABLE","DATA_LOSS"})) {
      ::mlir::StringAttr attrVal;
      ::mlir::OptionalParseResult parseResult =
        parser.parseOptionalAttribute(attrVal,
                                      parser.getBuilder().getNoneType(),
                                      "error_code", attrStorage);
      if (parseResult.hasValue()) {
        if (failed(*parseResult))
          return ::mlir::failure();
        attrStr = attrVal.getValue();
      } else {
        return parser.emitError(loc, "expected string or keyword containing one of the following enum values for attribute 'error_code' [OK, CANCELLED, UNKNOWN, INVALID_ARGUMENT, DEADLINE_EXCEEDED, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, UNAUTHENTICATED, RESOURCE_EXHAUSTED, FAILED_PRECONDITION, ABORTED, OUT_OF_RANGE, UNIMPLEMENTED, INTERNAL, UNAVAILABLE, DATA_LOSS]");
      }
    }
    if (!attrStr.empty()) {
      auto attrOptional = ::mlir::kernel_gen::tf_framework::symbolizeErrorCode(attrStr);
      if (!attrOptional)
        return parser.emitError(loc, "invalid ")
               << "error_code attribute specification: \"" << attrStr << '"';;

      error_codeAttr = ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(parser.getBuilder().getContext(), attrOptional.getValue());
      result.addAttribute("error_code", error_codeAttr);
    }
  }
  if (parser.parseComma())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(msgAttr, parser.getBuilder().getType<::mlir::NoneType>(), "msg",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  if (parser.resolveOperands(ctxOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ReportErrorOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << ctx();
  _odsPrinter << ",";
  _odsPrinter << ' ';

  {
    auto caseValue = error_code();
    auto caseValueStr = stringifyErrorCode(caseValue);
    _odsPrinter << caseValueStr;
  }
  _odsPrinter << ",";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(msgAttr());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"error_code", "msg"});
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::ReportErrorOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::TFAllocOp definitions
//===----------------------------------------------------------------------===//

TFAllocOpAdaptor::TFAllocOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

TFAllocOpAdaptor::TFAllocOpAdaptor(TFAllocOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange TFAllocOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> TFAllocOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {false, true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 1) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange TFAllocOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFAllocOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::ValueRange TFAllocOpAdaptor::dyn_sizes() {
  return getODSOperands(1);
}

::mlir::DictionaryAttr TFAllocOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::ArrayAttr TFAllocOpAdaptor::input_indices() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("input_indices").dyn_cast_or_null<::mlir::ArrayAttr>();
  return attr;
}

::mlir::IntegerAttr TFAllocOpAdaptor::output_index() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::IntegerAttr attr = odsAttrs.get("output_index").dyn_cast_or_null<::mlir::IntegerAttr>();
  return attr;
}

::mlir::LogicalResult TFAllocOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_input_indices = odsAttrs.get("input_indices");
    if (tblgen_input_indices && !(((tblgen_input_indices.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_input_indices.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); }))))
      return emitError(loc, "'tf_framework.alloc' op ""attribute 'input_indices' failed to satisfy constraint: 32-bit integer array attribute");
  }
  {
    auto tblgen_output_index = odsAttrs.get("output_index");
    if (tblgen_output_index && !(((tblgen_output_index.isa<::mlir::IntegerAttr>())) && ((tblgen_output_index.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))))
      return emitError(loc, "'tf_framework.alloc' op ""attribute 'output_index' failed to satisfy constraint: 32-bit signless integer attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> TFAllocOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {false, true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 1) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range TFAllocOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFAllocOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Operation::operand_range TFAllocOp::dyn_sizes() {
  return getODSOperands(1);
}

::mlir::MutableOperandRange TFAllocOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange TFAllocOp::dyn_sizesMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> TFAllocOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range TFAllocOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFAllocOp::result() {
  return *getODSResults(0).begin();
}

::mlir::ArrayAttr TFAllocOp::input_indicesAttr() {
  return (*this)->getAttr(input_indicesAttrName()).dyn_cast_or_null<::mlir::ArrayAttr>();
}

::llvm::Optional< ::mlir::ArrayAttr > TFAllocOp::input_indices() {
  auto attr = input_indicesAttr();
  return attr ? ::llvm::Optional< ::mlir::ArrayAttr >(attr) : (::llvm::None);
}

::mlir::IntegerAttr TFAllocOp::output_indexAttr() {
  return (*this)->getAttr(output_indexAttrName()).dyn_cast_or_null<::mlir::IntegerAttr>();
}

::llvm::Optional<uint32_t> TFAllocOp::output_index() {
  auto attr = output_indexAttr();
  return attr ? ::llvm::Optional<uint32_t>(attr.getValue().getZExtValue()) : (::llvm::None);
}

void TFAllocOp::input_indicesAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(input_indicesAttrName(), attr);
}

void TFAllocOp::output_indexAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(output_indexAttrName(), attr);
}

::mlir::Attribute TFAllocOp::removeInput_indicesAttr() {
  return (*this)->removeAttr(input_indicesAttrName());
}

::mlir::Attribute TFAllocOp::removeOutput_indexAttr() {
  return (*this)->removeAttr(output_indexAttrName());
}

void TFAllocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, MemRefType memref_type, Value ctx) {
      odsState.addOperands(ctx);
      odsState.types.push_back(memref_type);
    
}

void TFAllocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, MemRefType memref_type, Value ctx, ValueRange dyn_sizes) {
      build(odsBuilder, odsState, memref_type, ctx);
      odsState.addOperands(dyn_sizes);
    
}

void TFAllocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value ctx, ::mlir::ValueRange dyn_sizes, /*optional*/::mlir::ArrayAttr input_indices, /*optional*/::mlir::IntegerAttr output_index) {
  odsState.addOperands(ctx);
  odsState.addOperands(dyn_sizes);
  if (input_indices) {
  odsState.addAttribute(input_indicesAttrName(odsState.name), input_indices);
  }
  if (output_index) {
  odsState.addAttribute(output_indexAttrName(odsState.name), output_index);
  }
  odsState.addTypes(result);
}

void TFAllocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::ValueRange dyn_sizes, /*optional*/::mlir::ArrayAttr input_indices, /*optional*/::mlir::IntegerAttr output_index) {
  odsState.addOperands(ctx);
  odsState.addOperands(dyn_sizes);
  if (input_indices) {
  odsState.addAttribute(input_indicesAttrName(odsState.name), input_indices);
  }
  if (output_index) {
  odsState.addAttribute(output_indexAttrName(odsState.name), output_index);
  }
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void TFAllocOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() >= 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult TFAllocOp::verify() {
  {
    auto tblgen_input_indices = (*this)->getAttr(input_indicesAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops5(*this, tblgen_input_indices, "input_indices")))
      return ::mlir::failure();
  }
  {
    auto tblgen_output_index = (*this)->getAttr(output_indexAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops6(*this, tblgen_output_index, "output_index")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops6(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<TFAllocOp>(*this);
}

::mlir::ParseResult TFAllocOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType ctxRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> ctxOperands(ctxRawOperands);  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> dyn_sizesOperands;
  ::llvm::SMLoc dyn_sizesOperandsLoc;
  (void)dyn_sizesOperandsLoc;
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);
  if (parser.parseLParen())
    return ::mlir::failure();

  ctxOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(ctxRawOperands[0]))
    return ::mlir::failure();
  if (succeeded(parser.parseOptionalComma())) {

  dyn_sizesOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperandList(dyn_sizesOperands))
    return ::mlir::failure();
  }
  if (parser.parseRParen())
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::MemRefType type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  ::mlir::Type odsBuildableType1 = parser.getBuilder().getIndexType();
  result.addTypes(resultTypes);
  if (parser.resolveOperands(ctxOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(dyn_sizesOperands, odsBuildableType1, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void TFAllocOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << "(";
  _odsPrinter << ctx();
  if (!dyn_sizes().empty()) {
  _odsPrinter << ",";
  _odsPrinter << ' ';
  _odsPrinter << dyn_sizes();
  }
  _odsPrinter << ")";
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::MemRefType>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void TFAllocOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  effects.emplace_back(::mlir::MemoryEffects::Allocate::get(), ::mlir::SideEffects::DefaultResource::get());
  for (::mlir::Value value : getODSResults(0))
    effects.emplace_back(::mlir::MemoryEffects::Allocate::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::TFAllocOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::TFAssertOp definitions
//===----------------------------------------------------------------------===//

TFAssertOpAdaptor::TFAssertOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

TFAssertOpAdaptor::TFAssertOpAdaptor(TFAssertOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange TFAssertOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> TFAssertOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange TFAssertOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFAssertOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value TFAssertOpAdaptor::arg() {
  return *getODSOperands(1).begin();
}

::mlir::DictionaryAttr TFAssertOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::kernel_gen::tf_framework::ErrorCodeAttr TFAssertOpAdaptor::error_code() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::kernel_gen::tf_framework::ErrorCodeAttr attr = odsAttrs.get("error_code").cast<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>();
  return attr;
}

::mlir::StringAttr TFAssertOpAdaptor::msg() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("msg").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::LogicalResult TFAssertOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_error_code = odsAttrs.get("error_code");
    if (!tblgen_error_code)
      return emitError(loc, "'tf_framework.assert' op ""requires attribute 'error_code'");

    if (tblgen_error_code && !((tblgen_error_code.isa<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>())))
      return emitError(loc, "'tf_framework.assert' op ""attribute 'error_code' failed to satisfy constraint: error code");
  }
  {
    auto tblgen_msg = odsAttrs.get("msg");
    if (!tblgen_msg)
      return emitError(loc, "'tf_framework.assert' op ""requires attribute 'msg'");

    if (tblgen_msg && !((tblgen_msg.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_framework.assert' op ""attribute 'msg' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> TFAssertOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range TFAssertOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFAssertOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value TFAssertOp::arg() {
  return *getODSOperands(1).begin();
}

::mlir::MutableOperandRange TFAssertOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange TFAssertOp::argMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> TFAssertOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range TFAssertOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::kernel_gen::tf_framework::ErrorCodeAttr TFAssertOp::error_codeAttr() {
  return (*this)->getAttr(error_codeAttrName()).cast<::mlir::kernel_gen::tf_framework::ErrorCodeAttr>();
}

::mlir::kernel_gen::tf_framework::ErrorCode TFAssertOp::error_code() {
  auto attr = error_codeAttr();
  return attr.getValue();
}

::mlir::StringAttr TFAssertOp::msgAttr() {
  return (*this)->getAttr(msgAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef TFAssertOp::msg() {
  auto attr = msgAttr();
  return attr.getValue();
}

void TFAssertOp::error_codeAttr(::mlir::kernel_gen::tf_framework::ErrorCodeAttr attr) {
  (*this)->setAttr(error_codeAttrName(), attr);
}

void TFAssertOp::msgAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(msgAttrName(), attr);
}

void TFAssertOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::Value arg, ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_code, ::mlir::StringAttr msg) {
  odsState.addOperands(ctx);
  odsState.addOperands(arg);
  odsState.addAttribute(error_codeAttrName(odsState.name), error_code);
  odsState.addAttribute(msgAttrName(odsState.name), msg);
}

void TFAssertOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::Value arg, ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_code, ::mlir::StringAttr msg) {
  odsState.addOperands(ctx);
  odsState.addOperands(arg);
  odsState.addAttribute(error_codeAttrName(odsState.name), error_code);
  odsState.addAttribute(msgAttrName(odsState.name), msg);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void TFAssertOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::Value arg, ::mlir::kernel_gen::tf_framework::ErrorCode error_code, ::llvm::StringRef msg) {
  odsState.addOperands(ctx);
  odsState.addOperands(arg);
  odsState.addAttribute(error_codeAttrName(odsState.name), ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(odsBuilder.getContext(), error_code));
  odsState.addAttribute(msgAttrName(odsState.name), odsBuilder.getStringAttr(msg));
}

void TFAssertOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::Value arg, ::mlir::kernel_gen::tf_framework::ErrorCode error_code, ::llvm::StringRef msg) {
  odsState.addOperands(ctx);
  odsState.addOperands(arg);
  odsState.addAttribute(error_codeAttrName(odsState.name), ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(odsBuilder.getContext(), error_code));
  odsState.addAttribute(msgAttrName(odsState.name), odsBuilder.getStringAttr(msg));
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void TFAssertOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 2u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult TFAssertOp::verify() {
  {
    auto tblgen_error_code = (*this)->getAttr(error_codeAttrName());
    if (!tblgen_error_code)
      return emitOpError("requires attribute 'error_code'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops4(*this, tblgen_error_code, "error_code")))
      return ::mlir::failure();
  }
  {
    auto tblgen_msg = (*this)->getAttr(msgAttrName());
    if (!tblgen_msg)
      return emitOpError("requires attribute 'msg'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_framework_ops0(*this, tblgen_msg, "msg")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<TFAssertOp>(*this);
}

::mlir::ParseResult TFAssertOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType ctxRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> ctxOperands(ctxRawOperands);  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::OpAsmParser::OperandType argRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> argOperands(argRawOperands);  ::llvm::SMLoc argOperandsLoc;
  (void)argOperandsLoc;
  ::mlir::kernel_gen::tf_framework::ErrorCodeAttr error_codeAttr;
  ::mlir::StringAttr msgAttr;

  ctxOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(ctxRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseComma())
    return ::mlir::failure();

  argOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(argRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseComma())
    return ::mlir::failure();

  {
    ::llvm::StringRef attrStr;
    ::mlir::NamedAttrList attrStorage;
    auto loc = parser.getCurrentLocation();
    if (parser.parseOptionalKeyword(&attrStr, {"OK","CANCELLED","UNKNOWN","INVALID_ARGUMENT","DEADLINE_EXCEEDED","NOT_FOUND","ALREADY_EXISTS","PERMISSION_DENIED","UNAUTHENTICATED","RESOURCE_EXHAUSTED","FAILED_PRECONDITION","ABORTED","OUT_OF_RANGE","UNIMPLEMENTED","INTERNAL","UNAVAILABLE","DATA_LOSS"})) {
      ::mlir::StringAttr attrVal;
      ::mlir::OptionalParseResult parseResult =
        parser.parseOptionalAttribute(attrVal,
                                      parser.getBuilder().getNoneType(),
                                      "error_code", attrStorage);
      if (parseResult.hasValue()) {
        if (failed(*parseResult))
          return ::mlir::failure();
        attrStr = attrVal.getValue();
      } else {
        return parser.emitError(loc, "expected string or keyword containing one of the following enum values for attribute 'error_code' [OK, CANCELLED, UNKNOWN, INVALID_ARGUMENT, DEADLINE_EXCEEDED, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, UNAUTHENTICATED, RESOURCE_EXHAUSTED, FAILED_PRECONDITION, ABORTED, OUT_OF_RANGE, UNIMPLEMENTED, INTERNAL, UNAVAILABLE, DATA_LOSS]");
      }
    }
    if (!attrStr.empty()) {
      auto attrOptional = ::mlir::kernel_gen::tf_framework::symbolizeErrorCode(attrStr);
      if (!attrOptional)
        return parser.emitError(loc, "invalid ")
               << "error_code attribute specification: \"" << attrStr << '"';;

      error_codeAttr = ::mlir::kernel_gen::tf_framework::ErrorCodeAttr::get(parser.getBuilder().getContext(), attrOptional.getValue());
      result.addAttribute("error_code", error_codeAttr);
    }
  }
  if (parser.parseComma())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(msgAttr, parser.getBuilder().getType<::mlir::NoneType>(), "msg",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  ::mlir::Type odsBuildableType1 = parser.getBuilder().getIntegerType(1);
  if (parser.resolveOperands(ctxOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(argOperands, odsBuildableType1, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void TFAssertOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << ctx();
  _odsPrinter << ",";
  _odsPrinter << ' ';
  _odsPrinter << arg();
  _odsPrinter << ",";
  _odsPrinter << ' ';

  {
    auto caseValue = error_code();
    auto caseValueStr = stringifyErrorCode(caseValue);
    _odsPrinter << caseValueStr;
  }
  _odsPrinter << ",";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(msgAttr());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"error_code", "msg"});
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::TFAssertOp)

namespace mlir {
namespace kernel_gen {
namespace tf_framework {

//===----------------------------------------------------------------------===//
// ::mlir::kernel_gen::tf_framework::TFDeallocOp definitions
//===----------------------------------------------------------------------===//

TFDeallocOpAdaptor::TFDeallocOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

TFDeallocOpAdaptor::TFDeallocOpAdaptor(TFDeallocOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange TFDeallocOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> TFDeallocOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange TFDeallocOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFDeallocOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value TFDeallocOpAdaptor::memref() {
  return *getODSOperands(1).begin();
}

::mlir::DictionaryAttr TFDeallocOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult TFDeallocOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> TFDeallocOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range TFDeallocOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TFDeallocOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value TFDeallocOp::memref() {
  return *getODSOperands(1).begin();
}

::mlir::MutableOperandRange TFDeallocOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange TFDeallocOp::memrefMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> TFDeallocOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range TFDeallocOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void TFDeallocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::Value memref) {
  odsState.addOperands(ctx);
  odsState.addOperands(memref);
}

void TFDeallocOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::Value memref) {
  odsState.addOperands(ctx);
  odsState.addOperands(memref);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void TFDeallocOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 2u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult TFDeallocOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_framework_ops5(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return Verify<TFDeallocOp>(*this);
}

::mlir::ParseResult TFDeallocOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType ctxRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> ctxOperands(ctxRawOperands);  ::llvm::SMLoc ctxOperandsLoc;
  (void)ctxOperandsLoc;
  ::mlir::OpAsmParser::OperandType memrefRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> memrefOperands(memrefRawOperands);  ::llvm::SMLoc memrefOperandsLoc;
  (void)memrefOperandsLoc;
  ::mlir::Type memrefRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> memrefTypes(memrefRawTypes);
  if (parser.parseLParen())
    return ::mlir::failure();

  ctxOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(ctxRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseComma())
    return ::mlir::failure();

  memrefOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(memrefRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseRParen())
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    memrefRawTypes[0] = type;
  }
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::kernel_gen::tf_framework::OpKernelContextType>();
  if (parser.resolveOperands(ctxOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  if (parser.resolveOperands(memrefOperands, memrefTypes, memrefOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void TFDeallocOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << "(";
  _odsPrinter << ctx();
  _odsPrinter << ",";
  _odsPrinter << ' ';
  _odsPrinter << memref();
  _odsPrinter << ")";
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = memref().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

void TFDeallocOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  effects.emplace_back(::mlir::MemoryEffects::Free::get(), ::mlir::SideEffects::DefaultResource::get());
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Free::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace tf_framework
} // namespace kernel_gen
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::kernel_gen::tf_framework::TFDeallocOp)


#endif  // GET_OP_CLASSES

