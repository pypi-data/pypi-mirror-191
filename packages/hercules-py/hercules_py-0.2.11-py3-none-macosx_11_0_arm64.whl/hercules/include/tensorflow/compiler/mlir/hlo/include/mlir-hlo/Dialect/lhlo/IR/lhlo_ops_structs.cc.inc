/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Struct Utility Definitions                                                 *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace lmhlo {
CustomCallTargetArgMapping CustomCallTargetArgMapping::get(
    ::mlir::IntegerAttr num_args,
    ::mlir::IntegerAttr num_results,
    ::mlir::ArrayAttr args_to_target_args,
    ::mlir::ArrayAttr results_to_target_results,
    ::mlir::MLIRContext* context) {
  ::llvm::SmallVector<::mlir::NamedAttribute, 4> fields;

  assert(num_args);
  auto num_args_id = ::mlir::StringAttr::get(context, "num_args");
  fields.emplace_back(num_args_id, num_args);

  assert(num_results);
  auto num_results_id = ::mlir::StringAttr::get(context, "num_results");
  fields.emplace_back(num_results_id, num_results);

  assert(args_to_target_args);
  auto args_to_target_args_id = ::mlir::StringAttr::get(context, "args_to_target_args");
  fields.emplace_back(args_to_target_args_id, args_to_target_args);

  assert(results_to_target_results);
  auto results_to_target_results_id = ::mlir::StringAttr::get(context, "results_to_target_results");
  fields.emplace_back(results_to_target_results_id, results_to_target_results);

  ::mlir::Attribute dict = ::mlir::DictionaryAttr::get(context, fields);
  return dict.dyn_cast<CustomCallTargetArgMapping>();
}

bool CustomCallTargetArgMapping::classof(::mlir::Attribute attr) {
  if (!attr)
    return false;
  auto derived = attr.dyn_cast<::mlir::DictionaryAttr>();
  if (!derived)
    return false;
  int num_absent_attrs = 0;

  auto num_args = derived.get("num_args");
  if (!num_args || !(((num_args.isa<::mlir::IntegerAttr>())) && ((num_args.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  auto num_results = derived.get("num_results");
  if (!num_results || !(((num_results.isa<::mlir::IntegerAttr>())) && ((num_results.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  auto args_to_target_args = derived.get("args_to_target_args");
  if (!args_to_target_args || !(((args_to_target_args.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(args_to_target_args.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  auto results_to_target_results = derived.get("results_to_target_results");
  if (!results_to_target_results || !(((results_to_target_results.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(results_to_target_results.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  return derived.size() + num_absent_attrs == 4;
}

::mlir::IntegerAttr CustomCallTargetArgMapping::num_args() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto num_args = derived.get("num_args");
  assert(num_args && "attribute not found.");
  assert(num_args.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return num_args.cast<::mlir::IntegerAttr>();
}

::mlir::IntegerAttr CustomCallTargetArgMapping::num_results() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto num_results = derived.get("num_results");
  assert(num_results && "attribute not found.");
  assert(num_results.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return num_results.cast<::mlir::IntegerAttr>();
}

::mlir::ArrayAttr CustomCallTargetArgMapping::args_to_target_args() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto args_to_target_args = derived.get("args_to_target_args");
  assert(args_to_target_args && "attribute not found.");
  assert(args_to_target_args.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return args_to_target_args.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr CustomCallTargetArgMapping::results_to_target_results() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto results_to_target_results = derived.get("results_to_target_results");
  assert(results_to_target_results && "attribute not found.");
  assert(results_to_target_results.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return results_to_target_results.cast<::mlir::ArrayAttr>();
}
} // namespace lmhlo
} // namespace mlir
