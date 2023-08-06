/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


static ::mlir::LogicalResult __mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Type type,
    ::llvm::StringRef failureStr) {
  if (!((!type.cast<ShapedType>().getElementType().isa<ComplexType>()))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": Non-complex element type";
    });
  }
  return ::mlir::success();
}
/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:38
*/
struct GeneratedConvert0 : public ::mlir::RewritePattern {
  GeneratedConvert0(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.acos", 1, context, {"mhlo.add", "mhlo.atan2", "mhlo.compare", "mhlo.multiply", "mhlo.select", "mhlo.sqrt", "mhlo.subtract"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AcosOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.acos' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLike(rewriter, odsLoc, -1, (*input.begin())); (void)nativeVar_0;
    auto nativeVar_1 = StringAttr(); (void)nativeVar_1;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_2;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = nativeVar_0;
      tblgen_CompareOp_2 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("NE"),
        /*compare_type=*/nativeVar_1
      );
    }
    auto nativeVar_3 = chlo::getConstantLike(rewriter, odsLoc, 2, (*input.begin())); (void)nativeVar_3;
    auto nativeVar_4 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_4;
    ::mlir::mhlo::MulOp tblgen_MulOp_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*input.begin()));
      tblgen_MulOp_5 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SubOp tblgen_SubOp_6;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_4);
      tblgen_values.push_back((*tblgen_MulOp_5.getODSResults(0).begin()));
      tblgen_SubOp_6 = rewriter.create<::mlir::mhlo::SubOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SubOp_6.getODSResults(0).begin()));
      tblgen_SqrtOp_7 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_8 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_8;
    ::mlir::mhlo::AddOp tblgen_AddOp_9;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_8);
      tblgen_values.push_back((*input.begin()));
      tblgen_AddOp_9 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::Atan2Op tblgen_Atan2Op_10;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SqrtOp_7.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_AddOp_9.getODSResults(0).begin()));
      tblgen_Atan2Op_10 = rewriter.create<::mlir::mhlo::Atan2Op>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_11;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_3);
      tblgen_values.push_back((*tblgen_Atan2Op_10.getODSResults(0).begin()));
      tblgen_MulOp_11 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_12 = chlo::getConstantLike(rewriter, odsLoc, M_PI, (*input.begin())); (void)nativeVar_12;
    ::mlir::mhlo::SelectOp tblgen_SelectOp_13;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_CompareOp_2.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_MulOp_11.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_12);
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_SelectOp_13 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_SelectOp_13.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:72
*/
struct GeneratedConvert1 : public ::mlir::RewritePattern {
  GeneratedConvert1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.acosh", 1, context, {"mhlo.add", "mhlo.compare", "mhlo.log", "mhlo.multiply", "mhlo.select", "mhlo.sqrt"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AcoshOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.acosh' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLike(rewriter, odsLoc, -1, (*input.begin())); (void)nativeVar_0;
    auto nativeVar_1 = StringAttr(); (void)nativeVar_1;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_2;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = nativeVar_0;
      tblgen_CompareOp_2 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("LT"),
        /*compare_type=*/nativeVar_1
      );
    }
    auto nativeVar_3 = chlo::getConstantLike(rewriter, odsLoc, NAN, (*input.begin())); (void)nativeVar_3;
    auto nativeVar_4 = chlo::getConstantLikeMaxFiniteValue(rewriter, odsLoc, (*input.begin())); (void)nativeVar_4;
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_4);
      tblgen_SqrtOp_5 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_6 = StringAttr(); (void)nativeVar_6;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_7;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SqrtOp_5.getODSResults(0).begin());
      tblgen_CompareOp_7 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("GE"),
        /*compare_type=*/nativeVar_6
      );
    }
    ::mlir::mhlo::LogOp tblgen_LogOp_8;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_LogOp_8 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_9 = chlo::getConstantLike(rewriter, odsLoc, 2, (*input.begin())); (void)nativeVar_9;
    ::mlir::mhlo::LogOp tblgen_LogOp_10;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_9);
      tblgen_LogOp_10 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_11;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_LogOp_8.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_LogOp_10.getODSResults(0).begin()));
      tblgen_AddOp_11 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_12 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_12;
    ::mlir::mhlo::AddOp tblgen_AddOp_13;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_12);
      tblgen_values.push_back((*input.begin()));
      tblgen_AddOp_13 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_14 = chlo::getConstantLike(rewriter, odsLoc, -1, (*input.begin())); (void)nativeVar_14;
    ::mlir::mhlo::AddOp tblgen_AddOp_15;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_14);
      tblgen_values.push_back((*input.begin()));
      tblgen_AddOp_15 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_16;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_13.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_AddOp_15.getODSResults(0).begin()));
      tblgen_MulOp_16 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_17;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_16.getODSResults(0).begin()));
      tblgen_SqrtOp_17 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_18;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*tblgen_SqrtOp_17.getODSResults(0).begin()));
      tblgen_AddOp_18 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::LogOp tblgen_LogOp_19;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_18.getODSResults(0).begin()));
      tblgen_LogOp_19 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SelectOp tblgen_SelectOp_20;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_7.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_AddOp_11.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_LogOp_19.getODSResults(0).begin());
      tblgen_SelectOp_20 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::mhlo::SelectOp tblgen_SelectOp_21;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_CompareOp_2.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_3);
      tblgen_values.push_back((*tblgen_SelectOp_20.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_SelectOp_21 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_SelectOp_21.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:118
*/
struct GeneratedConvert2 : public ::mlir::RewritePattern {
  GeneratedConvert2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.asin", 1, context, {"mhlo.add", "mhlo.atan2", "mhlo.multiply", "mhlo.sqrt", "mhlo.subtract"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AsinOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.asin' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLike(rewriter, odsLoc, 2, (*input.begin())); (void)nativeVar_0;
    auto nativeVar_1 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_1;
    auto nativeVar_2 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_2;
    ::mlir::mhlo::MulOp tblgen_MulOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*input.begin()));
      tblgen_MulOp_3 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SubOp tblgen_SubOp_4;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_2);
      tblgen_values.push_back((*tblgen_MulOp_3.getODSResults(0).begin()));
      tblgen_SubOp_4 = rewriter.create<::mlir::mhlo::SubOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SubOp_4.getODSResults(0).begin()));
      tblgen_SqrtOp_5 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_6;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_1);
      tblgen_values.push_back((*tblgen_SqrtOp_5.getODSResults(0).begin()));
      tblgen_AddOp_6 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::Atan2Op tblgen_Atan2Op_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*tblgen_AddOp_6.getODSResults(0).begin()));
      tblgen_Atan2Op_7 = rewriter.create<::mlir::mhlo::Atan2Op>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_8;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_0);
      tblgen_values.push_back((*tblgen_Atan2Op_7.getODSResults(0).begin()));
      tblgen_MulOp_8 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MulOp_8.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:155
