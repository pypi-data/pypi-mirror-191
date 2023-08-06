/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_LIST
#undef GET_ATTRDEF_LIST

::mlir::vhlo::ArgResultAliasV1Attr,
::mlir::vhlo::ArrayV1Attr,
::mlir::vhlo::ChannelHandleV1Attr,
::mlir::vhlo::ComparisonDirectionV1Attr,
::mlir::vhlo::ComparisonTypeV1Attr,
::mlir::vhlo::ConvDimensionNumbersV1Attr,
::mlir::vhlo::CustomCallApiVersionV1Attr,
::mlir::vhlo::DenseIntOrFPElementsV1Attr,
::mlir::vhlo::DictionaryV1Attr,
::mlir::vhlo::DotDimensionNumbersV1Attr,
::mlir::vhlo::FftTypeV1Attr,
::mlir::vhlo::FlatSymbolRefV1Attr,
::mlir::vhlo::FloatV1Attr,
::mlir::vhlo::GatherDimensionNumbersV1Attr,
::mlir::vhlo::IntegerV1Attr,
::mlir::vhlo::OutputOperandAliasV1Attr,
::mlir::vhlo::PrecisionV1Attr,
::mlir::vhlo::RngAlgorithmV1Attr,
::mlir::vhlo::RngDistributionV1Attr,
::mlir::vhlo::ScatterDimensionNumbersV1Attr,
::mlir::vhlo::StringV1Attr,
::mlir::vhlo::TransposeV1Attr,
::mlir::vhlo::TypeV1Attr,
::mlir::vhlo::TypeExtensionsV1Attr,
::mlir::vhlo::UnitV1Attr

#endif  // GET_ATTRDEF_LIST

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES

static ::mlir::OptionalParseResult generatedAttributeParser(::mlir::AsmParser &parser, ::llvm::StringRef *mnemonic, ::mlir::Type type, ::mlir::Attribute &value) {
  return ::mlir::AsmParser::KeywordSwitch<::mlir::OptionalParseResult>(parser)
    .Case(::mlir::vhlo::ArgResultAliasV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ArgResultAliasV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ArrayV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ArrayV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ChannelHandleV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ChannelHandleV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ComparisonDirectionV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ComparisonDirectionV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ComparisonTypeV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ComparisonTypeV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ConvDimensionNumbersV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ConvDimensionNumbersV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::CustomCallApiVersionV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::CustomCallApiVersionV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::DenseIntOrFPElementsV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::DenseIntOrFPElementsV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::DictionaryV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::DictionaryV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::DotDimensionNumbersV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::DotDimensionNumbersV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::FftTypeV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::FftTypeV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::FlatSymbolRefV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::FlatSymbolRefV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::FloatV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::FloatV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::GatherDimensionNumbersV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::GatherDimensionNumbersV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::IntegerV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::IntegerV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::OutputOperandAliasV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::OutputOperandAliasV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::PrecisionV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::PrecisionV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::RngAlgorithmV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::RngAlgorithmV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::RngDistributionV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::RngDistributionV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::ScatterDimensionNumbersV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::ScatterDimensionNumbersV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::StringV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::StringV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::TransposeV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::TransposeV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::TypeV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::TypeV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::TypeExtensionsV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::TypeExtensionsV1Attr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::vhlo::UnitV1Attr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::vhlo::UnitV1Attr::get(parser.getContext());
      return ::mlir::success(!!value);
    })
    .Default([&](llvm::StringRef keyword, llvm::SMLoc) {
      *mnemonic = keyword;
      return std::nullopt;
    });
}

static ::mlir::LogicalResult generatedAttributePrinter(::mlir::Attribute def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Attribute, ::mlir::LogicalResult>(def)    .Case<::mlir::vhlo::ArgResultAliasV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ArgResultAliasV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ArrayV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ArrayV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ChannelHandleV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ChannelHandleV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ComparisonDirectionV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ComparisonDirectionV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ComparisonTypeV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ComparisonTypeV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ConvDimensionNumbersV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ConvDimensionNumbersV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::CustomCallApiVersionV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::CustomCallApiVersionV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::DenseIntOrFPElementsV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::DenseIntOrFPElementsV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::DictionaryV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::DictionaryV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::DotDimensionNumbersV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::DotDimensionNumbersV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::FftTypeV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::FftTypeV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::FlatSymbolRefV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::FlatSymbolRefV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::FloatV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::FloatV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::GatherDimensionNumbersV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::GatherDimensionNumbersV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::IntegerV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::IntegerV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::OutputOperandAliasV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::OutputOperandAliasV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::PrecisionV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::PrecisionV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::RngAlgorithmV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::RngAlgorithmV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::RngDistributionV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::RngDistributionV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::ScatterDimensionNumbersV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::ScatterDimensionNumbersV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::StringV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::StringV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::TransposeV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::TransposeV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::TypeV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::TypeV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::TypeExtensionsV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::TypeExtensionsV1Attr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::vhlo::UnitV1Attr>([&](auto t) {
      printer << ::mlir::vhlo::UnitV1Attr::getMnemonic();
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace vhlo {
namespace detail {
struct ArgResultAliasV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, int64_t, ::llvm::ArrayRef<int64_t>, bool>;
  ArgResultAliasV1AttrStorage(::llvm::ArrayRef<int64_t> argTupleIndices, int64_t resultIndex, ::llvm::ArrayRef<int64_t> resultTupleIndices, bool isMustAlias) : argTupleIndices(argTupleIndices), resultIndex(resultIndex), resultTupleIndices(resultTupleIndices), isMustAlias(isMustAlias) {}

  KeyTy getAsKey() const {
    return KeyTy(argTupleIndices, resultIndex, resultTupleIndices, isMustAlias);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (argTupleIndices == std::get<0>(tblgenKey)) && (resultIndex == std::get<1>(tblgenKey)) && (resultTupleIndices == std::get<2>(tblgenKey)) && (isMustAlias == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static ArgResultAliasV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto argTupleIndices = std::get<0>(tblgenKey);
    auto resultIndex = std::get<1>(tblgenKey);
    auto resultTupleIndices = std::get<2>(tblgenKey);
    auto isMustAlias = std::get<3>(tblgenKey);
    argTupleIndices = allocator.copyInto(argTupleIndices);
    resultTupleIndices = allocator.copyInto(resultTupleIndices);
    return new (allocator.allocate<ArgResultAliasV1AttrStorage>()) ArgResultAliasV1AttrStorage(argTupleIndices, resultIndex, resultTupleIndices, isMustAlias);
  }

  ::llvm::ArrayRef<int64_t> argTupleIndices;
  int64_t resultIndex;
  ::llvm::ArrayRef<int64_t> resultTupleIndices;
  bool isMustAlias;
};
} // namespace detail
ArgResultAliasV1Attr ArgResultAliasV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> argTupleIndices, int64_t resultIndex, ::llvm::ArrayRef<int64_t> resultTupleIndices, bool isMustAlias) {
  return Base::get(context, argTupleIndices, resultIndex, resultTupleIndices, isMustAlias);
}

::mlir::Attribute ArgResultAliasV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_argTupleIndices;
  ::mlir::FailureOr<int64_t> _result_resultIndex;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_resultTupleIndices;
  ::mlir::FailureOr<bool> _result_isMustAlias;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_argTupleIndices = false;
  bool _seen_resultIndex = false;
  bool _seen_resultTupleIndices = false;
  bool _seen_isMustAlias = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_argTupleIndices && _paramKey == "argTupleIndices") {
        _seen_argTupleIndices = true;

        // Parse variable 'argTupleIndices'
        _result_argTupleIndices = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_argTupleIndices)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ArgResultAliasAttrV1 parameter 'argTupleIndices' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_resultIndex && _paramKey == "resultIndex") {
        _seen_resultIndex = true;

        // Parse variable 'resultIndex'
        _result_resultIndex = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_resultIndex)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ArgResultAliasAttrV1 parameter 'resultIndex' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_resultTupleIndices && _paramKey == "resultTupleIndices") {
        _seen_resultTupleIndices = true;

        // Parse variable 'resultTupleIndices'
        _result_resultTupleIndices = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_resultTupleIndices)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ArgResultAliasAttrV1 parameter 'resultTupleIndices' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_isMustAlias && _paramKey == "isMustAlias") {
        _seen_isMustAlias = true;

        // Parse variable 'isMustAlias'
        _result_isMustAlias = ::mlir::FieldParser<bool>::parse(odsParser);
        if (::mlir::failed(_result_isMustAlias)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ArgResultAliasAttrV1 parameter 'isMustAlias' which is to be a `bool`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 4; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 4 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_argTupleIndices));
  assert(::mlir::succeeded(_result_resultIndex));
  assert(::mlir::succeeded(_result_resultTupleIndices));
  assert(::mlir::succeeded(_result_isMustAlias));
  return ArgResultAliasV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_argTupleIndices)),
      int64_t((*_result_resultIndex)),
      ::llvm::ArrayRef<int64_t>((*_result_resultTupleIndices)),
      bool((*_result_isMustAlias)));
}

