/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::tf_device::ClusterFuncOp,
::mlir::tf_device::ClusterOp,
::mlir::tf_device::LaunchFuncOp,
::mlir::tf_device::LaunchOp,
::mlir::tf_device::ParallelExecuteOp,
::mlir::tf_device::ReceiveOp,
::mlir::tf_device::RemoteRunOp,
::mlir::tf_device::ReplicateOp,
::mlir::tf_device::ReturnOp,
::mlir::tf_device::SendOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace tf_device {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tf_device_ops0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((true))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be any type, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_device_ops0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::FlatSymbolRefAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: flat symbol reference attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_device_ops1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::StringAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: string attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_device_ops2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::DenseIntElementsAttr>())) && ((attr.cast<::mlir::DenseIntElementsAttr>().getType().getElementType().isSignlessInteger(32))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit signless integer elements attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_device_ops3(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && ((attr.cast<::mlir::IntegerAttr>().getInt() >= 2)))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 32-bit signless integer attribute whose minimum value is 2";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tf_device_ops4(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !((attr.isa<::mlir::DictionaryAttr>()))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: dictionary of named attribute values";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_region_constraint_tf_device_ops0(
    ::mlir::Operation *op, ::mlir::Region &region, ::llvm::StringRef regionName,
    unsigned regionIndex) {
  if (!((::llvm::hasNItems(region, 1)))) {
    return op->emitOpError("region #") << regionIndex
        << (regionName.empty() ? " " : " ('" + regionName + "') ")
        << "failed to verify constraint: region with 1 blocks";
  }
  return ::mlir::success();
}
} // namespace tf_device
} // namespace mlir
namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ClusterFuncOp definitions
//===----------------------------------------------------------------------===//

ClusterFuncOpAdaptor::ClusterFuncOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ClusterFuncOpAdaptor::ClusterFuncOpAdaptor(ClusterFuncOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ClusterFuncOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ClusterFuncOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange ClusterFuncOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange ClusterFuncOpAdaptor::operands() {
  return getODSOperands(0);
}

::mlir::DictionaryAttr ClusterFuncOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::FlatSymbolRefAttr ClusterFuncOpAdaptor::func() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::FlatSymbolRefAttr attr = odsAttrs.get("func").cast<::mlir::FlatSymbolRefAttr>();
  return attr;
}

::mlir::LogicalResult ClusterFuncOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_func = odsAttrs.get("func");
    if (!tblgen_func)
      return emitError(loc, "'tf_device.cluster_func' op ""requires attribute 'func'");

    if (tblgen_func && !((tblgen_func.isa<::mlir::FlatSymbolRefAttr>())))
      return emitError(loc, "'tf_device.cluster_func' op ""attribute 'func' failed to satisfy constraint: flat symbol reference attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ClusterFuncOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range ClusterFuncOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range ClusterFuncOp::operands() {
  return getODSOperands(0);
}

::mlir::MutableOperandRange ClusterFuncOp::operandsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> ClusterFuncOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range ClusterFuncOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range ClusterFuncOp::results() {
  return getODSResults(0);
}

::mlir::FlatSymbolRefAttr ClusterFuncOp::funcAttr() {
  return (*this)->getAttr(funcAttrName()).cast<::mlir::FlatSymbolRefAttr>();
}

::llvm::StringRef ClusterFuncOp::func() {
  auto attr = funcAttr();
  return attr.getValue();
}

void ClusterFuncOp::funcAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(funcAttrName(), attr);
}

void ClusterFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::FlatSymbolRefAttr func, ::mlir::ValueRange operands) {
  odsState.addOperands(operands);
  odsState.addAttribute(funcAttrName(odsState.name), func);
  odsState.addTypes(results);
}

void ClusterFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::llvm::StringRef func, ::mlir::ValueRange operands) {
  odsState.addOperands(operands);
  odsState.addAttribute(funcAttrName(odsState.name), ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), func));
  odsState.addTypes(results);
}

void ClusterFuncOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ClusterFuncOp::verify() {
  {
    auto tblgen_func = (*this)->getAttr(funcAttrName());
    if (!tblgen_func)
      return emitOpError("requires attribute 'func'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops0(*this, tblgen_func, "func")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ClusterFuncOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ClusterOp definitions
//===----------------------------------------------------------------------===//

ClusterOpAdaptor::ClusterOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ClusterOpAdaptor::ClusterOpAdaptor(ClusterOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ClusterOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ClusterOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange ClusterOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr ClusterOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr ClusterOpAdaptor::policy() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("policy").dyn_cast_or_null<::mlir::StringAttr>();
  return attr;
}

::mlir::RegionRange ClusterOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &ClusterOpAdaptor::body() {
  return *odsRegions[0];
}

::mlir::LogicalResult ClusterOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_policy = odsAttrs.get("policy");
    if (tblgen_policy && !((tblgen_policy.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.cluster' op ""attribute 'policy' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ClusterOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ClusterOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> ClusterOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range ClusterOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range ClusterOp::results() {
  return getODSResults(0);
}

::mlir::Region &ClusterOp::body() {
  return (*this)->getRegion(0);
}

::mlir::StringAttr ClusterOp::policyAttr() {
  return (*this)->getAttr(policyAttrName()).dyn_cast_or_null<::mlir::StringAttr>();
}

::llvm::Optional< ::llvm::StringRef > ClusterOp::policy() {
  auto attr = policyAttr();
  return attr ? ::llvm::Optional< ::llvm::StringRef >(attr.getValue()) : (::llvm::None);
}

void ClusterOp::policyAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(policyAttrName(), attr);
}

::mlir::Attribute ClusterOp::removePolicyAttr() {
  return (*this)->removeAttr(policyAttrName());
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, TypeRange resultTypes) {
      build(odsBuilder, odsState, resultTypes, mlir::StringAttr {});
    
}

void ClusterOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, /*optional*/::mlir::StringAttr policy) {
  if (policy) {
  odsState.addAttribute(policyAttrName(odsState.name), policy);
  }
  (void)odsState.addRegion();
  odsState.addTypes(results);
}

void ClusterOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ClusterOp::verify() {
  {
    auto tblgen_policy = (*this)->getAttr(policyAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_policy, "policy")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_tf_device_ops0(*this, region, "body", index++)))
        return ::mlir::failure();
  }
  return ::mlir::success();
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ClusterOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::LaunchFuncOp definitions
//===----------------------------------------------------------------------===//

LaunchFuncOpAdaptor::LaunchFuncOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

LaunchFuncOpAdaptor::LaunchFuncOpAdaptor(LaunchFuncOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange LaunchFuncOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> LaunchFuncOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange LaunchFuncOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange LaunchFuncOpAdaptor::operands() {
  return getODSOperands(0);
}

::mlir::DictionaryAttr LaunchFuncOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr LaunchFuncOpAdaptor::device() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("device").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::FlatSymbolRefAttr LaunchFuncOpAdaptor::func() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::FlatSymbolRefAttr attr = odsAttrs.get("func").cast<::mlir::FlatSymbolRefAttr>();
  return attr;
}

::mlir::LogicalResult LaunchFuncOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_device = odsAttrs.get("device");
    if (!tblgen_device)
      return emitError(loc, "'tf_device.launch_func' op ""requires attribute 'device'");

    if (tblgen_device && !((tblgen_device.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.launch_func' op ""attribute 'device' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_func = odsAttrs.get("func");
    if (!tblgen_func)
      return emitError(loc, "'tf_device.launch_func' op ""requires attribute 'func'");

    if (tblgen_func && !((tblgen_func.isa<::mlir::FlatSymbolRefAttr>())))
      return emitError(loc, "'tf_device.launch_func' op ""attribute 'func' failed to satisfy constraint: flat symbol reference attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> LaunchFuncOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range LaunchFuncOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range LaunchFuncOp::operands() {
  return getODSOperands(0);
}

::mlir::MutableOperandRange LaunchFuncOp::operandsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> LaunchFuncOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range LaunchFuncOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range LaunchFuncOp::results() {
  return getODSResults(0);
}

::mlir::StringAttr LaunchFuncOp::deviceAttr() {
  return (*this)->getAttr(deviceAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef LaunchFuncOp::device() {
  auto attr = deviceAttr();
  return attr.getValue();
}

::mlir::FlatSymbolRefAttr LaunchFuncOp::funcAttr() {
  return (*this)->getAttr(funcAttrName()).cast<::mlir::FlatSymbolRefAttr>();
}

::llvm::StringRef LaunchFuncOp::func() {
  auto attr = funcAttr();
  return attr.getValue();
}

void LaunchFuncOp::deviceAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(deviceAttrName(), attr);
}

void LaunchFuncOp::funcAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(funcAttrName(), attr);
}

void LaunchFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::StringAttr device, ::mlir::FlatSymbolRefAttr func, ::mlir::ValueRange operands) {
  odsState.addOperands(operands);
  odsState.addAttribute(deviceAttrName(odsState.name), device);
  odsState.addAttribute(funcAttrName(odsState.name), func);
  odsState.addTypes(results);
}

void LaunchFuncOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::llvm::StringRef device, ::llvm::StringRef func, ::mlir::ValueRange operands) {
  odsState.addOperands(operands);
  odsState.addAttribute(deviceAttrName(odsState.name), odsBuilder.getStringAttr(device));
  odsState.addAttribute(funcAttrName(odsState.name), ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), func));
  odsState.addTypes(results);
}

void LaunchFuncOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult LaunchFuncOp::verify() {
  {
    auto tblgen_device = (*this)->getAttr(deviceAttrName());
    if (!tblgen_device)
      return emitOpError("requires attribute 'device'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_device, "device")))
      return ::mlir::failure();
  }
  {
    auto tblgen_func = (*this)->getAttr(funcAttrName());
    if (!tblgen_func)
      return emitOpError("requires attribute 'func'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops0(*this, tblgen_func, "func")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::LaunchFuncOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::LaunchOp definitions
//===----------------------------------------------------------------------===//

LaunchOpAdaptor::LaunchOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

LaunchOpAdaptor::LaunchOpAdaptor(LaunchOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange LaunchOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> LaunchOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange LaunchOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr LaunchOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr LaunchOpAdaptor::device() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("device").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::RegionRange LaunchOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &LaunchOpAdaptor::body() {
  return *odsRegions[0];
}

::mlir::LogicalResult LaunchOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_device = odsAttrs.get("device");
    if (!tblgen_device)
      return emitError(loc, "'tf_device.launch' op ""requires attribute 'device'");

    if (tblgen_device && !((tblgen_device.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.launch' op ""attribute 'device' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> LaunchOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range LaunchOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> LaunchOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range LaunchOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range LaunchOp::results() {
  return getODSResults(0);
}

::mlir::Region &LaunchOp::body() {
  return (*this)->getRegion(0);
}

::mlir::StringAttr LaunchOp::deviceAttr() {
  return (*this)->getAttr(deviceAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef LaunchOp::device() {
  auto attr = deviceAttr();
  return attr.getValue();
}

void LaunchOp::deviceAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(deviceAttrName(), attr);
}

void LaunchOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, StringAttr device, TypeRange result_types) {
      odsState.addAttribute("device", device);
      odsState.addTypes(result_types);
      odsState.addRegion();
    
}

void LaunchOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::StringAttr device) {
  odsState.addAttribute(deviceAttrName(odsState.name), device);
  (void)odsState.addRegion();
  odsState.addTypes(results);
}

void LaunchOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::llvm::StringRef device) {
  odsState.addAttribute(deviceAttrName(odsState.name), odsBuilder.getStringAttr(device));
  (void)odsState.addRegion();
  odsState.addTypes(results);
}

void LaunchOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult LaunchOp::verify() {
  {
    auto tblgen_device = (*this)->getAttr(deviceAttrName());
    if (!tblgen_device)
      return emitOpError("requires attribute 'device'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_device, "device")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_tf_device_ops0(*this, region, "body", index++)))
        return ::mlir::failure();
  }
  return ::mlir::success();
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::LaunchOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ParallelExecuteOp definitions
//===----------------------------------------------------------------------===//

ParallelExecuteOpAdaptor::ParallelExecuteOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ParallelExecuteOpAdaptor::ParallelExecuteOpAdaptor(ParallelExecuteOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ParallelExecuteOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ParallelExecuteOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange ParallelExecuteOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr ParallelExecuteOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::RegionRange ParallelExecuteOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::RegionRange ParallelExecuteOpAdaptor::regions() {
  return odsRegions.drop_front(0);
}

::mlir::LogicalResult ParallelExecuteOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ParallelExecuteOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ParallelExecuteOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> ParallelExecuteOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range ParallelExecuteOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range ParallelExecuteOp::execute_outputs() {
  return getODSResults(0);
}

::mlir::MutableArrayRef<::mlir::Region> ParallelExecuteOp::regions() {
  return (*this)->getRegions().drop_front(0);
}

void ParallelExecuteOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange execute_outputs, unsigned regionsCount) {
  for (unsigned i = 0; i < regionsCount; ++i)
    (void)odsState.addRegion();
  odsState.addTypes(execute_outputs);
}

void ParallelExecuteOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes, unsigned numRegions) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != numRegions; ++i)
    (void)odsState.addRegion();
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ParallelExecuteOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : regions())
      if (::mlir::failed(__mlir_ods_local_region_constraint_tf_device_ops0(*this, region, "regions", index++)))
        return ::mlir::failure();
  }
  return Verify(*this);
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ParallelExecuteOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ReceiveOp definitions
//===----------------------------------------------------------------------===//

ReceiveOpAdaptor::ReceiveOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ReceiveOpAdaptor::ReceiveOpAdaptor(ReceiveOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ReceiveOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ReceiveOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange ReceiveOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr ReceiveOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr ReceiveOpAdaptor::key() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("key").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::StringAttr ReceiveOpAdaptor::src_host() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("src_host").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::LogicalResult ReceiveOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_key = odsAttrs.get("key");
    if (!tblgen_key)
      return emitError(loc, "'tf_device.receive' op ""requires attribute 'key'");

    if (tblgen_key && !((tblgen_key.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.receive' op ""attribute 'key' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_src_host = odsAttrs.get("src_host");
    if (!tblgen_src_host)
      return emitError(loc, "'tf_device.receive' op ""requires attribute 'src_host'");

    if (tblgen_src_host && !((tblgen_src_host.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.receive' op ""attribute 'src_host' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReceiveOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range ReceiveOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> ReceiveOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ReceiveOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value ReceiveOp::result() {
  return *getODSResults(0).begin();
}

::mlir::StringAttr ReceiveOp::keyAttr() {
  return (*this)->getAttr(keyAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef ReceiveOp::key() {
  auto attr = keyAttr();
  return attr.getValue();
}

::mlir::StringAttr ReceiveOp::src_hostAttr() {
  return (*this)->getAttr(src_hostAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef ReceiveOp::src_host() {
  auto attr = src_hostAttr();
  return attr.getValue();
}

void ReceiveOp::keyAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(keyAttrName(), attr);
}

void ReceiveOp::src_hostAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(src_hostAttrName(), attr);
}

void ReceiveOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::StringAttr key, ::mlir::StringAttr src_host) {
  odsState.addAttribute(keyAttrName(odsState.name), key);
  odsState.addAttribute(src_hostAttrName(odsState.name), src_host);
  odsState.addTypes(result);
}

void ReceiveOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr key, ::mlir::StringAttr src_host) {
  odsState.addAttribute(keyAttrName(odsState.name), key);
  odsState.addAttribute(src_hostAttrName(odsState.name), src_host);
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReceiveOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::llvm::StringRef key, ::llvm::StringRef src_host) {
  odsState.addAttribute(keyAttrName(odsState.name), odsBuilder.getStringAttr(key));
  odsState.addAttribute(src_hostAttrName(odsState.name), odsBuilder.getStringAttr(src_host));
  odsState.addTypes(result);
}

void ReceiveOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef key, ::llvm::StringRef src_host) {
  odsState.addAttribute(keyAttrName(odsState.name), odsBuilder.getStringAttr(key));
  odsState.addAttribute(src_hostAttrName(odsState.name), odsBuilder.getStringAttr(src_host));
  assert(resultTypes.size() == 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void ReceiveOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ReceiveOp::verify() {
  {
    auto tblgen_key = (*this)->getAttr(keyAttrName());
    if (!tblgen_key)
      return emitOpError("requires attribute 'key'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_key, "key")))
      return ::mlir::failure();
  }
  {
    auto tblgen_src_host = (*this)->getAttr(src_hostAttrName());
    if (!tblgen_src_host)
      return emitOpError("requires attribute 'src_host'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_src_host, "src_host")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::ParseResult ReceiveOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::StringAttr keyAttr;
  ::mlir::StringAttr src_hostAttr;
  ::mlir::Type resultRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> resultTypes(resultRawTypes);

  if (parser.parseCustomAttributeWithFallback(keyAttr, parser.getBuilder().getType<::mlir::NoneType>(), "key",
          result.attributes)) {
    return ::mlir::failure();
  }

  if (parser.parseCustomAttributeWithFallback(src_hostAttr, parser.getBuilder().getType<::mlir::NoneType>(), "src_host",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    resultRawTypes[0] = type;
  }
  result.addTypes(resultTypes);
  return ::mlir::success();
}

void ReceiveOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(keyAttr());
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(src_hostAttr());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"key", "src_host"});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = result().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ReceiveOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::RemoteRunOp definitions
//===----------------------------------------------------------------------===//

RemoteRunOpAdaptor::RemoteRunOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

RemoteRunOpAdaptor::RemoteRunOpAdaptor(RemoteRunOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange RemoteRunOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> RemoteRunOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange RemoteRunOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange RemoteRunOpAdaptor::callee_args() {
  return getODSOperands(0);
}

::mlir::DictionaryAttr RemoteRunOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr RemoteRunOpAdaptor::host() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("host").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::FlatSymbolRefAttr RemoteRunOpAdaptor::callee() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::FlatSymbolRefAttr attr = odsAttrs.get("callee").cast<::mlir::FlatSymbolRefAttr>();
  return attr;
}

::mlir::LogicalResult RemoteRunOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_host = odsAttrs.get("host");
    if (!tblgen_host)
      return emitError(loc, "'tf_device.remote_run' op ""requires attribute 'host'");

    if (tblgen_host && !((tblgen_host.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.remote_run' op ""attribute 'host' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_callee = odsAttrs.get("callee");
    if (!tblgen_callee)
      return emitError(loc, "'tf_device.remote_run' op ""requires attribute 'callee'");

    if (tblgen_callee && !((tblgen_callee.isa<::mlir::FlatSymbolRefAttr>())))
      return emitError(loc, "'tf_device.remote_run' op ""attribute 'callee' failed to satisfy constraint: flat symbol reference attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> RemoteRunOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range RemoteRunOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range RemoteRunOp::callee_args() {
  return getODSOperands(0);
}

::mlir::MutableOperandRange RemoteRunOp::callee_argsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> RemoteRunOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range RemoteRunOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range RemoteRunOp::results() {
  return getODSResults(0);
}

::mlir::StringAttr RemoteRunOp::hostAttr() {
  return (*this)->getAttr(hostAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef RemoteRunOp::host() {
  auto attr = hostAttr();
  return attr.getValue();
}

::mlir::FlatSymbolRefAttr RemoteRunOp::calleeAttr() {
  return (*this)->getAttr(calleeAttrName()).cast<::mlir::FlatSymbolRefAttr>();
}

::llvm::StringRef RemoteRunOp::callee() {
  auto attr = calleeAttr();
  return attr.getValue();
}

void RemoteRunOp::hostAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(hostAttrName(), attr);
}

void RemoteRunOp::calleeAttr(::mlir::FlatSymbolRefAttr attr) {
  (*this)->setAttr(calleeAttrName(), attr);
}

void RemoteRunOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::StringAttr host, ::mlir::FlatSymbolRefAttr callee, ::mlir::ValueRange callee_args) {
  odsState.addOperands(callee_args);
  odsState.addAttribute(hostAttrName(odsState.name), host);
  odsState.addAttribute(calleeAttrName(odsState.name), callee);
  odsState.addTypes(results);
}

void RemoteRunOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::llvm::StringRef host, ::llvm::StringRef callee, ::mlir::ValueRange callee_args) {
  odsState.addOperands(callee_args);
  odsState.addAttribute(hostAttrName(odsState.name), odsBuilder.getStringAttr(host));
  odsState.addAttribute(calleeAttrName(odsState.name), ::mlir::SymbolRefAttr::get(odsBuilder.getContext(), callee));
  odsState.addTypes(results);
}

void RemoteRunOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult RemoteRunOp::verify() {
  {
    auto tblgen_host = (*this)->getAttr(hostAttrName());
    if (!tblgen_host)
      return emitOpError("requires attribute 'host'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_host, "host")))
      return ::mlir::failure();
  }
  {
    auto tblgen_callee = (*this)->getAttr(calleeAttrName());
    if (!tblgen_callee)
      return emitOpError("requires attribute 'callee'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops0(*this, tblgen_callee, "callee")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::ParseResult RemoteRunOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::StringAttr hostAttr;
  ::mlir::FlatSymbolRefAttr calleeAttr;
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> callee_argsOperands;
  ::llvm::SMLoc callee_argsOperandsLoc;
  (void)callee_argsOperandsLoc;
  ::llvm::ArrayRef<::mlir::Type> callee_argsTypes;
  ::llvm::ArrayRef<::mlir::Type> resultsTypes;

  if (parser.parseCustomAttributeWithFallback(hostAttr, parser.getBuilder().getType<::mlir::NoneType>(), "host",
          result.attributes)) {
    return ::mlir::failure();
  }

  if (parser.parseCustomAttributeWithFallback(calleeAttr, parser.getBuilder().getType<::mlir::NoneType>(), "callee",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseLParen())
    return ::mlir::failure();

  callee_argsOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperandList(callee_argsOperands))
    return ::mlir::failure();
  if (parser.parseRParen())
    return ::mlir::failure();
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  ::mlir::FunctionType callee_args__results_functionType;
  if (parser.parseType(callee_args__results_functionType))
    return ::mlir::failure();
  callee_argsTypes = callee_args__results_functionType.getInputs();
  resultsTypes = callee_args__results_functionType.getResults();
  result.addTypes(resultsTypes);
  if (parser.resolveOperands(callee_argsOperands, callee_argsTypes, callee_argsOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void RemoteRunOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(hostAttr());
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(calleeAttr());
  _odsPrinter << "(";
  _odsPrinter << callee_args();
  _odsPrinter << ")";
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"host", "callee"});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  _odsPrinter.printFunctionalType(callee_args().getTypes(), results().getTypes());
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::RemoteRunOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ReplicateOp definitions
//===----------------------------------------------------------------------===//

ReplicateOpAdaptor::ReplicateOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ReplicateOpAdaptor::ReplicateOpAdaptor(ReplicateOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ReplicateOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ReplicateOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  assert(odsAttrs && "missing segment size attribute for op");
  auto sizeAttr = odsAttrs.get("operand_segment_sizes").cast<::mlir::DenseIntElementsAttr>();

  const uint32_t *sizeAttrValueIt = &*sizeAttr.value_begin<uint32_t>();
  if (sizeAttr.isSplat())
    return {*sizeAttrValueIt * index, *sizeAttrValueIt};

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttrValueIt[i];
  return {start, sizeAttrValueIt[index]};
}

::mlir::ValueRange ReplicateOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange ReplicateOpAdaptor::replicated_inputs() {
  return getODSOperands(0);
}

::mlir::ValueRange ReplicateOpAdaptor::packed_inputs() {
  return getODSOperands(1);
}

::mlir::DictionaryAttr ReplicateOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::DenseIntElementsAttr ReplicateOpAdaptor::operand_segment_sizes() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::DenseIntElementsAttr attr = odsAttrs.get("operand_segment_sizes").cast<::mlir::DenseIntElementsAttr>();
  return attr;
}

::mlir::IntegerAttr ReplicateOpAdaptor::n() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::IntegerAttr attr = odsAttrs.get("n").cast<::mlir::IntegerAttr>();
  return attr;
}

::mlir::DictionaryAttr ReplicateOpAdaptor::devices() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::DictionaryAttr attr = odsAttrs.get("devices").dyn_cast_or_null<::mlir::DictionaryAttr>();
  return attr;
}

::mlir::RegionRange ReplicateOpAdaptor::getRegions() {
  return odsRegions;
}

::mlir::Region &ReplicateOpAdaptor::body() {
  return *odsRegions[0];
}

::mlir::LogicalResult ReplicateOpAdaptor::verify(::mlir::Location loc) {
  {
    auto sizeAttr = odsAttrs.get("operand_segment_sizes").dyn_cast<::mlir::DenseIntElementsAttr>();
    if (!sizeAttr)
      return emitError(loc, "'tf_device.replicate' op ""missing segment sizes attribute 'operand_segment_sizes'");
    auto numElements =
        sizeAttr.getType().cast<::mlir::ShapedType>().getNumElements();
    if (numElements != 2)
      return emitError(loc, "'tf_device.replicate' op ""'operand_segment_sizes' attribute for specifying operand segments must have 2 "
                "elements, but got ") << numElements;
  }
    {
    auto tblgen_operand_segment_sizes = odsAttrs.get("operand_segment_sizes");
    if (!tblgen_operand_segment_sizes)
      return emitError(loc, "'tf_device.replicate' op ""requires attribute 'operand_segment_sizes'");

    if (tblgen_operand_segment_sizes && !(((tblgen_operand_segment_sizes.isa<::mlir::DenseIntElementsAttr>())) && ((tblgen_operand_segment_sizes.cast<::mlir::DenseIntElementsAttr>().getType().getElementType().isSignlessInteger(32)))))
      return emitError(loc, "'tf_device.replicate' op ""attribute 'operand_segment_sizes' failed to satisfy constraint: 32-bit signless integer elements attribute");
  }
  {
    auto tblgen_n = odsAttrs.get("n");
    if (!tblgen_n)
      return emitError(loc, "'tf_device.replicate' op ""requires attribute 'n'");

    if (tblgen_n && !((((tblgen_n.isa<::mlir::IntegerAttr>())) && ((tblgen_n.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && ((tblgen_n.cast<::mlir::IntegerAttr>().getInt() >= 2))))
      return emitError(loc, "'tf_device.replicate' op ""attribute 'n' failed to satisfy constraint: 32-bit signless integer attribute whose minimum value is 2");
  }
  {
    auto tblgen_devices = odsAttrs.get("devices");
    if (tblgen_devices && !((tblgen_devices.isa<::mlir::DictionaryAttr>())))
      return emitError(loc, "'tf_device.replicate' op ""attribute 'devices' failed to satisfy constraint: dictionary of named attribute values");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReplicateOp::getODSOperandIndexAndLength(unsigned index) {
  auto sizeAttr =
      (*this)->getAttr(operand_segment_sizesAttrName()).cast<::mlir::DenseIntElementsAttr>();

  const uint32_t *sizeAttrValueIt = &*sizeAttr.value_begin<uint32_t>();
  if (sizeAttr.isSplat())
    return {*sizeAttrValueIt * index, *sizeAttrValueIt};

  unsigned start = 0;
  for (unsigned i = 0; i < index; ++i)
    start += sizeAttrValueIt[i];
  return {start, sizeAttrValueIt[index]};
}

::mlir::Operation::operand_range ReplicateOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range ReplicateOp::replicated_inputs() {
  return getODSOperands(0);
}

::mlir::Operation::operand_range ReplicateOp::packed_inputs() {
  return getODSOperands(1);
}

::mlir::MutableOperandRange ReplicateOp::replicated_inputsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(0u, *getOperation()->getAttrDictionary().getNamed(operand_segment_sizesAttrName())));
  return mutableRange;
}

::mlir::MutableOperandRange ReplicateOp::packed_inputsMutable() {
  auto range = getODSOperandIndexAndLength(1);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second, ::mlir::MutableOperandRange::OperandSegment(1u, *getOperation()->getAttrDictionary().getNamed(operand_segment_sizesAttrName())));
  return mutableRange;
}

std::pair<unsigned, unsigned> ReplicateOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range ReplicateOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range ReplicateOp::replicated_outputs() {
  return getODSResults(0);
}

::mlir::Region &ReplicateOp::body() {
  return (*this)->getRegion(0);
}

::mlir::DenseIntElementsAttr ReplicateOp::operand_segment_sizesAttr() {
  return (*this)->getAttr(operand_segment_sizesAttrName()).cast<::mlir::DenseIntElementsAttr>();
}

::mlir::DenseIntElementsAttr ReplicateOp::operand_segment_sizes() {
  auto attr = operand_segment_sizesAttr();
  return attr;
}

::mlir::IntegerAttr ReplicateOp::nAttr() {
  return (*this)->getAttr(nAttrName()).cast<::mlir::IntegerAttr>();
}

uint32_t ReplicateOp::n() {
  auto attr = nAttr();
  return attr.getValue().getZExtValue();
}

::mlir::DictionaryAttr ReplicateOp::devicesAttr() {
  return (*this)->getAttr(devicesAttrName()).dyn_cast_or_null<::mlir::DictionaryAttr>();
}

::llvm::Optional< ::mlir::DictionaryAttr > ReplicateOp::devices() {
  auto attr = devicesAttr();
  return attr ? ::llvm::Optional< ::mlir::DictionaryAttr >(attr) : (::llvm::None);
}

void ReplicateOp::operand_segment_sizesAttr(::mlir::DenseIntElementsAttr attr) {
  (*this)->setAttr(operand_segment_sizesAttrName(), attr);
}

void ReplicateOp::nAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(nAttrName(), attr);
}

void ReplicateOp::devicesAttr(::mlir::DictionaryAttr attr) {
  (*this)->setAttr(devicesAttrName(), attr);
}

::mlir::Attribute ReplicateOp::removeDevicesAttr() {
  return (*this)->removeAttr(devicesAttrName());
}

void ReplicateOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange replicated_outputs, ::mlir::ValueRange replicated_inputs, ::mlir::ValueRange packed_inputs, ::mlir::DenseIntElementsAttr operand_segment_sizes, ::mlir::IntegerAttr n, /*optional*/::mlir::DictionaryAttr devices) {
  odsState.addOperands(replicated_inputs);
  odsState.addOperands(packed_inputs);
  odsState.addAttribute(operand_segment_sizesAttrName(odsState.name), odsBuilder.getI32VectorAttr({static_cast<int32_t>(replicated_inputs.size()), static_cast<int32_t>(packed_inputs.size())}));
  odsState.addAttribute(operand_segment_sizesAttrName(odsState.name), operand_segment_sizes);
  odsState.addAttribute(nAttrName(odsState.name), n);
  if (devices) {
  odsState.addAttribute(devicesAttrName(odsState.name), devices);
  }
  (void)odsState.addRegion();
  odsState.addTypes(replicated_outputs);
}

void ReplicateOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange replicated_outputs, ::mlir::ValueRange replicated_inputs, ::mlir::ValueRange packed_inputs, ::mlir::DenseIntElementsAttr operand_segment_sizes, uint32_t n, /*optional*/::mlir::DictionaryAttr devices) {
  odsState.addOperands(replicated_inputs);
  odsState.addOperands(packed_inputs);
  odsState.addAttribute(operand_segment_sizesAttrName(odsState.name), odsBuilder.getI32VectorAttr({static_cast<int32_t>(replicated_inputs.size()), static_cast<int32_t>(packed_inputs.size())}));
  odsState.addAttribute(operand_segment_sizesAttrName(odsState.name), operand_segment_sizes);
  odsState.addAttribute(nAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(32), n));
  if (devices) {
  odsState.addAttribute(devicesAttrName(odsState.name), devices);
  }
  (void)odsState.addRegion();
  odsState.addTypes(replicated_outputs);
}

void ReplicateOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  for (unsigned i = 0; i != 1; ++i)
    (void)odsState.addRegion();
  odsState.addTypes(resultTypes);
}

::mlir::ParseResult ReplicateOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  return ParseReplicateOp(&parser, &result);
}

void ReplicateOp::print(::mlir::OpAsmPrinter &p) {
  return Print(*this, &p);
}

::mlir::LogicalResult ReplicateOp::verify() {
  {
    auto sizeAttr = (*this)->getAttr(operand_segment_sizesAttrName()).dyn_cast<::mlir::DenseIntElementsAttr>();
    if (!sizeAttr)
      return emitOpError("missing segment sizes attribute 'operand_segment_sizes'");
    auto numElements =
        sizeAttr.getType().cast<::mlir::ShapedType>().getNumElements();
    if (numElements != 2)
      return emitOpError("'operand_segment_sizes' attribute for specifying operand segments must have 2 "
                "elements, but got ") << numElements;
  }
    {
    auto tblgen_operand_segment_sizes = (*this)->getAttr(operand_segment_sizesAttrName());
    if (!tblgen_operand_segment_sizes)
      return emitOpError("requires attribute 'operand_segment_sizes'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops2(*this, tblgen_operand_segment_sizes, "operand_segment_sizes")))
      return ::mlir::failure();
  }
  {
    auto tblgen_n = (*this)->getAttr(nAttrName());
    if (!tblgen_n)
      return emitOpError("requires attribute 'n'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops3(*this, tblgen_n, "n")))
      return ::mlir::failure();
  }
  {
    auto tblgen_devices = (*this)->getAttr(devicesAttrName());
    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops4(*this, tblgen_devices, "devices")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;

    for (auto &region : ::llvm::makeMutableArrayRef((*this)->getRegion(0)))
      if (::mlir::failed(__mlir_ods_local_region_constraint_tf_device_ops0(*this, region, "body", index++)))
        return ::mlir::failure();
  }
  return Verify(*this);
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ReplicateOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::ReturnOp definitions
//===----------------------------------------------------------------------===//

ReturnOpAdaptor::ReturnOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

ReturnOpAdaptor::ReturnOpAdaptor(ReturnOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange ReturnOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> ReturnOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (odsOperands.size() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::ValueRange ReturnOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::ValueRange ReturnOpAdaptor::results() {
  return getODSOperands(0);
}

::mlir::DictionaryAttr ReturnOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::LogicalResult ReturnOpAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> ReturnOp::getODSOperandIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumOperands() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::operand_range ReturnOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::operand_range ReturnOp::results() {
  return getODSOperands(0);
}

::mlir::MutableOperandRange ReturnOp::resultsMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> ReturnOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range ReturnOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void ReturnOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState) {
      build(odsBuilder, odsState, {});
    
}

void ReturnOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange results) {
  odsState.addOperands(results);
}

void ReturnOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult ReturnOp::verify() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::ParseResult ReturnOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::SmallVector<::mlir::OpAsmParser::OperandType, 4> resultsOperands;
  ::llvm::SMLoc resultsOperandsLoc;
  (void)resultsOperandsLoc;
  ::mlir::SmallVector<::mlir::Type, 1> resultsTypes;
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();

  resultsOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperandList(resultsOperands))
    return ::mlir::failure();
  if (!resultsOperands.empty()) {
  if (parser.parseColon())
    return ::mlir::failure();

  if (parser.parseTypeList(resultsTypes))
    return ::mlir::failure();
  }
  if (parser.resolveOperands(resultsOperands, resultsTypes, resultsOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void ReturnOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{});
  if (!results().empty()) {
  _odsPrinter << ' ';
  _odsPrinter << results();
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  _odsPrinter << results().getTypes();
  }
}

void ReturnOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::ReturnOp)

namespace mlir {
namespace tf_device {

//===----------------------------------------------------------------------===//
// ::mlir::tf_device::SendOp definitions
//===----------------------------------------------------------------------===//

SendOpAdaptor::SendOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

SendOpAdaptor::SendOpAdaptor(SendOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange SendOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> SendOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange SendOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SendOpAdaptor::value() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr SendOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::StringAttr SendOpAdaptor::key() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("key").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::StringAttr SendOpAdaptor::dst_host() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::StringAttr attr = odsAttrs.get("dst_host").cast<::mlir::StringAttr>();
  return attr;
}

::mlir::LogicalResult SendOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_key = odsAttrs.get("key");
    if (!tblgen_key)
      return emitError(loc, "'tf_device.send' op ""requires attribute 'key'");

    if (tblgen_key && !((tblgen_key.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.send' op ""attribute 'key' failed to satisfy constraint: string attribute");
  }
  {
    auto tblgen_dst_host = odsAttrs.get("dst_host");
    if (!tblgen_dst_host)
      return emitError(loc, "'tf_device.send' op ""requires attribute 'dst_host'");

    if (tblgen_dst_host && !((tblgen_dst_host.isa<::mlir::StringAttr>())))
      return emitError(loc, "'tf_device.send' op ""attribute 'dst_host' failed to satisfy constraint: string attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> SendOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range SendOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value SendOp::value() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange SendOp::valueMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> SendOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range SendOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::StringAttr SendOp::keyAttr() {
  return (*this)->getAttr(keyAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef SendOp::key() {
  auto attr = keyAttr();
  return attr.getValue();
}

::mlir::StringAttr SendOp::dst_hostAttr() {
  return (*this)->getAttr(dst_hostAttrName()).cast<::mlir::StringAttr>();
}

::llvm::StringRef SendOp::dst_host() {
  auto attr = dst_hostAttr();
  return attr.getValue();
}

void SendOp::keyAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(keyAttrName(), attr);
}

void SendOp::dst_hostAttr(::mlir::StringAttr attr) {
  (*this)->setAttr(dst_hostAttrName(), attr);
}

void SendOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::StringAttr key, ::mlir::StringAttr dst_host) {
  odsState.addOperands(value);
  odsState.addAttribute(keyAttrName(odsState.name), key);
  odsState.addAttribute(dst_hostAttrName(odsState.name), dst_host);
}

void SendOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::StringAttr key, ::mlir::StringAttr dst_host) {
  odsState.addOperands(value);
  odsState.addAttribute(keyAttrName(odsState.name), key);
  odsState.addAttribute(dst_hostAttrName(odsState.name), dst_host);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void SendOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::llvm::StringRef key, ::llvm::StringRef dst_host) {
  odsState.addOperands(value);
  odsState.addAttribute(keyAttrName(odsState.name), odsBuilder.getStringAttr(key));
  odsState.addAttribute(dst_hostAttrName(odsState.name), odsBuilder.getStringAttr(dst_host));
}

void SendOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::llvm::StringRef key, ::llvm::StringRef dst_host) {
  odsState.addOperands(value);
  odsState.addAttribute(keyAttrName(odsState.name), odsBuilder.getStringAttr(key));
  odsState.addAttribute(dst_hostAttrName(odsState.name), odsBuilder.getStringAttr(dst_host));
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void SendOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult SendOp::verify() {
  {
    auto tblgen_key = (*this)->getAttr(keyAttrName());
    if (!tblgen_key)
      return emitOpError("requires attribute 'key'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_key, "key")))
      return ::mlir::failure();
  }
  {
    auto tblgen_dst_host = (*this)->getAttr(dst_hostAttrName());
    if (!tblgen_dst_host)
      return emitOpError("requires attribute 'dst_host'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tf_device_ops1(*this, tblgen_dst_host, "dst_host")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tf_device_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::ParseResult SendOp::parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result) {
  ::mlir::OpAsmParser::OperandType valueRawOperands[1];
  ::llvm::ArrayRef<::mlir::OpAsmParser::OperandType> valueOperands(valueRawOperands);  ::llvm::SMLoc valueOperandsLoc;
  (void)valueOperandsLoc;
  ::mlir::StringAttr keyAttr;
  ::mlir::StringAttr dst_hostAttr;
  ::mlir::Type valueRawTypes[1];
  ::llvm::ArrayRef<::mlir::Type> valueTypes(valueRawTypes);

  valueOperandsLoc = parser.getCurrentLocation();
  if (parser.parseOperand(valueRawOperands[0]))
    return ::mlir::failure();

  if (parser.parseCustomAttributeWithFallback(keyAttr, parser.getBuilder().getType<::mlir::NoneType>(), "key",
          result.attributes)) {
    return ::mlir::failure();
  }

  if (parser.parseCustomAttributeWithFallback(dst_hostAttr, parser.getBuilder().getType<::mlir::NoneType>(), "dst_host",
          result.attributes)) {
    return ::mlir::failure();
  }
  if (parser.parseOptionalAttrDict(result.attributes))
    return ::mlir::failure();
  if (parser.parseColon())
    return ::mlir::failure();

  {
    ::mlir::Type type;
    if (parser.parseCustomTypeWithFallback(type))
      return ::mlir::failure();
    valueRawTypes[0] = type;
  }
  if (parser.resolveOperands(valueOperands, valueTypes, valueOperandsLoc, result.operands))
    return ::mlir::failure();
  return ::mlir::success();
}

void SendOp::print(::mlir::OpAsmPrinter &_odsPrinter) {
  _odsPrinter << ' ';
  _odsPrinter << value();
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(keyAttr());
  _odsPrinter << ' ';
  _odsPrinter.printAttributeWithoutType(dst_hostAttr());
  _odsPrinter.printOptionalAttrDict((*this)->getAttrs(), /*elidedAttrs=*/{"key", "dst_host"});
  _odsPrinter << ' ' << ":";
  _odsPrinter << ' ';
  {
    auto type = value().getType();
    if (auto validType = type.dyn_cast<::mlir::Type>())
      _odsPrinter.printStrippedAttrOrType(validType);
   else
     _odsPrinter << type;
  }
}

} // namespace tf_device
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::tf_device::SendOp)


#endif  // GET_OP_CLASSES

