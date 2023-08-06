/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Struct Utility Declarations                                                *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace TFL {

// Dimension metadata.
class DimensionMetadataAttr : public ::mlir::DictionaryAttr {
public:
  using ::mlir::DictionaryAttr::DictionaryAttr;
  static bool classof(::mlir::Attribute attr);
  static DimensionMetadataAttr get(
      ::mlir::StringAttr format,
      ::mlir::IntegerAttr dense_size,
      ::mlir::ArrayAttr segments,
      ::mlir::ArrayAttr indices,
      ::mlir::MLIRContext* context);

  ::mlir::StringAttr format() const;
  ::mlir::IntegerAttr dense_size() const;
  ::mlir::ArrayAttr segments() const;
  ::mlir::ArrayAttr indices() const;
};

} // namespace mlir
} // namespace TFL
namespace mlir {
namespace TFL {

// Sparsity parameter.
class SparsityParameterAttr : public ::mlir::DictionaryAttr {
public:
  using ::mlir::DictionaryAttr::DictionaryAttr;
  static bool classof(::mlir::Attribute attr);
  static SparsityParameterAttr get(
      ::mlir::ArrayAttr traversal_order,
      ::mlir::ArrayAttr block_map,
      ::mlir::ArrayAttr dim_metadata,
      ::mlir::MLIRContext* context);

  ::mlir::ArrayAttr traversal_order() const;
  ::mlir::ArrayAttr block_map() const;
  ::mlir::ArrayAttr dim_metadata() const;
};

} // namespace mlir
} // namespace TFL