*/
struct GeneratedConvert3 : public ::mlir::RewritePattern {
  GeneratedConvert3(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.asinh", 1, context, {"mhlo.abs", "mhlo.add", "mhlo.compare", "mhlo.divide", "mhlo.log", "mhlo.log_plus_one", "mhlo.multiply", "mhlo.select", "mhlo.sign", "mhlo.sqrt"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AsinhOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.asinh' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::SignOp tblgen_SignOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_SignOp_0 = rewriter.create<::mlir::mhlo::SignOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_1 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_2 = chlo::getConstantLikeMaxFiniteValue(rewriter, odsLoc, (*input.begin())); (void)nativeVar_2;
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_2);
      tblgen_SqrtOp_3 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_4 = StringAttr(); (void)nativeVar_4;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_5;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AbsOp_1.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SqrtOp_3.getODSResults(0).begin());
      tblgen_CompareOp_5 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("GE"),
        /*compare_type=*/nativeVar_4
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_6;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_6 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::LogOp tblgen_LogOp_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_6.getODSResults(0).begin()));
      tblgen_LogOp_7 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_8 = chlo::getConstantLike(rewriter, odsLoc, 2, (*input.begin())); (void)nativeVar_8;
    ::mlir::mhlo::LogOp tblgen_LogOp_9;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_8);
      tblgen_LogOp_9 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_10;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_LogOp_7.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_LogOp_9.getODSResults(0).begin()));
      tblgen_AddOp_10 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_11;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_11 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_12 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_12;
    auto nativeVar_13 = StringAttr(); (void)nativeVar_13;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_14;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AbsOp_11.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_12;
      tblgen_CompareOp_14 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("LE"),
        /*compare_type=*/nativeVar_13
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_15;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_15 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_16;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_16 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_17;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_17 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_18 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_18;
    ::mlir::mhlo::AbsOp tblgen_AbsOp_19;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_19 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_20;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_20 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_21;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_19.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_AbsOp_20.getODSResults(0).begin()));
      tblgen_MulOp_21 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_22 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_22;
    ::mlir::mhlo::AddOp tblgen_AddOp_23;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_21.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_22);
      tblgen_AddOp_23 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_24;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_23.getODSResults(0).begin()));
      tblgen_SqrtOp_24 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_25;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back(nativeVar_18);
      tblgen_values.push_back((*tblgen_SqrtOp_24.getODSResults(0).begin()));
      tblgen_AddOp_25 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::DivOp tblgen_DivOp_26;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_17.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_AddOp_25.getODSResults(0).begin()));
      tblgen_DivOp_26 = rewriter.create<::mlir::mhlo::DivOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_27;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_16.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_DivOp_26.getODSResults(0).begin()));
      tblgen_MulOp_27 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_28;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_15.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_MulOp_27.getODSResults(0).begin()));
      tblgen_AddOp_28 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::Log1pOp tblgen_Log1pOp_29;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_28.getODSResults(0).begin()));
      tblgen_Log1pOp_29 = rewriter.create<::mlir::mhlo::Log1pOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_30;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_30 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_31;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_31 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::AbsOp tblgen_AbsOp_32;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_32 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_33;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_31.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_AbsOp_32.getODSResults(0).begin()));
      tblgen_MulOp_33 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_34 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_34;
    ::mlir::mhlo::AddOp tblgen_AddOp_35;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_MulOp_33.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_34);
      tblgen_AddOp_35 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SqrtOp tblgen_SqrtOp_36;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_35.getODSResults(0).begin()));
      tblgen_SqrtOp_36 = rewriter.create<::mlir::mhlo::SqrtOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::AddOp tblgen_AddOp_37;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_30.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_SqrtOp_36.getODSResults(0).begin()));
      tblgen_AddOp_37 = rewriter.create<::mlir::mhlo::AddOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::LogOp tblgen_LogOp_38;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AddOp_37.getODSResults(0).begin()));
      tblgen_LogOp_38 = rewriter.create<::mlir::mhlo::LogOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SelectOp tblgen_SelectOp_39;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_14.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_Log1pOp_29.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_LogOp_38.getODSResults(0).begin());
      tblgen_SelectOp_39 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::mhlo::SelectOp tblgen_SelectOp_40;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_5.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_AddOp_10.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_SelectOp_39.getODSResults(0).begin());
      tblgen_SelectOp_40 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::mhlo::MulOp tblgen_MulOp_41;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SignOp_0.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_SelectOp_40.getODSResults(0).begin()));
      tblgen_MulOp_41 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MulOp_41.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:225
