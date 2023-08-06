/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


static ::mlir::LogicalResult __mlir_ods_local_type_constraint_mhlo_canonicalize0(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Type type,
    ::llvm::StringRef failureStr) {
  if (!(((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((elementType.isa<::mlir::FloatType>())) || ((elementType.isSignlessInteger(1))) || ((((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isSignlessInteger(32))) || ((elementType.isSignlessInteger(64)))) || (((elementType.isUnsignedInteger(8))) || ((elementType.isUnsignedInteger(16))) || ((elementType.isUnsignedInteger(32))) || ((elementType.isUnsignedInteger(64))))) || (((elementType.isa<::mlir::ComplexType>())) && (((elementType.cast<::mlir::ComplexType>().getElementType().isF32())) || ((elementType.cast<::mlir::ComplexType>().getElementType().isF64())))); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": tensor of floating-point or pred (AKA boolean or 1-bit integer) or 8/16/32/64-bit signless integer or 8/16/32/64-bit unsigned integer or complex type with 32-bit float or 64-bit float elements values";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_mhlo_canonicalize0(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!((hlo::IsSequenceStartingWith0(attr)))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": ";
    });
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_mhlo_canonicalize1(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Attribute attr,
    ::llvm::StringRef failureStr) {
  if (!(((attr.isa<::mlir::DenseIntElementsAttr>())) && ((attr.cast<::mlir::DenseIntElementsAttr>().getType().getElementType().isSignlessInteger(64))))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": 64-bit signless integer elements attribute";
    });
  }
  return ::mlir::success();
}
/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/mhlo_canonicalize.td:48
*/
struct DPadToPad : public ::mlir::RewritePattern {
  DPadToPad(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_pad", 4, context, {"mhlo.pad"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr interior_paddin;
    ::mlir::ElementsAttr edge_padding_low;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::ElementsAttr edge_padding_high;
    ::mlir::Operation::operand_range padding_value(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicPadOp>(op0); (void)castedOp0;
    input = castedOp0.getODSOperands(0);
    padding_value = castedOp0.getODSOperands(1);
    {
      auto *op1 = (*castedOp0.getODSOperands(2).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 2 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        edge_padding_low = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(3).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 3 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        edge_padding_high = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(4).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 4 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        interior_paddin = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = edge_padding_low.cast<DenseIntElementsAttr>(); (void)nativeVar_0;
    auto nativeVar_1 = edge_padding_high.cast<DenseIntElementsAttr>(); (void)nativeVar_1;
    auto nativeVar_2 = interior_paddin.cast<DenseIntElementsAttr>(); (void)nativeVar_2;
    ::mlir::mhlo::PadOp tblgen_PadOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*padding_value.begin()));
      if (auto tmpAttr = nativeVar_0) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("edge_padding_low"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("edge_padding_high"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_2) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("interior_padding"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_PadOp_3 = rewriter.create<::mlir::mhlo::PadOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_PadOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/mhlo_canonicalize.td:61
*/
struct RealDSliceToSlice : public ::mlir::RewritePattern {
  RealDSliceToSlice(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.real_dynamic_slice", 4, context, {"mhlo.slice"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr strides;
    ::mlir::Operation::operand_range operand(op0->getOperands());
    ::mlir::ElementsAttr limit_indices;
    ::mlir::ElementsAttr start_indices;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::RealDynamicSliceOp>(op0); (void)castedOp0;
    operand = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        start_indices = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(2).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 2 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        limit_indices = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(3).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 3 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::mhlo::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::mhlo::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'mhlo.constant' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize1(rewriter, op1, tblgen_attr, "op 'mhlo.constant' attribute 'value' failed to satisfy constraint: '64-bit signless integer elements attribute'"))) {
          return ::mlir::failure();
        }
        strides = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = start_indices.cast<DenseIntElementsAttr>(); (void)nativeVar_0;
    auto nativeVar_1 = limit_indices.cast<DenseIntElementsAttr>(); (void)nativeVar_1;
    auto nativeVar_2 = strides.cast<DenseIntElementsAttr>(); (void)nativeVar_2;
    ::mlir::mhlo::SliceOp tblgen_SliceOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*operand.begin()));
      if (auto tmpAttr = nativeVar_0) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("start_indices"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_1) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("limit_indices"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_2) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("strides"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_SliceOp_3 = rewriter.create<::mlir::mhlo::SliceOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_SliceOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/mhlo_canonicalize.td:39
*/
struct RemoveRedundantDynamicBroadcast : public ::mlir::RewritePattern {
  RemoveRedundantDynamicBroadcast(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_broadcast_in_dim", 2, context, {"mhlo.dynamic_reshape"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::DenseIntElementsAttr dims;
    ::mlir::Operation::operand_range operand(op0->getOperands());
    ::mlir::Operation::operand_range shape(op0->getOperands());
    ::mlir::Operation::operand_range shape0(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicBroadcastInDimOp>(op0); (void)castedOp0;
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
      operand = castedOp1.getODSOperands(0);
      shape = castedOp1.getODSOperands(1);
      tblgen_ops.push_back(op1);
    }
    shape0 = castedOp0.getODSOperands(1);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::DenseIntElementsAttr>("broadcast_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.dynamic_broadcast_in_dim' to have attribute 'broadcast_dimensions' of type '::mlir::DenseIntElementsAttr'";
        });
      }
      if(failed(__mlir_ods_local_attr_constraint_mhlo_canonicalize0(rewriter, op0, tblgen_attr, "op 'mhlo.dynamic_broadcast_in_dim' attribute 'broadcast_dimensions' failed to satisfy constraint: ''"))) {
        return ::mlir::failure();
      }
      dims = tblgen_attr;
    }
    if (!(*shape.begin() == *shape0.begin())){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "Operands 'shape' and 'shape0' must be equal";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::DynamicReshapeOp tblgen_DynamicReshapeOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*operand.begin()));
      tblgen_values.push_back((*shape.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DynamicReshapeOp_0 = rewriter.create<::mlir::mhlo::DynamicReshapeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DynamicReshapeOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/mhlo_canonicalize.td:33
*/
struct RemoveRedundantDynamicReshape : public ::mlir::RewritePattern {
  RemoveRedundantDynamicReshape(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.dynamic_reshape", 2, context, {"mhlo.dynamic_reshape"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range shape1(op0->getOperands());
    ::mlir::Operation::operand_range shape2(op0->getOperands());
    ::mlir::Operation::operand_range operand(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::DynamicReshapeOp>(op0); (void)castedOp0;
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
      operand = castedOp1.getODSOperands(0);
      shape1 = castedOp1.getODSOperands(1);
      tblgen_ops.push_back(op1);
    }
    shape2 = castedOp0.getODSOperands(1);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::mhlo::DynamicReshapeOp tblgen_DynamicReshapeOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*operand.begin()));
      tblgen_values.push_back((*shape2.begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DynamicReshapeOp_0 = rewriter.create<::mlir::mhlo::DynamicReshapeOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DynamicReshapeOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/hlo/lib/Dialect/mhlo/IR/mhlo_canonicalize.td:27
*/
struct UnaryEinsumToEinsum : public ::mlir::RewritePattern {
  UnaryEinsumToEinsum(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("mhlo.unary_einsum", 1, context, {"mhlo.constant", "mhlo.einsum"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range operand(op0->getOperands());
    ::mlir::StringAttr equation;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::mhlo::UnaryEinsumOp>(op0); (void)castedOp0;
    operand = castedOp0.getODSOperands(0);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::StringAttr>("einsum_config");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'mhlo.unary_einsum' to have attribute 'einsum_config' of type '::mlir::StringAttr'";
        });
      }
      equation = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = hlo::GetScalarOfType(getElementTypeOrSelf((*operand.begin())),1); (void)nativeVar_0;
    ::mlir::mhlo::ConstOp tblgen_ConstOp_1;
    {
      tblgen_ConstOp_1 = rewriter.create<::mlir::mhlo::ConstOp>(odsLoc,
        /*value=*/nativeVar_0
      );
    }
    auto nativeVar_2 = rewriter.getStringAttr("," + equation.getValue().str()); (void)nativeVar_2;
    ::mlir::mhlo::EinsumOp tblgen_EinsumOp_3;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_ConstOp_1.getODSResults(0).begin()));
      tblgen_values.push_back((*operand.begin()));
      if (auto tmpAttr = nativeVar_2) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("einsum_config"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_EinsumOp_3 = rewriter.create<::mlir::mhlo::EinsumOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_EinsumOp_3.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<DPadToPad>(patterns.getContext());
  patterns.add<RealDSliceToSlice>(patterns.getContext());
  patterns.add<RemoveRedundantDynamicBroadcast>(patterns.getContext());
  patterns.add<RemoveRedundantDynamicReshape>(patterns.getContext());
  patterns.add<UnaryEinsumToEinsum>(patterns.getContext());
}
