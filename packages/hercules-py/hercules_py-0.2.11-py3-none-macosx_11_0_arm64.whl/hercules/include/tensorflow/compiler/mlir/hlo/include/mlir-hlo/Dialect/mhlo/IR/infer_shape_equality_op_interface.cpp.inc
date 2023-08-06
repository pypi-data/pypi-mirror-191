/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

bool InferShapeEqualityOpInterface::inferInputsShapeEquality(int lhs, int rhs) {
      return getImpl()->inferInputsShapeEquality(getImpl(), getOperation(), lhs, rhs);
  }
bool InferShapeEqualityOpInterface::inferOutputsShapeEquality(int lhs, int rhs) {
      return getImpl()->inferOutputsShapeEquality(getImpl(), getOperation(), lhs, rhs);
  }
bool InferShapeEqualityOpInterface::inferInputOutputShapeEquality(int input, int output) {
      return getImpl()->inferInputOutputShapeEquality(getImpl(), getOperation(), input, output);
  }
