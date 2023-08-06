/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

SmallVector<unsigned, 4> FoldOperandsTransposeInterface::GetLayoutDependentArgs() {
      return getImpl()->GetLayoutDependentArgs(getImpl(), getOperation());
  }
SmallVector<unsigned, 4> FoldOperandsTransposeInterface::GetLayoutDependentResults() {
      return getImpl()->GetLayoutDependentResults(getImpl(), getOperation());
  }
LogicalResult FoldOperandsTransposeInterface::FoldOperandsPermutation(ArrayRef<int64_t> permutation) {
      return getImpl()->FoldOperandsPermutation(getImpl(), getOperation(), permutation);
  }
int64_t GetResourceInstanceInterface::GetResourceInstanceId() {
      return getImpl()->GetResourceInstanceId(getImpl(), getOperation());
  }
StringRef LayoutSensitiveInterface::data_format() {
      return getImpl()->data_format(getImpl(), getOperation());
  }
SmallVector<unsigned, 4> LayoutSensitiveInterface::GetLayoutDependentArgs() {
      return getImpl()->GetLayoutDependentArgs(getImpl(), getOperation());
  }
SmallVector<unsigned, 4> LayoutSensitiveInterface::GetLayoutDependentResults() {
      return getImpl()->GetLayoutDependentResults(getImpl(), getOperation());
  }
StringRef LayoutSensitiveInterface::GetOptimalLayout(const RuntimeDevices& devices) {
      return getImpl()->GetOptimalLayout(getImpl(), getOperation(), devices);
  }
LogicalResult LayoutSensitiveInterface::UpdateDataFormat(StringRef data_format) {
      return getImpl()->UpdateDataFormat(getImpl(), getOperation(), data_format);
  }
llvm::SmallVector<ResourceHandleValueAndId, 4> ResourceHandleAllocatorInterface::GetResourceHandleValueAndIdList(llvm::SmallDenseMap<ResourceHandle, int64_t>& resource_handle_id_map, int64_t& next_id) {
      return getImpl()->GetResourceHandleValueAndIdList(getImpl(), getOperation(), resource_handle_id_map, next_id);
  }
