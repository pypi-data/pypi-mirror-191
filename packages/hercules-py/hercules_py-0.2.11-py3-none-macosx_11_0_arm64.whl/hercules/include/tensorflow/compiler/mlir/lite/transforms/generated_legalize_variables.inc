/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/legalize_variables.td:36
*/
struct LegalizeAssignVariable : public ::mlir::RewritePattern {
  LegalizeAssignVariable(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.AssignVariableOp", 1, context, {"tfl.assign_variable"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::BoolAttr validate_shape;
    ::mlir::Operation::operand_range value(op0->getOperands());
    ::mlir::Operation::operand_range resource(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::AssignVariableOp>(op0); (void)castedOp0;
    resource = castedOp0.getODSOperands(0);
    value = castedOp0.getODSOperands(1);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("validate_shape");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
      validate_shape = tblgen_attr;
    }
    if (!((IsSupportedElementType((*value.begin()).getType().cast<ShapedType>())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'value' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::mlir::TFL::AssignVariableOp tblgen_AssignVariableOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*resource.begin()));
      tblgen_values.push_back((*value.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      tblgen_AssignVariableOp_0 = rewriter.create<::mlir::TFL::AssignVariableOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }
    rewriter.eraseOp(op0);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/legalize_variables.td:31
*/
struct LegalizeReadVariable : public ::mlir::RewritePattern {
  LegalizeReadVariable(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.ReadVariableOp", 1, context, {"tfl.read_variable"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range resource(op0->getOperands());
    ::mlir::TF::ReadVariableOp result;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::ReadVariableOp>(op0); (void)castedOp0;
    result = castedOp0;
    resource = castedOp0.getODSOperands(0);
    if (!((HasSupportedElementType((*result.getODSResults(0).begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'result' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TFL::ReadVariableOp tblgen_ReadVariableOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*resource.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_ReadVariableOp_0 = rewriter.create<::mlir::TFL::ReadVariableOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_ReadVariableOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/legalize_variables.td:26
*/
struct LegalizeVarHandle : public ::mlir::RewritePattern {
  LegalizeVarHandle(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.VarHandleOp", 1, context, {"tfl.var_handle"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::StringAttr shared_name;
    ::mlir::TF::VarHandleOp result;
    ::mlir::StringAttr container;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::VarHandleOp>(op0); (void)castedOp0;
    result = castedOp0;
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::StringAttr>("container");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getStringAttr("");
      container = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::StringAttr>("shared_name");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getStringAttr("");
      shared_name = tblgen_attr;
    }
    if (!((HasSupportedElementType((*result.getODSResults(0).begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'result' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TFL::VarHandleOp tblgen_VarHandleOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      if (auto tmpAttr = container) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("container"), tmpAttr);
      }
      if (auto tmpAttr = shared_name) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("shared_name"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_VarHandleOp_0 = rewriter.create<::mlir::TFL::VarHandleOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_VarHandleOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<LegalizeAssignVariable>(patterns.getContext());
  patterns.add<LegalizeReadVariable>(patterns.getContext());
  patterns.add<LegalizeVarHandle>(patterns.getContext());
}
