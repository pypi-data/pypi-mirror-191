/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Generated Ops Quant Spec Getters                                           *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

static std::unique_ptr<quant::OpQuantSpec> GetOpQuantSpec(mlir::Operation *op) {
  if (auto lstm_op = llvm::dyn_cast<TFL::LSTMOp>(op)) {
    return GetLstmOpQuantSpec<TFL::LSTMOp>(lstm_op);
  } else if (auto lstm_op = llvm::dyn_cast<TFL::UnidirectionalSequenceLSTMOp>(op)) {
    return GetLstmOpQuantSpec<TFL::UnidirectionalSequenceLSTMOp>(lstm_op);
  }
  auto spec = absl::make_unique<quant::OpQuantSpec>();
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::AbsOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::AddOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ArgMaxOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ArgMinOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::AssignVariableOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::AveragePool2DOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::BasicLSTMOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::BatchMatMulOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::BatchToSpaceNdOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::BidirectionalSequenceLSTMOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::BroadcastToOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ConcatenationOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ConstOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Conv2DOp>(op)) {
    spec->biases_params.emplace(std::make_pair(2, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Conv2DOp>(op)) {
    spec->coeff_op_quant_dim[tfl.GetCoefficientOperandIndex()] = tfl.GetQuantizationDim();
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Conv2DOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Conv3DOp>(op)) {
    spec->biases_params.emplace(std::make_pair(2, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Conv3DTransposeOp>(op)) {
    spec->biases_params.emplace(std::make_pair(2, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::DepthToSpaceOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::DepthwiseConv2DOp>(op)) {
    spec->biases_params.emplace(std::make_pair(2, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::DepthwiseConv2DOp>(op)) {
    spec->coeff_op_quant_dim[tfl.GetCoefficientOperandIndex()] = tfl.GetQuantizationDim();
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::DepthwiseConv2DOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::EqualOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ExpandDimsOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ExternalConstOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::FakeQuantOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::FillOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::FullyConnectedOp>(op)) {
    spec->biases_params.emplace(std::make_pair(2, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::FullyConnectedOp>(op)) {
    spec->coeff_op_quant_dim[tfl.GetCoefficientOperandIndex()] = tfl.GetQuantizationDim();
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::FullyConnectedOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::GatherNdOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::GatherOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::GreaterEqualOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::GreaterOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::HardSwishOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::IfOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::L2NormalizationOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LSTMOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LeakyReluOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LessEqualOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LessOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LogSoftmaxOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::LogisticOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MatrixDiagOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MatrixSetDiagOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MaxPool2DOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MaximumOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MeanOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MinimumOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MirrorPadOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::MulOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::NumericVerifyOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::OneHotOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::PReluOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::PackOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::PadOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::PadV2Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::RankOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReadVariableOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReduceMaxOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReduceMinOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReduceProdOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Relu1Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::Relu6Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReluOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReshapeOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ResizeBilinearOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ResizeNearestNeighborOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReverseSequenceOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ReverseV2Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::RsqrtOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SVDFOp>(op)) {
    spec->biases_params.emplace(std::make_pair(3, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SVDFOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ScatterNdOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SelectOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SelectV2Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::ShapeOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SliceOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SoftmaxOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SpaceToBatchNdOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SpaceToDepthOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SparseConstOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SparseToDenseOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SplitOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SplitVOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SquaredDifferenceOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SqueezeOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::StridedSliceOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SubOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::SumOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TanhOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TileOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TopKV2Op>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TransposeConvOp>(op)) {
    spec->biases_params.emplace(std::make_pair(3, std::make_pair(tfl.GetAllNonBiasOperands(),quant::GetUniformQuantizedTypeForBias)));
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TransposeConvOp>(op)) {
    spec->coeff_op_quant_dim[tfl.GetCoefficientOperandIndex()] = tfl.GetQuantizationDim();
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TransposeConvOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::TransposeOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::UnidirectionalSequenceLSTMOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::UnidirectionalSequenceRNNOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::UniqueOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::UnpackOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::WhileOp>(op)) {
  }
  if (auto tfl = llvm::dyn_cast<::mlir::TFL::YieldOp>(op)) {
  }
  return spec;
}