void ArgResultAliasV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "argTupleIndices = ";
    mlir::hlo::printDimSizes(odsPrinter, getArgTupleIndices());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "resultIndex = ";
    odsPrinter.printStrippedAttrOrType(getResultIndex());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "resultTupleIndices = ";
    mlir::hlo::printDimSizes(odsPrinter, getResultTupleIndices());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "isMustAlias = ";
    odsPrinter.printStrippedAttrOrType(getIsMustAlias());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> ArgResultAliasV1Attr::getArgTupleIndices() const {
  return getImpl()->argTupleIndices;
}

int64_t ArgResultAliasV1Attr::getResultIndex() const {
  return getImpl()->resultIndex;
}

::llvm::ArrayRef<int64_t> ArgResultAliasV1Attr::getResultTupleIndices() const {
  return getImpl()->resultTupleIndices;
}

bool ArgResultAliasV1Attr::getIsMustAlias() const {
  return getImpl()->isMustAlias;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ArgResultAliasV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ArrayV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<mlir::Attribute>>;
  ArrayV1AttrStorage(::llvm::ArrayRef<mlir::Attribute> value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static ArrayV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    value = allocator.copyInto(value);
    return new (allocator.allocate<ArrayV1AttrStorage>()) ArrayV1AttrStorage(value);
  }

  ::llvm::ArrayRef<mlir::Attribute> value;
};
} // namespace detail
LogicalResult ArrayV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, ArrayRef<mlir::Attribute> value) {
  if (!allFromVhlo(value)) return errFn() << "expected array of VHLO attriutes";
  return success();
}
ArrayV1Attr ArrayV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<mlir::Attribute> value) {
  return Base::get(context, value);
}

ArrayV1Attr ArrayV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<mlir::Attribute> value) {
  return Base::getChecked(emitError, context, value);
}

::mlir::Attribute ArrayV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<mlir::Attribute>> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  {
    auto odsCustomLoc = odsParser.getCurrentLocation();
    (void)odsCustomLoc;
    auto odsCustomResult = parseAttributeArray(odsParser,
      ::mlir::detail::unwrapForCustomParse(_result_value));
    if (::mlir::failed(odsCustomResult)) return {};
    if (::mlir::failed(_result_value)) {
      odsParser.emitError(odsCustomLoc, "custom parser failed to parse parameter 'value'");
      return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_value));
  return odsParser.getChecked<ArrayV1Attr>(odsLoc, odsParser.getContext(),
      ::llvm::ArrayRef<mlir::Attribute>((*_result_value)));
}

void ArrayV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  printAttributeArray(odsPrinter,
    getValue());
  odsPrinter << ">";
}

::llvm::ArrayRef<mlir::Attribute> ArrayV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ArrayV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ChannelHandleV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<int64_t, int64_t>;
  ChannelHandleV1AttrStorage(int64_t handle, int64_t type) : handle(handle), type(type) {}

  KeyTy getAsKey() const {
    return KeyTy(handle, type);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (handle == std::get<0>(tblgenKey)) && (type == std::get<1>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static ChannelHandleV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto handle = std::get<0>(tblgenKey);
    auto type = std::get<1>(tblgenKey);
    return new (allocator.allocate<ChannelHandleV1AttrStorage>()) ChannelHandleV1AttrStorage(handle, type);
  }

  int64_t handle;
  int64_t type;
};
} // namespace detail
ChannelHandleV1Attr ChannelHandleV1Attr::get(::mlir::MLIRContext *context, int64_t handle, int64_t type) {
  return Base::get(context, handle, type);
}

::mlir::Attribute ChannelHandleV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<int64_t> _result_handle;
  ::mlir::FailureOr<int64_t> _result_type;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_handle = false;
  bool _seen_type = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_handle && _paramKey == "handle") {
        _seen_handle = true;

        // Parse variable 'handle'
        _result_handle = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_handle)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ChannelHandleAttrV1 parameter 'handle' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_type && _paramKey == "type") {
        _seen_type = true;

        // Parse variable 'type'
        _result_type = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_type)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ChannelHandleAttrV1 parameter 'type' which is to be a `int64_t`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 2; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 2 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_handle));
  assert(::mlir::succeeded(_result_type));
  return ChannelHandleV1Attr::get(odsParser.getContext(),
      int64_t((*_result_handle)),
      int64_t((*_result_type)));
}

void ChannelHandleV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "handle = ";
    odsPrinter.printStrippedAttrOrType(getHandle());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "type = ";
    odsPrinter.printStrippedAttrOrType(getType());
  }
  odsPrinter << ">";
}

int64_t ChannelHandleV1Attr::getHandle() const {
  return getImpl()->handle;
}

int64_t ChannelHandleV1Attr::getType() const {
  return getImpl()->type;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ChannelHandleV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ComparisonDirectionV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::ComparisonDirectionV1>;
  ComparisonDirectionV1AttrStorage(::mlir::vhlo::ComparisonDirectionV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static ComparisonDirectionV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<ComparisonDirectionV1AttrStorage>()) ComparisonDirectionV1AttrStorage(value);
  }

  ::mlir::vhlo::ComparisonDirectionV1 value;
};
} // namespace detail
ComparisonDirectionV1Attr ComparisonDirectionV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::ComparisonDirectionV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute ComparisonDirectionV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::ComparisonDirectionV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::ComparisonDirectionV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeComparisonDirectionV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::ComparisonDirectionV1" << " to be one of: " << "EQ" << ", " << "NE" << ", " << "GE" << ", " << "GT" << ", " << "LE" << ", " << "LT")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ComparisonDirectionAttrV1 parameter 'value' which is to be a `::mlir::vhlo::ComparisonDirectionV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return ComparisonDirectionV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::ComparisonDirectionV1((*_result_value)));
}

void ComparisonDirectionV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyComparisonDirectionV1(getValue());
}

::mlir::vhlo::ComparisonDirectionV1 ComparisonDirectionV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ComparisonDirectionV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ComparisonTypeV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::ComparisonTypeV1>;
  ComparisonTypeV1AttrStorage(::mlir::vhlo::ComparisonTypeV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static ComparisonTypeV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<ComparisonTypeV1AttrStorage>()) ComparisonTypeV1AttrStorage(value);
  }

  ::mlir::vhlo::ComparisonTypeV1 value;
};
} // namespace detail
ComparisonTypeV1Attr ComparisonTypeV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::ComparisonTypeV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute ComparisonTypeV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::ComparisonTypeV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::ComparisonTypeV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeComparisonTypeV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::ComparisonTypeV1" << " to be one of: " << "NOTYPE" << ", " << "FLOAT" << ", " << "TOTALORDER" << ", " << "SIGNED" << ", " << "UNSIGNED")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ComparisonTypeAttrV1 parameter 'value' which is to be a `::mlir::vhlo::ComparisonTypeV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return ComparisonTypeV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::ComparisonTypeV1((*_result_value)));
}

void ComparisonTypeV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyComparisonTypeV1(getValue());
}

