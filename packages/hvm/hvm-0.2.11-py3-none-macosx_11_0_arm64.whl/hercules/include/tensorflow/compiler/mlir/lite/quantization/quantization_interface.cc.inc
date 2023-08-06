/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

int AffineQuantizedOpInterface::GetAffineOperandIndex() {
      return getImpl()->GetAffineOperandIndex(getImpl(), getOperation());
  }
bool AffineQuantizedOpInterface::RequiredNarrowRangeAffineOperand() {
      return getImpl()->RequiredNarrowRangeAffineOperand(getImpl(), getOperation());
  }
int AffineQuantizedOpInterface::GetQuantizationDimIndex() {
      return getImpl()->GetQuantizationDimIndex(getImpl(), getOperation());
  }
int AffineQuantizedOpInterface::GetChannelDimIndex() {
      return getImpl()->GetChannelDimIndex(getImpl(), getOperation());
  }
std::vector<int> DynamicRangeQuantizedOpInterface::GetQuantizableOperandIndices() {
      return getImpl()->GetQuantizableOperandIndices(getImpl(), getOperation());
  }
bool DynamicRangeQuantizedOpInterface::GetDynamicRangeQuantKernelSupport() {
      return getImpl()->GetDynamicRangeQuantKernelSupport(getImpl(), getOperation());
  }
bool DynamicRangeQuantizedOpInterface::RequireAsymmetricQuantizeInputsAttr() {
      return getImpl()->RequireAsymmetricQuantizeInputsAttr(getImpl(), getOperation());
  }
UniformQuantizedType FixedOutputRangeInterface::GetFixedOutputRange(bool sign, int bit_width) {
      return getImpl()->GetFixedOutputRange(getImpl(), getOperation(), sign, bit_width);
  }
bool SameScalesOpInterface::RequiredSameOperandsAndResultsScale(bool sign, int bit_width) {
      return getImpl()->RequiredSameOperandsAndResultsScale(getImpl(), getOperation(), sign, bit_width);
  }
bool SameScalesOpInterface::RequiredSameQuantizedAxes() {
      return getImpl()->RequiredSameQuantizedAxes(getImpl(), getOperation());
  }
