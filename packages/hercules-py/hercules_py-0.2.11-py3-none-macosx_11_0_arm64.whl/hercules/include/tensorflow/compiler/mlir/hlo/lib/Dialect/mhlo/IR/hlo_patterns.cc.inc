/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

static ::mlir::LogicalResult static_dag_matcher_0(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::Operation::operand_range &x) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::shape::ShapeOfOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::shape::ShapeOfOp type";
    });
  }
  x = castedOp1.getODSOperands(0);
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_1(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::Operation::operand_range &x) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::shape::ToExtentTensorOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::shape::ToExtentTensorOp type";
    });
  }
  {
    auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
    if (!(op2)){
      return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
        diag << "There's no operation that defines operand 0 of castedOp1";
      });
    }
    if(failed(static_dag_matcher_0(rewriter, op2, tblgen_ops, x))) {
      return ::mlir::failure();
    }
    tblgen_ops.push_back(op2);
  }
  return ::mlir::success();
}

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:26
*/
struct DynamicBroadcastToOwnShape_1 : public ::mlir::RewritePattern {
  DynamicBroadcastToOwnShape_1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_broadcast_in_dim", 3, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::DynamicBroadcastInDimOp op;
    ::mlir::Operation::operand_range x(op0->getOperands());
    ::mlir::Operation::operand_range x0(op0->getOperands());
    ::mlir::DenseIntElementsAttr attr;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicBroadcastInDimOp>(op0); (void)castedOp0;
    op = castedOp0;
    x = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_1(rewriter, op1, tblgen_ops, x0))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.dynamic_broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
        });
      }
      attr = tblgen_attr;
    }
    if (!(*x.begin() == *x0.begin())){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "Operands 'x' and 'x0' must be equal";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ x }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:30
*/
struct DynamicBroadcastToOwnShape_2 : public ::mlir::RewritePattern {
  DynamicBroadcastToOwnShape_2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_broadcast_in_dim", 2, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::DynamicBroadcastInDimOp op;
    ::mlir::Operation::operand_range x(op0->getOperands());
    ::mlir::Operation::operand_range x0(op0->getOperands());
    ::mlir::DenseIntElementsAttr attr;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicBroadcastInDimOp>(op0); (void)castedOp0;
    op = castedOp0;
    x = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_0(rewriter, op1, tblgen_ops, x0))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.dynamic_broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
        });
      }
      attr = tblgen_attr;
    }
    if (!(*x.begin() == *x0.begin())){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "Operands 'x' and 'x0' must be equal";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ x }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:33