::mlir::vhlo::ComparisonTypeV1 ComparisonTypeV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ComparisonTypeV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ConvDimensionNumbersV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<int64_t, int64_t, ::llvm::ArrayRef<int64_t>, int64_t, int64_t, ::llvm::ArrayRef<int64_t>, int64_t, int64_t, ::llvm::ArrayRef<int64_t>>;
  ConvDimensionNumbersV1AttrStorage(int64_t inputBatchDimension, int64_t inputFeatureDimension, ::llvm::ArrayRef<int64_t> inputSpatialDimensions, int64_t kernelInputFeatureDimension, int64_t kernelOutputFeatureDimension, ::llvm::ArrayRef<int64_t> kernelSpatialDimensions, int64_t outputBatchDimension, int64_t outputFeatureDimension, ::llvm::ArrayRef<int64_t> outputSpatialDimensions) : inputBatchDimension(inputBatchDimension), inputFeatureDimension(inputFeatureDimension), inputSpatialDimensions(inputSpatialDimensions), kernelInputFeatureDimension(kernelInputFeatureDimension), kernelOutputFeatureDimension(kernelOutputFeatureDimension), kernelSpatialDimensions(kernelSpatialDimensions), outputBatchDimension(outputBatchDimension), outputFeatureDimension(outputFeatureDimension), outputSpatialDimensions(outputSpatialDimensions) {}

  KeyTy getAsKey() const {
    return KeyTy(inputBatchDimension, inputFeatureDimension, inputSpatialDimensions, kernelInputFeatureDimension, kernelOutputFeatureDimension, kernelSpatialDimensions, outputBatchDimension, outputFeatureDimension, outputSpatialDimensions);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (inputBatchDimension == std::get<0>(tblgenKey)) && (inputFeatureDimension == std::get<1>(tblgenKey)) && (inputSpatialDimensions == std::get<2>(tblgenKey)) && (kernelInputFeatureDimension == std::get<3>(tblgenKey)) && (kernelOutputFeatureDimension == std::get<4>(tblgenKey)) && (kernelSpatialDimensions == std::get<5>(tblgenKey)) && (outputBatchDimension == std::get<6>(tblgenKey)) && (outputFeatureDimension == std::get<7>(tblgenKey)) && (outputSpatialDimensions == std::get<8>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey), std::get<4>(tblgenKey), std::get<5>(tblgenKey), std::get<6>(tblgenKey), std::get<7>(tblgenKey), std::get<8>(tblgenKey));
  }

  static ConvDimensionNumbersV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
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
    return new (allocator.allocate<ConvDimensionNumbersV1AttrStorage>()) ConvDimensionNumbersV1AttrStorage(inputBatchDimension, inputFeatureDimension, inputSpatialDimensions, kernelInputFeatureDimension, kernelOutputFeatureDimension, kernelSpatialDimensions, outputBatchDimension, outputFeatureDimension, outputSpatialDimensions);
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
ConvDimensionNumbersV1Attr ConvDimensionNumbersV1Attr::get(::mlir::MLIRContext *context, int64_t inputBatchDimension, int64_t inputFeatureDimension, ::llvm::ArrayRef<int64_t> inputSpatialDimensions, int64_t kernelInputFeatureDimension, int64_t kernelOutputFeatureDimension, ::llvm::ArrayRef<int64_t> kernelSpatialDimensions, int64_t outputBatchDimension, int64_t outputFeatureDimension, ::llvm::ArrayRef<int64_t> outputSpatialDimensions) {
  return Base::get(context, inputBatchDimension, inputFeatureDimension, inputSpatialDimensions, kernelInputFeatureDimension, kernelOutputFeatureDimension, kernelSpatialDimensions, outputBatchDimension, outputFeatureDimension, outputSpatialDimensions);
}

::mlir::Attribute ConvDimensionNumbersV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<int64_t> _result_inputBatchDimension;
  ::mlir::FailureOr<int64_t> _result_inputFeatureDimension;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_inputSpatialDimensions;
  ::mlir::FailureOr<int64_t> _result_kernelInputFeatureDimension;
  ::mlir::FailureOr<int64_t> _result_kernelOutputFeatureDimension;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_kernelSpatialDimensions;
  ::mlir::FailureOr<int64_t> _result_outputBatchDimension;
  ::mlir::FailureOr<int64_t> _result_outputFeatureDimension;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_outputSpatialDimensions;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_inputBatchDimension = false;
  bool _seen_inputFeatureDimension = false;
  bool _seen_inputSpatialDimensions = false;
  bool _seen_kernelInputFeatureDimension = false;
  bool _seen_kernelOutputFeatureDimension = false;
  bool _seen_kernelSpatialDimensions = false;
  bool _seen_outputBatchDimension = false;
  bool _seen_outputFeatureDimension = false;
  bool _seen_outputSpatialDimensions = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_inputBatchDimension && _paramKey == "inputBatchDimension") {
        _seen_inputBatchDimension = true;

        // Parse variable 'inputBatchDimension'
        _result_inputBatchDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_inputBatchDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'inputBatchDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_inputFeatureDimension && _paramKey == "inputFeatureDimension") {
        _seen_inputFeatureDimension = true;

        // Parse variable 'inputFeatureDimension'
        _result_inputFeatureDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_inputFeatureDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'inputFeatureDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_inputSpatialDimensions && _paramKey == "inputSpatialDimensions") {
        _seen_inputSpatialDimensions = true;

        // Parse variable 'inputSpatialDimensions'
        _result_inputSpatialDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_inputSpatialDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'inputSpatialDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_kernelInputFeatureDimension && _paramKey == "kernelInputFeatureDimension") {
        _seen_kernelInputFeatureDimension = true;

        // Parse variable 'kernelInputFeatureDimension'
        _result_kernelInputFeatureDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_kernelInputFeatureDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'kernelInputFeatureDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_kernelOutputFeatureDimension && _paramKey == "kernelOutputFeatureDimension") {
        _seen_kernelOutputFeatureDimension = true;

        // Parse variable 'kernelOutputFeatureDimension'
        _result_kernelOutputFeatureDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_kernelOutputFeatureDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'kernelOutputFeatureDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_kernelSpatialDimensions && _paramKey == "kernelSpatialDimensions") {
        _seen_kernelSpatialDimensions = true;

        // Parse variable 'kernelSpatialDimensions'
        _result_kernelSpatialDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_kernelSpatialDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'kernelSpatialDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_outputBatchDimension && _paramKey == "outputBatchDimension") {
        _seen_outputBatchDimension = true;

        // Parse variable 'outputBatchDimension'
        _result_outputBatchDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_outputBatchDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'outputBatchDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_outputFeatureDimension && _paramKey == "outputFeatureDimension") {
        _seen_outputFeatureDimension = true;

        // Parse variable 'outputFeatureDimension'
        _result_outputFeatureDimension = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_outputFeatureDimension)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'outputFeatureDimension' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_outputSpatialDimensions && _paramKey == "outputSpatialDimensions") {
        _seen_outputSpatialDimensions = true;

        // Parse variable 'outputSpatialDimensions'
        _result_outputSpatialDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_outputSpatialDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ConvDimensionNumbersAttrV1 parameter 'outputSpatialDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 9; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 9 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_inputBatchDimension));
  assert(::mlir::succeeded(_result_inputFeatureDimension));
  assert(::mlir::succeeded(_result_inputSpatialDimensions));
  assert(::mlir::succeeded(_result_kernelInputFeatureDimension));
  assert(::mlir::succeeded(_result_kernelOutputFeatureDimension));
  assert(::mlir::succeeded(_result_kernelSpatialDimensions));
  assert(::mlir::succeeded(_result_outputBatchDimension));
  assert(::mlir::succeeded(_result_outputFeatureDimension));
  assert(::mlir::succeeded(_result_outputSpatialDimensions));
  return ConvDimensionNumbersV1Attr::get(odsParser.getContext(),
      int64_t((*_result_inputBatchDimension)),
      int64_t((*_result_inputFeatureDimension)),
      ::llvm::ArrayRef<int64_t>((*_result_inputSpatialDimensions)),
      int64_t((*_result_kernelInputFeatureDimension)),
      int64_t((*_result_kernelOutputFeatureDimension)),
      ::llvm::ArrayRef<int64_t>((*_result_kernelSpatialDimensions)),
      int64_t((*_result_outputBatchDimension)),
      int64_t((*_result_outputFeatureDimension)),
      ::llvm::ArrayRef<int64_t>((*_result_outputSpatialDimensions)));
}

