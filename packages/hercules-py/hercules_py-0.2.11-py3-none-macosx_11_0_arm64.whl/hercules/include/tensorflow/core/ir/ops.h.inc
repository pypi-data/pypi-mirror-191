/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace tfg {
class GetResultOp;
} // namespace tfg
} // namespace mlir
namespace mlir {
namespace tfg {
class GraphFuncOp;
} // namespace tfg
} // namespace mlir
namespace mlir {
namespace tfg {
class GraphOp;
} // namespace tfg
} // namespace mlir
namespace mlir {
namespace tfg {
class ReturnOp;
} // namespace tfg
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GetResultOp declarations
//===----------------------------------------------------------------------===//

class GetResultOpAdaptor {
public:
  GetResultOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  GetResultOpAdaptor(GetResultOp &op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value value();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr name();
  ::mlir::IntegerAttr number();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class GetResultOp : public ::mlir::Op<GetResultOp, ::mlir::OpTrait::ZeroRegion, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::tf_type::OpaqueTensorType>::Impl, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::OneOperand, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::InferTypeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = GetResultOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("name"), ::llvm::StringRef("number")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr nameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr numberAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr numberAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tfg.get_result");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value value();
  ::mlir::MutableOperandRange valueMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value result();
  ::mlir::StringAttr nameAttr();
  ::llvm::StringRef name();
  ::mlir::IntegerAttr numberAttr();
  uint32_t number();
  void nameAttr(::mlir::StringAttr attr);
  void numberAttr(::mlir::IntegerAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::StringAttr name, ::mlir::IntegerAttr number);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value value, ::llvm::StringRef name, uint32_t number);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::llvm::StringRef name, uint32_t number);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::llvm::StringRef name, uint32_t number);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verify();
  static ::mlir::LogicalResult inferReturnTypes(::mlir::MLIRContext *context, ::llvm::Optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes);
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace tfg
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tfg::GetResultOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GraphFuncOp declarations
//===----------------------------------------------------------------------===//

class GraphFuncOpAdaptor {
public:
  GraphFuncOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  GraphFuncOpAdaptor(GraphFuncOp &op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr sym_name();
  ::mlir::TypeAttr type();
  ::mlir::UnitAttr generic();
  ::mlir::RegionRange getRegions();
  ::mlir::Region &body();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class GraphFuncOp : public ::mlir::Op<GraphFuncOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::ZeroResult, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::ZeroOperands, ::mlir::RegionKindInterface::Trait, ::mlir::OpTrait::HasOnlyGraphRegion, ::mlir::OpTrait::SingleBlock, ::mlir::CallableOpInterface::Trait, ::mlir::OpTrait::FunctionLike, ::mlir::OpTrait::IsIsolatedFromAbove, ::mlir::SymbolOpInterface::Trait, ::mlir::OpAsmOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = GraphFuncOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("sym_name"), ::llvm::StringRef("type"), ::llvm::StringRef("generic")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr sym_nameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr sym_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr typeAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr typeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr genericAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr genericAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tfg.func");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Region &body();
  ::mlir::StringAttr sym_nameAttr();
  ::llvm::StringRef sym_name();
  ::mlir::TypeAttr typeAttr();
  ::mlir::Type type();
  ::mlir::UnitAttr genericAttr();
  bool generic();
  void sym_nameAttr(::mlir::StringAttr attr);
  void typeAttr(::mlir::TypeAttr attr);
  void genericAttr(::mlir::UnitAttr attr);
  ::mlir::Attribute removeGenericAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::StringAttr sym_name, ::mlir::TypeAttr type, /*optional*/::mlir::UnitAttr generic);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr sym_name, ::mlir::TypeAttr type, /*optional*/::mlir::UnitAttr generic);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::llvm::StringRef sym_name, ::mlir::Type type, /*optional*/bool generic);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef sym_name, ::mlir::Type type, /*optional*/bool generic);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verify();
  static ::mlir::LogicalResult canonicalize(GraphFuncOp op, ::mlir::PatternRewriter &rewriter);
  static void getCanonicalizationPatterns(::mlir::RewritePatternSet &results, ::mlir::MLIRContext *context);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
    using SingleBlock::getBody;

    FlatSymbolRefAttr getGradient() {
      return (*this)->getAttrOfType<FlatSymbolRefAttr>("gradient");
    }

    TFGraphDialect *getDialect() {
      return cast<TFGraphDialect>((*this)->getDialect());
    }

    // Returns true if this function is marked for JIT compilation.
    bool isMarkedForCompilation();

    // Return the function called by this operation if this operation is a call
    // and the function exists in the symbol_table, otherwise return null.
    static GraphFuncOp getCalledFunction(Operation *op,
                                         SymbolTable &symbol_table);

    //===------------------------------------------------------------------===//
    // OpAsmOpInterface
    //===------------------------------------------------------------------===//

    // This will filter the `tfg.` prefix in front of operations inside the
    // func body.
    static StringRef getDefaultDialect() {
      return "tfg";
    }

    /// Get a special name to use when printing block arguments.
    void getAsmBlockArgumentNames(Region &region, OpAsmSetValueNameFn set_name_fn);

    //===------------------------------------------------------------------===//
    // CallableOpInterface
    //===------------------------------------------------------------------===//

    // Returns the region on the current operation that is callable. This may
    // return null in the case of an external callable object, e.g. an external
    // function.
    Region *getCallableRegion() {
      return isExternal() ? nullptr : &FunctionLike::getBody();
    }

    // Returns the results types that the callable region produces when
    // executed.
    ArrayRef<Type> getCallableResults() { return getType().getResults(); }

    //===------------------------------------------------------------------===//
    // SymbolOpInterface Methods
    //===------------------------------------------------------------------===//

    bool isDeclaration() { return isExternal(); }

  private:
    // This trait needs access to the hooks defined below.
    friend class OpTrait::FunctionLike<GraphFuncOp>;

    // Returns the number of arguments. Hook for OpTrait::FunctionLike.
    unsigned getNumFuncArguments() { return getType().getNumInputs(); }

    // Returns the number of results. Hook for OpTrait::FunctionLike.
    unsigned getNumFuncResults() { return getType().getNumResults(); }

    // Hook for OpTrait::FunctionLike, called after verifying that the 'type'
    // attribute is present and checks if it holds a function type. Ensures
    // getType, getNumFuncArguments, and getNumFuncResults can be called safely
    LogicalResult verifyType();

    // Hook for OpTrait::FunctionLike, called after verifying the function
    // type and the presence of the (potentially empty) function body.
    LogicalResult verifyBody();
};
} // namespace tfg
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tfg::GraphFuncOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::GraphOp declarations
//===----------------------------------------------------------------------===//