*/
struct DynamicBroadcastToOwnShape_3 : public ::mlir::RewritePattern {
  DynamicBroadcastToOwnShape_3(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_broadcast_in_dim", 4, context, {"tensor.cast"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::DynamicBroadcastInDimOp op;
    ::mlir::Operation::operand_range x(op0->getOperands());
    ::mlir::Operation::operand_range x0(op0->getOperands());
    ::mlir::DenseIntElementsAttr attr;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicBroadcastInDimOp>(op0); (void)castedOp0;
    op = castedOp0;
    x = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::tensor::CastOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::tensor::CastOp type";
        });
      }
      {
        auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 0 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_1(rewriter, op2, tblgen_ops, x0))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.dynamic_broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
        });
      }
      attr = tblgen_attr;
    }
    if (!(*x.begin() == *x0.begin())){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "Operands 'x' and 'x0' must be equal";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::tensor::CastOp tblgen_CastOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*x.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_CastOp_0 = rewriter.create<::mlir::tensor::CastOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_CastOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:37
*/
struct DynamicBroadcastToOwnShape_4 : public ::mlir::RewritePattern {
  DynamicBroadcastToOwnShape_4(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_broadcast_in_dim", 3, context, {"tensor.cast"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::DynamicBroadcastInDimOp op;
    ::mlir::Operation::operand_range x(op0->getOperands());
    ::mlir::Operation::operand_range x0(op0->getOperands());
    ::mlir::DenseIntElementsAttr attr;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicBroadcastInDimOp>(op0); (void)castedOp0;
    op = castedOp0;
    x = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::tensor::CastOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::tensor::CastOp type";
        });
      }
      {
        auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 0 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_0(rewriter, op2, tblgen_ops, x0))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.dynamic_broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
        });
      }
      attr = tblgen_attr;
    }
    if (!(*x.begin() == *x0.begin())){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "Operands 'x' and 'x0' must be equal";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::tensor::CastOp tblgen_CastOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*x.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_CastOp_0 = rewriter.create<::mlir::tensor::CastOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_CastOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:56
*/
struct EliminateIdentityConvert : public ::mlir::RewritePattern {
  EliminateIdentityConvert(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.convert", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::ConvertOp res;
    ::mlir::Operation::operand_range src(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::ConvertOp>(op0); (void)castedOp0;
    res = castedOp0;
    src = castedOp0.getODSOperands(0);
    if (!(((*res.getODSResults(0).begin()).getType() == (*src.begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'res, src' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ src }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:66
*/
struct EliminateIdentityReshape : public ::mlir::RewritePattern {
  EliminateIdentityReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.reshape", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::ReshapeOp res;
    ::mlir::Operation::operand_range src(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::ReshapeOp>(op0); (void)castedOp0;
    res = castedOp0;
    src = castedOp0.getODSOperands(0);
    if (!(((*res.getODSResults(0).begin()).getType() == (*src.begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'res, src' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ src }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:61
*/
struct EliminateRedundantReshape : public ::mlir::RewritePattern {
  EliminateRedundantReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.reshape", 2, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::ReshapeOp res;
    ::mlir::Operation::operand_range src(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::ReshapeOp>(op0); (void)castedOp0;
    res = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ReshapeOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ReshapeOp type";
        });
      }
      src = castedOp1.getODSOperands(0);
      tblgen_ops.push_back(op1);
    }
    if (!(((*res.getODSResults(0).begin()).getType() == (*src.begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'res, src' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ src }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:51
*/
struct IdentityBroadcastInDimReshape : public ::mlir::RewritePattern {
  IdentityBroadcastInDimReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.reshape", 2, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::ReshapeOp op;
    ::mlir::DenseIntElementsAttr dims;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::ReshapeOp>(op0); (void)castedOp0;
    op = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::BroadcastInDimOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::BroadcastInDimOp type";
        });
      }
      input = castedOp1.getODSOperands(0);
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
          });
        }
        dims = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    if (!(((*input.begin()).getType() == (*op.getODSResults(0).begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input, op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ input }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:46
*/
struct IdentityBroadcastReshape : public ::mlir::RewritePattern {
  IdentityBroadcastReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.reshape", 2, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::mhlo::ReshapeOp op;
    ::mlir::DenseIntElementsAttr dims;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::ReshapeOp>(op0); (void)castedOp0;
    op = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::BroadcastOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::BroadcastOp type";
        });
      }
      input = castedOp1.getODSOperands(0);
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_sizes");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.broadcast' to have attribute 'broadcast_sizes' of type '::mlir::DenseIntElementsAttr'";
          });
        }
        dims = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    if (!(((*input.begin()).getType() == (*op.getODSResults(0).begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input, op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ input }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/hlo_patterns.td:41
*/
struct ShapeOfDynamicReshape : public ::mlir::RewritePattern {
  ShapeOfDynamicReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("shape.shape_of", 2, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range shape(op0->getOperands());
    ::mlir::shape::ShapeOfOp op;
    ::mlir::Operation::operand_range x(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::shape::ShapeOfOp>(op0); (void)castedOp0;
    op = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::DynamicReshapeOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::DynamicReshapeOp type";
        });
      }
      x = castedOp1.getODSOperands(0);
      shape = castedOp1.getODSOperands(1);
      tblgen_ops.push_back(op1);
    }
    if (!(((*shape.begin()).getType() == (*op.getODSResults(0).begin()).getType()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'shape, op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ shape }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<DynamicBroadcastToOwnShape_1>(patterns.getContext());
  patterns.add<DynamicBroadcastToOwnShape_2>(patterns.getContext());
  patterns.add<DynamicBroadcastToOwnShape_3>(patterns.getContext());
  patterns.add<DynamicBroadcastToOwnShape_4>(patterns.getContext());
  patterns.add<EliminateIdentityConvert>(patterns.getContext());
  patterns.add<EliminateIdentityReshape>(patterns.getContext());
  patterns.add<EliminateRedundantReshape>(patterns.getContext());
  patterns.add<IdentityBroadcastInDimReshape>(patterns.getContext());
  patterns.add<IdentityBroadcastReshape>(patterns.getContext());
  patterns.add<ShapeOfDynamicReshape>(patterns.getContext());
}
