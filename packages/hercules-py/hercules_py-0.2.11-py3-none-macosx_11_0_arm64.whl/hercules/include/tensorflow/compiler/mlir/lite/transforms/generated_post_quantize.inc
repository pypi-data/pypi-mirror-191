/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/post_quantize_patterns.td:24
*/
struct GeneratedConvert0 : public ::mlir::RewritePattern {
  GeneratedConvert0(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tfl.quantize", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qt;
    ::mlir::TFL::QuantizeOp op;
    ::mlir::Operation::operand_range in(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TFL::QuantizeOp>(op0); (void)castedOp0;
    op = castedOp0;
    in = castedOp0.getODSOperands(0);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::TypeAttr>("qtype");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tfl.quantize' to have attribute 'qtype' of type '::mlir::TypeAttr'";
        });
      }
      qt = tblgen_attr;
    }
    if (!(((*op.getODSResults(0).begin()).use_empty()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities '' failed to satisfy constraint: 'has no use'";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ in }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/post_quantize_patterns.td:25
*/
struct GeneratedConvert1 : public ::mlir::RewritePattern {
  GeneratedConvert1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tfl.dequantize", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TFL::DequantizeOp op;
    ::mlir::Operation::operand_range in(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TFL::DequantizeOp>(op0); (void)castedOp0;
    op = castedOp0;
    in = castedOp0.getODSOperands(0);
    if (!(((*op.getODSResults(0).begin()).use_empty()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities '' failed to satisfy constraint: 'has no use'";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ in }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<GeneratedConvert0>(patterns.getContext());
  patterns.add<GeneratedConvert1>(patterns.getContext());
}