class GraphOpAdaptor {
public:
  GraphOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  GraphOpAdaptor(GraphOp &op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::tf_type::VersionAttr version();
  ::mlir::RegionRange getRegions();
  ::mlir::Region &nodes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class GraphOp : public ::mlir::Op<GraphOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::ZeroResult, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::HasOnlyGraphRegion, ::mlir::OpTrait::SingleBlock, ::mlir::OpTrait::IsIsolatedFromAbove, ::mlir::OpAsmOpInterface::Trait, ::mlir::OpTrait::NoTerminator, ::mlir::RegionKindInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = GraphOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("version")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr versionAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr versionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tfg.graph");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Region &nodes();
  ::mlir::tf_type::VersionAttr versionAttr();
  VersionAttr version();
  void versionAttr(::mlir::tf_type::VersionAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::tf_type::VersionAttr version);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::tf_type::VersionAttr version);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verify();
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  TFGraphDialect *getDialect() {
    return cast<TFGraphDialect>((*this)->getDialect());
  }

  // Override the getOps() inherited from the OneRegion trait to return a
  // range of TFOp instead of the generic mlir::Operation.
  auto getOps() { return getRegion().template getOps<TFOp>(); }

  //===------------------------------------------------------------------===//
  // OpAsmOpInterface
  //===------------------------------------------------------------------===//

  // This will filter the `tfg.` prefix in front of operations inside the
  // graph body.
  static StringRef getDefaultDialect() {
    return "tfg";
  }
};
} // namespace tfg
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tfg::GraphOp)

namespace mlir {
namespace tfg {

//===----------------------------------------------------------------------===//
// ::mlir::tfg::ReturnOp declarations
//===----------------------------------------------------------------------===//

class ReturnOpAdaptor {
public:
  ReturnOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ReturnOpAdaptor(ReturnOp &op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange operands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class ReturnOp : public ::mlir::Op<ReturnOp, ::mlir::OpTrait::ZeroRegion, ::mlir::OpTrait::ZeroResult, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::VariadicOperands, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::HasParent<GraphFuncOp>::Impl, ::mlir::OpTrait::ReturnLike, ::mlir::OpTrait::IsTerminator> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ReturnOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tfg.return");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range operands();
  ::mlir::MutableOperandRange operandsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verify();
  void getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace tfg
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tfg::ReturnOp)


#endif  // GET_OP_CLASSES

