/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::disc_ral::DispatchOp,
::mlir::disc_ral::RecvInputOp,
::mlir::disc_ral::SendOutputOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace disc_ral {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_disc_ral_ops0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::disc_ral::RalExecutionContextType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be context, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_disc_ral_ops1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((true))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be any type, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_disc_ral_ops2(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::IndexType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be index, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_disc_ral_ops3(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::MemRefType>())) && ([](::mlir::Type elementType) { return (true); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be memref of any type values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_disc_ral_ops0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::StringAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: string attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_disc_ral_ops1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::BoolAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: bool attribute";
  }
  return ::mlir::success();
}
} // namespace disc_ral
} // namespace mlir
namespace mlir {
namespace disc_ral {

//===----------------------------------------------------------------------===//
// ::mlir::disc_ral::DispatchOp definitions
//===----------------------------------------------------------------------===//

DispatchOpAdaptor::DispatchOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

DispatchOpAdaptor::DispatchOpAdaptor(DispatchOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange DispatchOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> DispatchOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
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

::mlir::ValueRange DispatchOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value DispatchOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::ValueRange DispatchOpAdaptor::args() {
  return getODSOperands(1);
}

::mlir::DictionaryAttr DispatchOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr DispatchOpAdaptor::call_target_name() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("call_target_name").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::BoolAttr DispatchOpAdaptor::has_side_effect() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::BoolAttr attr = odsAttrs.get("has_side_effect").dyn_cast_or_null<::mlir::BoolAttr>();
  if (!attr)
    attr = ::mlir::Builder(odsAttrs.getContext()).getBoolAttr(false);
  return attr;
}

::mlir::StringAttr DispatchOpAdaptor::backend_config() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("backend_config").dyn_cast_or_null<::mlir::StringAttr>();
  if (!attr)
    attr = ::mlir::Builder(odsAttrs.getContext()).getStringAttr("");
  return attr;
}

::mlir::LogicalResult DispatchOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_call_target_name = odsAttrs.get("call_target_name");
    if (!tblgen_call_target_name)
      return emitError(loc, "'disc_ral.dispatch' op ""requires attribute 'call_target_name'");

