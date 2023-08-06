/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

class AffineQuantizedOpInterface;
namespace detail {
struct AffineQuantizedOpInterfaceInterfaceTraits {
  struct Concept {
    int (*GetAffineOperandIndex)(const Concept *impl, ::mlir::Operation *);
    bool (*RequiredNarrowRangeAffineOperand)(const Concept *impl, ::mlir::Operation *);
    int (*GetQuantizationDimIndex)(const Concept *impl, ::mlir::Operation *);
    int (*GetChannelDimIndex)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = AffineQuantizedOpInterface;
    Model() : Concept{GetAffineOperandIndex, RequiredNarrowRangeAffineOperand, GetQuantizationDimIndex, GetChannelDimIndex} {}

    static inline int GetAffineOperandIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool RequiredNarrowRangeAffineOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int GetQuantizationDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int GetChannelDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = AffineQuantizedOpInterface;
    FallbackModel() : Concept{GetAffineOperandIndex, RequiredNarrowRangeAffineOperand, GetQuantizationDimIndex, GetChannelDimIndex} {}

    static inline int GetAffineOperandIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool RequiredNarrowRangeAffineOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int GetQuantizationDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline int GetChannelDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    int GetAffineOperandIndex(::mlir::Operation *tablegen_opaque_val) const;
    bool RequiredNarrowRangeAffineOperand(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct AffineQuantizedOpInterfaceTrait;

} // namespace detail
class AffineQuantizedOpInterface : public ::mlir::OpInterface<AffineQuantizedOpInterface, detail::AffineQuantizedOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<AffineQuantizedOpInterface, detail::AffineQuantizedOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::AffineQuantizedOpInterfaceTrait<ConcreteOp> {};
  int GetAffineOperandIndex();
  bool RequiredNarrowRangeAffineOperand();
  int GetQuantizationDimIndex();
  int GetChannelDimIndex();
};
namespace detail {
  template <typename ConcreteOp>
  struct AffineQuantizedOpInterfaceTrait : public ::mlir::OpInterface<AffineQuantizedOpInterface, detail::AffineQuantizedOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    int GetAffineOperandIndex() {
      return 1;
    }
    bool RequiredNarrowRangeAffineOperand() {
      return true;
    }
  };
}// namespace detail
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetAffineOperandIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetAffineOperandIndex();
}
template<typename ConcreteOp>
bool detail::AffineQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::RequiredNarrowRangeAffineOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).RequiredNarrowRangeAffineOperand();
}
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetQuantizationDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetQuantizationDimIndex();
}
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetChannelDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetChannelDimIndex();
}
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetAffineOperandIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetAffineOperandIndex(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::AffineQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::RequiredNarrowRangeAffineOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->RequiredNarrowRangeAffineOperand(tablegen_opaque_val);
}
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetQuantizationDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetQuantizationDimIndex(tablegen_opaque_val);
}
template<typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetChannelDimIndex(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetChannelDimIndex(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
int detail::AffineQuantizedOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::GetAffineOperandIndex(::mlir::Operation *tablegen_opaque_val) const {
return 1;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::AffineQuantizedOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::RequiredNarrowRangeAffineOperand(::mlir::Operation *tablegen_opaque_val) const {
return true;
}
class DynamicRangeQuantizedOpInterface;
namespace detail {
struct DynamicRangeQuantizedOpInterfaceInterfaceTraits {
  struct Concept {
    std::vector<int> (*GetQuantizableOperandIndices)(const Concept *impl, ::mlir::Operation *);
    bool (*GetDynamicRangeQuantKernelSupport)(const Concept *impl, ::mlir::Operation *);
    bool (*RequireAsymmetricQuantizeInputsAttr)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = DynamicRangeQuantizedOpInterface;
    Model() : Concept{GetQuantizableOperandIndices, GetDynamicRangeQuantKernelSupport, RequireAsymmetricQuantizeInputsAttr} {}

    static inline std::vector<int> GetQuantizableOperandIndices(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool GetDynamicRangeQuantKernelSupport(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool RequireAsymmetricQuantizeInputsAttr(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = DynamicRangeQuantizedOpInterface;
    FallbackModel() : Concept{GetQuantizableOperandIndices, GetDynamicRangeQuantKernelSupport, RequireAsymmetricQuantizeInputsAttr} {}

    static inline std::vector<int> GetQuantizableOperandIndices(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool GetDynamicRangeQuantKernelSupport(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool RequireAsymmetricQuantizeInputsAttr(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    std::vector<int> GetQuantizableOperandIndices(::mlir::Operation *tablegen_opaque_val) const;
    bool GetDynamicRangeQuantKernelSupport(::mlir::Operation *tablegen_opaque_val) const;
    bool RequireAsymmetricQuantizeInputsAttr(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct DynamicRangeQuantizedOpInterfaceTrait;

} // namespace detail
class DynamicRangeQuantizedOpInterface : public ::mlir::OpInterface<DynamicRangeQuantizedOpInterface, detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<DynamicRangeQuantizedOpInterface, detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::DynamicRangeQuantizedOpInterfaceTrait<ConcreteOp> {};
  std::vector<int> GetQuantizableOperandIndices();
  bool GetDynamicRangeQuantKernelSupport();
  bool RequireAsymmetricQuantizeInputsAttr();
};
namespace detail {
  template <typename ConcreteOp>
  struct DynamicRangeQuantizedOpInterfaceTrait : public ::mlir::OpInterface<DynamicRangeQuantizedOpInterface, detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    std::vector<int> GetQuantizableOperandIndices() {
      return {};
    }
    bool GetDynamicRangeQuantKernelSupport() {
      return false;
    }
    bool RequireAsymmetricQuantizeInputsAttr() {
      return false;
    }
  };
}// namespace detail
template<typename ConcreteOp>
std::vector<int> detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetQuantizableOperandIndices(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetQuantizableOperandIndices();
}
template<typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetDynamicRangeQuantKernelSupport(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetDynamicRangeQuantKernelSupport();
}
template<typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::Model<ConcreteOp>::RequireAsymmetricQuantizeInputsAttr(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).RequireAsymmetricQuantizeInputsAttr();
}
template<typename ConcreteOp>
std::vector<int> detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetQuantizableOperandIndices(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetQuantizableOperandIndices(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetDynamicRangeQuantKernelSupport(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetDynamicRangeQuantKernelSupport(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::RequireAsymmetricQuantizeInputsAttr(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->RequireAsymmetricQuantizeInputsAttr(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
std::vector<int> detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::GetQuantizableOperandIndices(::mlir::Operation *tablegen_opaque_val) const {
return {};
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::GetDynamicRangeQuantKernelSupport(::mlir::Operation *tablegen_opaque_val) const {
return false;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::DynamicRangeQuantizedOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::RequireAsymmetricQuantizeInputsAttr(::mlir::Operation *tablegen_opaque_val) const {
return false;
}
class FixedOutputRangeInterface;
namespace detail {
struct FixedOutputRangeInterfaceInterfaceTraits {
  struct Concept {
    UniformQuantizedType (*GetFixedOutputRange)(const Concept *impl, ::mlir::Operation *, bool, int);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = FixedOutputRangeInterface;
    Model() : Concept{GetFixedOutputRange} {}

    static inline UniformQuantizedType GetFixedOutputRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = FixedOutputRangeInterface;
    FallbackModel() : Concept{GetFixedOutputRange} {}

    static inline UniformQuantizedType GetFixedOutputRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct FixedOutputRangeInterfaceTrait;

} // namespace detail
class FixedOutputRangeInterface : public ::mlir::OpInterface<FixedOutputRangeInterface, detail::FixedOutputRangeInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<FixedOutputRangeInterface, detail::FixedOutputRangeInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::FixedOutputRangeInterfaceTrait<ConcreteOp> {};
  UniformQuantizedType GetFixedOutputRange(bool sign, int bit_width);
};
namespace detail {
  template <typename ConcreteOp>
  struct FixedOutputRangeInterfaceTrait : public ::mlir::OpInterface<FixedOutputRangeInterface, detail::FixedOutputRangeInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
UniformQuantizedType detail::FixedOutputRangeInterfaceInterfaceTraits::Model<ConcreteOp>::GetFixedOutputRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetFixedOutputRange(sign, bit_width);
}
template<typename ConcreteOp>
UniformQuantizedType detail::FixedOutputRangeInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetFixedOutputRange(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) {
  return static_cast<const ConcreteOp *>(impl)->GetFixedOutputRange(tablegen_opaque_val, sign, bit_width);
}
class SameScalesOpInterface;
namespace detail {
struct SameScalesOpInterfaceInterfaceTraits {
  struct Concept {
    bool (*RequiredSameOperandsAndResultsScale)(const Concept *impl, ::mlir::Operation *, bool, int);
    bool (*RequiredSameQuantizedAxes)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = SameScalesOpInterface;
    Model() : Concept{RequiredSameOperandsAndResultsScale, RequiredSameQuantizedAxes} {}

    static inline bool RequiredSameOperandsAndResultsScale(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width);
    static inline bool RequiredSameQuantizedAxes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = SameScalesOpInterface;
    FallbackModel() : Concept{RequiredSameOperandsAndResultsScale, RequiredSameQuantizedAxes} {}

    static inline bool RequiredSameOperandsAndResultsScale(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width);
    static inline bool RequiredSameQuantizedAxes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    bool RequiredSameOperandsAndResultsScale(::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) const;
    bool RequiredSameQuantizedAxes(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct SameScalesOpInterfaceTrait;

} // namespace detail
class SameScalesOpInterface : public ::mlir::OpInterface<SameScalesOpInterface, detail::SameScalesOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<SameScalesOpInterface, detail::SameScalesOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::SameScalesOpInterfaceTrait<ConcreteOp> {};
  bool RequiredSameOperandsAndResultsScale(bool sign, int bit_width);
  bool RequiredSameQuantizedAxes();
};
namespace detail {
  template <typename ConcreteOp>
  struct SameScalesOpInterfaceTrait : public ::mlir::OpInterface<SameScalesOpInterface, detail::SameScalesOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    bool RequiredSameOperandsAndResultsScale(bool sign, int bit_width) {
      return true;
    }
    bool RequiredSameQuantizedAxes() {
      return true;
    }
    static ::mlir::LogicalResult verifyTrait(::mlir::Operation *op) {
      return quant::VerifySameScales(op);
    }
  };
}// namespace detail
template<typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::Model<ConcreteOp>::RequiredSameOperandsAndResultsScale(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).RequiredSameOperandsAndResultsScale(sign, bit_width);
}
template<typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::Model<ConcreteOp>::RequiredSameQuantizedAxes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).RequiredSameQuantizedAxes();
}
template<typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::RequiredSameOperandsAndResultsScale(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) {
  return static_cast<const ConcreteOp *>(impl)->RequiredSameOperandsAndResultsScale(tablegen_opaque_val, sign, bit_width);
}
template<typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::RequiredSameQuantizedAxes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->RequiredSameQuantizedAxes(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::RequiredSameOperandsAndResultsScale(::mlir::Operation *tablegen_opaque_val, bool sign, int bit_width) const {
return true;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::SameScalesOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::RequiredSameQuantizedAxes(::mlir::Operation *tablegen_opaque_val) const {
return true;
}
