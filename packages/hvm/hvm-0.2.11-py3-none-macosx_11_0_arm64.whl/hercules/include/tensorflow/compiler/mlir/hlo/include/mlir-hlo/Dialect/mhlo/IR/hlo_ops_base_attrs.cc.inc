/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_LIST
#undef GET_ATTRDEF_LIST

::mlir::mhlo::ArgResultAliasAttr,
::mlir::mhlo::ConvDimensionNumbersAttr,
::mlir::mhlo::DotDimensionNumbersAttr,
::mlir::mhlo::GatherDimensionNumbersAttr,
::mlir::mhlo::ScatterDimensionNumbersAttr

#endif  // GET_ATTRDEF_LIST

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES

static ::mlir::OptionalParseResult generatedAttributeParser(::mlir::AsmParser &parser, ::llvm::StringRef mnemonic, ::mlir::Type type, ::mlir::Attribute &value) {
  if (mnemonic == ::mlir::mhlo::ArgResultAliasAttr::getMnemonic()) {
    value = ::mlir::mhlo::ArgResultAliasAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::mhlo::ConvDimensionNumbersAttr::getMnemonic()) {
    value = ::mlir::mhlo::ConvDimensionNumbersAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::mhlo::DotDimensionNumbersAttr::getMnemonic()) {
    value = ::mlir::mhlo::DotDimensionNumbersAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::mhlo::GatherDimensionNumbersAttr::getMnemonic()) {
    value = ::mlir::mhlo::GatherDimensionNumbersAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  if (mnemonic == ::mlir::mhlo::ScatterDimensionNumbersAttr::getMnemonic()) {
    value = ::mlir::mhlo::ScatterDimensionNumbersAttr::parse(parser, type);
    return ::mlir::success(!!value);
  }
  return {};
}

static ::mlir::LogicalResult generatedAttributePrinter(::mlir::Attribute def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Attribute, ::mlir::LogicalResult>(def)    .Case<::mlir::mhlo::ArgResultAliasAttr>([&](auto t) {
      printer << ::mlir::mhlo::ArgResultAliasAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::mhlo::ConvDimensionNumbersAttr>([&](auto t) {
      printer << ::mlir::mhlo::ConvDimensionNumbersAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::mhlo::DotDimensionNumbersAttr>([&](auto t) {
      printer << ::mlir::mhlo::DotDimensionNumbersAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::mhlo::GatherDimensionNumbersAttr>([&](auto t) {
      printer << ::mlir::mhlo::GatherDimensionNumbersAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::mhlo::ScatterDimensionNumbersAttr>([&](auto t) {
      printer << ::mlir::mhlo::ScatterDimensionNumbersAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace mhlo {
namespace detail {
struct ArgResultAliasAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, int64_t, ::llvm::ArrayRef<int64_t>, bool>;
  ArgResultAliasAttrStorage(::llvm::ArrayRef<int64_t> argTupleIndices, int64_t resultIndex, ::llvm::ArrayRef<int64_t> resultTupleIndices, bool isMustAlias) : ::mlir::AttributeStorage(), argTupleIndices(argTupleIndices), resultIndex(resultIndex), resultTupleIndices(resultTupleIndices), isMustAlias(isMustAlias) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (argTupleIndices == std::get<0>(tblgenKey)) && (resultIndex == std::get<1>(tblgenKey)) && (resultTupleIndices == std::get<2>(tblgenKey)) && (isMustAlias == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static ArgResultAliasAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto argTupleIndices = std::get<0>(tblgenKey);
    auto resultIndex = std::get<1>(tblgenKey);
    auto resultTupleIndices = std::get<2>(tblgenKey);
    auto isMustAlias = std::get<3>(tblgenKey);
    argTupleIndices = allocator.copyInto(argTupleIndices);
    resultTupleIndices = allocator.copyInto(resultTupleIndices);
    return new (allocator.allocate<ArgResultAliasAttrStorage>()) ArgResultAliasAttrStorage(argTupleIndices, resultIndex, resultTupleIndices, isMustAlias);
  }

  ::llvm::ArrayRef<int64_t> argTupleIndices;
  int64_t resultIndex;
  ::llvm::ArrayRef<int64_t> resultTupleIndices;
  bool isMustAlias;
};
} // namespace detail
ArgResultAliasAttr ArgResultAliasAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> argTupleIndices, int64_t resultIndex, ::llvm::ArrayRef<int64_t> resultTupleIndices, bool isMustAlias) {
  return Base::get(context, argTupleIndices, resultIndex, resultTupleIndices, isMustAlias);
}

::llvm::ArrayRef<int64_t> ArgResultAliasAttr::getArgTupleIndices() const {
  return getImpl()->argTupleIndices;
}

int64_t ArgResultAliasAttr::getResultIndex() const {
  return getImpl()->resultIndex;
}

::llvm::ArrayRef<int64_t> ArgResultAliasAttr::getResultTupleIndices() const {
  return getImpl()->resultTupleIndices;
}

bool ArgResultAliasAttr::getIsMustAlias() const {
  return getImpl()->isMustAlias;
}

} // namespace mhlo
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::mhlo::ArgResultAliasAttr)
namespace mlir {
namespace mhlo {
namespace detail {
struct ConvDimensionNumbersAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<int64_t, int64_t, ::llvm::ArrayRef<int64_t>, int64_t, int64_t, ::llvm::ArrayRef<int64_t>, int64_t, int64_t, ::llvm::ArrayRef<int64_t>>;
  ConvDimensionNumbersAttrStorage(int64_t inputBatchDimension, int64_t inputFeatureDimension, ::llvm::ArrayRef<int64_t> inputSpatialDimensions, int64_t kernelInputFeatureDimension, int64_t kernelOutputFeatureDimension, ::llvm::ArrayRef<int64_t> kernelSpatialDimensions, int64_t outputBatchDimension, int64_t outputFeatureDimension, ::llvm::ArrayRef<int64_t> outputSpatialDimensions) : ::mlir::AttributeStorage(), inputBatchDimension(inputBatchDimension), inputFeatureDimension(inputFeatureDimension), inputSpatialDimensions(inputSpatialDimensions), kernelInputFeatureDimension(kernelInputFeatureDimension), kernelOutputFeatureDimension(kernelOutputFeatureDimension), kernelSpatialDimensions(kernelSpatialDimensions), outputBatchDimension(outputBatchDimension), outputFeatureDimension(outputFeatureDimension), outputSpatialDimensions(outputSpatialDimensions) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (inputBatchDimension == std::get<0>(tblgenKey)) && (inputFeatureDimension == std::get<1>(tblgenKey)) && (inputSpatialDimensions == std::get<2>(tblgenKey)) && (kernelInputFeatureDimension == std::get<3>(tblgenKey)) && (kernelOutputFeatureDimension == std::get<4>(tblgenKey)) && (kernelSpatialDimensions == std::get<5>(tblgenKey)) && (outputBatchDimension == std::get<6>(tblgenKey)) && (outputFeatureDimension == std::get<7>(tblgenKey)) && (outputSpatialDimensions == std::get<8>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey), std::get<4>(tblgenKey), std::get<5>(tblgenKey), std::get<6>(tblgenKey), std::get<7>(tblgenKey), std::get<8>(tblgenKey));
  }

  static ConvDimensionNumbersAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto inputBatchDimension = std::get<0>(tblgenKey);
    auto inputFeatureDimension = std::get<1>(tblgenKey);
    auto inputSpatialDimensions = std::get<2>(tblgenKey);
    auto kernelInputFeatureDimension = std::get<3>(tblgenKey);
    auto kernelOutputFeatureDimension = std::get<4>(tblgenKey);
    auto kernelSpatialDimensions = std::get<5>(tblgenKey);
    auto outputBatchDimension = std::get<6>(tblgenKey);
    auto outputFeatureDimension = std::get<7>(tblgenKey);
    auto outputSpatialDimensions = std::get<8>(tblgenKey);
    inputSpatialDimensions = allocator.copyInto(inputSpatialDimensions);
    kernelSpatialDimensions = allocator.copyInto(kernelSpatialDimensions);
    outputSpatialDimensions = allocator.copyInto(outputSpatialDimensions);
    return new (allocator.allocate<ConvDimensionNumbersAttrStorage>()) ConvDimensionNumbersAttrStorage(inputBatchDimension, inputFeatureDimension, inputSpatialDimensions, kernelInputFeatureDimension, kernelOutputFeatureDimension, kernelSpatialDimensions, outputBatchDimension, outputFeatureDimension, outputSpatialDimensions);
  }

  int64_t inputBatchDimension;
  int64_t inputFeatureDimension;
  ::llvm::ArrayRef<int64_t> inputSpatialDimensions;
  int64_t kernelInputFeatureDimension;
  int64_t kernelOutputFeatureDimension;
  ::llvm::ArrayRef<int64_t> kernelSpatialDimensions;
  int64_t outputBatchDimension;
  int64_t outputFeatureDimension;
  ::llvm::ArrayRef<int64_t> outputSpatialDimensions;
};
} // namespace detail
ConvDimensionNumbersAttr ConvDimensionNumbersAttr::get(::mlir::MLIRContext *context, int64_t inputBatchDimension, int64_t inputFeatureDimension, ::llvm::ArrayRef<int64_t> inputSpatialDimensions, int64_t kernelInputFeatureDimension, int64_t kernelOutputFeatureDimension, ::llvm::ArrayRef<int64_t> kernelSpatialDimensions, int64_t outputBatchDimension, int64_t outputFeatureDimension, ::llvm::ArrayRef<int64_t> outputSpatialDimensions) {
  return Base::get(context, inputBatchDimension, inputFeatureDimension, inputSpatialDimensions, kernelInputFeatureDimension, kernelOutputFeatureDimension, kernelSpatialDimensions, outputBatchDimension, outputFeatureDimension, outputSpatialDimensions);
}

int64_t ConvDimensionNumbersAttr::getInputBatchDimension() const {
  return getImpl()->inputBatchDimension;
}

int64_t ConvDimensionNumbersAttr::getInputFeatureDimension() const {
  return getImpl()->inputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersAttr::getInputSpatialDimensions() const {
  return getImpl()->inputSpatialDimensions;
}

int64_t ConvDimensionNumbersAttr::getKernelInputFeatureDimension() const {
  return getImpl()->kernelInputFeatureDimension;
}

int64_t ConvDimensionNumbersAttr::getKernelOutputFeatureDimension() const {
  return getImpl()->kernelOutputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersAttr::getKernelSpatialDimensions() const {
  return getImpl()->kernelSpatialDimensions;
}

int64_t ConvDimensionNumbersAttr::getOutputBatchDimension() const {
  return getImpl()->outputBatchDimension;
}

int64_t ConvDimensionNumbersAttr::getOutputFeatureDimension() const {
  return getImpl()->outputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersAttr::getOutputSpatialDimensions() const {
  return getImpl()->outputSpatialDimensions;
}

} // namespace mhlo
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::mhlo::ConvDimensionNumbersAttr)
namespace mlir {
namespace mhlo {
namespace detail {
struct DotDimensionNumbersAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>>;
  DotDimensionNumbersAttrStorage(::llvm::ArrayRef<int64_t> lhsBatchingDimensions, ::llvm::ArrayRef<int64_t> rhsBatchingDimensions, ::llvm::ArrayRef<int64_t> lhsContractingDimensions, ::llvm::ArrayRef<int64_t> rhsContractingDimensions) : ::mlir::AttributeStorage(), lhsBatchingDimensions(lhsBatchingDimensions), rhsBatchingDimensions(rhsBatchingDimensions), lhsContractingDimensions(lhsContractingDimensions), rhsContractingDimensions(rhsContractingDimensions) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (lhsBatchingDimensions == std::get<0>(tblgenKey)) && (rhsBatchingDimensions == std::get<1>(tblgenKey)) && (lhsContractingDimensions == std::get<2>(tblgenKey)) && (rhsContractingDimensions == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static DotDimensionNumbersAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto lhsBatchingDimensions = std::get<0>(tblgenKey);
    auto rhsBatchingDimensions = std::get<1>(tblgenKey);
    auto lhsContractingDimensions = std::get<2>(tblgenKey);
    auto rhsContractingDimensions = std::get<3>(tblgenKey);
    lhsBatchingDimensions = allocator.copyInto(lhsBatchingDimensions);
    rhsBatchingDimensions = allocator.copyInto(rhsBatchingDimensions);
    lhsContractingDimensions = allocator.copyInto(lhsContractingDimensions);
    rhsContractingDimensions = allocator.copyInto(rhsContractingDimensions);
    return new (allocator.allocate<DotDimensionNumbersAttrStorage>()) DotDimensionNumbersAttrStorage(lhsBatchingDimensions, rhsBatchingDimensions, lhsContractingDimensions, rhsContractingDimensions);
  }

  ::llvm::ArrayRef<int64_t> lhsBatchingDimensions;
  ::llvm::ArrayRef<int64_t> rhsBatchingDimensions;
  ::llvm::ArrayRef<int64_t> lhsContractingDimensions;
  ::llvm::ArrayRef<int64_t> rhsContractingDimensions;
};
} // namespace detail
DotDimensionNumbersAttr DotDimensionNumbersAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> lhsBatchingDimensions, ::llvm::ArrayRef<int64_t> rhsBatchingDimensions, ::llvm::ArrayRef<int64_t> lhsContractingDimensions, ::llvm::ArrayRef<int64_t> rhsContractingDimensions) {
  return Base::get(context, lhsBatchingDimensions, rhsBatchingDimensions, lhsContractingDimensions, rhsContractingDimensions);
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersAttr::getLhsBatchingDimensions() const {
  return getImpl()->lhsBatchingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersAttr::getRhsBatchingDimensions() const {
  return getImpl()->rhsBatchingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersAttr::getLhsContractingDimensions() const {
  return getImpl()->lhsContractingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersAttr::getRhsContractingDimensions() const {
  return getImpl()->rhsContractingDimensions;
}

} // namespace mhlo
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::mhlo::DotDimensionNumbersAttr)
namespace mlir {
namespace mhlo {
namespace detail {
struct GatherDimensionNumbersAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, int64_t>;
  GatherDimensionNumbersAttrStorage(::llvm::ArrayRef<int64_t> offsetDims, ::llvm::ArrayRef<int64_t> collapsedSliceDims, ::llvm::ArrayRef<int64_t> startIndexMap, int64_t indexVectorDim) : ::mlir::AttributeStorage(), offsetDims(offsetDims), collapsedSliceDims(collapsedSliceDims), startIndexMap(startIndexMap), indexVectorDim(indexVectorDim) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (offsetDims == std::get<0>(tblgenKey)) && (collapsedSliceDims == std::get<1>(tblgenKey)) && (startIndexMap == std::get<2>(tblgenKey)) && (indexVectorDim == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static GatherDimensionNumbersAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto offsetDims = std::get<0>(tblgenKey);
    auto collapsedSliceDims = std::get<1>(tblgenKey);
    auto startIndexMap = std::get<2>(tblgenKey);
    auto indexVectorDim = std::get<3>(tblgenKey);
    offsetDims = allocator.copyInto(offsetDims);
    collapsedSliceDims = allocator.copyInto(collapsedSliceDims);
    startIndexMap = allocator.copyInto(startIndexMap);
    return new (allocator.allocate<GatherDimensionNumbersAttrStorage>()) GatherDimensionNumbersAttrStorage(offsetDims, collapsedSliceDims, startIndexMap, indexVectorDim);
  }

  ::llvm::ArrayRef<int64_t> offsetDims;
  ::llvm::ArrayRef<int64_t> collapsedSliceDims;
  ::llvm::ArrayRef<int64_t> startIndexMap;
  int64_t indexVectorDim;
};
} // namespace detail
GatherDimensionNumbersAttr GatherDimensionNumbersAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> offsetDims, ::llvm::ArrayRef<int64_t> collapsedSliceDims, ::llvm::ArrayRef<int64_t> startIndexMap, int64_t indexVectorDim) {
  return Base::get(context, offsetDims, collapsedSliceDims, startIndexMap, indexVectorDim);
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersAttr::getOffsetDims() const {
  return getImpl()->offsetDims;
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersAttr::getCollapsedSliceDims() const {
  return getImpl()->collapsedSliceDims;
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersAttr::getStartIndexMap() const {
  return getImpl()->startIndexMap;
}

int64_t GatherDimensionNumbersAttr::getIndexVectorDim() const {
  return getImpl()->indexVectorDim;
}

} // namespace mhlo
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::mhlo::GatherDimensionNumbersAttr)
namespace mlir {
namespace mhlo {
namespace detail {
struct ScatterDimensionNumbersAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, int64_t>;
  ScatterDimensionNumbersAttrStorage(::llvm::ArrayRef<int64_t> updateWindowDims, ::llvm::ArrayRef<int64_t> insertedWindowDims, ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims, int64_t indexVectorDim) : ::mlir::AttributeStorage(), updateWindowDims(updateWindowDims), insertedWindowDims(insertedWindowDims), scatterDimsToOperandDims(scatterDimsToOperandDims), indexVectorDim(indexVectorDim) {}

  bool operator==(const KeyTy &tblgenKey) const {
    return (updateWindowDims == std::get<0>(tblgenKey)) && (insertedWindowDims == std::get<1>(tblgenKey)) && (scatterDimsToOperandDims == std::get<2>(tblgenKey)) && (indexVectorDim == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static ScatterDimensionNumbersAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto updateWindowDims = std::get<0>(tblgenKey);
    auto insertedWindowDims = std::get<1>(tblgenKey);
    auto scatterDimsToOperandDims = std::get<2>(tblgenKey);
    auto indexVectorDim = std::get<3>(tblgenKey);
    updateWindowDims = allocator.copyInto(updateWindowDims);
    insertedWindowDims = allocator.copyInto(insertedWindowDims);
    scatterDimsToOperandDims = allocator.copyInto(scatterDimsToOperandDims);
    return new (allocator.allocate<ScatterDimensionNumbersAttrStorage>()) ScatterDimensionNumbersAttrStorage(updateWindowDims, insertedWindowDims, scatterDimsToOperandDims, indexVectorDim);
  }

  ::llvm::ArrayRef<int64_t> updateWindowDims;
  ::llvm::ArrayRef<int64_t> insertedWindowDims;
  ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims;
  int64_t indexVectorDim;
};
} // namespace detail
ScatterDimensionNumbersAttr ScatterDimensionNumbersAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> updateWindowDims, ::llvm::ArrayRef<int64_t> insertedWindowDims, ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims, int64_t indexVectorDim) {
  return Base::get(context, updateWindowDims, insertedWindowDims, scatterDimsToOperandDims, indexVectorDim);
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersAttr::getUpdateWindowDims() const {
  return getImpl()->updateWindowDims;
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersAttr::getInsertedWindowDims() const {
  return getImpl()->insertedWindowDims;
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersAttr::getScatterDimsToOperandDims() const {
  return getImpl()->scatterDimsToOperandDims;
}

int64_t ScatterDimensionNumbersAttr::getIndexVectorDim() const {
  return getImpl()->indexVectorDim;
}

} // namespace mhlo
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::mhlo::ScatterDimensionNumbersAttr)

#endif  // GET_ATTRDEF_CLASSES