void ConvDimensionNumbersV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "inputBatchDimension = ";
    odsPrinter.printStrippedAttrOrType(getInputBatchDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "inputFeatureDimension = ";
    odsPrinter.printStrippedAttrOrType(getInputFeatureDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "inputSpatialDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getInputSpatialDimensions());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "kernelInputFeatureDimension = ";
    odsPrinter.printStrippedAttrOrType(getKernelInputFeatureDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "kernelOutputFeatureDimension = ";
    odsPrinter.printStrippedAttrOrType(getKernelOutputFeatureDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "kernelSpatialDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getKernelSpatialDimensions());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "outputBatchDimension = ";
    odsPrinter.printStrippedAttrOrType(getOutputBatchDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "outputFeatureDimension = ";
    odsPrinter.printStrippedAttrOrType(getOutputFeatureDimension());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "outputSpatialDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getOutputSpatialDimensions());
  }
  odsPrinter << ">";
}

int64_t ConvDimensionNumbersV1Attr::getInputBatchDimension() const {
  return getImpl()->inputBatchDimension;
}

int64_t ConvDimensionNumbersV1Attr::getInputFeatureDimension() const {
  return getImpl()->inputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersV1Attr::getInputSpatialDimensions() const {
  return getImpl()->inputSpatialDimensions;
}

int64_t ConvDimensionNumbersV1Attr::getKernelInputFeatureDimension() const {
  return getImpl()->kernelInputFeatureDimension;
}

int64_t ConvDimensionNumbersV1Attr::getKernelOutputFeatureDimension() const {
  return getImpl()->kernelOutputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersV1Attr::getKernelSpatialDimensions() const {
  return getImpl()->kernelSpatialDimensions;
}

int64_t ConvDimensionNumbersV1Attr::getOutputBatchDimension() const {
  return getImpl()->outputBatchDimension;
}

int64_t ConvDimensionNumbersV1Attr::getOutputFeatureDimension() const {
  return getImpl()->outputFeatureDimension;
}

::llvm::ArrayRef<int64_t> ConvDimensionNumbersV1Attr::getOutputSpatialDimensions() const {
  return getImpl()->outputSpatialDimensions;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ConvDimensionNumbersV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct CustomCallApiVersionV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::CustomCallApiVersionV1>;
  CustomCallApiVersionV1AttrStorage(::mlir::vhlo::CustomCallApiVersionV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static CustomCallApiVersionV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<CustomCallApiVersionV1AttrStorage>()) CustomCallApiVersionV1AttrStorage(value);
  }

  ::mlir::vhlo::CustomCallApiVersionV1 value;
};
} // namespace detail
CustomCallApiVersionV1Attr CustomCallApiVersionV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::CustomCallApiVersionV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute CustomCallApiVersionV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::CustomCallApiVersionV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::CustomCallApiVersionV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeCustomCallApiVersionV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::CustomCallApiVersionV1" << " to be one of: " << "API_VERSION_UNSPECIFIED" << ", " << "API_VERSION_ORIGINAL" << ", " << "API_VERSION_STATUS_RETURNING" << ", " << "API_VERSION_STATUS_RETURNING_UNIFIED")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_CustomCallApiVersionAttrV1 parameter 'value' which is to be a `::mlir::vhlo::CustomCallApiVersionV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return CustomCallApiVersionV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::CustomCallApiVersionV1((*_result_value)));
}

void CustomCallApiVersionV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyCustomCallApiVersionV1(getValue());
}

::mlir::vhlo::CustomCallApiVersionV1 CustomCallApiVersionV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::CustomCallApiVersionV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct DenseIntOrFPElementsV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::Type, ::llvm::ArrayRef<char>>;
  DenseIntOrFPElementsV1AttrStorage(::mlir::Type type, ::llvm::ArrayRef<char> raw_data) : type(type), raw_data(raw_data) {}

  KeyTy getAsKey() const {
    return KeyTy(type, raw_data);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (type == std::get<0>(tblgenKey)) && (raw_data == std::get<1>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static DenseIntOrFPElementsV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto type = std::get<0>(tblgenKey);
    auto raw_data = std::get<1>(tblgenKey);
    raw_data = allocator.copyInto(raw_data);
    return new (allocator.allocate<DenseIntOrFPElementsV1AttrStorage>()) DenseIntOrFPElementsV1AttrStorage(type, raw_data);
  }

  ::mlir::Type type;
  ::llvm::ArrayRef<char> raw_data;
};
} // namespace detail
LogicalResult DenseIntOrFPElementsV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, mlir::Type type, ArrayRef<char>) {
  if (!isFromVhlo(type)) errFn() << "expected VHLO type";
  return success();
}
DenseIntOrFPElementsV1Attr DenseIntOrFPElementsV1Attr::get(::mlir::MLIRContext *context, ::mlir::Type type, ::llvm::ArrayRef<char> raw_data) {
  return Base::get(context, type, raw_data);
}

DenseIntOrFPElementsV1Attr DenseIntOrFPElementsV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Type type, ::llvm::ArrayRef<char> raw_data) {
  return Base::getChecked(emitError, context, type, raw_data);
}

::mlir::Type DenseIntOrFPElementsV1Attr::getType() const {
  return getImpl()->type;
}

::llvm::ArrayRef<char> DenseIntOrFPElementsV1Attr::getRawData() const {
  return getImpl()->raw_data;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::DenseIntOrFPElementsV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct DictionaryV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>>>;
  DictionaryV1AttrStorage(::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static DictionaryV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    value = allocator.copyInto(value);
    return new (allocator.allocate<DictionaryV1AttrStorage>()) DictionaryV1AttrStorage(value);
  }

  ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value;
};
} // namespace detail
LogicalResult DictionaryV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn,
    ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value) {
  for (auto & entry : value)
    if (!isFromVhlo(entry.first) || !isFromVhlo(entry.second))
      errFn() << "expected VHLO attribute";
  return success();
}
DictionaryV1Attr DictionaryV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value) {
  return Base::get(context, value);
}

DictionaryV1Attr DictionaryV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> value) {
  return Base::getChecked(emitError, context, value);
}

::mlir::Attribute DictionaryV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<std::pair<mlir::Attribute, mlir::Attribute>>> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  {
    auto odsCustomLoc = odsParser.getCurrentLocation();
    (void)odsCustomLoc;
    auto odsCustomResult = parseAttributeDictionary(odsParser,
      ::mlir::detail::unwrapForCustomParse(_result_value));
    if (::mlir::failed(odsCustomResult)) return {};
    if (::mlir::failed(_result_value)) {
      odsParser.emitError(odsCustomLoc, "custom parser failed to parse parameter 'value'");
      return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_value));
  return odsParser.getChecked<DictionaryV1Attr>(odsLoc, odsParser.getContext(),
      ::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>>((*_result_value)));
}

void DictionaryV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  printAttributeDictionary(odsPrinter,
    getValue());
  odsPrinter << ">";
}

::llvm::ArrayRef<std::pair<mlir::Attribute, mlir::Attribute>> DictionaryV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::DictionaryV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct DotDimensionNumbersV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>>;
  DotDimensionNumbersV1AttrStorage(::llvm::ArrayRef<int64_t> lhsBatchingDimensions, ::llvm::ArrayRef<int64_t> rhsBatchingDimensions, ::llvm::ArrayRef<int64_t> lhsContractingDimensions, ::llvm::ArrayRef<int64_t> rhsContractingDimensions) : lhsBatchingDimensions(lhsBatchingDimensions), rhsBatchingDimensions(rhsBatchingDimensions), lhsContractingDimensions(lhsContractingDimensions), rhsContractingDimensions(rhsContractingDimensions) {}

  KeyTy getAsKey() const {
    return KeyTy(lhsBatchingDimensions, rhsBatchingDimensions, lhsContractingDimensions, rhsContractingDimensions);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (lhsBatchingDimensions == std::get<0>(tblgenKey)) && (rhsBatchingDimensions == std::get<1>(tblgenKey)) && (lhsContractingDimensions == std::get<2>(tblgenKey)) && (rhsContractingDimensions == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static DotDimensionNumbersV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto lhsBatchingDimensions = std::get<0>(tblgenKey);
    auto rhsBatchingDimensions = std::get<1>(tblgenKey);
    auto lhsContractingDimensions = std::get<2>(tblgenKey);
    auto rhsContractingDimensions = std::get<3>(tblgenKey);
    lhsBatchingDimensions = allocator.copyInto(lhsBatchingDimensions);
    rhsBatchingDimensions = allocator.copyInto(rhsBatchingDimensions);
    lhsContractingDimensions = allocator.copyInto(lhsContractingDimensions);
    rhsContractingDimensions = allocator.copyInto(rhsContractingDimensions);
    return new (allocator.allocate<DotDimensionNumbersV1AttrStorage>()) DotDimensionNumbersV1AttrStorage(lhsBatchingDimensions, rhsBatchingDimensions, lhsContractingDimensions, rhsContractingDimensions);
  }

  ::llvm::ArrayRef<int64_t> lhsBatchingDimensions;
  ::llvm::ArrayRef<int64_t> rhsBatchingDimensions;
  ::llvm::ArrayRef<int64_t> lhsContractingDimensions;
  ::llvm::ArrayRef<int64_t> rhsContractingDimensions;
};
} // namespace detail
DotDimensionNumbersV1Attr DotDimensionNumbersV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> lhsBatchingDimensions, ::llvm::ArrayRef<int64_t> rhsBatchingDimensions, ::llvm::ArrayRef<int64_t> lhsContractingDimensions, ::llvm::ArrayRef<int64_t> rhsContractingDimensions) {
  return Base::get(context, lhsBatchingDimensions, rhsBatchingDimensions, lhsContractingDimensions, rhsContractingDimensions);
}

