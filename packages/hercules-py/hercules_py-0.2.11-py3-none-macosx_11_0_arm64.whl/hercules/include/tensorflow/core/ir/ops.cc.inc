/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::tfg::GetResultOp,
::mlir::tfg::GraphFuncOp,
::mlir::tfg::GraphOp,
::mlir::tfg::ReturnOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace tfg {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ops0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::tf_type::OpaqueTensorType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be , but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ops1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((true))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be any type, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_ops0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::StringAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: string attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_ops1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit signless integer attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_ops2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::TypeAttr>())) && ((attr.cast<::mlir::TypeAttr>().getValue().isa<::mlir::Type>())))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: any type attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_ops3(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::UnitAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: unit attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_ops4(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::tf_type::VersionAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: An Attribute describing the version for a TensorFlow Graph";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_region_constraint_ops0(
    ::mlir::Operation *op, ::mlir::Region &region, ::llvm::StringRef regionName,
    unsigned regionIndex) {
  if (!((true))) {
    return op->emitOpError("region #") << regionIndex
        << (regionName.empty() ? " " : " ('" + regionName + "') ")
        << "failed to verify constraint: any region";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_region_constraint_ops1(
    ::mlir::Operation *op, ::mlir::Region &region, ::llvm::StringRef regionName,
    unsigned regionIndex) {
  if (!((::llvm::hasNItems(region, 1)))) {
    return op->emitOpError("region #") << regionIndex
        << (regionName.empty() ? " " : " ('" + regionName + "') ")
        << "failed to verify constraint: region with 1 blocks";
  }
  return ::mlir::success();
}
} // namespace tfg
} // namespace mlir
namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GetResultOp definitions
//===----------------------------------------------------------------------===//

GetResultOpAdaptor::GetResultOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

GetResultOpAdaptor::GetResultOpAdaptor(GetResultOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange GetResultOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> GetResultOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange GetResultOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value GetResultOpAdaptor::value() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr GetResultOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr GetResultOpAdaptor::name() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("name").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::IntegerAttr GetResultOpAdaptor::number() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::IntegerAttr attr = odsAttrs.get("number").cast<::mlir::IntegerAttr>();
  return attr;
}

::mlir::LogicalResult GetResultOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_name = odsAttrs.get("name");
    if (!tblgen_name)
      return emitError(loc, "'tfg.get_result' op ""requires attribute 'name'");

    if (tblgen_name && !((tblgen_name.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tfg.get_result' op ""attribute 'name' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_number = odsAttrs.get("number");
    if (!tblgen_number)
      return emitError(loc, "'tfg.get_result' op ""requires attribute 'number'");

    if (tblgen_number && !(((tblgen_number.isa<::mlir::IntegerAttr>())) && ((tblgen_number.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))))
      return emitError(loc, "'tfg.get_result' op ""attribute 'number' failed to satisfy constraint: 32-bit signless integer attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> GetResultOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range GetResultOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value GetResultOp::value() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange GetResultOp::valueMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> GetResultOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range GetResultOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value GetResultOp::result() {
  return *getODSResults(0).begin();
}

::mlir::StringAttr GetResultOp::nameAttr() {
  return (*this)->getAttr(nameAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef GetResultOp::name() {
  auto attr = nameAttr();
  return attr.getValue();
}

::mlir::IntegerAttr GetResultOp::numberAttr() {
  return (*this)->getAttr(numberAttrName()).cast<::mlir::IntegerAttr>();
}

uint32_t GetResultOp::number() {
  auto attr = numberAttr();
  return attr.getValue().getZExtValue();
}

void GetResultOp::nameAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(nameAttrName(), attr);
}

void GetResultOp::numberAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(numberAttrName(), attr);
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), name);
  odsState.addAttribute(numberAttrName(odsState.name), number);
  odsState.addTypes(result);
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), name);
  odsState.addAttribute(numberAttrName(odsState.name), number);

        ::llvm::SmallVector<::mlir::Type, 2> inferredReturnTypes;
        if (::mlir::succeeded(GetResultOp::inferReturnTypes(odsBuilder.getContext(),
                      odsState.location, odsState.operands,
                      odsState.attributes.getDictionary(odsState.getContext()),
                      /*regions=*/{}, inferredReturnTypes)))
          odsState.addTypes(inferredReturnTypes);
        else
          ::llvm::report_fatal_error("Failed to infer result type(s).");
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), name);
  odsState.addAttribute(numberAttrName(odsState.name), number);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value value, ::llvm::StringRef name, uint32_t number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), odsBuilder.getStringAttr(name));
  odsState.addAttribute(numberAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), number));
  odsState.addTypes(result);
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::llvm::StringRef name, uint32_t number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), odsBuilder.getStringAttr(name));
  odsState.addAttribute(numberAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), number));

        ::llvm::SmallVector<::mlir::Type, 2> inferredReturnTypes;
        if (::mlir::succeeded(GetResultOp::inferReturnTypes(odsBuilder.getContext(),
                      odsState.location, odsState.operands,
                      odsState.attributes.getDictionary(odsState.getContext()),
                      /*regions=*/{}, inferredReturnTypes)))
          odsState.addTypes(inferredReturnTypes);
        else
          ::llvm::report_fatal_error("Failed to infer result type(s).");
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::llvm::StringRef name, uint32_t number) {
  odsState.addOperands(value);
  odsState.addAttribute(nameAttrName(odsState.name), odsBuilder.getStringAttr(name));
  odsState.addAttribute(numberAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), number));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void GetResultOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

void GetResultOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);

  ::mlir::SmallVector<::mlir::Type, 2> inferredReturnTypes;
  if (::mlir::succeeded(GetResultOp::inferReturnTypes(odsBuilder.getContext(),
          odsState.location, operands,
          odsState.attributes.getDictionary(odsState.getContext()),
          odsState.regions, inferredReturnTypes))) {
    assert(inferredReturnTypes.size() == 1u && "mismatched number of return types");
    odsState.addTypes(inferredReturnTypes);
  } else {
    ::llvm::report_fatal_error("Failed to infer result type(s).");
  }
}

::mlir::LogicalResult GetResultOp::verify() {
  {
    auto tblgen_name = (*this)->getAttr(nameAttrName());
    if (!tblgen_name)
      return emitOpError("requires attribute 'name'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops0(*this, tblgen_name, "name")))
      return ::mlir::failure();
  }
  {
    auto tblgen_number = (*this)->getAttr(numberAttrName());
    if (!tblgen_number)
      return emitOpError("requires attribute 'number'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops1(*this, tblgen_number, "number")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult GetResultOp::inferReturnTypes(::mlir::MLIRContext *context, ::llvm::Optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes) {
  inferredReturnTypes.resize(1);
  ::mlir::Builder odsBuilder(context);
  inferredReturnTypes[0] = odsBuilder.getType<::mlir::tf_type::OpaqueTensorType>();
  return ::mlir::success();
}

::mlir::ParseResult GetResultOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType valueRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> valueOperands(valueRawOperands);  ::llvm::SMLoc valueOperandsLoc;
  (void)valueOperandsLoc;
  ::mlir::StringAttr nameAttr;
  ::mlir::IntegerAttr numberAttr;
  if (parser.parseLParen())
    return ::mlir::failure();

  valueOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(valueRawOperands[0]))
    return ::mlir::failure();
  if (parser.parseRParen())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(nameAttr, parser.getBuilder().getType<::mlir::NoneType>(), "name",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseColon())
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(numberAttr, parser.getBuilder().getIntegerType(32), "number",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDictWithKeyword(result.attributes))
    return ::mlir::failure();
  ::mlir::Type odsBuildableType0 = parser.getBuilder().getType<::mlir::tf_type::OpaqueTensorType>();
  result.addTypes(odsBuildableType0);
  if (parser.resolveOperands(valueOperands, odsBuildableType0, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void GetResultOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << "(";
  _odsPrinter << value();
  _odsPrinter << ")";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(nameAttr());
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(numberAttr());
  _odsPrinter.printOptionalAttrDictWithKeyword((*this)->getAttrs(), /*elidedAttrs=*/{"name", "number"});
}

void GetResultOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace tfg
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tfg::GetResultOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GraphFuncOp definitions
//===----------------------------------------------------------------------===//

GraphFuncOpAdaptor::GraphFuncOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

GraphFuncOpAdaptor::GraphFuncOpAdaptor(GraphFuncOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange GraphFuncOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> GraphFuncOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange GraphFuncOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr GraphFuncOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr GraphFuncOpAdaptor::sym_name() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("sym_name").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::TypeAttr GraphFuncOpAdaptor::type() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::TypeAttr attr = odsAttrs.get("type").cast<::mlir::TypeAttr>();
  return attr;
}

::mlir::UnitAttr GraphFuncOpAdaptor::generic() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::UnitAttr attr = odsAttrs.get("generic").dyn_cast_or_null<::mlir::UnitAttr>();
  return attr;
}

::mlir::RegionRange GraphFuncOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &GraphFuncOpAdaptor::body() {
  return *odsRegions[0];
}

::mlir::LogicalResult GraphFuncOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_sym_name = odsAttrs.get("sym_name");
    if (!tblgen_sym_name)
      return emitError(loc, "'tfg.func' op ""requires attribute 'sym_name'");

    if (tblgen_sym_name && !((tblgen_sym_name.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tfg.func' op ""attribute 'sym_name' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_type = odsAttrs.get("type");
    if (!tblgen_type)
      return emitError(loc, "'tfg.func' op ""requires attribute 'type'");

    if (tblgen_type && !(((tblgen_type.isa<::mlir::TypeAttr>())) && ((tblgen_type.cast<::mlir::TypeAttr>().getValue().isa<::mlir::Type>()))))
      return emitError(loc, "'tfg.func' op ""attribute 'type' failed to satisfy constraint: any type attribute");
  }
  {
    auto tblgen_generic = odsAttrs.get("generic");
    if (tblgen_generic && !((tblgen_generic.isa<::mlir::UnitAttr>())))
      return emitError(loc, "'tfg.func' op ""attribute 'generic' failed to satisfy constraint: unit attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> GraphFuncOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range GraphFuncOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> GraphFuncOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range GraphFuncOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Region &GraphFuncOp::body() {
  return (*this)->getRegion(0);
}

::mlir::StringAttr GraphFuncOp::sym_nameAttr() {
  return (*this)->getAttr(sym_nameAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef GraphFuncOp::sym_name() {
  auto attr = sym_nameAttr();
  return attr.getValue();
}

::mlir::TypeAttr GraphFuncOp::typeAttr() {
  return (*this)->getAttr(typeAttrName()).cast<::mlir::TypeAttr>();
}

::mlir::Type GraphFuncOp::type() {
  auto attr = typeAttr();
  return attr.getValue().cast<::mlir::Type>();
}

::mlir::UnitAttr GraphFuncOp::genericAttr() {
  return (*this)->getAttr(genericAttrName()).dyn_cast_or_null<::mlir::UnitAttr>();
}

bool GraphFuncOp::generic() {
  auto attr = genericAttr();
  return attr != nullptr;
}

void GraphFuncOp::sym_nameAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(sym_nameAttrName(), attr);
}

void GraphFuncOp::typeAttr(::mlir::TypeAttr attr) {
  (*this)->setAttr(typeAttrName(), attr);
}

void GraphFuncOp::genericAttr(::mlir::UnitAttr attr) {
  (*this)->setAttr(genericAttrName(), attr);
}

::mlir::Attribute GraphFuncOp::removeGenericAttr() {
  return (*this)->removeAttr(genericAttrName());
}

void GraphFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::StringAttr sym_name, ::mlir::TypeAttr type, /*optional*/::mlir::UnitAttr generic) {
  odsState.addAttribute(sym_nameAttrName(odsState.name), sym_name);
  odsState.addAttribute(typeAttrName(odsState.name), type);
  if (generic) {
  odsState.addAttribute(genericAttrName(odsState.name), generic);
  }
  (void)odsState.addRegion();
}

void GraphFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr sym_name, ::mlir::TypeAttr type, /*optional*/::mlir::UnitAttr generic) {
  odsState.addAttribute(sym_nameAttrName(odsState.name), sym_name);
  odsState.addAttribute(typeAttrName(odsState.name), type);
  if (generic) {
  odsState.addAttribute(genericAttrName(odsState.name), generic);
  }
  (void)odsState.addRegion();
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void GraphFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::llvm::StringRef sym_name, ::mlir::Type type, /*optional*/bool generic) {
  odsState.addAttribute(sym_nameAttrName(odsState.name), odsBuilder.getStringAttr(sym_name));
  odsState.addAttribute(typeAttrName(odsState.name), ::mlir::TypeAttr::get(type));
  if (generic) {
  odsState.addAttribute(genericAttrName(odsState.name), odsBuilder.getUnitAttr());
  }
  (void)odsState.addRegion();
}

void GraphFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef sym_name, ::mlir::Type type, /*optional*/bool generic) {
  odsState.addAttribute(sym_nameAttrName(odsState.name), odsBuilder.getStringAttr(sym_name));
  odsState.addAttribute(typeAttrName(odsState.name), ::mlir::TypeAttr::get(type));
  if (generic) {
  odsState.addAttribute(genericAttrName(odsState.name), odsBuilder.getUnitAttr());
  }
  (void)odsState.addRegion();
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void GraphFuncOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::ParseResult GraphFuncOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  return parseGraphFunc(parser, result);
}

void GraphFuncOp::print(::mlir::OpAsmPrinter &p) {
  return printGraphFunc(*this, p);
}

::mlir::LogicalResult GraphFuncOp::verify() {
  {
    auto tblgen_sym_name = (*this)->getAttr(sym_nameAttrName());
    if (!tblgen_sym_name)
      return emitOpError("requires attribute 'sym_name'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops0(*this, tblgen_sym_name, "sym_name")))
      return ::mlir::failure();
  }
  {
    auto tblgen_type = (*this)->getAttr(typeAttrName());
    if (!tblgen_type)
      return emitOpError("requires attribute 'type'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops2(*this, tblgen_type, "type")))
      return ::mlir::failure();
  }
  {
    auto tblgen_generic = (*this)->getAttr(genericAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops3(*this, tblgen_generic, "generic")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_ops0(*this, region, "body", index++)))
        return ::mlir::failure();
  }
  return verifyGraphFunc(*this);
}

void GraphFuncOp::getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context) {
  results.add(canonicalize);
}

} // namespace tfg
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tfg::GraphFuncOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GraphOp definitions
//===----------------------------------------------------------------------===//

GraphOpAdaptor::GraphOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

GraphOpAdaptor::GraphOpAdaptor(GraphOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange GraphOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> GraphOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange GraphOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr GraphOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::tf_type::VersionAttr GraphOpAdaptor::version() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::tf_type::VersionAttr attr = odsAttrs.get("version").cast<::mlir::tf_type::VersionAttr>();
  return attr;
}

::mlir::RegionRange GraphOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &GraphOpAdaptor::nodes() {
  return *odsRegions[0];
}

::mlir::LogicalResult GraphOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_version = odsAttrs.get("version");
    if (!tblgen_version)
      return emitError(loc, "'tfg.graph' op ""requires attribute 'version'");

    if (tblgen_version && !((tblgen_version.isa<::mlir::tf_type::VersionAttr>())))
      return emitError(loc, "'tfg.graph' op ""attribute 'version' failed to satisfy constraint: An Attribute describing the version for a TensorFlow Graph");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> GraphOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range GraphOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> GraphOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range GraphOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Region &GraphOp::nodes() {
  return (*this)->getRegion(0);
}

::mlir::tf_type::VersionAttr GraphOp::versionAttr() {
  return (*this)->getAttr(versionAttrName()).cast<::mlir::tf_type::VersionAttr>();
}

VersionAttr GraphOp::version() {
  auto attr = versionAttr();
  return attr.cast<VersionAttr>();
}

void GraphOp::versionAttr(::mlir::tf_type::VersionAttr attr) {
  (*this)->setAttr(versionAttrName(), attr);
}

void GraphOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::tf_type::VersionAttr version) {
  odsState.addAttribute(versionAttrName(odsState.name), version);
  (void)odsState.addRegion();
}

void GraphOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::tf_type::VersionAttr version) {
  odsState.addAttribute(versionAttrName(odsState.name), version);
  (void)odsState.addRegion();
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void GraphOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::ParseResult GraphOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  return parseGraphOp(parser, result);
}