    if (tblgen_call_target_name && !((tblgen_call_target_name.isa<::mlir::StringAttr>())))
      return emitError(loc, "'disc_ral.dispatch' op ""attribute 'call_target_name' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_has_side_effect = odsAttrs.get("has_side_effect");
    if (tblgen_has_side_effect && !((tblgen_has_side_effect.isa<::mlir::BoolAttr>())))
      return emitError(loc, "'disc_ral.dispatch' op ""attribute 'has_side_effect' failed to satisfy constraint: bool attribute");
  }
  {
    auto tblgen_backend_config = odsAttrs.get("backend_config");
    if (tblgen_backend_config && !((tblgen_backend_config.isa<::mlir::StringAttr>())))
      return emitError(loc, "'disc_ral.dispatch' op ""attribute 'backend_config' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> DispatchOp::getODSOperandIndexAndLength(unsigned index) {
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

::mlir::Operation::operand_range DispatchOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value DispatchOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Operation::operand_range DispatchOp::args() {
  return getODSOperands(1);
}

::mlir::MutableOperandRange DispatchOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange DispatchOp::argsMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> DispatchOp::getODSResultIndexAndLength(unsigned index) {
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

::mlir::Operation::result_range DispatchOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::StringAttr DispatchOp::call_target_nameAttr() {
  return (*this)->getAttr(call_target_nameAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef DispatchOp::call_target_name() {
  auto attr = call_target_nameAttr();
  return attr.getValue();
}

::mlir::BoolAttr DispatchOp::has_side_effectAttr() {
  return (*this)->getAttr(has_side_effectAttrName()).dyn_cast_or_null<::mlir::BoolAttr>();
}

bool DispatchOp::has_side_effect() {
  auto attr = has_side_effectAttr();
    if (!attr)
      return ::mlir::Builder((*this)->getContext()).getBoolAttr(false).getValue();
  return attr.getValue();
}

::mlir::StringAttr DispatchOp::backend_configAttr() {
  return (*this)->getAttr(backend_configAttrName()).dyn_cast_or_null<::mlir::StringAttr>();
}

::llvm::StringRef DispatchOp::backend_config() {
  auto attr = backend_configAttr();
    if (!attr)
      return ::mlir::Builder((*this)->getContext()).getStringAttr("").getValue();
  return attr.getValue();
}

void DispatchOp::call_target_nameAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(call_target_nameAttrName(), attr);
}

void DispatchOp::has_side_effectAttr(::mlir::BoolAttr attr) {
  (*this)->setAttr(has_side_effectAttrName(), attr);
}

void DispatchOp::backend_configAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(backend_configAttrName(), attr);
}

void DispatchOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value ctx, ::mlir::ValueRange args, ::mlir::StringAttr call_target_name, ::mlir::BoolAttr has_side_effect, ::mlir::StringAttr backend_config) {
  odsState.addOperands(ctx);
  odsState.addOperands(args);
  odsState.addAttribute(call_target_nameAttrName(odsState.name), call_target_name);
  odsState.addAttribute(has_side_effectAttrName(odsState.name), has_side_effect);
  odsState.addAttribute(backend_configAttrName(odsState.name), backend_config);
  odsState.addTypes(resultType0);
}

void DispatchOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value ctx, ::mlir::ValueRange args, ::llvm::StringRef call_target_name, bool has_side_effect, ::llvm::StringRef backend_config) {
  odsState.addOperands(ctx);
  odsState.addOperands(args);
  odsState.addAttribute(call_target_nameAttrName(odsState.name), odsBuilder.getStringAttr(call_target_name));
  odsState.addAttribute(has_side_effectAttrName(odsState.name), odsBuilder.getBoolAttr(has_side_effect));
  odsState.addAttribute(backend_configAttrName(odsState.name), odsBuilder.getStringAttr(backend_config));
  odsState.addTypes(resultType0);
}

void DispatchOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() >= 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult DispatchOp::verify() {
  {
    auto tblgen_call_target_name = (*this)->getAttr(call_target_nameAttrName());
    if (!tblgen_call_target_name)
      return emitOpError("requires attribute 'call_target_name'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_disc_ral_ops0(*this, tblgen_call_target_name, "call_target_name")))
      return ::mlir::failure();
  }
  {
    auto tblgen_has_side_effect = (*this)->getAttr(has_side_effectAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_disc_ral_ops1(*this, tblgen_has_side_effect, "has_side_effect")))
      return ::mlir::failure();
  }
  {
    auto tblgen_backend_config = (*this)->getAttr(backend_configAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_disc_ral_ops0(*this, tblgen_backend_config, "backend_config")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops1(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify(*this);
}

} // namespace disc_ral
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::disc_ral::DispatchOp)

namespace mlir {
namespace disc_ral {

//===----------------------------------------------------------------------===//
// ::mlir::disc_ral::RecvInputOp definitions
//===----------------------------------------------------------------------===//

RecvInputOpAdaptor::RecvInputOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

RecvInputOpAdaptor::RecvInputOpAdaptor(RecvInputOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange RecvInputOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> RecvInputOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange RecvInputOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value RecvInputOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value RecvInputOpAdaptor::input_idx() {
  return *getODSOperands(1).begin();
}

::mlir::DictionaryAttr RecvInputOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult RecvInputOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> RecvInputOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range RecvInputOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value RecvInputOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value RecvInputOp::input_idx() {
  return *getODSOperands(1).begin();
}

::mlir::MutableOperandRange RecvInputOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange RecvInputOp::input_idxMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> RecvInputOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range RecvInputOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void RecvInputOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type resultType0, ::mlir::Value ctx, ::mlir::Value input_idx) {
  odsState.addOperands(ctx);
  odsState.addOperands(input_idx);
  odsState.addTypes(resultType0);
}

void RecvInputOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::Value input_idx) {
  odsState.addOperands(ctx);
  odsState.addOperands(input_idx);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void RecvInputOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 2u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult RecvInputOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops3(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify(*this);
}

} // namespace disc_ral
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::disc_ral::RecvInputOp)

namespace mlir {
namespace disc_ral {

//===----------------------------------------------------------------------===//
// ::mlir::disc_ral::SendOutputOp definitions
//===----------------------------------------------------------------------===//

SendOutputOpAdaptor::SendOutputOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

SendOutputOpAdaptor::SendOutputOpAdaptor(SendOutputOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange SendOutputOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> SendOutputOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange SendOutputOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SendOutputOpAdaptor::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value SendOutputOpAdaptor::output_idx() {
  return *getODSOperands(1).begin();
}

::mlir::Value SendOutputOpAdaptor::result() {
  return *getODSOperands(2).begin();
}

::mlir::DictionaryAttr SendOutputOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult SendOutputOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> SendOutputOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range SendOutputOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SendOutputOp::ctx() {
  return *getODSOperands(0).begin();
}

::mlir::Value SendOutputOp::output_idx() {
  return *getODSOperands(1).begin();
}

::mlir::Value SendOutputOp::result() {
  return *getODSOperands(2).begin();
}

::mlir::MutableOperandRange SendOutputOp::ctxMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange SendOutputOp::output_idxMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

::mlir::MutableOperandRange SendOutputOp::resultMutable() {
  auto range = getODSOperandIndexAndLength(2);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> SendOutputOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range SendOutputOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void SendOutputOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value ctx, ::mlir::Value output_idx, ::mlir::Value result) {
  odsState.addOperands(ctx);
  odsState.addOperands(output_idx);
  odsState.addOperands(result);
}

void SendOutputOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value ctx, ::mlir::Value output_idx, ::mlir::Value result) {
  odsState.addOperands(ctx);
  odsState.addOperands(output_idx);
  odsState.addOperands(result);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void SendOutputOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 3u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult SendOutputOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_disc_ral_ops3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return Verify(*this);
}

} // namespace disc_ral
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::disc_ral::SendOutputOp)


#endif  // GET_OP_CLASSES