::mlir::Attribute DotDimensionNumbersV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_lhsBatchingDimensions;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_rhsBatchingDimensions;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_lhsContractingDimensions;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_rhsContractingDimensions;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_lhsBatchingDimensions = false;
  bool _seen_rhsBatchingDimensions = false;
  bool _seen_lhsContractingDimensions = false;
  bool _seen_rhsContractingDimensions = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_lhsBatchingDimensions && _paramKey == "lhsBatchingDimensions") {
        _seen_lhsBatchingDimensions = true;

        // Parse variable 'lhsBatchingDimensions'
        _result_lhsBatchingDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_lhsBatchingDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_DotDimensionNumbersAttrV1 parameter 'lhsBatchingDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_rhsBatchingDimensions && _paramKey == "rhsBatchingDimensions") {
        _seen_rhsBatchingDimensions = true;

        // Parse variable 'rhsBatchingDimensions'
        _result_rhsBatchingDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_rhsBatchingDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_DotDimensionNumbersAttrV1 parameter 'rhsBatchingDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_lhsContractingDimensions && _paramKey == "lhsContractingDimensions") {
        _seen_lhsContractingDimensions = true;

        // Parse variable 'lhsContractingDimensions'
        _result_lhsContractingDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_lhsContractingDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_DotDimensionNumbersAttrV1 parameter 'lhsContractingDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_rhsContractingDimensions && _paramKey == "rhsContractingDimensions") {
        _seen_rhsContractingDimensions = true;

        // Parse variable 'rhsContractingDimensions'
        _result_rhsContractingDimensions = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_rhsContractingDimensions)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_DotDimensionNumbersAttrV1 parameter 'rhsContractingDimensions' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 4; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 4 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_lhsBatchingDimensions));
  assert(::mlir::succeeded(_result_rhsBatchingDimensions));
  assert(::mlir::succeeded(_result_lhsContractingDimensions));
  assert(::mlir::succeeded(_result_rhsContractingDimensions));
  return DotDimensionNumbersV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_lhsBatchingDimensions)),
      ::llvm::ArrayRef<int64_t>((*_result_rhsBatchingDimensions)),
      ::llvm::ArrayRef<int64_t>((*_result_lhsContractingDimensions)),
      ::llvm::ArrayRef<int64_t>((*_result_rhsContractingDimensions)));
}

void DotDimensionNumbersV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "lhsBatchingDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getLhsBatchingDimensions());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "rhsBatchingDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getRhsBatchingDimensions());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "lhsContractingDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getLhsContractingDimensions());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "rhsContractingDimensions = ";
    mlir::hlo::printDimSizes(odsPrinter, getRhsContractingDimensions());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersV1Attr::getLhsBatchingDimensions() const {
  return getImpl()->lhsBatchingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersV1Attr::getRhsBatchingDimensions() const {
  return getImpl()->rhsBatchingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersV1Attr::getLhsContractingDimensions() const {
  return getImpl()->lhsContractingDimensions;
}

::llvm::ArrayRef<int64_t> DotDimensionNumbersV1Attr::getRhsContractingDimensions() const {
  return getImpl()->rhsContractingDimensions;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::DotDimensionNumbersV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct FftTypeV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::FftTypeV1>;
  FftTypeV1AttrStorage(::mlir::vhlo::FftTypeV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static FftTypeV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<FftTypeV1AttrStorage>()) FftTypeV1AttrStorage(value);
  }

  ::mlir::vhlo::FftTypeV1 value;
};
} // namespace detail
FftTypeV1Attr FftTypeV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::FftTypeV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute FftTypeV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::FftTypeV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::FftTypeV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeFftTypeV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::FftTypeV1" << " to be one of: " << "FFT" << ", " << "IFFT" << ", " << "RFFT" << ", " << "IRFFT")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_FftTypeAttrV1 parameter 'value' which is to be a `::mlir::vhlo::FftTypeV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return FftTypeV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::FftTypeV1((*_result_value)));
}

void FftTypeV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyFftTypeV1(getValue());
}

::mlir::vhlo::FftTypeV1 FftTypeV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::FftTypeV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct FlatSymbolRefV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::Attribute>;
  FlatSymbolRefV1AttrStorage(::mlir::Attribute root_reference) : root_reference(root_reference) {}

  KeyTy getAsKey() const {
    return KeyTy(root_reference);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (root_reference == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static FlatSymbolRefV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto root_reference = std::get<0>(tblgenKey);
    return new (allocator.allocate<FlatSymbolRefV1AttrStorage>()) FlatSymbolRefV1AttrStorage(root_reference);
  }

  ::mlir::Attribute root_reference;
};
} // namespace detail
LogicalResult FlatSymbolRefV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, mlir::Attribute rootReference) {
  if (!isFromVhlo(rootReference)) return errFn() << "expected VHLO attribute";
  return success();
}
FlatSymbolRefV1Attr FlatSymbolRefV1Attr::get(::mlir::MLIRContext *context, ::mlir::Attribute root_reference) {
  return Base::get(context, root_reference);
}

FlatSymbolRefV1Attr FlatSymbolRefV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Attribute root_reference) {
  return Base::getChecked(emitError, context, root_reference);
}

::mlir::Attribute FlatSymbolRefV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::Attribute> _result_root_reference;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'root_reference'
  _result_root_reference = ::mlir::FieldParser<::mlir::Attribute>::parse(odsParser);
  if (::mlir::failed(_result_root_reference)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_FlatSymbolRefAttrV1 parameter 'root_reference' which is to be a `::mlir::Attribute`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_root_reference));
  return odsParser.getChecked<FlatSymbolRefV1Attr>(odsLoc, odsParser.getContext(),
      ::mlir::Attribute((*_result_root_reference)));
}

void FlatSymbolRefV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter.printStrippedAttrOrType(getRootReference());
  odsPrinter << ">";
}

::mlir::Attribute FlatSymbolRefV1Attr::getRootReference() const {
  return getImpl()->root_reference;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::FlatSymbolRefV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct FloatV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<mlir::Type, ::llvm::APFloat>;
  FloatV1AttrStorage(mlir::Type type, ::llvm::APFloat value) : type(type), value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(type, value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (type == std::get<0>(tblgenKey)) && (value.bitwiseIsEqual(std::get<1>(tblgenKey)));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static FloatV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto type = std::get<0>(tblgenKey);
    auto value = std::get<1>(tblgenKey);
    return new (allocator.allocate<FloatV1AttrStorage>()) FloatV1AttrStorage(type, value);
  }

  mlir::Type type;
  ::llvm::APFloat value;
};
} // namespace detail
LogicalResult FloatV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, mlir::Type type, APFloat value) {
  if (!isFromVhlo(type)) return errFn() << "expected VHLO type";
  return success();
}
FloatV1Attr FloatV1Attr::get(::mlir::MLIRContext *context, mlir::Type type, ::llvm::APFloat value) {
  return Base::get(context, type, value);
}

FloatV1Attr FloatV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, mlir::Type type, ::llvm::APFloat value) {
  return Base::getChecked(emitError, context, type, value);
}

::mlir::Attribute FloatV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<mlir::Type> _result_type;
  ::mlir::FailureOr<::llvm::APFloat> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'value'
  _result_value = 
      [&]() -> FailureOr<llvm::APFloat> {
        double value;
        if (failed(odsParser.parseFloat(value))) {
          return failure();
        }
        return APFloat(value);
      }()
    ;
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_FloatAttrV1 parameter 'value' which is to be a `::llvm::APFloat`");
    return {};
  }
  // Parse literal ':'
  if (odsParser.parseColon()) return {};

  // Parse variable 'type'
  _result_type = ::mlir::FieldParser<mlir::Type>::parse(odsParser);
  if (::mlir::failed(_result_type)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_FloatAttrV1 parameter 'type' which is to be a `mlir::Type`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_type));
  assert(::mlir::succeeded(_result_value));
  return odsParser.getChecked<FloatV1Attr>(odsLoc, odsParser.getContext(),
      mlir::Type((*_result_type)),
      ::llvm::APFloat((*_result_value)));
}

