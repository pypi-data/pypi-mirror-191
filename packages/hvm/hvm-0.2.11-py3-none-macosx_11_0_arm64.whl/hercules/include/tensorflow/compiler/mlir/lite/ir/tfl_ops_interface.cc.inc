/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

int64_t TflArithmeticCountOpInterface::GetArithmeticCount(Operation* op) {
      return getImpl()->GetArithmeticCount(op);
  }
LogicalResult TflRuntimeVerifyOpInterface::VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail) {
      return getImpl()->VerifyTflRuntimeConstraints(op, emit_error_on_verify_fail);
  }
std::vector<int> SparseOpInterface::GetSparseOperands() {
      return getImpl()->GetSparseOperands(getImpl(), getOperation());
  }
std::vector<std::vector<int>> SparseOpInterface::GetFloatBlockSize() {
      return getImpl()->GetFloatBlockSize(getImpl(), getOperation());
  }
std::vector<std::vector<int>> SparseOpInterface::GetQuantizedBlockSize() {
      return getImpl()->GetQuantizedBlockSize(getImpl(), getOperation());
  }
std::vector<int> StatefulOpInterface::GetStatefulOperands() {
      return getImpl()->GetStatefulOperands(getImpl(), getOperation());
  }