*/
struct GeneratedConvert4 : public ::mlir::RewritePattern {
  GeneratedConvert4(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.atan", 1, context, {"mhlo.atan2"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AtanOp>(op0); (void)castedOp0;
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_0;
    ::mlir::mhlo::Atan2Op tblgen_Atan2Op_1;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back(nativeVar_0);
      tblgen_Atan2Op_1 = rewriter.create<::mlir::mhlo::Atan2Op>(odsLoc, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_Atan2Op_1.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:234
*/
struct GeneratedConvert5 : public ::mlir::RewritePattern {
  GeneratedConvert5(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.atanh", 1, context, {"mhlo.abs", "mhlo.compare", "mhlo.log_plus_one", "mhlo.multiply", "mhlo.negate", "mhlo.select", "mhlo.subtract"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::AtanhOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.atanh' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::AbsOp tblgen_AbsOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_0 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_1 = chlo::getConstantLike(rewriter, odsLoc, 1, (*input.begin())); (void)nativeVar_1;
    auto nativeVar_2 = StringAttr(); (void)nativeVar_2;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_3;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AbsOp_0.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_1;
      tblgen_CompareOp_3 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        rewriter.getStringAttr("GT"),
        /*compare_type=*/nativeVar_2
      );
    }
    auto nativeVar_4 = chlo::getConstantLike(rewriter, odsLoc, NAN, (*input.begin())); (void)nativeVar_4;
    ::mlir::mhlo::Log1pOp tblgen_Log1pOp_5;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_Log1pOp_5 = rewriter.create<::mlir::mhlo::Log1pOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::NegOp tblgen_NegOp_6;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_NegOp_6 = rewriter.create<::mlir::mhlo::NegOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::Log1pOp tblgen_Log1pOp_7;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_NegOp_6.getODSResults(0).begin()));
      tblgen_Log1pOp_7 = rewriter.create<::mlir::mhlo::Log1pOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SubOp tblgen_SubOp_8;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_Log1pOp_5.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_Log1pOp_7.getODSResults(0).begin()));
      tblgen_SubOp_8 = rewriter.create<::mlir::mhlo::SubOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    auto nativeVar_9 = chlo::getConstantLike(rewriter, odsLoc, 0.5, (*input.begin())); (void)nativeVar_9;
    ::mlir::mhlo::MulOp tblgen_MulOp_10;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SubOp_8.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_9);
      tblgen_MulOp_10 = rewriter.create<::mlir::mhlo::MulOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::SelectOp tblgen_SelectOp_11;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_CompareOp_3.getODSResults(0).begin()));
      tblgen_values.push_back(nativeVar_4);
      tblgen_values.push_back((*tblgen_MulOp_10.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_SelectOp_11 = rewriter.create<::mlir::mhlo::SelectOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_SelectOp_11.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:256
*/
struct GeneratedConvert6 : public ::mlir::RewritePattern {
  GeneratedConvert6(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.conj", 1, context, {"mhlo.complex", "mhlo.imag", "mhlo.negate", "mhlo.real"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range v(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::ConjOp>(op0); (void)castedOp0;
    v = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::RealOp tblgen_RealOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*v.begin());
      tblgen_RealOp_0 = rewriter.create<::mlir::mhlo::RealOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::ImagOp tblgen_ImagOp_1;
    {
      ::mlir::Value tblgen_value_0 = (*v.begin());
      tblgen_ImagOp_1 = rewriter.create<::mlir::mhlo::ImagOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::mhlo::NegOp tblgen_NegOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_ImagOp_1.getODSResults(0).begin()));
      tblgen_NegOp_2 = rewriter.create<::mlir::mhlo::NegOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::ComplexOp tblgen_ComplexOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_RealOp_0.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_NegOp_2.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_ComplexOp_3 = rewriter.create<::mlir::mhlo::ComplexOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_ComplexOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:261
*/
struct GeneratedConvert7 : public ::mlir::RewritePattern {
  GeneratedConvert7(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.is_inf", 1, context, {"chlo.is_pos_inf", "mhlo.abs"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::IsInfOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.is_inf' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::AbsOp tblgen_AbsOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      tblgen_AbsOp_0 = rewriter.create<::mlir::mhlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::chlo::IsPosInfOp tblgen_IsPosInfOp_1;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_AbsOp_0.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_IsPosInfOp_1 = rewriter.create<::mlir::chlo::IsPosInfOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_IsPosInfOp_1.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:268
*/
struct GeneratedConvert8 : public ::mlir::RewritePattern {
  GeneratedConvert8(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.is_pos_inf", 1, context, {"mhlo.compare"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::IsPosInfOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.is_pos_inf' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLikeInfValue(rewriter, odsLoc, (*input.begin()), /*negative=*/false); (void)nativeVar_0;
    auto nativeVar_1 = StringAttr(); (void)nativeVar_1;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back(nativeVar_0);
      if (auto tmpAttr = rewriter.getStringAttr("EQ")) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("comparison_direction"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("compare_type"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_CompareOp_2 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_CompareOp_2.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:278
*/
struct GeneratedConvert9 : public ::mlir::RewritePattern {
  GeneratedConvert9(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.is_neg_inf", 1, context, {"mhlo.compare"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::IsNegInfOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.is_neg_inf' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = chlo::getConstantLikeInfValue(rewriter, odsLoc, (*input.begin()), /*negative=*/true); (void)nativeVar_0;
    auto nativeVar_1 = StringAttr(); (void)nativeVar_1;
    ::mlir::mhlo::CompareOp tblgen_CompareOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back(nativeVar_0);
      if (auto tmpAttr = rewriter.getStringAttr("EQ")) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("comparison_direction"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("compare_type"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_CompareOp_2 = rewriter.create<::mlir::mhlo::CompareOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_CompareOp_2.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/transforms/chlo_legalize_to_hlo_patterns.td:288
*/
struct GeneratedConvert10 : public ::mlir::RewritePattern {
  GeneratedConvert10(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("chlo.tan", 1, context, {"mhlo.cosine", "mhlo.divide", "mhlo.sine"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::chlo::TanOp>(op0); (void)castedOp0;
    if(failed(__mlir_ods_local_type_constraint_chlo_legalize_to_hlo_patterns0(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'chlo.tan' failed to satisfy constraint: 'Non-complex element type'"))) {
      return ::mlir::failure();
    }
    input = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::SinOp tblgen_SinOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_SinOp_0 = rewriter.create<::mlir::mhlo::SinOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::CosOp tblgen_CosOp_1;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_CosOp_1 = rewriter.create<::mlir::mhlo::CosOp>(odsLoc, tblgen_values, tblgen_attrs);
    }
    ::mlir::mhlo::DivOp tblgen_DivOp_2;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SinOp_0.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_CosOp_1.getODSResults(0).begin()));
      tblgen_DivOp_2 = rewriter.create<::mlir::mhlo::DivOp>(odsLoc, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DivOp_2.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<GeneratedConvert0>(patterns.getContext());
  patterns.add<GeneratedConvert1>(patterns.getContext());
  patterns.add<GeneratedConvert2>(patterns.getContext());
  patterns.add<GeneratedConvert3>(patterns.getContext());
  patterns.add<GeneratedConvert4>(patterns.getContext());
  patterns.add<GeneratedConvert5>(patterns.getContext());
  patterns.add<GeneratedConvert6>(patterns.getContext());
  patterns.add<GeneratedConvert7>(patterns.getContext());
  patterns.add<GeneratedConvert8>(patterns.getContext());
  patterns.add<GeneratedConvert9>(patterns.getContext());
  patterns.add<GeneratedConvert10>(patterns.getContext());
}