void FloatV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter.printFloat(getValue());;
  odsPrinter << ' ' << ":";
  odsPrinter << ' ';
  odsPrinter.printStrippedAttrOrType(getType());
  odsPrinter << ">";
}

mlir::Type FloatV1Attr::getType() const {
  return getImpl()->type;
}

::llvm::APFloat FloatV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::FloatV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct GatherDimensionNumbersV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, int64_t>;
  GatherDimensionNumbersV1AttrStorage(::llvm::ArrayRef<int64_t> offsetDims, ::llvm::ArrayRef<int64_t> collapsedSliceDims, ::llvm::ArrayRef<int64_t> startIndexMap, int64_t indexVectorDim) : offsetDims(offsetDims), collapsedSliceDims(collapsedSliceDims), startIndexMap(startIndexMap), indexVectorDim(indexVectorDim) {}

  KeyTy getAsKey() const {
    return KeyTy(offsetDims, collapsedSliceDims, startIndexMap, indexVectorDim);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (offsetDims == std::get<0>(tblgenKey)) && (collapsedSliceDims == std::get<1>(tblgenKey)) && (startIndexMap == std::get<2>(tblgenKey)) && (indexVectorDim == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static GatherDimensionNumbersV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto offsetDims = std::get<0>(tblgenKey);
    auto collapsedSliceDims = std::get<1>(tblgenKey);
    auto startIndexMap = std::get<2>(tblgenKey);
    auto indexVectorDim = std::get<3>(tblgenKey);
    offsetDims = allocator.copyInto(offsetDims);
    collapsedSliceDims = allocator.copyInto(collapsedSliceDims);
    startIndexMap = allocator.copyInto(startIndexMap);
    return new (allocator.allocate<GatherDimensionNumbersV1AttrStorage>()) GatherDimensionNumbersV1AttrStorage(offsetDims, collapsedSliceDims, startIndexMap, indexVectorDim);
  }

  ::llvm::ArrayRef<int64_t> offsetDims;
  ::llvm::ArrayRef<int64_t> collapsedSliceDims;
  ::llvm::ArrayRef<int64_t> startIndexMap;
  int64_t indexVectorDim;
};
} // namespace detail
GatherDimensionNumbersV1Attr GatherDimensionNumbersV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> offsetDims, ::llvm::ArrayRef<int64_t> collapsedSliceDims, ::llvm::ArrayRef<int64_t> startIndexMap, int64_t indexVectorDim) {
  return Base::get(context, offsetDims, collapsedSliceDims, startIndexMap, indexVectorDim);
}

::mlir::Attribute GatherDimensionNumbersV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_offsetDims;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_collapsedSliceDims;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_startIndexMap;
  ::mlir::FailureOr<int64_t> _result_indexVectorDim;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_offsetDims = false;
  bool _seen_collapsedSliceDims = false;
  bool _seen_startIndexMap = false;
  bool _seen_indexVectorDim = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_offsetDims && _paramKey == "offsetDims") {
        _seen_offsetDims = true;

        // Parse variable 'offsetDims'
        _result_offsetDims = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_offsetDims)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_GatherDimensionNumbersAttrV1 parameter 'offsetDims' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_collapsedSliceDims && _paramKey == "collapsedSliceDims") {
        _seen_collapsedSliceDims = true;

        // Parse variable 'collapsedSliceDims'
        _result_collapsedSliceDims = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_collapsedSliceDims)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_GatherDimensionNumbersAttrV1 parameter 'collapsedSliceDims' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_startIndexMap && _paramKey == "startIndexMap") {
        _seen_startIndexMap = true;

        // Parse variable 'startIndexMap'
        _result_startIndexMap = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_startIndexMap)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_GatherDimensionNumbersAttrV1 parameter 'startIndexMap' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_indexVectorDim && _paramKey == "indexVectorDim") {
        _seen_indexVectorDim = true;

        // Parse variable 'indexVectorDim'
        _result_indexVectorDim = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_indexVectorDim)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_GatherDimensionNumbersAttrV1 parameter 'indexVectorDim' which is to be a `int64_t`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 4; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 4 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_offsetDims));
  assert(::mlir::succeeded(_result_collapsedSliceDims));
  assert(::mlir::succeeded(_result_startIndexMap));
  assert(::mlir::succeeded(_result_indexVectorDim));
  return GatherDimensionNumbersV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_offsetDims)),
      ::llvm::ArrayRef<int64_t>((*_result_collapsedSliceDims)),
      ::llvm::ArrayRef<int64_t>((*_result_startIndexMap)),
      int64_t((*_result_indexVectorDim)));
}

void GatherDimensionNumbersV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "offsetDims = ";
    mlir::hlo::printDimSizes(odsPrinter, getOffsetDims());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "collapsedSliceDims = ";
    mlir::hlo::printDimSizes(odsPrinter, getCollapsedSliceDims());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "startIndexMap = ";
    mlir::hlo::printDimSizes(odsPrinter, getStartIndexMap());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "indexVectorDim = ";
    odsPrinter.printStrippedAttrOrType(getIndexVectorDim());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersV1Attr::getOffsetDims() const {
  return getImpl()->offsetDims;
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersV1Attr::getCollapsedSliceDims() const {
  return getImpl()->collapsedSliceDims;
}

::llvm::ArrayRef<int64_t> GatherDimensionNumbersV1Attr::getStartIndexMap() const {
  return getImpl()->startIndexMap;
}

int64_t GatherDimensionNumbersV1Attr::getIndexVectorDim() const {
  return getImpl()->indexVectorDim;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::GatherDimensionNumbersV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct IntegerV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<mlir::Type, APInt>;
  IntegerV1AttrStorage(mlir::Type type, APInt value) : type(type), value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(type, value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (type == std::get<0>(tblgenKey)) && (value == std::get<1>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey));
  }

  static IntegerV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto type = std::get<0>(tblgenKey);
    auto value = std::get<1>(tblgenKey);
    return new (allocator.allocate<IntegerV1AttrStorage>()) IntegerV1AttrStorage(type, value);
  }

  mlir::Type type;
  APInt value;
};
} // namespace detail
LogicalResult IntegerV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, mlir::Type type, APInt value) {
  if (!isFromVhlo(type)) return errFn() << "expected VHLO type";
  return success();
}
IntegerV1Attr IntegerV1Attr::get(::mlir::MLIRContext *context, mlir::Type type, APInt value) {
  return Base::get(context, type, value);
}

IntegerV1Attr IntegerV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, mlir::Type type, APInt value) {
  return Base::getChecked(emitError, context, type, value);
}

mlir::Type IntegerV1Attr::getType() const {
  return getImpl()->type;
}

APInt IntegerV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct OutputOperandAliasV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, int64_t, ::llvm::ArrayRef<int64_t>>;
  OutputOperandAliasV1AttrStorage(::llvm::ArrayRef<int64_t> outputTupleIndices, int64_t operandIndex, ::llvm::ArrayRef<int64_t> operandTupleIndices) : outputTupleIndices(outputTupleIndices), operandIndex(operandIndex), operandTupleIndices(operandTupleIndices) {}

  KeyTy getAsKey() const {
    return KeyTy(outputTupleIndices, operandIndex, operandTupleIndices);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (outputTupleIndices == std::get<0>(tblgenKey)) && (operandIndex == std::get<1>(tblgenKey)) && (operandTupleIndices == std::get<2>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey));
  }

  static OutputOperandAliasV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto outputTupleIndices = std::get<0>(tblgenKey);
    auto operandIndex = std::get<1>(tblgenKey);
    auto operandTupleIndices = std::get<2>(tblgenKey);
    outputTupleIndices = allocator.copyInto(outputTupleIndices);
    operandTupleIndices = allocator.copyInto(operandTupleIndices);
    return new (allocator.allocate<OutputOperandAliasV1AttrStorage>()) OutputOperandAliasV1AttrStorage(outputTupleIndices, operandIndex, operandTupleIndices);
  }

  ::llvm::ArrayRef<int64_t> outputTupleIndices;
  int64_t operandIndex;
  ::llvm::ArrayRef<int64_t> operandTupleIndices;
};
} // namespace detail
OutputOperandAliasV1Attr OutputOperandAliasV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> outputTupleIndices, int64_t operandIndex, ::llvm::ArrayRef<int64_t> operandTupleIndices) {
  return Base::get(context, outputTupleIndices, operandIndex, operandTupleIndices);
}

