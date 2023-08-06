/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace vhlo {
class ArgResultAliasV1Attr;
class ArrayV1Attr;
class ChannelHandleV1Attr;
class ComparisonDirectionV1Attr;
class ComparisonTypeV1Attr;
class ConvDimensionNumbersV1Attr;
class CustomCallApiVersionV1Attr;
class DenseIntOrFPElementsV1Attr;
class DictionaryV1Attr;
class DotDimensionNumbersV1Attr;
class FftTypeV1Attr;
class FlatSymbolRefV1Attr;
class FloatV1Attr;
class GatherDimensionNumbersV1Attr;
class IntegerV1Attr;
class OutputOperandAliasV1Attr;
class PrecisionV1Attr;
class RngAlgorithmV1Attr;
class RngDistributionV1Attr;
class ScatterDimensionNumbersV1Attr;
class StringV1Attr;
class TransposeV1Attr;
class TypeV1Attr;
class TypeExtensionsV1Attr;
class UnitV1Attr;
namespace detail {
struct ArgResultAliasV1AttrStorage;
} // namespace detail
class ArgResultAliasV1Attr : public ::mlir::Attribute::AttrBase<ArgResultAliasV1Attr, ::mlir::Attribute, detail::ArgResultAliasV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ArgResultAliasV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ArgResultAliasV1");
    return *version;
  }
  static ArgResultAliasV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> argTupleIndices, int64_t resultIndex, ::llvm::ArrayRef<int64_t> resultTupleIndices, bool isMustAlias);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"result_alias"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getArgTupleIndices() const;
  int64_t getResultIndex() const;
  ::llvm::ArrayRef<int64_t> getResultTupleIndices() const;
  bool getIsMustAlias() const;
};
namespace detail {
struct ArrayV1AttrStorage;
} // namespace detail
class ArrayV1Attr : public ::mlir::Attribute::AttrBase<ArrayV1Attr, ::mlir::Attribute, detail::ArrayV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ArrayV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ArrayV1");
    return *version;
  }
  using Base::getChecked;
  static ArrayV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<mlir::Attribute> value);
  static ArrayV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<mlir::Attribute> value);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<mlir::Attribute> value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"array"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<mlir::Attribute> getValue() const;
};
namespace detail {
struct ChannelHandleV1AttrStorage;
} // namespace detail
class ChannelHandleV1Attr : public ::mlir::Attribute::AttrBase<ChannelHandleV1Attr, ::mlir::Attribute, detail::ChannelHandleV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ChannelHandleV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ChannelHandleV1");
    return *version;
  }
  static ChannelHandleV1Attr get(::mlir::MLIRContext *context, int64_t handle, int64_t type);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"channel_handle"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  int64_t getHandle() const;
  int64_t getType() const;
};
namespace detail {
struct ComparisonDirectionV1AttrStorage;
} // namespace detail
class ComparisonDirectionV1Attr : public ::mlir::Attribute::AttrBase<ComparisonDirectionV1Attr, ::mlir::Attribute, detail::ComparisonDirectionV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static ComparisonDirectionV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::ComparisonDirectionV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"comparison_direction"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::ComparisonDirectionV1 getValue() const;
};
namespace detail {
struct ComparisonTypeV1AttrStorage;
} // namespace detail
class ComparisonTypeV1Attr : public ::mlir::Attribute::AttrBase<ComparisonTypeV1Attr, ::mlir::Attribute, detail::ComparisonTypeV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static ComparisonTypeV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::ComparisonTypeV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"comparison_type"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::ComparisonTypeV1 getValue() const;
};
namespace detail {
struct ConvDimensionNumbersV1AttrStorage;
} // namespace detail
class ConvDimensionNumbersV1Attr : public ::mlir::Attribute::AttrBase<ConvDimensionNumbersV1Attr, ::mlir::Attribute, detail::ConvDimensionNumbersV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ConvDimensionNumbersV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ConvDimensionNumbersV1");
    return *version;
  }
  static ConvDimensionNumbersV1Attr get(::mlir::MLIRContext *context, int64_t inputBatchDimension, int64_t inputFeatureDimension, ::llvm::ArrayRef<int64_t> inputSpatialDimensions, int64_t kernelInputFeatureDimension, int64_t kernelOutputFeatureDimension, ::llvm::ArrayRef<int64_t> kernelSpatialDimensions, int64_t outputBatchDimension, int64_t outputFeatureDimension, ::llvm::ArrayRef<int64_t> outputSpatialDimensions);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"conv"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  int64_t getInputBatchDimension() const;
  int64_t getInputFeatureDimension() const;
  ::llvm::ArrayRef<int64_t> getInputSpatialDimensions() const;
  int64_t getKernelInputFeatureDimension() const;
  int64_t getKernelOutputFeatureDimension() const;
  ::llvm::ArrayRef<int64_t> getKernelSpatialDimensions() const;
  int64_t getOutputBatchDimension() const;
  int64_t getOutputFeatureDimension() const;
  ::llvm::ArrayRef<int64_t> getOutputSpatialDimensions() const;
};
namespace detail {
struct CustomCallApiVersionV1AttrStorage;
} // namespace detail
class CustomCallApiVersionV1Attr : public ::mlir::Attribute::AttrBase<CustomCallApiVersionV1Attr, ::mlir::Attribute, detail::CustomCallApiVersionV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static CustomCallApiVersionV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::CustomCallApiVersionV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"api_version"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::CustomCallApiVersionV1 getValue() const;
};
namespace detail {
struct DenseIntOrFPElementsV1AttrStorage;
} // namespace detail
class DenseIntOrFPElementsV1Attr : public ::mlir::Attribute::AttrBase<DenseIntOrFPElementsV1Attr, ::mlir::Attribute, detail::DenseIntOrFPElementsV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in DenseIntOrFPElementsV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in DenseIntOrFPElementsV1");
    return *version;
  }
  using Base::getChecked;
  static DenseIntOrFPElementsV1Attr get(::mlir::MLIRContext *context, ::mlir::Type type, ::llvm::ArrayRef<char> raw_data);
  static DenseIntOrFPElementsV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Type type, ::llvm::ArrayRef<char> raw_data);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::Type type, ::llvm::ArrayRef<char> raw_data);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"dense"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::Type getType() const;
  ::llvm::ArrayRef<char> getRawData() const;
};
namespace detail {
struct DictionaryV1AttrStorage;
} // namespace detail
class DictionaryV1Attr : public ::mlir::Attribute::AttrBase<DictionaryV1Attr, ::mlir::Attribute, detail::DictionaryV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in DictionaryV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in DictionaryV1");
    return *version;
  }
  using Base::getChecked;
  static DictionaryV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value);
  static DictionaryV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"dict"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> getValue() const;
};
namespace detail {
struct DotDimensionNumbersV1AttrStorage;
} // namespace detail
class DotDimensionNumbersV1Attr : public ::mlir::Attribute::AttrBase<DotDimensionNumbersV1Attr, ::mlir::Attribute, detail::DotDimensionNumbersV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in DotDimensionNumbersV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in DotDimensionNumbersV1");
    return *version;
  }
  static DotDimensionNumbersV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> lhsBatchingDimensions, ::llvm::ArrayRef<int64_t> rhsBatchingDimensions, ::llvm::ArrayRef<int64_t> lhsContractingDimensions, ::llvm::ArrayRef<int64_t> rhsContractingDimensions);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"dot"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getLhsBatchingDimensions() const;
  ::llvm::ArrayRef<int64_t> getRhsBatchingDimensions() const;
  ::llvm::ArrayRef<int64_t> getLhsContractingDimensions() const;
  ::llvm::ArrayRef<int64_t> getRhsContractingDimensions() const;
};
namespace detail {
struct FftTypeV1AttrStorage;
} // namespace detail
class FftTypeV1Attr : public ::mlir::Attribute::AttrBase<FftTypeV1Attr, ::mlir::Attribute, detail::FftTypeV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static FftTypeV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::FftTypeV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"fft_type"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::FftTypeV1 getValue() const;
};
namespace detail {
struct FlatSymbolRefV1AttrStorage;
} // namespace detail
class FlatSymbolRefV1Attr : public ::mlir::Attribute::AttrBase<FlatSymbolRefV1Attr, ::mlir::Attribute, detail::FlatSymbolRefV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in FlatSymbolRefV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in FlatSymbolRefV1");
    return *version;
  }
  using Base::getChecked;
  static FlatSymbolRefV1Attr get(::mlir::MLIRContext *context, ::mlir::Attribute root_reference);
  static FlatSymbolRefV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Attribute root_reference);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::Attribute root_reference);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"sym"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::Attribute getRootReference() const;
};
namespace detail {
struct FloatV1AttrStorage;
} // namespace detail
class FloatV1Attr : public ::mlir::Attribute::AttrBase<FloatV1Attr, ::mlir::Attribute, detail::FloatV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in FloatV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in FloatV1");
    return *version;
  }
  using Base::getChecked;
  static FloatV1Attr get(::mlir::MLIRContext *context, mlir::Type type, ::llvm::APFloat value);
  static FloatV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, mlir::Type type, ::llvm::APFloat value);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, mlir::Type type, ::llvm::APFloat value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"float"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  mlir::Type getType() const;
  ::llvm::APFloat getValue() const;
};
namespace detail {
struct GatherDimensionNumbersV1AttrStorage;
} // namespace detail
class GatherDimensionNumbersV1Attr : public ::mlir::Attribute::AttrBase<GatherDimensionNumbersV1Attr, ::mlir::Attribute, detail::GatherDimensionNumbersV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in GatherDimensionNumbersV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in GatherDimensionNumbersV1");
    return *version;
  }
  static GatherDimensionNumbersV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> offsetDims, ::llvm::ArrayRef<int64_t> collapsedSliceDims, ::llvm::ArrayRef<int64_t> startIndexMap, int64_t indexVectorDim);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"gather"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getOffsetDims() const;
  ::llvm::ArrayRef<int64_t> getCollapsedSliceDims() const;
  ::llvm::ArrayRef<int64_t> getStartIndexMap() const;
  int64_t getIndexVectorDim() const;
};
namespace detail {
struct IntegerV1AttrStorage;
} // namespace detail
class IntegerV1Attr : public ::mlir::Attribute::AttrBase<IntegerV1Attr, ::mlir::Attribute, detail::IntegerV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in IntegerV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in IntegerV1");
    return *version;
  }
  using Base::getChecked;
  static IntegerV1Attr get(::mlir::MLIRContext *context, mlir::Type type, APInt value);
  static IntegerV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, mlir::Type type, APInt value);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, mlir::Type type, APInt value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"integer"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  mlir::Type getType() const;
  APInt getValue() const;
};
namespace detail {
struct OutputOperandAliasV1AttrStorage;
} // namespace detail
class OutputOperandAliasV1Attr : public ::mlir::Attribute::AttrBase<OutputOperandAliasV1Attr, ::mlir::Attribute, detail::OutputOperandAliasV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.4.0");
    if (failed(version)) llvm_unreachable("invalid version 0.4.0 in OutputOperandAliasV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in OutputOperandAliasV1");
    return *version;
  }
  static OutputOperandAliasV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> outputTupleIndices, int64_t operandIndex, ::llvm::ArrayRef<int64_t> operandTupleIndices);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"output_operand_alias"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getOutputTupleIndices() const;
  int64_t getOperandIndex() const;
  ::llvm::ArrayRef<int64_t> getOperandTupleIndices() const;
};
namespace detail {
struct PrecisionV1AttrStorage;
} // namespace detail
class PrecisionV1Attr : public ::mlir::Attribute::AttrBase<PrecisionV1Attr, ::mlir::Attribute, detail::PrecisionV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static PrecisionV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::PrecisionV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"precision"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::PrecisionV1 getValue() const;
};
namespace detail {
struct RngAlgorithmV1AttrStorage;
} // namespace detail
class RngAlgorithmV1Attr : public ::mlir::Attribute::AttrBase<RngAlgorithmV1Attr, ::mlir::Attribute, detail::RngAlgorithmV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static RngAlgorithmV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::RngAlgorithmV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"rng_algorithm"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::RngAlgorithmV1 getValue() const;
};
namespace detail {
struct RngDistributionV1AttrStorage;
} // namespace detail
class RngDistributionV1Attr : public ::mlir::Attribute::AttrBase<RngDistributionV1Attr, ::mlir::Attribute, detail::RngDistributionV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static RngDistributionV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::RngDistributionV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"rng_distribution"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::RngDistributionV1 getValue() const;
};
namespace detail {
struct ScatterDimensionNumbersV1AttrStorage;
} // namespace detail
class ScatterDimensionNumbersV1Attr : public ::mlir::Attribute::AttrBase<ScatterDimensionNumbersV1Attr, ::mlir::Attribute, detail::ScatterDimensionNumbersV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ScatterDimensionNumbersV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ScatterDimensionNumbersV1");
    return *version;
  }
  static ScatterDimensionNumbersV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> updateWindowDims, ::llvm::ArrayRef<int64_t> insertedWindowDims, ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims, int64_t indexVectorDim);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"scatter"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getUpdateWindowDims() const;
  ::llvm::ArrayRef<int64_t> getInsertedWindowDims() const;
  ::llvm::ArrayRef<int64_t> getScatterDimsToOperandDims() const;
  int64_t getIndexVectorDim() const;
};
namespace detail {
struct StringV1AttrStorage;
} // namespace detail
class StringV1Attr : public ::mlir::Attribute::AttrBase<StringV1Attr, ::mlir::Attribute, detail::StringV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in StringV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in StringV1");
    return *version;
  }
  static StringV1Attr get(::mlir::MLIRContext *context, ::llvm::StringRef value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"string"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::StringRef getValue() const;
};
namespace detail {
struct TransposeV1AttrStorage;
} // namespace detail
class TransposeV1Attr : public ::mlir::Attribute::AttrBase<TransposeV1Attr, ::mlir::Attribute, detail::TransposeV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    return *mlir::vhlo::Version::fromString("0.3.0");
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    return *mlir::vhlo::Version::fromString("current");
  }
  static TransposeV1Attr get(::mlir::MLIRContext *context, ::mlir::vhlo::TransposeV1 value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"transpose"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::vhlo::TransposeV1 getValue() const;
};
namespace detail {
struct TypeV1AttrStorage;
} // namespace detail
class TypeV1Attr : public ::mlir::Attribute::AttrBase<TypeV1Attr, ::mlir::Attribute, detail::TypeV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in TypeV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in TypeV1");
    return *version;
  }
  using Base::getChecked;
  static TypeV1Attr get(::mlir::MLIRContext *context, ::mlir::Type value);
  static TypeV1Attr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Type value);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::Type value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"type"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::Type getValue() const;
};
namespace detail {
struct TypeExtensionsV1AttrStorage;
} // namespace detail
class TypeExtensionsV1Attr : public ::mlir::Attribute::AttrBase<TypeExtensionsV1Attr, ::mlir::Attribute, detail::TypeExtensionsV1AttrStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in TypeExtensionsV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in TypeExtensionsV1");
    return *version;
  }
  static TypeExtensionsV1Attr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> bounds);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"type_extensions"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getBounds() const;
};
class UnitV1Attr : public ::mlir::Attribute::AttrBase<UnitV1Attr, ::mlir::Attribute, ::mlir::AttributeStorage, ::mlir::vhlo::VersionedAttrInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in UnitV1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in UnitV1");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"unit"};
  }

};
} // namespace vhlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ArgResultAliasV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ArrayV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ChannelHandleV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ComparisonDirectionV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ComparisonTypeV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ConvDimensionNumbersV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::CustomCallApiVersionV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::DenseIntOrFPElementsV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::DictionaryV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::DotDimensionNumbersV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::FftTypeV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::FlatSymbolRefV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::FloatV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::GatherDimensionNumbersV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::OutputOperandAliasV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::PrecisionV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::RngAlgorithmV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::RngDistributionV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ScatterDimensionNumbersV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::StringV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::TransposeV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::TypeV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::TypeExtensionsV1Attr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::UnitV1Attr)

#endif  // GET_ATTRDEF_CLASSES