void GraphOp::print(::mlir::OpAsmPrinter &p) {
  printGraphOp(p, *this);
}

::mlir::LogicalResult GraphOp::verify() {
  {
    auto tblgen_version = (*this)->getAttr(versionAttrName());
    if (!tblgen_version)
      return emitOpError("requires attribute 'version'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_ops4(*this, tblgen_version, "version")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_ops1(*this, region, "nodes", index++)))
        return ::mlir::failure();
  }
  return verifyGraph(*this);
}

} // namespace tfg
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tfg::GraphOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::ReturnOp definitions
//===----------------------------------------------------------------------===//

ReturnOpAdaptor::ReturnOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ReturnOpAdaptor::ReturnOpAdaptor(ReturnOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ReturnOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ReturnOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
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

::mlir::ValueRange ReturnOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange ReturnOpAdaptor::operands() {
  return getODSOperands(0);
}

::mlir::DictionaryAttr ReturnOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult ReturnOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReturnOp::getODSOperandIndexAndLength(unsigned index) {
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

::mlir::Operation::operand_range ReturnOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range ReturnOp::operands() {
  return getODSOperands(0);
}

::mlir::MutableOperandRange ReturnOp::operandsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> ReturnOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ReturnOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void ReturnOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState) {
 build(odsBuilder, odsState, llvm::None); 
}

void ReturnOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands) {
  odsState.addOperands(operands);
}

void ReturnOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::ParseResult ReturnOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  return parseCustomTfOp(parser, result);
}

void ReturnOp::print(::mlir::OpAsmPrinter &p) {
  printCustomTfOp(*this, p);
}

::mlir::LogicalResult ReturnOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ops1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

void ReturnOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace tfg
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tfg::ReturnOp)


#endif  // GET_OP_CLASSES