::mlir::Attribute OutputOperandAliasV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_outputTupleIndices;
  ::mlir::FailureOr<int64_t> _result_operandIndex;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_operandTupleIndices;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_outputTupleIndices = false;
  bool _seen_operandIndex = false;
  bool _seen_operandTupleIndices = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_outputTupleIndices && _paramKey == "outputTupleIndices") {
        _seen_outputTupleIndices = true;

        // Parse variable 'outputTupleIndices'
        _result_outputTupleIndices = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_outputTupleIndices)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_OutputOperandAliasAttrV1 parameter 'outputTupleIndices' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_operandIndex && _paramKey == "operandIndex") {
        _seen_operandIndex = true;

        // Parse variable 'operandIndex'
        _result_operandIndex = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_operandIndex)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_OutputOperandAliasAttrV1 parameter 'operandIndex' which is to be a `int64_t`");
          return {};
        }
      } else if (!_seen_operandTupleIndices && _paramKey == "operandTupleIndices") {
        _seen_operandTupleIndices = true;

        // Parse variable 'operandTupleIndices'
        _result_operandTupleIndices = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_operandTupleIndices)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_OutputOperandAliasAttrV1 parameter 'operandTupleIndices' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 3; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 3 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_outputTupleIndices));
  assert(::mlir::succeeded(_result_operandIndex));
  assert(::mlir::succeeded(_result_operandTupleIndices));
  return OutputOperandAliasV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_outputTupleIndices)),
      int64_t((*_result_operandIndex)),
      ::llvm::ArrayRef<int64_t>((*_result_operandTupleIndices)));
}

void OutputOperandAliasV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "outputTupleIndices = ";
    mlir::hlo::printDimSizes(odsPrinter, getOutputTupleIndices());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "operandIndex = ";
    odsPrinter.printStrippedAttrOrType(getOperandIndex());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "operandTupleIndices = ";
    mlir::hlo::printDimSizes(odsPrinter, getOperandTupleIndices());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> OutputOperandAliasV1Attr::getOutputTupleIndices() const {
  return getImpl()->outputTupleIndices;
}

int64_t OutputOperandAliasV1Attr::getOperandIndex() const {
  return getImpl()->operandIndex;
}

::llvm::ArrayRef<int64_t> OutputOperandAliasV1Attr::getOperandTupleIndices() const {
  return getImpl()->operandTupleIndices;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::OutputOperandAliasV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct PrecisionV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::PrecisionV1>;
  PrecisionV1AttrStorage(::mlir::vhlo::PrecisionV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static PrecisionV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<PrecisionV1AttrStorage>()) PrecisionV1AttrStorage(value);
  }

  ::mlir::vhlo::PrecisionV1 value;
};
} // namespace detail
PrecisionV1Attr PrecisionV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::PrecisionV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute PrecisionV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::PrecisionV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::PrecisionV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizePrecisionV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::PrecisionV1" << " to be one of: " << "DEFAULT" << ", " << "HIGH" << ", " << "HIGHEST")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_PrecisionAttrV1 parameter 'value' which is to be a `::mlir::vhlo::PrecisionV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return PrecisionV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::PrecisionV1((*_result_value)));
}

void PrecisionV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyPrecisionV1(getValue());
}

::mlir::vhlo::PrecisionV1 PrecisionV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::PrecisionV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct RngAlgorithmV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::RngAlgorithmV1>;
  RngAlgorithmV1AttrStorage(::mlir::vhlo::RngAlgorithmV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static RngAlgorithmV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<RngAlgorithmV1AttrStorage>()) RngAlgorithmV1AttrStorage(value);
  }

  ::mlir::vhlo::RngAlgorithmV1 value;
};
} // namespace detail
RngAlgorithmV1Attr RngAlgorithmV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::RngAlgorithmV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute RngAlgorithmV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::RngAlgorithmV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::RngAlgorithmV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeRngAlgorithmV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::RngAlgorithmV1" << " to be one of: " << "DEFAULT" << ", " << "THREE_FRY" << ", " << "PHILOX")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_RngAlgorithmAttrV1 parameter 'value' which is to be a `::mlir::vhlo::RngAlgorithmV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return RngAlgorithmV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::RngAlgorithmV1((*_result_value)));
}

void RngAlgorithmV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyRngAlgorithmV1(getValue());
}

::mlir::vhlo::RngAlgorithmV1 RngAlgorithmV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::RngAlgorithmV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct RngDistributionV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::RngDistributionV1>;
  RngDistributionV1AttrStorage(::mlir::vhlo::RngDistributionV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static RngDistributionV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<RngDistributionV1AttrStorage>()) RngDistributionV1AttrStorage(value);
  }

  ::mlir::vhlo::RngDistributionV1 value;
};
} // namespace detail
RngDistributionV1Attr RngDistributionV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::RngDistributionV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute RngDistributionV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::RngDistributionV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::RngDistributionV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeRngDistributionV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::RngDistributionV1" << " to be one of: " << "UNIFORM" << ", " << "NORMAL")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_RngDistributionAttrV1 parameter 'value' which is to be a `::mlir::vhlo::RngDistributionV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return RngDistributionV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::RngDistributionV1((*_result_value)));
}

void RngDistributionV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyRngDistributionV1(getValue());
}

::mlir::vhlo::RngDistributionV1 RngDistributionV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::RngDistributionV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct ScatterDimensionNumbersV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, ::llvm::ArrayRef<int64_t>, int64_t>;
  ScatterDimensionNumbersV1AttrStorage(::llvm::ArrayRef<int64_t> updateWindowDims, ::llvm::ArrayRef<int64_t> insertedWindowDims, ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims, int64_t indexVectorDim) : updateWindowDims(updateWindowDims), insertedWindowDims(insertedWindowDims), scatterDimsToOperandDims(scatterDimsToOperandDims), indexVectorDim(indexVectorDim) {}

  KeyTy getAsKey() const {
    return KeyTy(updateWindowDims, insertedWindowDims, scatterDimsToOperandDims, indexVectorDim);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (updateWindowDims == std::get<0>(tblgenKey)) && (insertedWindowDims == std::get<1>(tblgenKey)) && (scatterDimsToOperandDims == std::get<2>(tblgenKey)) && (indexVectorDim == std::get<3>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey));
  }

  static ScatterDimensionNumbersV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto updateWindowDims = std::get<0>(tblgenKey);
    auto insertedWindowDims = std::get<1>(tblgenKey);
    auto scatterDimsToOperandDims = std::get<2>(tblgenKey);
    auto indexVectorDim = std::get<3>(tblgenKey);
    updateWindowDims = allocator.copyInto(updateWindowDims);
    insertedWindowDims = allocator.copyInto(insertedWindowDims);
    scatterDimsToOperandDims = allocator.copyInto(scatterDimsToOperandDims);
    return new (allocator.allocate<ScatterDimensionNumbersV1AttrStorage>()) ScatterDimensionNumbersV1AttrStorage(updateWindowDims, insertedWindowDims, scatterDimsToOperandDims, indexVectorDim);
  }

  ::llvm::ArrayRef<int64_t> updateWindowDims;
  ::llvm::ArrayRef<int64_t> insertedWindowDims;
  ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims;
  int64_t indexVectorDim;
};
} // namespace detail
ScatterDimensionNumbersV1Attr ScatterDimensionNumbersV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> updateWindowDims, ::llvm::ArrayRef<int64_t> insertedWindowDims, ::llvm::ArrayRef<int64_t> scatterDimsToOperandDims, int64_t indexVectorDim) {
  return Base::get(context, updateWindowDims, insertedWindowDims, scatterDimsToOperandDims, indexVectorDim);
}

