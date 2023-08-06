/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyComparisonDirection(ComparisonDirection val) {
  switch (val) {
    case ComparisonDirection::EQ: return "EQ";
    case ComparisonDirection::NE: return "NE";
    case ComparisonDirection::GE: return "GE";
    case ComparisonDirection::GT: return "GT";
    case ComparisonDirection::LE: return "LE";
    case ComparisonDirection::LT: return "LT";
  }
  return "";
}

::llvm::Optional<ComparisonDirection> symbolizeComparisonDirection(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ComparisonDirection>>(str)
      .Case("EQ", ComparisonDirection::EQ)
      .Case("NE", ComparisonDirection::NE)
      .Case("GE", ComparisonDirection::GE)
      .Case("GT", ComparisonDirection::GT)
      .Case("LE", ComparisonDirection::LE)
      .Case("LT", ComparisonDirection::LT)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyComparisonType(ComparisonType val) {
  switch (val) {
    case ComparisonType::FLOAT: return "FLOAT";
    case ComparisonType::TOTALORDER: return "TOTALORDER";
    case ComparisonType::SIGNED: return "SIGNED";
    case ComparisonType::UNSIGNED: return "UNSIGNED";
  }
  return "";
}

::llvm::Optional<ComparisonType> symbolizeComparisonType(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ComparisonType>>(str)
      .Case("FLOAT", ComparisonType::FLOAT)
      .Case("TOTALORDER", ComparisonType::TOTALORDER)
      .Case("SIGNED", ComparisonType::SIGNED)
      .Case("UNSIGNED", ComparisonType::UNSIGNED)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyCustomCallApiVersion(CustomCallApiVersion val) {
  switch (val) {
    case CustomCallApiVersion::API_VERSION_UNSPECIFIED: return "API_VERSION_UNSPECIFIED";
    case CustomCallApiVersion::API_VERSION_ORIGINAL: return "API_VERSION_ORIGINAL";
    case CustomCallApiVersion::API_VERSION_STATUS_RETURNING: return "API_VERSION_STATUS_RETURNING";
  }
  return "";
}

::llvm::Optional<CustomCallApiVersion> symbolizeCustomCallApiVersion(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<CustomCallApiVersion>>(str)
      .Case("API_VERSION_UNSPECIFIED", CustomCallApiVersion::API_VERSION_UNSPECIFIED)
      .Case("API_VERSION_ORIGINAL", CustomCallApiVersion::API_VERSION_ORIGINAL)
      .Case("API_VERSION_STATUS_RETURNING", CustomCallApiVersion::API_VERSION_STATUS_RETURNING)
      .Default(::llvm::None);
}
::llvm::Optional<CustomCallApiVersion> symbolizeCustomCallApiVersion(uint32_t value) {
  switch (value) {
  case 0: return CustomCallApiVersion::API_VERSION_UNSPECIFIED;
  case 1: return CustomCallApiVersion::API_VERSION_ORIGINAL;
  case 2: return CustomCallApiVersion::API_VERSION_STATUS_RETURNING;
  default: return ::llvm::None;
  }
}

bool CustomCallApiVersionAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 0)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)));
}
CustomCallApiVersionAttr CustomCallApiVersionAttr::get(::mlir::MLIRContext *context, CustomCallApiVersion val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<CustomCallApiVersionAttr>();
}
CustomCallApiVersion CustomCallApiVersionAttr::getValue() const {
  return static_cast<CustomCallApiVersion>(::mlir::IntegerAttr::getInt());
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyDequantizeMode(DequantizeMode val) {
  switch (val) {
    case DequantizeMode::MIN_COMBINED: return "MIN_COMBINED";
  }
  return "";
}

::llvm::Optional<DequantizeMode> symbolizeDequantizeMode(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<DequantizeMode>>(str)
      .Case("MIN_COMBINED", DequantizeMode::MIN_COMBINED)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyFftType(FftType val) {
  switch (val) {
    case FftType::FFT: return "FFT";
    case FftType::IFFT: return "IFFT";
    case FftType::RFFT: return "RFFT";
    case FftType::IRFFT: return "IRFFT";
  }
  return "";
}

::llvm::Optional<FftType> symbolizeFftType(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<FftType>>(str)
      .Case("FFT", FftType::FFT)
      .Case("IFFT", FftType::IFFT)
      .Case("RFFT", FftType::RFFT)
      .Case("IRFFT", FftType::IRFFT)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyFusionKind(FusionKind val) {
  switch (val) {
    case FusionKind::kLoop: return "kLoop";
    case FusionKind::kInput: return "kInput";
    case FusionKind::kOutput: return "kOutput";
    case FusionKind::kCustom: return "kCustom";
  }
  return "";
}

::llvm::Optional<FusionKind> symbolizeFusionKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<FusionKind>>(str)
      .Case("kLoop", FusionKind::kLoop)
      .Case("kInput", FusionKind::kInput)
      .Case("kOutput", FusionKind::kOutput)
      .Case("kCustom", FusionKind::kCustom)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyPrecision(Precision val) {
  switch (val) {
    case Precision::DEFAULT: return "DEFAULT";
    case Precision::HIGH: return "HIGH";
    case Precision::HIGHEST: return "HIGHEST";
  }
  return "";
}

::llvm::Optional<Precision> symbolizePrecision(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<Precision>>(str)
      .Case("DEFAULT", Precision::DEFAULT)
      .Case("HIGH", Precision::HIGH)
      .Case("HIGHEST", Precision::HIGHEST)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

namespace mlir {
namespace mhlo {
::llvm::StringRef stringifyTranspose(Transpose val) {
  switch (val) {
    case Transpose::TRANSPOSE_INVALID: return "TRANSPOSE_INVALID";
    case Transpose::NO_TRANSPOSE: return "NO_TRANSPOSE";
    case Transpose::TRANSPOSE: return "TRANSPOSE";
    case Transpose::ADJOINT: return "ADJOINT";
  }
  return "";
}

::llvm::Optional<Transpose> symbolizeTranspose(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<Transpose>>(str)
      .Case("TRANSPOSE_INVALID", Transpose::TRANSPOSE_INVALID)
      .Case("NO_TRANSPOSE", Transpose::NO_TRANSPOSE)
      .Case("TRANSPOSE", Transpose::TRANSPOSE)
      .Case("ADJOINT", Transpose::ADJOINT)
      .Default(::llvm::None);
}
} // namespace mhlo
} // namespace mlir

