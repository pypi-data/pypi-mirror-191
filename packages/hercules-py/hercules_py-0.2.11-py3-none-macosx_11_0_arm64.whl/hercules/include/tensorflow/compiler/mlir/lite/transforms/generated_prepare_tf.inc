/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns0(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!(((attr.isa<::mlir::FloatAttr>())) && ((attr.cast<::mlir::FloatAttr>().getType().isF32())))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": 32-bit float attribute";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns1(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((attr == rewriter.getBoolAttr(false)))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": constant attribute false";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns2(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((attr.cast<ElementsAttr>().getType().getElementType().isF32()))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": float constant tensor";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns3(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((attr == ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef({0})).cast<::mlir::DenseIntElementsAttr>()))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": constant attribute {0}";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns4(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((!attr.isa<OpaqueElementsAttr>()))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": non-opaque constant tensor";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns5(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((attr == rewriter.getStringAttr("NHWC")))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": constant attribute \"NHWC\"";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_prepare_patterns6(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((attr == rewriter.getBoolAttr(true)))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": constant attribute true";
    });
  }
  return ::mlir::success();
}
static ::mlir::LogicalResult static_dag_matcher_0(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::arith::ConstantOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::arith::ConstantOp type";
    });
  }
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'arith.constant' to have attribute 'value' of type '::mlir::Attribute'";
      });
    }
    if(failed(__mlir_ods_local_attr_constraint_prepare_patterns3(rewriter, op0, tblgen_attr, "op 'arith.constant' attribute 'value' failed to satisfy constraint: 'constant attribute {0}'"))) {
      return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_1(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::TypeAttr &qtype, ::mlir::Operation::operand_range &input) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TFL::DequantizeOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TFL::DequantizeOp type";
    });
  }
  {
    auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
    if (!(op2)){
      return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
        diag << "There's no operation that defines operand 0 of castedOp1";
      });
    }
    auto castedOp2 = ::llvm::dyn_cast<::mlir::TFL::QuantizeOp>(op2); (void)castedOp2;
    if (!(castedOp2)){
      return rewriter.notifyMatchFailure(op2, [&](::mlir::Diagnostic &diag) {
        diag << "castedOp2 is not ::mlir::TFL::QuantizeOp type";
      });
    }
    input = castedOp2.getODSOperands(0);
    {
      auto tblgen_attr = op2->getAttrOfType<::mlir::TypeAttr>("qtype");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op2, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tfl.quantize' to have attribute 'qtype' of type '::mlir::TypeAttr'";
        });
      }
      qtype = tblgen_attr;
    }
    tblgen_ops.push_back(op2);
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_2(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::Attribute &bias) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::arith::ConstantOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::arith::ConstantOp type";
    });
  }
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'arith.constant' to have attribute 'value' of type '::mlir::Attribute'";
      });
    }
    if(failed(__mlir_ods_local_attr_constraint_prepare_patterns2(rewriter, op0, tblgen_attr, "op 'arith.constant' attribute 'value' failed to satisfy constraint: 'float constant tensor'"))) {
      return ::mlir::failure();
    }
    bias = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_3(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::Attribute &value) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::arith::ConstantOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::arith::ConstantOp type";
    });
  }
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'arith.constant' to have attribute 'value' of type '::mlir::Attribute'";
      });
    }
    if(failed(__mlir_ods_local_attr_constraint_prepare_patterns2(rewriter, op0, tblgen_attr, "op 'arith.constant' attribute 'value' failed to satisfy constraint: 'float constant tensor'"))) {
      return ::mlir::failure();
    }
    value = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_4(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::TypeAttr &qtype, ::mlir::Operation::operand_range &input, ::mlir::Operation::operand_range &shape, ::mlir::TF::ReshapeOp &old_value) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ReshapeOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::ReshapeOp type";
    });
  }
  old_value = castedOp1;
  {
    auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
    if (!(op2)){
      return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
        diag << "There's no operation that defines operand 0 of castedOp1";
      });
    }
    if(failed(static_dag_matcher_1(rewriter, op2, tblgen_ops, qtype, input))) {
      return ::mlir::failure();
    }
    tblgen_ops.push_back(op2);
  }
  shape = castedOp1.getODSOperands(1);
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_5(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::Operation::operand_range &max, ::mlir::IntegerAttr &num_bits, ::mlir::Operation::operand_range &min, ::mlir::Operation::operand_range &input, ::mlir::BoolAttr &narrow_range) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::FakeQuantWithMinMaxVarsOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::FakeQuantWithMinMaxVarsOp type";
    });
  }
  input = castedOp1.getODSOperands(0);
  min = castedOp1.getODSOperands(1);
  max = castedOp1.getODSOperands(2);
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::IntegerAttr>("num_bits");(void)tblgen_attr;
    if (!tblgen_attr) tblgen_attr = rewriter.getIntegerAttr(rewriter.getIntegerType(64), 8);
    num_bits = tblgen_attr;
  }
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("narrow_range");(void)tblgen_attr;
    if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
    narrow_range = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_6(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::TypeAttr &qtype, ::mlir::Operation::operand_range &perm, ::mlir::Operation::operand_range &input, ::mlir::TF::TransposeOp &old_value) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::TransposeOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::TransposeOp type";
    });
  }
  old_value = castedOp1;
  {
    auto *op2 = (*castedOp1.getODSOperands(0).begin()).getDefiningOp();
    if (!(op2)){
      return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
        diag << "There's no operation that defines operand 0 of castedOp1";
      });
    }
    if(failed(static_dag_matcher_1(rewriter, op2, tblgen_ops, qtype, input))) {
      return ::mlir::failure();
    }
    tblgen_ops.push_back(op2);
  }
  perm = castedOp1.getODSOperands(1);
  return ::mlir::success();
}

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:36
*/
struct ConvertBatchNormWithGlobalNormalization_1 : public ::mlir::RewritePattern {
  ConvertBatchNormWithGlobalNormalization_1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.BatchNormWithGlobalNormalization", 1, context, {"tf.Add", "tf.Const", "tf.Mul", "tf.Rsqrt", "tf.Sub"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::BoolAttr scale_after_normalization;
    ::mlir::Operation::operand_range beta(op0->getOperands());
    ::mlir::Operation::operand_range m(op0->getOperands());
    ::mlir::Operation::operand_range v(op0->getOperands());
    ::mlir::Operation::operand_range gamma(op0->getOperands());
    ::mlir::FloatAttr variance_epsilon;
    ::mlir::Operation::operand_range t(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::BatchNormWithGlobalNormalizationOp>(op0); (void)castedOp0;
    t = castedOp0.getODSOperands(0);
    m = castedOp0.getODSOperands(1);
    v = castedOp0.getODSOperands(2);
    beta = castedOp0.getODSOperands(3);
    gamma = castedOp0.getODSOperands(4);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::FloatAttr>("variance_epsilon");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.BatchNormWithGlobalNormalization' to have attribute 'variance_epsilon' of type '::mlir::FloatAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns0(rewriter, op0, tblgen_attr, "op 'tf.BatchNormWithGlobalNormalization' attribute 'variance_epsilon' failed to satisfy constraint: '32-bit float attribute'"))) {
        return ::mlir::failure();
      }
      variance_epsilon = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("scale_after_normalization");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.BatchNormWithGlobalNormalization' to have attribute 'scale_after_normalization' of type '::mlir::BoolAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns1(rewriter, op0, tblgen_attr, "op 'tf.BatchNormWithGlobalNormalization' attribute 'scale_after_normalization' failed to satisfy constraint: 'constant attribute false'"))) {
        return ::mlir::failure();
      }
      scale_after_normalization = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ConstOp tblgen_ConstOp_0;
    {
      tblgen_ConstOp_0 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        /*value=*/variance_epsilon
      );
    }
    ::mlir::TF::AddOp tblgen_AddOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*v.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_0.getODSResults(0).begin());
      tblgen_AddOp_1 = rewriter.create<::mlir::TF::AddOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::RsqrtOp rsqrt;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_1.getODSResults(0).begin()));
      rsqrt = rewriter.create<::mlir::TF::RsqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TF::MulOp tblgen_MulOp_2;
    {
      ::mlir::Value tblgen_value_0 = (*t.begin());
      ::mlir::Value tblgen_value_1 = (*rsqrt.getODSResults(0).begin());
      tblgen_MulOp_2 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_3;
    {
      ::mlir::Value tblgen_value_0 = (*m.begin());
      ::mlir::Value tblgen_value_1 = (*rsqrt.getODSResults(0).begin());
      tblgen_MulOp_3 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::SubOp tblgen_SubOp_4;
    {
      ::mlir::Value tblgen_value_0 = (*beta.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_3.getODSResults(0).begin());
      tblgen_SubOp_4 = rewriter.create<::mlir::TF::SubOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::AddOp tblgen_AddOp_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_2.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_SubOp_4.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_AddOp_5 = rewriter.create<::mlir::TF::AddOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_AddOp_5.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:42
*/
struct ConvertBatchNormWithGlobalNormalization_2 : public ::mlir::RewritePattern {
  ConvertBatchNormWithGlobalNormalization_2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.BatchNormWithGlobalNormalization", 1, context, {"tf.Add", "tf.Const", "tf.Mul", "tf.Rsqrt", "tf.Sub"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::BoolAttr scale_after_normalization;
    ::mlir::Operation::operand_range beta(op0->getOperands());
    ::mlir::Operation::operand_range m(op0->getOperands());
    ::mlir::Operation::operand_range v(op0->getOperands());
    ::mlir::Operation::operand_range gamma(op0->getOperands());
    ::mlir::FloatAttr variance_epsilon;
    ::mlir::Operation::operand_range t(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::BatchNormWithGlobalNormalizationOp>(op0); (void)castedOp0;
    t = castedOp0.getODSOperands(0);
    m = castedOp0.getODSOperands(1);
    v = castedOp0.getODSOperands(2);
    beta = castedOp0.getODSOperands(3);
    gamma = castedOp0.getODSOperands(4);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::FloatAttr>("variance_epsilon");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.BatchNormWithGlobalNormalization' to have attribute 'variance_epsilon' of type '::mlir::FloatAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns0(rewriter, op0, tblgen_attr, "op 'tf.BatchNormWithGlobalNormalization' attribute 'variance_epsilon' failed to satisfy constraint: '32-bit float attribute'"))) {
        return ::mlir::failure();
      }
      variance_epsilon = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("scale_after_normalization");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.BatchNormWithGlobalNormalization' to have attribute 'scale_after_normalization' of type '::mlir::BoolAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns6(rewriter, op0, tblgen_attr, "op 'tf.BatchNormWithGlobalNormalization' attribute 'scale_after_normalization' failed to satisfy constraint: 'constant attribute true'"))) {
        return ::mlir::failure();
      }
      scale_after_normalization = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ConstOp tblgen_ConstOp_0;
    {
      tblgen_ConstOp_0 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        /*value=*/variance_epsilon
      );
    }
    ::mlir::TF::AddOp tblgen_AddOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*v.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_0.getODSResults(0).begin());
      tblgen_AddOp_1 = rewriter.create<::mlir::TF::AddOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::RsqrtOp tblgen_RsqrtOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_1.getODSResults(0).begin()));
      tblgen_RsqrtOp_2 = rewriter.create<::mlir::TF::RsqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TF::MulOp mul;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_RsqrtOp_2.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*gamma.begin());
      mul = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_3;
    {
      ::mlir::Value tblgen_value_0 = (*t.begin());
      ::mlir::Value tblgen_value_1 = (*mul.getODSResults(0).begin());
      tblgen_MulOp_3 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_4;
    {
      ::mlir::Value tblgen_value_0 = (*m.begin());
      ::mlir::Value tblgen_value_1 = (*mul.getODSResults(0).begin());
      tblgen_MulOp_4 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::SubOp tblgen_SubOp_5;
    {
      ::mlir::Value tblgen_value_0 = (*beta.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_4.getODSResults(0).begin());
      tblgen_SubOp_5 = rewriter.create<::mlir::TF::SubOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::AddOp tblgen_AddOp_6;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_3.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_SubOp_5.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_AddOp_6 = rewriter.create<::mlir::TF::AddOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_AddOp_6.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/tensorflow/transforms/optimize.td:108
*/
struct ConvertCastComplexFFTToRFFT : public ::mlir::RewritePattern {
  ConvertCastComplexFFTToRFFT(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.FFT", 2, context, {"arith.constant", "tf.RFFT"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::FFTOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::CastOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::CastOp type";
        });
      }
      input = castedOp1.getODSOperands(0);
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::BoolAttr>("Truncate");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
        if(failed(__mlir_ods_local_attr_constraint_prepare_patterns1(rewriter, op1, tblgen_attr, "op 'tf.Cast' attribute 'Truncate' failed to satisfy constraint: 'constant attribute false'"))) {
          return ::mlir::failure();
        }
      }
      tblgen_ops.push_back(op1);
    }
    if (!((((*input.begin()).getType().isa<RankedTensorType>())) && ((!(*input.begin()).getType().cast<ShapedType>().isDynamicDim(   (*input.begin()).getType().cast<RankedTensorType>().getRank() - 1))))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }
    if (!((((*input.begin()).getType().isa<RankedTensorType>())) && ((!(*input.begin()).getType().cast<ShapedType>().getElementType().isa<ComplexType>())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = DenseElementsAttr::get(RankedTensorType::get({1}, rewriter.getIntegerType(32)), static_cast<int32_t>((*input.begin()).getType().cast<RankedTensorType>().getDimSize(    (*input.begin()).getType().cast<RankedTensorType>().getRank() - 1))); (void)nativeVar_0;
    ::mlir::arith::ConstantOp tblgen_ConstantOp_1;
    {
      tblgen_ConstantOp_1 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/nativeVar_0
      );
    }
    ::mlir::TF::RFFTOp tblgen_RFFTOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*tblgen_ConstantOp_1.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_RFFTOp_2 = rewriter.create<::mlir::TF::RFFTOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_RFFTOp_2.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:71
*/
struct ConvertCheckNumerics : public ::mlir::RewritePattern {
  ConvertCheckNumerics(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.CheckNumerics", 1, context, {"tf.Identity"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::mlir::StringAttr msg;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::CheckNumericsOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::StringAttr>("message");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.CheckNumerics' to have attribute 'message' of type '::mlir::StringAttr'";
        });
      }
      msg = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::IdentityOp tblgen_IdentityOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*arg.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_IdentityOp_0 = rewriter.create<::mlir::TF::IdentityOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_IdentityOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:63
*/
struct ConvertMatmulWithTranspose : public ::mlir::RewritePattern {
  ConvertMatmulWithTranspose(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.MatMul", 1, context, {"tf.Const", "tf.MatMul", "tf.Range", "tf.Rank", "tf.Sub", "tf.Transpose"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::BoolAttr bt;
    ::mlir::Operation::operand_range b(op0->getOperands());
    ::mlir::Operation::operand_range a(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MatMulOp>(op0); (void)castedOp0;
    a = castedOp0.getODSOperands(0);
    b = castedOp0.getODSOperands(1);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("transpose_a");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns6(rewriter, op0, tblgen_attr, "op 'tf.MatMul' attribute 'transpose_a' failed to satisfy constraint: 'constant attribute true'"))) {
        return ::mlir::failure();
      }
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("transpose_b");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
      bt = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::RankOp tblgen_RankOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*a.begin());
      tblgen_RankOp_0 = rewriter.create<::mlir::TF::RankOp>(odsLoc,
        /*input=*/tblgen_value_0
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_1;
    {
      tblgen_ConstOp_1 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(0)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_2;
    {
      tblgen_ConstOp_2 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(-1)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::RangeOp tblgen_RangeOp_3;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_RankOp_0.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_1.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_ConstOp_2.getODSResults(0).begin());
      tblgen_RangeOp_3 = rewriter.create<::mlir::TF::RangeOp>(odsLoc,
        /*start=*/tblgen_value_0,
        /*limit=*/tblgen_value_1,
        /*delta=*/tblgen_value_2
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_4;
    {
      tblgen_ConstOp_4 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(1)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::SubOp tblgen_SubOp_5;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_RangeOp_3.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_4.getODSResults(0).begin());
      tblgen_SubOp_5 = rewriter.create<::mlir::TF::SubOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::TransposeOp tblgen_TransposeOp_6;
    {
      ::mlir::Value tblgen_value_0 = (*a.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubOp_5.getODSResults(0).begin());
      tblgen_TransposeOp_6 = rewriter.create<::mlir::TF::TransposeOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*perm=*/tblgen_value_1
      );
    }
    ::mlir::TF::MatMulOp tblgen_MatMulOp_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_TransposeOp_6.getODSResults(0).begin()));
      tblgen_values.push_back((*b.begin()));
      if (auto tmpAttr = rewriter.getBoolAttr(false)) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("transpose_a"), tmpAttr);
      }
      if (auto tmpAttr = bt) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("transpose_b"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MatMulOp_7 = rewriter.create<::mlir::TF::MatMulOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MatMulOp_7.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:53
*/
struct ConvertMatmulWithoutTransposeToWithTranspose : public ::mlir::RewritePattern {
  ConvertMatmulWithoutTransposeToWithTranspose(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.MatMul", 1, context, {"tf.Const", "tf.MatMul", "tf.Range", "tf.Rank", "tf.Sub", "tf.Transpose"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range b(op0->getOperands());
    ::mlir::BoolAttr at;
    ::mlir::Operation::operand_range a(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MatMulOp>(op0); (void)castedOp0;
    a = castedOp0.getODSOperands(0);
    b = castedOp0.getODSOperands(1);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("transpose_a");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns1(rewriter, op0, tblgen_attr, "op 'tf.MatMul' attribute 'transpose_a' failed to satisfy constraint: 'constant attribute false'"))) {
        return ::mlir::failure();
      }
      at = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::BoolAttr>("transpose_b");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(false);
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns1(rewriter, op0, tblgen_attr, "op 'tf.MatMul' attribute 'transpose_b' failed to satisfy constraint: 'constant attribute false'"))) {
        return ::mlir::failure();
      }
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::RankOp tblgen_RankOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*b.begin());
      tblgen_RankOp_0 = rewriter.create<::mlir::TF::RankOp>(odsLoc,
        /*input=*/tblgen_value_0
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_1;
    {
      tblgen_ConstOp_1 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(0)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_2;
    {
      tblgen_ConstOp_2 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(-1)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::RangeOp tblgen_RangeOp_3;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_RankOp_0.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_1.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_ConstOp_2.getODSResults(0).begin());
      tblgen_RangeOp_3 = rewriter.create<::mlir::TF::RangeOp>(odsLoc,
        /*start=*/tblgen_value_0,
        /*limit=*/tblgen_value_1,
        /*delta=*/tblgen_value_2
      );
    }
    ::mlir::TF::ConstOp tblgen_ConstOp_4;
    {
      tblgen_ConstOp_4 = rewriter.create<::mlir::TF::ConstOp>(odsLoc,
        ::mlir::DenseElementsAttr::get(::mlir::RankedTensorType::get({}, rewriter.getIntegerType(32)), ::llvm::makeArrayRef(1)).cast<::mlir::DenseIntElementsAttr>()
      );
    }
    ::mlir::TF::SubOp tblgen_SubOp_5;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_RangeOp_3.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstOp_4.getODSResults(0).begin());
      tblgen_SubOp_5 = rewriter.create<::mlir::TF::SubOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::TransposeOp tblgen_TransposeOp_6;
    {
      ::mlir::Value tblgen_value_0 = (*b.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubOp_5.getODSResults(0).begin());
      tblgen_TransposeOp_6 = rewriter.create<::mlir::TF::TransposeOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*perm=*/tblgen_value_1
      );
    }
    ::mlir::TF::MatMulOp tblgen_MatMulOp_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*a.begin()));
      tblgen_values.push_back((*tblgen_TransposeOp_6.getODSResults(0).begin()));
      if (auto tmpAttr = at) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("transpose_a"), tmpAttr);
      }
      if (auto tmpAttr = rewriter.getBoolAttr(true)) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("transpose_b"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MatMulOp_7 = rewriter.create<::mlir::TF::MatMulOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MatMulOp_7.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:163
*/
struct ConvertMatrixSetDiagV2ToMatrixSetDiag : public ::mlir::RewritePattern {
  ConvertMatrixSetDiagV2ToMatrixSetDiag(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.MatrixSetDiagV2", 2, context, {"tf.MatrixSetDiag"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range diagonal(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MatrixSetDiagV2Op>(op0); (void)castedOp0;
    input = castedOp0.getODSOperands(0);
    diagonal = castedOp0.getODSOperands(1);
    {
      auto *op1 = (*castedOp0.getODSOperands(2).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 2 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_0(rewriter, op1, tblgen_ops))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MatrixSetDiagOp tblgen_MatrixSetDiagOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*diagonal.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MatrixSetDiagOp_0 = rewriter.create<::mlir::TF::MatrixSetDiagOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MatrixSetDiagOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:170
*/
struct ConvertMatrixSetDiagV3ToMatrixSetDiag : public ::mlir::RewritePattern {
  ConvertMatrixSetDiagV3ToMatrixSetDiag(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.MatrixSetDiagV3", 2, context, {"tf.MatrixSetDiag"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::StringAttr align;
    ::mlir::Operation::operand_range diagonal(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MatrixSetDiagV3Op>(op0); (void)castedOp0;
    input = castedOp0.getODSOperands(0);
    diagonal = castedOp0.getODSOperands(1);
    {
      auto *op1 = (*castedOp0.getODSOperands(2).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 2 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_0(rewriter, op1, tblgen_ops))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::StringAttr>("align");(void)tblgen_attr;
      if (!tblgen_attr) tblgen_attr = rewriter.getStringAttr("RIGHT_LEFT");
      align = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MatrixSetDiagOp tblgen_MatrixSetDiagOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*diagonal.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MatrixSetDiagOp_0 = rewriter.create<::mlir::TF::MatrixSetDiagOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MatrixSetDiagOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:74
*/
struct ConvertPlaceholderWithDefault : public ::mlir::RewritePattern {
  ConvertPlaceholderWithDefault(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.PlaceholderWithDefault", 1, context, {"tf.Identity"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::PlaceholderWithDefaultOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::IdentityOp tblgen_IdentityOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*arg.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_IdentityOp_0 = rewriter.create<::mlir::TF::IdentityOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_IdentityOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:72
*/
struct ConvertSnapshot : public ::mlir::RewritePattern {
  ConvertSnapshot(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Snapshot", 1, context, {"tf.Identity"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::SnapshotOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::IdentityOp tblgen_IdentityOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*arg.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_IdentityOp_0 = rewriter.create<::mlir::TF::IdentityOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_IdentityOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:73
*/
struct ConvertStopGradient : public ::mlir::RewritePattern {
  ConvertStopGradient(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.StopGradient", 1, context, {"tf.Identity"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::StopGradientOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::IdentityOp tblgen_IdentityOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*arg.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_IdentityOp_0 = rewriter.create<::mlir::TF::IdentityOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_IdentityOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:32
*/
struct ConvertTfConst : public ::mlir::RewritePattern {
  ConvertTfConst(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Const", 1, context, {"arith.constant"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr value;
    ::mlir::TF::ConstOp res;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op0); (void)castedOp0;
    res = castedOp0;
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_prepare_patterns4(rewriter, op0, tblgen_attr, "op 'tf.Const' attribute 'value' failed to satisfy constraint: 'non-opaque constant tensor'"))) {
        return ::mlir::failure();
      }
      value = tblgen_attr;
    }
    if (!((((((*res.getODSResults(0).begin()).getType()).isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return (true); }(((*res.getODSResults(0).begin()).getType()).cast<::mlir::ShapedType>().getElementType()))) && ((((*res.getODSResults(0).begin()).getType()).cast<::mlir::ShapedType>().hasStaticShape())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "value entity 'res' failed to satisfy constraint: 'statically shaped tensor of any type values'";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::arith::ConstantOp tblgen_ConstantOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      if (auto tmpAttr = value) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("value"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_ConstantOp_0 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_ConstantOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/tensorflow/transforms/optimize.td:52
*/
struct FuseMulAndConv2D : public ::mlir::RewritePattern {
  FuseMulAndConv2D(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Mul", 4, context, {"arith.constant", "tf.Conv2D", "tf.Mul"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::arith::ConstantOp multiplier;
    ::mlir::StringAttr data_format;
    ::mlir::Attribute mul_value;
    ::mlir::ArrayAttr explicit_padding;
    ::mlir::TF::Conv2DOp conv;
    ::mlir::ArrayAttr dilations;
    ::mlir::BoolAttr use_cudnn;
    ::mlir::arith::ConstantOp filter;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::StringAttr padding;
    ::mlir::TF::MulOp mul;
    ::mlir::ArrayAttr strides;
    ::mlir::Attribute filter_value;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MulOp>(op0); (void)castedOp0;
    mul = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::Conv2DOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::Conv2DOp type";
        });
      }
      conv = castedOp1;
      input = castedOp1.getODSOperands(0);
      {
        auto *op2 = (*castedOp1.getODSOperands(1).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 1 of castedOp1";
          });
        }
        auto castedOp2 = ::llvm::dyn_cast<::mlir::arith::ConstantOp>(op2); (void)castedOp2;
        if (!(castedOp2)){
          return rewriter.notifyMatchFailure(op2, [&](::mlir::Diagnostic &diag) {
            diag << "castedOp2 is not ::mlir::arith::ConstantOp type";
          });
        }
        filter = castedOp2;
        {
          auto tblgen_attr = op2->getAttrOfType<::mlir::Attribute>("value");(void)tblgen_attr;
          if (!(tblgen_attr)){
            return rewriter.notifyMatchFailure(op2, [&](::mlir::Diagnostic &diag) {
              diag << "expected op 'arith.constant' to have attribute 'value' of type '::mlir::Attribute'";
            });
          }
          if(failed(__mlir_ods_local_attr_constraint_prepare_patterns2(rewriter, op2, tblgen_attr, "op 'arith.constant' attribute 'value' failed to satisfy constraint: 'float constant tensor'"))) {
            return ::mlir::failure();
          }
          filter_value = tblgen_attr;
        }
        tblgen_ops.push_back(op2);
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ArrayAttr>("strides");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'tf.Conv2D' to have attribute 'strides' of type '::mlir::ArrayAttr'";
          });
        }
        strides = tblgen_attr;
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::BoolAttr>("use_cudnn_on_gpu");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getBoolAttr(true);
        use_cudnn = tblgen_attr;
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::StringAttr>("padding");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'tf.Conv2D' to have attribute 'padding' of type '::mlir::StringAttr'";
          });
        }
        padding = tblgen_attr;
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ArrayAttr>("explicit_paddings");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getI64ArrayAttr({});
        explicit_padding = tblgen_attr;
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::StringAttr>("data_format");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getStringAttr("NHWC");
        if(failed(__mlir_ods_local_attr_constraint_prepare_patterns5(rewriter, op1, tblgen_attr, "op 'tf.Conv2D' attribute 'data_format' failed to satisfy constraint: 'constant attribute \"NHWC\"'"))) {
          return ::mlir::failure();
        }
        data_format = tblgen_attr;
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ArrayAttr>("dilations");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getI64ArrayAttr({1, 1, 1, 1});
        dilations = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::arith::ConstantOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::arith::ConstantOp type";
        });
      }
      multiplier = castedOp1;
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::Attribute>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'arith.constant' to have attribute 'value' of type '::mlir::Attribute'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_prepare_patterns2(rewriter, op1, tblgen_attr, "op 'arith.constant' attribute 'value' failed to satisfy constraint: 'float constant tensor'"))) {
          return ::mlir::failure();
        }
        mul_value = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    if (!((TFL::IsBroadcastableElementsAttrs(filter_value, mul_value) && TFL::IsDimensionsDegenerateExceptLastOne(mul_value)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'filter_value, mul_value' failed to satisfy constraint: ''";
      });
    }
    if (!(((*conv.getODSResults(0).begin()).hasOneUse()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'conv' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::arith::ConstantOp tblgen_ConstantOp_0;
    {
      tblgen_ConstantOp_0 = rewriter.create<::mlir::arith::ConstantOp>((*filter.getODSResults(0).begin()).getLoc(),
        /*value=*/filter_value
      );
    }
    ::mlir::arith::ConstantOp tblgen_ConstantOp_1;
    {
      tblgen_ConstantOp_1 = rewriter.create<::mlir::arith::ConstantOp>((*multiplier.getODSResults(0).begin()).getLoc(),
        /*value=*/mul_value
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_2;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_ConstantOp_0.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstantOp_1.getODSResults(0).begin());
      tblgen_MulOp_2 = rewriter.create<::mlir::TF::MulOp>((*mul.getODSResults(0).begin()).getLoc(),
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::Conv2DOp tblgen_Conv2DOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*tblgen_MulOp_2.getODSResults(0).begin()));
      if (auto tmpAttr = strides) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("strides"), tmpAttr);
      }
      if (auto tmpAttr = use_cudnn) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("use_cudnn_on_gpu"), tmpAttr);
      }
      if (auto tmpAttr = padding) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("padding"), tmpAttr);
      }
      if (auto tmpAttr = explicit_padding) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("explicit_paddings"), tmpAttr);
      }
      if (auto tmpAttr = data_format) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("data_format"), tmpAttr);
      }
      if (auto tmpAttr = dilations) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("dilations"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_Conv2DOp_3 = rewriter.create<::mlir::TF::Conv2DOp>((*conv.getODSResults(0).begin()).getLoc(), tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_Conv2DOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:180
*/
struct LowerTensorScatterAdd : public ::mlir::RewritePattern {
  LowerTensorScatterAdd(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.TensorScatterAdd", 1, context, {"tf.Add", "tf.TensorScatterUpdate"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range updates(op0->getOperands());
    ::mlir::Operation::operand_range indices(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::TensorScatterAddOp>(op0); (void)castedOp0;
    input = castedOp0.getODSOperands(0);
    indices = castedOp0.getODSOperands(1);
    updates = castedOp0.getODSOperands(2);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = rewriter.create<TF::GatherNdOp>((*updates.begin()).getLoc(), (*updates.begin()).getType(), (*input.begin()), (*indices.begin())); (void)nativeVar_0;
    ::mlir::TF::AddOp tblgen_AddOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*updates.begin());
      ::mlir::Value tblgen_value_1 = nativeVar_0;
      tblgen_AddOp_1 = rewriter.create<::mlir::TF::AddOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::TensorScatterUpdateOp tblgen_TensorScatterUpdateOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*indices.begin()));
      tblgen_values.push_back((*tblgen_AddOp_1.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_TensorScatterUpdateOp_2 = rewriter.create<::mlir::TF::TensorScatterUpdateOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_TensorScatterUpdateOp_2.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:191
*/
struct LowerUInt32AddV2 : public ::mlir::RewritePattern {
  LowerUInt32AddV2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.AddV2", 1, context, {"tf.AddV2", "tf.Cast"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range rhs(op0->getOperands());
    ::mlir::Operation::operand_range lhs(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::AddV2Op>(op0); (void)castedOp0;
    lhs = castedOp0.getODSOperands(0);
    rhs = castedOp0.getODSOperands(1);
    if (!(((((*lhs.begin()).getType()).isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isUnsignedInteger(32))) || ((elementType.isa<mlir::TF::Uint32RefType>())); }(((*lhs.begin()).getType()).cast<::mlir::ShapedType>().getElementType())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "value entity 'lhs' failed to satisfy constraint: 'tensor of 32-bit unsigned integer values'";
      });
    }
    if (!(((((*rhs.begin()).getType()).isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isUnsignedInteger(32))) || ((elementType.isa<mlir::TF::Uint32RefType>())); }(((*rhs.begin()).getType()).cast<::mlir::ShapedType>().getElementType())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "value entity 'rhs' failed to satisfy constraint: 'tensor of 32-bit unsigned integer values'";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = CreateTFCastOpI32(&rewriter, odsLoc, (*lhs.begin()), rewriter.getBoolAttr(false)); (void)nativeVar_0;
    auto nativeVar_1 = CreateTFCastOpI32(&rewriter, odsLoc, (*rhs.begin()), rewriter.getBoolAttr(false)); (void)nativeVar_1;
    ::mlir::TF::AddV2Op tblgen_AddV2Op_2;
    {
      ::mlir::Value tblgen_value_0 = nativeVar_0;
      ::mlir::Value tblgen_value_1 = nativeVar_1;
      tblgen_AddV2Op_2 = rewriter.create<::mlir::TF::AddV2Op>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::CastOp tblgen_CastOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddV2Op_2.getODSResults(0).begin()));
      if (auto tmpAttr = rewriter.getBoolAttr(false)) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("Truncate"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_CastOp_3 = rewriter.create<::mlir::TF::CastOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_CastOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:158
*/
struct OptimizeAwayRankDequantQuant : public ::mlir::RewritePattern {
  OptimizeAwayRankDequantQuant(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Rank", 3, context, {"tf.Rank"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qtype;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::RankOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_1(rewriter, op1, tblgen_ops, qtype, input))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::RankOp tblgen_RankOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_RankOp_0 = rewriter.create<::mlir::TF::RankOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_RankOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/tensorflow/transforms/optimize.td:98
*/
struct PassthroughMulAndAddV2 : public ::mlir::RewritePattern {
  PassthroughMulAndAddV2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Mul", 4, context, {"arith.constant", "tf.AddV2", "tf.Mul"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::Attribute value;
    ::mlir::TF::AddV2Op output;
    ::mlir::Attribute bias;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MulOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::AddV2Op>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::AddV2Op type";
        });
      }
      output = castedOp1;
      input = castedOp1.getODSOperands(0);
      {
        auto *op2 = (*castedOp1.getODSOperands(1).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 1 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_2(rewriter, op2, tblgen_ops, bias))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_3(rewriter, op1, tblgen_ops, value))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((llvm::isa_and_nonnull<mlir::TF::Conv2DOp>((*input.begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }
    if (!(((*output.getODSResults(0).begin()).hasOneUse()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'output' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::arith::ConstantOp tblgen_ConstantOp_0;
    {
      tblgen_ConstantOp_0 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/value
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstantOp_0.getODSResults(0).begin());
      tblgen_MulOp_1 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::arith::ConstantOp tblgen_ConstantOp_2;
    {
      tblgen_ConstantOp_2 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/bias
      );
    }
    ::mlir::arith::ConstantOp tblgen_ConstantOp_3;
    {
      tblgen_ConstantOp_3 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/value
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_4;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_ConstantOp_2.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstantOp_3.getODSResults(0).begin());
      tblgen_MulOp_4 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::AddV2Op tblgen_AddV2Op_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_1.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_MulOp_4.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_AddV2Op_5 = rewriter.create<::mlir::TF::AddV2Op>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_AddV2Op_5.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/tensorflow/transforms/optimize.td:79
*/
struct PassthroughMulAndBiasAdd : public ::mlir::RewritePattern {
  PassthroughMulAndBiasAdd(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Mul", 4, context, {"arith.constant", "tf.AddV2", "tf.Mul"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::StringAttr format;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::Attribute value;
    ::mlir::TF::BiasAddOp output;
    ::mlir::Attribute bias;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MulOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::BiasAddOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::BiasAddOp type";
        });
      }
      output = castedOp1;
      input = castedOp1.getODSOperands(0);
      {
        auto *op2 = (*castedOp1.getODSOperands(1).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 1 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_2(rewriter, op2, tblgen_ops, bias))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::StringAttr>("data_format");(void)tblgen_attr;
        if (!tblgen_attr) tblgen_attr = rewriter.getStringAttr("NHWC");
        if(failed(__mlir_ods_local_attr_constraint_prepare_patterns5(rewriter, op1, tblgen_attr, "op 'tf.BiasAdd' attribute 'data_format' failed to satisfy constraint: 'constant attribute \"NHWC\"'"))) {
          return ::mlir::failure();
        }
        format = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_3(rewriter, op1, tblgen_ops, value))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((llvm::isa_and_nonnull<mlir::TF::Conv2DOp>((*input.begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }
    if (!(((*output.getODSResults(0).begin()).hasOneUse()))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'output' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::arith::ConstantOp tblgen_ConstantOp_0;
    {
      tblgen_ConstantOp_0 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/value
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstantOp_0.getODSResults(0).begin());
      tblgen_MulOp_1 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::arith::ConstantOp tblgen_ConstantOp_2;
    {
      tblgen_ConstantOp_2 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/bias
      );
    }
    ::mlir::arith::ConstantOp tblgen_ConstantOp_3;
    {
      tblgen_ConstantOp_3 = rewriter.create<::mlir::arith::ConstantOp>(odsLoc,
        /*value=*/value
      );
    }
    ::mlir::TF::MulOp tblgen_MulOp_4;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_ConstantOp_2.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_ConstantOp_3.getODSResults(0).begin());
      tblgen_MulOp_4 = rewriter.create<::mlir::TF::MulOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    ::mlir::TF::AddV2Op tblgen_AddV2Op_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_1.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_MulOp_4.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_AddV2Op_5 = rewriter.create<::mlir::TF::AddV2Op>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_AddV2Op_5.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:79
*/
struct RemoveIdentity : public ::mlir::RewritePattern {
  RemoveIdentity(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Identity", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::IdentityOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ arg }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:80
*/
struct RemoveIdentityN : public ::mlir::RewritePattern {
  RemoveIdentityN(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.IdentityN", 1, context, {}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range arg(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::IdentityNOp>(op0); (void)castedOp0;
    arg = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ arg }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:125
*/
struct ReorderReshapeDequantQuant : public ::mlir::RewritePattern {
  ReorderReshapeDequantQuant(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Reshape", 3, context, {"tf.Reshape", "tfl.dequantize", "tfl.quantize"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qtype;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::Operation::operand_range shape(op0->getOperands());
    ::mlir::TF::ReshapeOp old_value;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    if(failed(static_dag_matcher_4(rewriter, op0, tblgen_ops, qtype, input, shape, old_value))) {
      return ::mlir::failure();
    }
    auto castedOp0 = ::llvm::dyn_cast_or_null<::mlir::TF::ReshapeOp>(op0); (void)castedOp0;
    if (!((quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), -1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'qtype, old_value' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ReshapeOp tblgen_ReshapeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*shape.begin());
      tblgen_ReshapeOp_0 = rewriter.create<::mlir::TF::ReshapeOp>(odsLoc,
        /*tensor=*/tblgen_value_0,
        /*shape=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), -1); (void)nativeVar_1;
    ::mlir::TFL::QuantizeOp tblgen_QuantizeOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_ReshapeOp_0.getODSResults(0).begin()));
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("qtype"), tmpAttr);
      }
      tblgen_QuantizeOp_2 = rewriter.create<::mlir::TFL::QuantizeOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TFL::DequantizeOp tblgen_DequantizeOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_QuantizeOp_2.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DequantizeOp_3 = rewriter.create<::mlir::TFL::DequantizeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DequantizeOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:146
*/
struct ReorderReshapeDequantQuantUsedByDepthwiseConv : public ::mlir::RewritePattern {
  ReorderReshapeDequantQuantUsedByDepthwiseConv(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Reshape", 13, context, {"tf.Reshape", "tfl.dequantize", "tfl.quantize"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qtype;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::Operation::operand_range shape(op0->getOperands());
    ::mlir::TF::ReshapeOp old_value;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    if(failed(static_dag_matcher_4(rewriter, op0, tblgen_ops, qtype, input, shape, old_value))) {
      return ::mlir::failure();
    }
    auto castedOp0 = ::llvm::dyn_cast_or_null<::mlir::TF::ReshapeOp>(op0); (void)castedOp0;
    if (!((llvm::isa<mlir::TFL::DepthwiseConv2DOp>(*(*old_value.getODSResults(0).begin()).getUsers().begin())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'old_value' failed to satisfy constraint: ''";
      });
    }
    if (!((quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), 3)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'qtype, old_value' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ReshapeOp tblgen_ReshapeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*shape.begin());
      tblgen_ReshapeOp_0 = rewriter.create<::mlir::TF::ReshapeOp>(odsLoc,
        /*tensor=*/tblgen_value_0,
        /*shape=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), 3); (void)nativeVar_1;
    ::mlir::TFL::QuantizeOp tblgen_QuantizeOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_ReshapeOp_0.getODSResults(0).begin()));
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("qtype"), tmpAttr);
      }
      tblgen_QuantizeOp_2 = rewriter.create<::mlir::TFL::QuantizeOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TFL::DequantizeOp tblgen_DequantizeOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_QuantizeOp_2.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DequantizeOp_3 = rewriter.create<::mlir::TFL::DequantizeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DequantizeOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:95
*/
struct ReorderReshapeFakeQuant : public ::mlir::RewritePattern {
  ReorderReshapeFakeQuant(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Reshape", 2, context, {"tf.FakeQuantWithMinMaxVars", "tf.Reshape"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range shape(op0->getOperands());
    ::mlir::Operation::operand_range max(op0->getOperands());
    ::mlir::IntegerAttr num_bits;
    ::mlir::Operation::operand_range min(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::BoolAttr narrow_range;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::ReshapeOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_5(rewriter, op1, tblgen_ops, max, num_bits, min, input, narrow_range))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    shape = castedOp0.getODSOperands(1);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ReshapeOp tblgen_ReshapeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*shape.begin());
      tblgen_ReshapeOp_0 = rewriter.create<::mlir::TF::ReshapeOp>(odsLoc,
        /*tensor=*/tblgen_value_0,
        /*shape=*/tblgen_value_1
      );
    }
    ::mlir::TF::FakeQuantWithMinMaxVarsOp tblgen_FakeQuantWithMinMaxVarsOp_1;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_ReshapeOp_0.getODSResults(0).begin()));
      tblgen_values.push_back((*min.begin()));
      tblgen_values.push_back((*max.begin()));
      if (auto tmpAttr = num_bits) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("num_bits"), tmpAttr);
      }
      if (auto tmpAttr = narrow_range) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("narrow_range"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_FakeQuantWithMinMaxVarsOp_1 = rewriter.create<::mlir::TF::FakeQuantWithMinMaxVarsOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_FakeQuantWithMinMaxVarsOp_1.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:117
*/
struct ReorderTransposeDequantQuant : public ::mlir::RewritePattern {
  ReorderTransposeDequantQuant(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Transpose", 3, context, {"tf.Transpose", "tfl.dequantize", "tfl.quantize"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qtype;
    ::mlir::Operation::operand_range perm(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::TF::TransposeOp old_value;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    if(failed(static_dag_matcher_6(rewriter, op0, tblgen_ops, qtype, perm, input, old_value))) {
      return ::mlir::failure();
    }
    auto castedOp0 = ::llvm::dyn_cast_or_null<::mlir::TF::TransposeOp>(op0); (void)castedOp0;
    if (!((quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), -1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'qtype, old_value' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::TransposeOp tblgen_TransposeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*perm.begin());
      tblgen_TransposeOp_0 = rewriter.create<::mlir::TF::TransposeOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*perm=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), -1); (void)nativeVar_1;
    ::mlir::TFL::QuantizeOp tblgen_QuantizeOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_TransposeOp_0.getODSResults(0).begin()));
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("qtype"), tmpAttr);
      }
      tblgen_QuantizeOp_2 = rewriter.create<::mlir::TFL::QuantizeOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TFL::DequantizeOp tblgen_DequantizeOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_QuantizeOp_2.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DequantizeOp_3 = rewriter.create<::mlir::TFL::DequantizeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DequantizeOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:134
*/
struct ReorderTransposeDequantQuantUsedByConv : public ::mlir::RewritePattern {
  ReorderTransposeDequantQuantUsedByConv(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Transpose", 13, context, {"tf.Transpose", "tfl.dequantize", "tfl.quantize"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TypeAttr qtype;
    ::mlir::Operation::operand_range perm(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::TF::TransposeOp old_value;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    if(failed(static_dag_matcher_6(rewriter, op0, tblgen_ops, qtype, perm, input, old_value))) {
      return ::mlir::failure();
    }
    auto castedOp0 = ::llvm::dyn_cast_or_null<::mlir::TF::TransposeOp>(op0); (void)castedOp0;
    if (!((llvm::isa<mlir::TFL::Conv2DOp>(*(*old_value.getODSResults(0).begin()).getUsers().begin())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'old_value' failed to satisfy constraint: ''";
      });
    }
    if (!((quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), 0)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'qtype, old_value' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::TransposeOp tblgen_TransposeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*perm.begin());
      tblgen_TransposeOp_0 = rewriter.create<::mlir::TF::TransposeOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*perm=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = quant::CastQuantizedTypeAttrFromExpressedType(rewriter, qtype, (*old_value.getODSResults(0).begin()).getType(), 0); (void)nativeVar_1;
    ::mlir::TFL::QuantizeOp tblgen_QuantizeOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_TransposeOp_0.getODSResults(0).begin()));
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("qtype"), tmpAttr);
      }
      tblgen_QuantizeOp_2 = rewriter.create<::mlir::TFL::QuantizeOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::TFL::DequantizeOp tblgen_DequantizeOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_QuantizeOp_2.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DequantizeOp_3 = rewriter.create<::mlir::TFL::DequantizeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DequantizeOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/transforms/prepare_patterns.td:87
*/
struct ReorderTransposeFakeQuant : public ::mlir::RewritePattern {
  ReorderTransposeFakeQuant(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Transpose", 2, context, {"tf.FakeQuantWithMinMaxVars", "tf.Transpose"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range perm(op0->getOperands());
    ::mlir::Operation::operand_range max(op0->getOperands());
    ::mlir::IntegerAttr num_bits;
    ::mlir::Operation::operand_range min(op0->getOperands());
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::BoolAttr narrow_range;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::TransposeOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_5(rewriter, op1, tblgen_ops, max, num_bits, min, input, narrow_range))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    perm = castedOp0.getODSOperands(1);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::TransposeOp tblgen_TransposeOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*perm.begin());
      tblgen_TransposeOp_0 = rewriter.create<::mlir::TF::TransposeOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*perm=*/tblgen_value_1
      );
    }
    ::mlir::TF::FakeQuantWithMinMaxVarsOp tblgen_FakeQuantWithMinMaxVarsOp_1;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_TransposeOp_0.getODSResults(0).begin()));
      tblgen_values.push_back((*min.begin()));
      tblgen_values.push_back((*max.begin()));
      if (auto tmpAttr = num_bits) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("num_bits"), tmpAttr);
      }
      if (auto tmpAttr = narrow_range) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("narrow_range"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_FakeQuantWithMinMaxVarsOp_1 = rewriter.create<::mlir::TF::FakeQuantWithMinMaxVarsOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_FakeQuantWithMinMaxVarsOp_1.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<ConvertBatchNormWithGlobalNormalization_1>(patterns.getContext());
  patterns.add<ConvertBatchNormWithGlobalNormalization_2>(patterns.getContext());
  patterns.add<ConvertCastComplexFFTToRFFT>(patterns.getContext());
  patterns.add<ConvertCheckNumerics>(patterns.getContext());
  patterns.add<ConvertMatmulWithTranspose>(patterns.getContext());
  patterns.add<ConvertMatmulWithoutTransposeToWithTranspose>(patterns.getContext());
  patterns.add<ConvertMatrixSetDiagV2ToMatrixSetDiag>(patterns.getContext());
  patterns.add<ConvertMatrixSetDiagV3ToMatrixSetDiag>(patterns.getContext());
  patterns.add<ConvertPlaceholderWithDefault>(patterns.getContext());
  patterns.add<ConvertSnapshot>(patterns.getContext());
  patterns.add<ConvertStopGradient>(patterns.getContext());
  patterns.add<ConvertTfConst>(patterns.getContext());
  patterns.add<FuseMulAndConv2D>(patterns.getContext());
  patterns.add<LowerTensorScatterAdd>(patterns.getContext());
  patterns.add<LowerUInt32AddV2>(patterns.getContext());
  patterns.add<OptimizeAwayRankDequantQuant>(patterns.getContext());
  patterns.add<PassthroughMulAndAddV2>(patterns.getContext());
  patterns.add<PassthroughMulAndBiasAdd>(patterns.getContext());
  patterns.add<RemoveIdentity>(patterns.getContext());
  patterns.add<RemoveIdentityN>(patterns.getContext());
  patterns.add<ReorderReshapeDequantQuant>(patterns.getContext());
  patterns.add<ReorderReshapeDequantQuantUsedByDepthwiseConv>(patterns.getContext());
  patterns.add<ReorderReshapeFakeQuant>(patterns.getContext());
  patterns.add<ReorderTransposeDequantQuant>(patterns.getContext());
  patterns.add<ReorderTransposeDequantQuantUsedByConv>(patterns.getContext());
  patterns.add<ReorderTransposeFakeQuant>(patterns.getContext());
}
