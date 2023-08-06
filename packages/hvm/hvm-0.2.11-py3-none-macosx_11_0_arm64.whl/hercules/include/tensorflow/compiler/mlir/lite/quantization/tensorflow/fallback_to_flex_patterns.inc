/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

static ::mlir::LogicalResult static_dag_matcher_0(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::ElementsAttr &bias, ::mlir::TF::ConstOp &bias_cst) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::ConstOp type";
    });
  }
  bias_cst = castedOp1;
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
      });
    }
    bias = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_1(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::ElementsAttr &NegOne, ::mlir::TF::ConstOp &cst_negone) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::ConstOp type";
    });
  }
  cst_negone = castedOp1;
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
      });
    }
    NegOne = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_2(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::TF::ConstOp &cst_one, ::mlir::ElementsAttr &One) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::ConstOp type";
    });
  }
  cst_one = castedOp1;
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
      });
    }
    One = tblgen_attr;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult static_dag_matcher_3(::mlir::PatternRewriter &rewriter, ::mlir::Operation *op0, ::llvm::SmallVector<::mlir::Operation *, 4> &tblgen_ops, ::mlir::ElementsAttr &cst_val, ::mlir::TF::ConstOp &cst) {
  (void)tblgen_ops;
  auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op0); (void)castedOp1;
  if (!(castedOp1)){
    return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
      diag << "castedOp1 is not ::mlir::TF::ConstOp type";
    });
  }
  cst = castedOp1;
  {
    auto tblgen_attr = op0->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
    if (!(tblgen_attr)){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
      });
    }
    cst_val = tblgen_attr;
  }
  return ::mlir::success();
}

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:77
*/
struct KeepAddV2Op : public ::mlir::RewritePattern {
  KeepAddV2Op(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.AddV2", 2, context, {"tf.AddV2"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TF::ConstOp bias_cst;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::TF::AddV2Op add_op;
    ::mlir::ElementsAttr bias;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::AddV2Op>(op0); (void)castedOp0;
    add_op = castedOp0;
    input = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_0(rewriter, op1, tblgen_ops, bias, bias_cst))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((IsFusibleWithBiasOp((*input.begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }
    if (!((RankEquals((*bias_cst.getODSResults(0).begin()), 1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'bias_cst' failed to satisfy constraint: ''";
      });
    }
    if (!((!(*add_op.getODSResults(0).begin()).getDefiningOp()->hasAttr(kNoFallbackAttr)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'add_op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::AddV2Op tblgen_AddV2Op_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*bias_cst.getODSResults(0).begin());
      tblgen_AddV2Op_0 = rewriter.create<::mlir::TF::AddV2Op>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = SetNoFallbackAttr(rewriter, tblgen_AddV2Op_0); (void)nativeVar_1;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ {nativeVar_1} }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:83
*/
struct KeepSubOp : public ::mlir::RewritePattern {
  KeepSubOp(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Sub", 2, context, {"tf.Sub"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::TF::ConstOp bias_cst;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::TF::SubOp sub_op;
    ::mlir::ElementsAttr bias;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::SubOp>(op0); (void)castedOp0;
    sub_op = castedOp0;
    input = castedOp0.getODSOperands(0);
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_0(rewriter, op1, tblgen_ops, bias, bias_cst))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((IsFusibleWithBiasOp((*input.begin()).getDefiningOp())))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'input' failed to satisfy constraint: ''";
      });
    }
    if (!((RankEquals((*bias_cst.getODSResults(0).begin()), 1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'bias_cst' failed to satisfy constraint: ''";
      });
    }
    if (!((!(*sub_op.getODSResults(0).begin()).getDefiningOp()->hasAttr(kNoFallbackAttr)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'sub_op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::SubOp tblgen_SubOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*bias_cst.getODSResults(0).begin());
      tblgen_SubOp_0 = rewriter.create<::mlir::TF::SubOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = SetNoFallbackAttr(rewriter, tblgen_SubOp_0); (void)nativeVar_1;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ {nativeVar_1} }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:54
*/
struct MatchRelu1Pattern1 : public ::mlir::RewritePattern {
  MatchRelu1Pattern1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Minimum", 4, context, {"tf.Maximum", "tf.Minimum"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr One;
    ::mlir::TF::ConstOp cst_one;
    ::mlir::ElementsAttr NegOne;
    ::mlir::TF::MinimumOp min_op;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::TF::ConstOp cst_negone;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MinimumOp>(op0); (void)castedOp0;
    min_op = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::MaximumOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::MaximumOp type";
        });
      }
      input = castedOp1.getODSOperands(0);
      {
        auto *op2 = (*castedOp1.getODSOperands(1).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 1 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_1(rewriter, op2, tblgen_ops, NegOne, cst_negone))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_2(rewriter, op1, tblgen_ops, cst_one, One))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((FloatValueEquals(NegOne, -1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'NegOne' failed to satisfy constraint: ''";
      });
    }
    if (!((FloatValueEquals(One, 1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'One' failed to satisfy constraint: ''";
      });
    }
    if (!((!(*min_op.getODSResults(0).begin()).getDefiningOp()->hasAttr(kNoFallbackAttr)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'min_op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MaximumOp tblgen_MaximumOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*cst_negone.getODSResults(0).begin());
      tblgen_MaximumOp_0 = rewriter.create<::mlir::TF::MaximumOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = SetNoFallbackAttr(rewriter, tblgen_MaximumOp_0); (void)nativeVar_1;
    ::mlir::TF::MinimumOp tblgen_MinimumOp_2;
    {
      ::mlir::Value tblgen_value_0 = nativeVar_1;
      ::mlir::Value tblgen_value_1 = (*cst_one.getODSResults(0).begin());
      tblgen_MinimumOp_2 = rewriter.create<::mlir::TF::MinimumOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_3 = SetNoFallbackAttr(rewriter, tblgen_MinimumOp_2); (void)nativeVar_3;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ {nativeVar_3} }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:65
*/
struct MatchRelu1Pattern2 : public ::mlir::RewritePattern {
  MatchRelu1Pattern2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Maximum", 4, context, {"tf.Maximum", "tf.Minimum"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr One;
    ::mlir::TF::ConstOp cst_one;
    ::mlir::TF::ConstOp cst_negone;
    ::mlir::TF::MaximumOp max_op;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::mlir::ElementsAttr NegOne;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MaximumOp>(op0); (void)castedOp0;
    max_op = castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::MinimumOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::MinimumOp type";
        });
      }
      input = castedOp1.getODSOperands(0);
      {
        auto *op2 = (*castedOp1.getODSOperands(1).begin()).getDefiningOp();
        if (!(op2)){
          return rewriter.notifyMatchFailure(castedOp1, [&](::mlir::Diagnostic &diag) {
            diag << "There's no operation that defines operand 1 of castedOp1";
          });
        }
        if(failed(static_dag_matcher_2(rewriter, op2, tblgen_ops, cst_one, One))) {
          return ::mlir::failure();
        }
        tblgen_ops.push_back(op2);
      }
      tblgen_ops.push_back(op1);
    }
    {
      auto *op1 = (*castedOp0.getODSOperands(1).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 1 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_1(rewriter, op1, tblgen_ops, NegOne, cst_negone))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    if (!((FloatValueEquals(NegOne, -1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'NegOne' failed to satisfy constraint: ''";
      });
    }
    if (!((FloatValueEquals(One, 1)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'One' failed to satisfy constraint: ''";
      });
    }
    if (!((!(*max_op.getODSResults(0).begin()).getDefiningOp()->hasAttr(kNoFallbackAttr)))){
      return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
        diag << "entities 'max_op' failed to satisfy constraint: ''";
      });
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc(), tblgen_ops[2]->getLoc(), tblgen_ops[3]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MinimumOp tblgen_MinimumOp_0;
    {
      ::mlir::Value tblgen_value_0 = (*input.begin());
      ::mlir::Value tblgen_value_1 = (*cst_one.getODSResults(0).begin());
      tblgen_MinimumOp_0 = rewriter.create<::mlir::TF::MinimumOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_1 = SetNoFallbackAttr(rewriter, tblgen_MinimumOp_0); (void)nativeVar_1;
    ::mlir::TF::MaximumOp tblgen_MaximumOp_2;
    {
      ::mlir::Value tblgen_value_0 = nativeVar_1;
      ::mlir::Value tblgen_value_1 = (*cst_negone.getODSResults(0).begin());
      tblgen_MaximumOp_2 = rewriter.create<::mlir::TF::MaximumOp>(odsLoc,
        /*x=*/tblgen_value_0,
        /*y=*/tblgen_value_1
      );
    }
    auto nativeVar_3 = SetNoFallbackAttr(rewriter, tblgen_MaximumOp_2); (void)nativeVar_3;

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ {nativeVar_3} }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:37
*/
struct RemoveConstIdentityOp : public ::mlir::RewritePattern {
  RemoveConstIdentityOp(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Identity", 2, context, {"tf.Const"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr input;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::IdentityOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      auto castedOp1 = ::llvm::dyn_cast<::mlir::TF::ConstOp>(op1); (void)castedOp1;
      if (!(castedOp1)){
        return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
          diag << "castedOp1 is not ::mlir::TF::ConstOp type";
        });
      }
      {
        auto tblgen_attr = op1->getAttrOfType<::mlir::ElementsAttr>("value");(void)tblgen_attr;
        if (!(tblgen_attr)){
          return rewriter.notifyMatchFailure(op1, [&](::mlir::Diagnostic &diag) {
            diag << "expected op 'tf.Const' to have attribute 'value' of type '::mlir::ElementsAttr'";
          });
        }
        input = tblgen_attr;
      }
      tblgen_ops.push_back(op1);
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::ConstOp tblgen_ConstOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      if (auto tmpAttr = input) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("value"), tmpAttr);
      }
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_ConstOp_0 = rewriter.create<::mlir::TF::ConstOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_ConstOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:43
*/
struct SwapMaximumOperands : public ::mlir::RewritePattern {
  SwapMaximumOperands(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Maximum", 2, context, {"tf.Maximum"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr cst_val;
    ::mlir::TF::ConstOp cst;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MaximumOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_3(rewriter, op1, tblgen_ops, cst_val, cst))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    input = castedOp0.getODSOperands(1);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MaximumOp tblgen_MaximumOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*cst.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MaximumOp_0 = rewriter.create<::mlir::TF::MaximumOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MaximumOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    tensorflow/compiler/mlir/lite/quantization/tensorflow/fallback_to_flex_patterns.td:47
*/
struct SwapMinimumOperands : public ::mlir::RewritePattern {
  SwapMinimumOperands(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("tf.Minimum", 2, context, {"tf.Minimum"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::ElementsAttr cst_val;
    ::mlir::TF::ConstOp cst;
    ::mlir::Operation::operand_range input(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::TF::MinimumOp>(op0); (void)castedOp0;
    {
      auto *op1 = (*castedOp0.getODSOperands(0).begin()).getDefiningOp();
      if (!(op1)){
        return rewriter.notifyMatchFailure(castedOp0, [&](::mlir::Diagnostic &diag) {
          diag << "There's no operation that defines operand 0 of castedOp0";
        });
      }
      if(failed(static_dag_matcher_3(rewriter, op1, tblgen_ops, cst_val, cst))) {
        return ::mlir::failure();
      }
      tblgen_ops.push_back(op1);
    }
    input = castedOp0.getODSOperands(1);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc(), tblgen_ops[1]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::TF::MinimumOp tblgen_MinimumOp_0;
    {
      ::mlir::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::mlir::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*input.begin()));
      tblgen_values.push_back((*cst.getODSResults(0).begin()));
      ::mlir::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_MinimumOp_0 = rewriter.create<::mlir::TF::MinimumOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_MinimumOp_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<KeepAddV2Op>(patterns.getContext());
  patterns.add<KeepSubOp>(patterns.getContext());
  patterns.add<MatchRelu1Pattern1>(patterns.getContext());
  patterns.add<MatchRelu1Pattern2>(patterns.getContext());
  patterns.add<RemoveConstIdentityOp>(patterns.getContext());
  patterns.add<SwapMaximumOperands>(patterns.getContext());
  patterns.add<SwapMinimumOperands>(patterns.getContext());
}