::mlir::Attribute ScatterDimensionNumbersV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_updateWindowDims;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_insertedWindowDims;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_scatterDimsToOperandDims;
  ::mlir::FailureOr<int64_t> _result_indexVectorDim;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_updateWindowDims = false;
  bool _seen_insertedWindowDims = false;
  bool _seen_scatterDimsToOperandDims = false;
  bool _seen_indexVectorDim = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_updateWindowDims && _paramKey == "updateWindowDims") {
        _seen_updateWindowDims = true;

        // Parse variable 'updateWindowDims'
        _result_updateWindowDims = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_updateWindowDims)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ScatterDimensionNumbersAttrV1 parameter 'updateWindowDims' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_insertedWindowDims && _paramKey == "insertedWindowDims") {
        _seen_insertedWindowDims = true;

        // Parse variable 'insertedWindowDims'
        _result_insertedWindowDims = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_insertedWindowDims)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ScatterDimensionNumbersAttrV1 parameter 'insertedWindowDims' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_scatterDimsToOperandDims && _paramKey == "scatterDimsToOperandDims") {
        _seen_scatterDimsToOperandDims = true;

        // Parse variable 'scatterDimsToOperandDims'
        _result_scatterDimsToOperandDims = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_scatterDimsToOperandDims)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ScatterDimensionNumbersAttrV1 parameter 'scatterDimsToOperandDims' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else if (!_seen_indexVectorDim && _paramKey == "indexVectorDim") {
        _seen_indexVectorDim = true;

        // Parse variable 'indexVectorDim'
        _result_indexVectorDim = ::mlir::FieldParser<int64_t>::parse(odsParser);
        if (::mlir::failed(_result_indexVectorDim)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_ScatterDimensionNumbersAttrV1 parameter 'indexVectorDim' which is to be a `int64_t`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 4; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 4 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_updateWindowDims));
  assert(::mlir::succeeded(_result_insertedWindowDims));
  assert(::mlir::succeeded(_result_scatterDimsToOperandDims));
  assert(::mlir::succeeded(_result_indexVectorDim));
  return ScatterDimensionNumbersV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_updateWindowDims)),
      ::llvm::ArrayRef<int64_t>((*_result_insertedWindowDims)),
      ::llvm::ArrayRef<int64_t>((*_result_scatterDimsToOperandDims)),
      int64_t((*_result_indexVectorDim)));
}

void ScatterDimensionNumbersV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "updateWindowDims = ";
    mlir::hlo::printDimSizes(odsPrinter, getUpdateWindowDims());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "insertedWindowDims = ";
    mlir::hlo::printDimSizes(odsPrinter, getInsertedWindowDims());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "scatterDimsToOperandDims = ";
    mlir::hlo::printDimSizes(odsPrinter, getScatterDimsToOperandDims());
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "indexVectorDim = ";
    odsPrinter.printStrippedAttrOrType(getIndexVectorDim());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersV1Attr::getUpdateWindowDims() const {
  return getImpl()->updateWindowDims;
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersV1Attr::getInsertedWindowDims() const {
  return getImpl()->insertedWindowDims;
}

::llvm::ArrayRef<int64_t> ScatterDimensionNumbersV1Attr::getScatterDimsToOperandDims() const {
  return getImpl()->scatterDimsToOperandDims;
}

int64_t ScatterDimensionNumbersV1Attr::getIndexVectorDim() const {
  return getImpl()->indexVectorDim;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::ScatterDimensionNumbersV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct StringV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::StringRef>;
  StringV1AttrStorage(::llvm::StringRef value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static StringV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    value = allocator.copyInto(value);
    return new (allocator.allocate<StringV1AttrStorage>()) StringV1AttrStorage(value);
  }

  ::llvm::StringRef value;
};
} // namespace detail
StringV1Attr StringV1Attr::get(::mlir::MLIRContext *context, ::llvm::StringRef value) {
  return Base::get(context, value);
}

::mlir::Attribute StringV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<std::string> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'value'
  _result_value = ::mlir::FieldParser<std::string>::parse(odsParser);
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_StringAttrV1 parameter 'value' which is to be a `::llvm::StringRef`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_value));
  return StringV1Attr::get(odsParser.getContext(),
      ::llvm::StringRef((*_result_value)));
}

void StringV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter << '"' << getValue() << '"';;
  odsPrinter << ">";
}

::llvm::StringRef StringV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::StringV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct TransposeV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::vhlo::TransposeV1>;
  TransposeV1AttrStorage(::mlir::vhlo::TransposeV1 value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static TransposeV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<TransposeV1AttrStorage>()) TransposeV1AttrStorage(value);
  }

  ::mlir::vhlo::TransposeV1 value;
};
} // namespace detail
TransposeV1Attr TransposeV1Attr::get(::mlir::MLIRContext *context, ::mlir::vhlo::TransposeV1 value) {
  return Base::get(context, value);
}

::mlir::Attribute TransposeV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::vhlo::TransposeV1> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::vhlo::TransposeV1> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::vhlo::symbolizeTransposeV1(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::vhlo::TransposeV1" << " to be one of: " << "TRANSPOSE_INVALID" << ", " << "NO_TRANSPOSE" << ", " << "TRANSPOSE" << ", " << "ADJOINT")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_TransposeAttrV1 parameter 'value' which is to be a `::mlir::vhlo::TransposeV1`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return TransposeV1Attr::get(odsParser.getContext(),
      ::mlir::vhlo::TransposeV1((*_result_value)));
}

void TransposeV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyTransposeV1(getValue());
}

::mlir::vhlo::TransposeV1 TransposeV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::TransposeV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct TypeV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::Type>;
  TypeV1AttrStorage(::mlir::Type value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static TypeV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<TypeV1AttrStorage>()) TypeV1AttrStorage(value);
  }

  ::mlir::Type value;
};
} // namespace detail
LogicalResult TypeV1Attr::verify(
    llvm::function_ref<mlir::InFlightDiagnostic ()> errFn, mlir::Type value) {
  if (!isFromVhlo(value)) return errFn() << "expected VHLO type";
  return success();
}
TypeV1Attr TypeV1Attr::get(::mlir::MLIRContext *context, ::mlir::Type value) {
  return Base::get(context, value);
}

TypeV1Attr TypeV1Attr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Type value) {
  return Base::getChecked(emitError, context, value);
}

::mlir::Attribute TypeV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::Type> _result_value;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'value'
  _result_value = ::mlir::FieldParser<::mlir::Type>::parse(odsParser);
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_TypeAttrV1 parameter 'value' which is to be a `::mlir::Type`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_value));
  return odsParser.getChecked<TypeV1Attr>(odsLoc, odsParser.getContext(),
      ::mlir::Type((*_result_value)));
}

void TypeV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter.printStrippedAttrOrType(getValue());
  odsPrinter << ">";
}

::mlir::Type TypeV1Attr::getValue() const {
  return getImpl()->value;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::TypeV1Attr)
namespace mlir {
namespace vhlo {
namespace detail {
struct TypeExtensionsV1AttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<int64_t>>;
  TypeExtensionsV1AttrStorage(::llvm::ArrayRef<int64_t> bounds) : bounds(bounds) {}

  KeyTy getAsKey() const {
    return KeyTy(bounds);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (bounds == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static TypeExtensionsV1AttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto bounds = std::get<0>(tblgenKey);
    bounds = allocator.copyInto(bounds);
    return new (allocator.allocate<TypeExtensionsV1AttrStorage>()) TypeExtensionsV1AttrStorage(bounds);
  }

  ::llvm::ArrayRef<int64_t> bounds;
};
} // namespace detail
TypeExtensionsV1Attr TypeExtensionsV1Attr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> bounds) {
  return Base::get(context, bounds);
}

::mlir::Attribute TypeExtensionsV1Attr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::llvm::SmallVector<int64_t>> _result_bounds;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_bounds = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_bounds && _paramKey == "bounds") {
        _seen_bounds = true;

        // Parse variable 'bounds'
        _result_bounds = mlir::hlo::parseDimSizes(odsParser);
        if (::mlir::failed(_result_bounds)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse VHLO_TypeExtensionsAttrV1 parameter 'bounds' which is to be a `::llvm::ArrayRef<int64_t>`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 1; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 1 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_bounds));
  return TypeExtensionsV1Attr::get(odsParser.getContext(),
      ::llvm::ArrayRef<int64_t>((*_result_bounds)));
}

void TypeExtensionsV1Attr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "bounds = ";
    mlir::hlo::printDimSizes(odsPrinter, getBounds());
  }
  odsPrinter << ">";
}

::llvm::ArrayRef<int64_t> TypeExtensionsV1Attr::getBounds() const {
  return getImpl()->bounds;
}

} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::TypeExtensionsV1Attr)
namespace mlir {
namespace vhlo {
} // namespace vhlo
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::vhlo::UnitV1Attr)

#endif  // GET_ATTRDEF_CLASSES

