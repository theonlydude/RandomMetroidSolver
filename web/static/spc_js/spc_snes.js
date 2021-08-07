var Module;
if (!Module) Module = (typeof Module !== "undefined" ? Module : null) || {};
var moduleOverrides = {};
for (var key in Module) {
    if (Module.hasOwnProperty(key)) {
        moduleOverrides[key] = Module[key];
    }
}
var ENVIRONMENT_IS_NODE = typeof process === "object" && typeof require === "function";
var ENVIRONMENT_IS_WEB = typeof window === "object";
var ENVIRONMENT_IS_WORKER = typeof importScripts === "function";
var ENVIRONMENT_IS_SHELL = !ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_NODE && !ENVIRONMENT_IS_WORKER;
if (ENVIRONMENT_IS_NODE) {
    if (!Module["print"])
        Module["print"] = function print(x) {
            process["stdout"].write(x + "\n");
        };
    if (!Module["printErr"])
        Module["printErr"] = function printErr(x) {
            process["stderr"].write(x + "\n");
        };
    var nodeFS = require("fs");
    var nodePath = require("path");
    Module["read"] = function read(filename, binary) {
        filename = nodePath["normalize"](filename);
        var ret = nodeFS["readFileSync"](filename);
        if (!ret && filename != nodePath["resolve"](filename)) {
            filename = path.join(__dirname, "..", "src", filename);
            ret = nodeFS["readFileSync"](filename);
        }
        if (ret && !binary) ret = ret.toString();
        return ret;
    };
    Module["readBinary"] = function readBinary(filename) {
        return Module["read"](filename, true);
    };
    Module["load"] = function load(f) {
        globalEval(read(f));
    };
    Module["thisProgram"] = process["argv"][1].replace(/\\/g, "/");
    Module["arguments"] = process["argv"].slice(2);
    if (typeof module !== "undefined") {
        module["exports"] = Module;
    }
    process["on"]("uncaughtException", function (ex) {
        if (!(ex instanceof ExitStatus)) {
            throw ex;
        }
    });
} else if (ENVIRONMENT_IS_SHELL) {
    if (!Module["print"]) Module["print"] = print;
    if (typeof printErr != "undefined") Module["printErr"] = printErr;
    if (typeof read != "undefined") {
        Module["read"] = read;
    } else {
        Module["read"] = function read() {
            throw "no read() available (jsc?)";
        };
    }
    Module["readBinary"] = function readBinary(f) {
        return read(f, "binary");
    };
    if (typeof scriptArgs != "undefined") {
        Module["arguments"] = scriptArgs;
    } else if (typeof arguments != "undefined") {
        Module["arguments"] = arguments;
    }
    this["Module"] = Module;
} else if (ENVIRONMENT_IS_WEB || ENVIRONMENT_IS_WORKER) {
    Module["read"] = function read(url) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, false);
        xhr.send(null);
        return xhr.responseText;
    };
    if (typeof arguments != "undefined") {
        Module["arguments"] = arguments;
    }
    if (typeof console !== "undefined") {
        if (!Module["print"])
            Module["print"] = function print(x) {
                console.log(x);
            };
        if (!Module["printErr"])
            Module["printErr"] = function printErr(x) {
                console.log(x);
            };
    } else {
        var TRY_USE_DUMP = false;
        if (!Module["print"])
            Module["print"] =
                TRY_USE_DUMP && typeof dump !== "undefined"
                    ? function (x) {
                          dump(x);
                      }
                    : function (x) {};
    }
    if (ENVIRONMENT_IS_WEB) {
        window["Module"] = Module;
    } else {
        Module["load"] = importScripts;
    }
} else {
    throw "Unknown runtime environment. Where are we?";
}
function globalEval(x) {
    eval.call(null, x);
}
if (!Module["load"] == "undefined" && Module["read"]) {
    Module["load"] = function load(f) {
        globalEval(Module["read"](f));
    };
}
if (!Module["print"]) {
    Module["print"] = function () {};
}
if (!Module["printErr"]) {
    Module["printErr"] = Module["print"];
}
if (!Module["arguments"]) {
    Module["arguments"] = [];
}
if (!Module["thisProgram"]) {
    Module["thisProgram"] = "./this.program";
}
Module.print = Module["print"];
Module.printErr = Module["printErr"];
Module["preRun"] = [];
Module["postRun"] = [];
for (var key in moduleOverrides) {
    if (moduleOverrides.hasOwnProperty(key)) {
        Module[key] = moduleOverrides[key];
    }
}
var Runtime = {
    setTempRet0: function (value) {
        tempRet0 = value;
    },
    getTempRet0: function () {
        return tempRet0;
    },
    stackSave: function () {
        return STACKTOP;
    },
    stackRestore: function (stackTop) {
        STACKTOP = stackTop;
    },
    forceAlign: function (target, quantum) {
        quantum = quantum || 4;
        if (quantum == 1) return target;
        if (isNumber(target) && isNumber(quantum)) {
            return Math.ceil(target / quantum) * quantum;
        } else if (isNumber(quantum) && isPowerOfTwo(quantum)) {
            return "(((" + target + ")+" + (quantum - 1) + ")&" + -quantum + ")";
        }
        return "Math.ceil((" + target + ")/" + quantum + ")*" + quantum;
    },
    isNumberType: function (type) {
        return type in Runtime.INT_TYPES || type in Runtime.FLOAT_TYPES;
    },
    isPointerType: function isPointerType(type) {
        return type[type.length - 1] == "*";
    },
    isStructType: function isStructType(type) {
        if (isPointerType(type)) return false;
        if (isArrayType(type)) return true;
        if (/<?\{ ?[^}]* ?\}>?/.test(type)) return true;
        return type[0] == "%";
    },
    INT_TYPES: { i1: 0, i8: 0, i16: 0, i32: 0, i64: 0 },
    FLOAT_TYPES: { float: 0, double: 0 },
    or64: function (x, y) {
        var l = x | 0 | (y | 0);
        var h = (Math.round(x / 4294967296) | Math.round(y / 4294967296)) * 4294967296;
        return l + h;
    },
    and64: function (x, y) {
        var l = (x | 0) & (y | 0);
        var h = (Math.round(x / 4294967296) & Math.round(y / 4294967296)) * 4294967296;
        return l + h;
    },
    xor64: function (x, y) {
        var l = (x | 0) ^ (y | 0);
        var h = (Math.round(x / 4294967296) ^ Math.round(y / 4294967296)) * 4294967296;
        return l + h;
    },
    getNativeTypeSize: function (type) {
        switch (type) {
            case "i1":
            case "i8":
                return 1;
            case "i16":
                return 2;
            case "i32":
                return 4;
            case "i64":
                return 8;
            case "float":
                return 4;
            case "double":
                return 8;
            default: {
                if (type[type.length - 1] === "*") {
                    return Runtime.QUANTUM_SIZE;
                } else if (type[0] === "i") {
                    var bits = parseInt(type.substr(1));
                    assert(bits % 8 === 0);
                    return bits / 8;
                } else {
                    return 0;
                }
            }
        }
    },
    getNativeFieldSize: function (type) {
        return Math.max(Runtime.getNativeTypeSize(type), Runtime.QUANTUM_SIZE);
    },
    dedup: function dedup(items, ident) {
        var seen = {};
        if (ident) {
            return items.filter(function (item) {
                if (seen[item[ident]]) return false;
                seen[item[ident]] = true;
                return true;
            });
        } else {
            return items.filter(function (item) {
                if (seen[item]) return false;
                seen[item] = true;
                return true;
            });
        }
    },
    set: function set() {
        var args = typeof arguments[0] === "object" ? arguments[0] : arguments;
        var ret = {};
        for (var i = 0; i < args.length; i++) {
            ret[args[i]] = 0;
        }
        return ret;
    },
    STACK_ALIGN: 8,
    getAlignSize: function (type, size, vararg) {
        if (!vararg && (type == "i64" || type == "double")) return 8;
        if (!type) return Math.min(size, 8);
        return Math.min(size || (type ? Runtime.getNativeFieldSize(type) : 0), Runtime.QUANTUM_SIZE);
    },
    calculateStructAlignment: function calculateStructAlignment(type) {
        type.flatSize = 0;
        type.alignSize = 0;
        var diffs = [];
        var prev = -1;
        var index = 0;
        type.flatIndexes = type.fields.map(function (field) {
            index++;
            var size, alignSize;
            if (Runtime.isNumberType(field) || Runtime.isPointerType(field)) {
                size = Runtime.getNativeTypeSize(field);
                alignSize = Runtime.getAlignSize(field, size);
            } else if (Runtime.isStructType(field)) {
                if (field[1] === "0") {
                    size = 0;
                    if (Types.types[field]) {
                        alignSize = Runtime.getAlignSize(null, Types.types[field].alignSize);
                    } else {
                        alignSize = type.alignSize || QUANTUM_SIZE;
                    }
                } else {
                    size = Types.types[field].flatSize;
                    alignSize = Runtime.getAlignSize(null, Types.types[field].alignSize);
                }
            } else if (field[0] == "b") {
                size = field.substr(1) | 0;
                alignSize = 1;
            } else if (field[0] === "<") {
                size = alignSize = Types.types[field].flatSize;
            } else if (field[0] === "i") {
                size = alignSize = parseInt(field.substr(1)) / 8;
                assert(size % 1 === 0, "cannot handle non-byte-size field " + field);
            } else {
                assert(false, "invalid type for calculateStructAlignment");
            }
            if (type.packed) alignSize = 1;
            type.alignSize = Math.max(type.alignSize, alignSize);
            var curr = Runtime.alignMemory(type.flatSize, alignSize);
            type.flatSize = curr + size;
            if (prev >= 0) {
                diffs.push(curr - prev);
            }
            prev = curr;
            return curr;
        });
        if (type.name_ && type.name_[0] === "[") {
            type.flatSize = (parseInt(type.name_.substr(1)) * type.flatSize) / 2;
        }
        type.flatSize = Runtime.alignMemory(type.flatSize, type.alignSize);
        if (diffs.length == 0) {
            type.flatFactor = type.flatSize;
        } else if (Runtime.dedup(diffs).length == 1) {
            type.flatFactor = diffs[0];
        }
        type.needsFlattening = type.flatFactor != 1;
        return type.flatIndexes;
    },
    generateStructInfo: function (struct, typeName, offset) {
        var type, alignment;
        if (typeName) {
            offset = offset || 0;
            type = (typeof Types === "undefined" ? Runtime.typeInfo : Types.types)[typeName];
            if (!type) return null;
            if (type.fields.length != struct.length) {
                printErr("Number of named fields must match the type for " + typeName + ": possibly duplicate struct names. Cannot return structInfo");
                return null;
            }
            alignment = type.flatIndexes;
        } else {
            var type = {
                fields: struct.map(function (item) {
                    return item[0];
                }),
            };
            alignment = Runtime.calculateStructAlignment(type);
        }
        var ret = { __size__: type.flatSize };
        if (typeName) {
            struct.forEach(function (item, i) {
                if (typeof item === "string") {
                    ret[item] = alignment[i] + offset;
                } else {
                    var key;
                    for (var k in item) key = k;
                    ret[key] = Runtime.generateStructInfo(item[key], type.fields[i], alignment[i]);
                }
            });
        } else {
            struct.forEach(function (item, i) {
                ret[item[1]] = alignment[i];
            });
        }
        return ret;
    },
    dynCall: function (sig, ptr, args) {
        if (args && args.length) {
            if (!args.splice) args = Array.prototype.slice.call(args);
            args.splice(0, 0, ptr);
            return Module["dynCall_" + sig].apply(null, args);
        } else {
            return Module["dynCall_" + sig].call(null, ptr);
        }
    },
    functionPointers: [],
    addFunction: function (func) {
        for (var i = 0; i < Runtime.functionPointers.length; i++) {
            if (!Runtime.functionPointers[i]) {
                Runtime.functionPointers[i] = func;
                return 2 * (1 + i);
            }
        }
        throw "Finished up all reserved function pointers. Use a higher value for RESERVED_FUNCTION_POINTERS.";
    },
    removeFunction: function (index) {
        Runtime.functionPointers[(index - 2) / 2] = null;
    },
    getAsmConst: function (code, numArgs) {
        if (!Runtime.asmConstCache) Runtime.asmConstCache = {};
        var func = Runtime.asmConstCache[code];
        if (func) return func;
        var args = [];
        for (var i = 0; i < numArgs; i++) {
            args.push(String.fromCharCode(36) + i);
        }
        var source = Pointer_stringify(code);
        if (source[0] === '"') {
            if (source.indexOf('"', 1) === source.length - 1) {
                source = source.substr(1, source.length - 2);
            } else {
                abort("invalid EM_ASM input |" + source + "|. Please use EM_ASM(..code..) (no quotes) or EM_ASM({ ..code($0).. }, input) (to input values)");
            }
        }
        try {
            var evalled = eval("(function(Module, FS) { return function(" + args.join(",") + "){ " + source + " } })")(Module, typeof FS !== "undefined" ? FS : null);
        } catch (e) {
            Module.printErr("error in executing inline EM_ASM code: " + e + " on: \n\n" + source + "\n\nwith args |" + args + "| (make sure to use the right one out of EM_ASM, EM_ASM_ARGS, etc.)");
            throw e;
        }
        return (Runtime.asmConstCache[code] = evalled);
    },
    warnOnce: function (text) {
        if (!Runtime.warnOnce.shown) Runtime.warnOnce.shown = {};
        if (!Runtime.warnOnce.shown[text]) {
            Runtime.warnOnce.shown[text] = 1;
            Module.printErr(text);
        }
    },
    funcWrappers: {},
    getFuncWrapper: function (func, sig) {
        assert(sig);
        if (!Runtime.funcWrappers[sig]) {
            Runtime.funcWrappers[sig] = {};
        }
        var sigCache = Runtime.funcWrappers[sig];
        if (!sigCache[func]) {
            sigCache[func] = function dynCall_wrapper() {
                return Runtime.dynCall(sig, func, arguments);
            };
        }
        return sigCache[func];
    },
    UTF8Processor: function () {
        var buffer = [];
        var needed = 0;
        this.processCChar = function (code) {
            code = code & 255;
            if (buffer.length == 0) {
                if ((code & 128) == 0) {
                    return String.fromCharCode(code);
                }
                buffer.push(code);
                if ((code & 224) == 192) {
                    needed = 1;
                } else if ((code & 240) == 224) {
                    needed = 2;
                } else {
                    needed = 3;
                }
                return "";
            }
            if (needed) {
                buffer.push(code);
                needed--;
                if (needed > 0) return "";
            }
            var c1 = buffer[0];
            var c2 = buffer[1];
            var c3 = buffer[2];
            var c4 = buffer[3];
            var ret;
            if (buffer.length == 2) {
                ret = String.fromCharCode(((c1 & 31) << 6) | (c2 & 63));
            } else if (buffer.length == 3) {
                ret = String.fromCharCode(((c1 & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
            } else {
                var codePoint = ((c1 & 7) << 18) | ((c2 & 63) << 12) | ((c3 & 63) << 6) | (c4 & 63);
                ret = String.fromCharCode((((codePoint - 65536) / 1024) | 0) + 55296, ((codePoint - 65536) % 1024) + 56320);
            }
            buffer.length = 0;
            return ret;
        };
        this.processJSString = function processJSString(string) {
            string = unescape(encodeURIComponent(string));
            var ret = [];
            for (var i = 0; i < string.length; i++) {
                ret.push(string.charCodeAt(i));
            }
            return ret;
        };
    },
    getCompilerSetting: function (name) {
        throw "You must build with -s RETAIN_COMPILER_SETTINGS=1 for Runtime.getCompilerSetting or emscripten_get_compiler_setting to work";
    },
    stackAlloc: function (size) {
        var ret = STACKTOP;
        STACKTOP = (STACKTOP + size) | 0;
        STACKTOP = (STACKTOP + 7) & -8;
        return ret;
    },
    staticAlloc: function (size) {
        var ret = STATICTOP;
        STATICTOP = (STATICTOP + size) | 0;
        STATICTOP = (STATICTOP + 7) & -8;
        return ret;
    },
    dynamicAlloc: function (size) {
        var ret = DYNAMICTOP;
        DYNAMICTOP = (DYNAMICTOP + size) | 0;
        DYNAMICTOP = (DYNAMICTOP + 7) & -8;
        if (DYNAMICTOP >= TOTAL_MEMORY) enlargeMemory();
        return ret;
    },
    alignMemory: function (size, quantum) {
        var ret = (size = Math.ceil(size / (quantum ? quantum : 8)) * (quantum ? quantum : 8));
        return ret;
    },
    makeBigInt: function (low, high, unsigned) {
        var ret = unsigned ? +(low >>> 0) + +(high >>> 0) * +4294967296 : +(low >>> 0) + +(high | 0) * +4294967296;
        return ret;
    },
    GLOBAL_BASE: 8,
    QUANTUM_SIZE: 4,
    __dummy__: 0,
};
Module["Runtime"] = Runtime;
var __THREW__ = 0;
var ABORT = false;
var EXITSTATUS = 0;
var undef = 0;
var tempValue, tempInt, tempBigInt, tempInt2, tempBigInt2, tempPair, tempBigIntI, tempBigIntR, tempBigIntS, tempBigIntP, tempBigIntD, tempDouble, tempFloat;
var tempI64, tempI64b;
var tempRet0, tempRet1, tempRet2, tempRet3, tempRet4, tempRet5, tempRet6, tempRet7, tempRet8, tempRet9;
function assert(condition, text) {
    if (!condition) {
        abort("Assertion failed: " + text);
    }
}
var globalScope = this;
function getCFunc(ident) {
    var func = Module["_" + ident];
    if (!func) {
        try {
            func = eval("_" + ident);
        } catch (e) {}
    }
    assert(func, "Cannot call unknown function " + ident + " (perhaps LLVM optimizations or closure removed it?)");
    return func;
}
var cwrap, ccall;
(function () {
    var stack = 0;
    var JSfuncs = {
        stackSave: function () {
            stack = Runtime.stackSave();
        },
        stackRestore: function () {
            Runtime.stackRestore(stack);
        },
        arrayToC: function (arr) {
            var ret = Runtime.stackAlloc(arr.length);
            writeArrayToMemory(arr, ret);
            return ret;
        },
        stringToC: function (str) {
            var ret = 0;
            if (str !== null && str !== undefined && str !== 0) {
                ret = Runtime.stackAlloc(str.length + 1);
                writeStringToMemory(str, ret);
            }
            return ret;
        },
    };
    var toC = { string: JSfuncs["stringToC"], array: JSfuncs["arrayToC"] };
    ccall = function ccallFunc(ident, returnType, argTypes, args) {
        var func = getCFunc(ident);
        var cArgs = [];
        if (args) {
            for (var i = 0; i < args.length; i++) {
                var converter = toC[argTypes[i]];
                if (converter) {
                    if (stack === 0) stack = Runtime.stackSave();
                    cArgs[i] = converter(args[i]);
                } else {
                    cArgs[i] = args[i];
                }
            }
        }
        var ret = func.apply(null, cArgs);
        if (returnType === "string") ret = Pointer_stringify(ret);
        if (stack !== 0) JSfuncs["stackRestore"]();
        return ret;
    };
    var sourceRegex = /^function\s*\(([^)]*)\)\s*{\s*([^*]*?)[\s;]*(?:return\s*(.*?)[;\s]*)?}$/;
    function parseJSFunc(jsfunc) {
        var parsed = jsfunc.toString().match(sourceRegex).slice(1);
        return { arguments: parsed[0], body: parsed[1], returnValue: parsed[2] };
    }
    var JSsource = {};
    for (var fun in JSfuncs) {
        if (JSfuncs.hasOwnProperty(fun)) {
            JSsource[fun] = parseJSFunc(JSfuncs[fun]);
        }
    }
    cwrap = function cwrap(ident, returnType, argTypes) {
        argTypes = argTypes || [];
        var cfunc = getCFunc(ident);
        var numericArgs = argTypes.every(function (type) {
            return type === "number";
        });
        var numericRet = returnType !== "string";
        if (numericRet && numericArgs) {
            return cfunc;
        }
        var argNames = argTypes.map(function (x, i) {
            return "$" + i;
        });
        var funcstr = "(function(" + argNames.join(",") + ") {";
        var nargs = argTypes.length;
        if (!numericArgs) {
            funcstr += JSsource["stackSave"].body + ";";
            for (var i = 0; i < nargs; i++) {
                var arg = argNames[i],
                    type = argTypes[i];
                if (type === "number") continue;
                var convertCode = JSsource[type + "ToC"];
                funcstr += "var " + convertCode.arguments + " = " + arg + ";";
                funcstr += convertCode.body + ";";
                funcstr += arg + "=" + convertCode.returnValue + ";";
            }
        }
        var cfuncname = parseJSFunc(function () {
            return cfunc;
        }).returnValue;
        funcstr += "var ret = " + cfuncname + "(" + argNames.join(",") + ");";
        if (!numericRet) {
            var strgfy = parseJSFunc(function () {
                return Pointer_stringify;
            }).returnValue;
            funcstr += "ret = " + strgfy + "(ret);";
        }
        if (!numericArgs) {
            funcstr += JSsource["stackRestore"].body + ";";
        }
        funcstr += "return ret})";
        return eval(funcstr);
    };
})();
Module["cwrap"] = cwrap;
Module["ccall"] = ccall;
function setValue(ptr, value, type, noSafe) {
    type = type || "i8";
    if (type.charAt(type.length - 1) === "*") type = "i32";
    switch (type) {
        case "i1":
            HEAP8[ptr >> 0] = value;
            break;
        case "i8":
            HEAP8[ptr >> 0] = value;
            break;
        case "i16":
            HEAP16[ptr >> 1] = value;
            break;
        case "i32":
            HEAP32[ptr >> 2] = value;
            break;
        case "i64":
            (tempI64 = [
                value >>> 0,
                ((tempDouble = value), +Math_abs(tempDouble) >= +1 ? (tempDouble > +0 ? (Math_min(+Math_floor(tempDouble / +4294967296), +4294967295) | 0) >>> 0 : ~~+Math_ceil((tempDouble - +(~~tempDouble >>> 0)) / +4294967296) >>> 0) : 0),
            ]),
                (HEAP32[ptr >> 2] = tempI64[0]),
                (HEAP32[(ptr + 4) >> 2] = tempI64[1]);
            break;
        case "float":
            HEAPF32[ptr >> 2] = value;
            break;
        case "double":
            HEAPF64[ptr >> 3] = value;
            break;
        default:
            abort("invalid type for setValue: " + type);
    }
}
Module["setValue"] = setValue;
function getValue(ptr, type, noSafe) {
    type = type || "i8";
    if (type.charAt(type.length - 1) === "*") type = "i32";
    switch (type) {
        case "i1":
            return HEAP8[ptr >> 0];
        case "i8":
            return HEAP8[ptr >> 0];
        case "i16":
            return HEAP16[ptr >> 1];
        case "i32":
            return HEAP32[ptr >> 2];
        case "i64":
            return HEAP32[ptr >> 2];
        case "float":
            return HEAPF32[ptr >> 2];
        case "double":
            return HEAPF64[ptr >> 3];
        default:
            abort("invalid type for setValue: " + type);
    }
    return null;
}
Module["getValue"] = getValue;
var ALLOC_NORMAL = 0;
var ALLOC_STACK = 1;
var ALLOC_STATIC = 2;
var ALLOC_DYNAMIC = 3;
var ALLOC_NONE = 4;
Module["ALLOC_NORMAL"] = ALLOC_NORMAL;
Module["ALLOC_STACK"] = ALLOC_STACK;
Module["ALLOC_STATIC"] = ALLOC_STATIC;
Module["ALLOC_DYNAMIC"] = ALLOC_DYNAMIC;
Module["ALLOC_NONE"] = ALLOC_NONE;
function allocate(slab, types, allocator, ptr) {
    var zeroinit, size;
    if (typeof slab === "number") {
        zeroinit = true;
        size = slab;
    } else {
        zeroinit = false;
        size = slab.length;
    }
    var singleType = typeof types === "string" ? types : null;
    var ret;
    if (allocator == ALLOC_NONE) {
        ret = ptr;
    } else {
        ret = [_malloc, Runtime.stackAlloc, Runtime.staticAlloc, Runtime.dynamicAlloc][allocator === undefined ? ALLOC_STATIC : allocator](Math.max(size, singleType ? 1 : types.length));
    }
    if (zeroinit) {
        var ptr = ret,
            stop;
        assert((ret & 3) == 0);
        stop = ret + (size & ~3);
        for (; ptr < stop; ptr += 4) {
            HEAP32[ptr >> 2] = 0;
        }
        stop = ret + size;
        while (ptr < stop) {
            HEAP8[ptr++ >> 0] = 0;
        }
        return ret;
    }
    if (singleType === "i8") {
        if (slab.subarray || slab.slice) {
            HEAPU8.set(slab, ret);
        } else {
            HEAPU8.set(new Uint8Array(slab), ret);
        }
        return ret;
    }
    var i = 0,
        type,
        typeSize,
        previousType;
    while (i < size) {
        var curr = slab[i];
        if (typeof curr === "function") {
            curr = Runtime.getFunctionIndex(curr);
        }
        type = singleType || types[i];
        if (type === 0) {
            i++;
            continue;
        }
        if (type == "i64") type = "i32";
        setValue(ret + i, curr, type);
        if (previousType !== type) {
            typeSize = Runtime.getNativeTypeSize(type);
            previousType = type;
        }
        i += typeSize;
    }
    return ret;
}
Module["allocate"] = allocate;
function Pointer_stringify(ptr, length) {
    var hasUtf = false;
    var t;
    var i = 0;
    while (1) {
        t = HEAPU8[(ptr + i) >> 0];
        if (t >= 128) hasUtf = true;
        else if (t == 0 && !length) break;
        i++;
        if (length && i == length) break;
    }
    if (!length) length = i;
    var ret = "";
    if (!hasUtf) {
        var MAX_CHUNK = 1024;
        var curr;
        while (length > 0) {
            curr = String.fromCharCode.apply(String, HEAPU8.subarray(ptr, ptr + Math.min(length, MAX_CHUNK)));
            ret = ret ? ret + curr : curr;
            ptr += MAX_CHUNK;
            length -= MAX_CHUNK;
        }
        return ret;
    }
    var utf8 = new Runtime.UTF8Processor();
    for (i = 0; i < length; i++) {
        t = HEAPU8[(ptr + i) >> 0];
        ret += utf8.processCChar(t);
    }
    return ret;
}
Module["Pointer_stringify"] = Pointer_stringify;
function UTF16ToString(ptr) {
    var i = 0;
    var str = "";
    while (1) {
        var codeUnit = HEAP16[(ptr + i * 2) >> 1];
        if (codeUnit == 0) return str;
        ++i;
        str += String.fromCharCode(codeUnit);
    }
}
Module["UTF16ToString"] = UTF16ToString;
function stringToUTF16(str, outPtr) {
    for (var i = 0; i < str.length; ++i) {
        var codeUnit = str.charCodeAt(i);
        HEAP16[(outPtr + i * 2) >> 1] = codeUnit;
    }
    HEAP16[(outPtr + str.length * 2) >> 1] = 0;
}
Module["stringToUTF16"] = stringToUTF16;
function UTF32ToString(ptr) {
    var i = 0;
    var str = "";
    while (1) {
        var utf32 = HEAP32[(ptr + i * 4) >> 2];
        if (utf32 == 0) return str;
        ++i;
        if (utf32 >= 65536) {
            var ch = utf32 - 65536;
            str += String.fromCharCode(55296 | (ch >> 10), 56320 | (ch & 1023));
        } else {
            str += String.fromCharCode(utf32);
        }
    }
}
Module["UTF32ToString"] = UTF32ToString;
function stringToUTF32(str, outPtr) {
    var iChar = 0;
    for (var iCodeUnit = 0; iCodeUnit < str.length; ++iCodeUnit) {
        var codeUnit = str.charCodeAt(iCodeUnit);
        if (codeUnit >= 55296 && codeUnit <= 57343) {
            var trailSurrogate = str.charCodeAt(++iCodeUnit);
            codeUnit = (65536 + ((codeUnit & 1023) << 10)) | (trailSurrogate & 1023);
        }
        HEAP32[(outPtr + iChar * 4) >> 2] = codeUnit;
        ++iChar;
    }
    HEAP32[(outPtr + iChar * 4) >> 2] = 0;
}
Module["stringToUTF32"] = stringToUTF32;
function demangle(func) {
    var hasLibcxxabi = !!Module["___cxa_demangle"];
    if (hasLibcxxabi) {
        try {
            var buf = _malloc(func.length);
            writeStringToMemory(func.substr(1), buf);
            var status = _malloc(4);
            var ret = Module["___cxa_demangle"](buf, 0, 0, status);
            if (getValue(status, "i32") === 0 && ret) {
                return Pointer_stringify(ret);
            }
        } catch (e) {
        } finally {
            if (buf) _free(buf);
            if (status) _free(status);
            if (ret) _free(ret);
        }
    }
    var i = 3;
    var basicTypes = {
        v: "void",
        b: "bool",
        c: "char",
        s: "short",
        i: "int",
        l: "long",
        f: "float",
        d: "double",
        w: "wchar_t",
        a: "signed char",
        h: "unsigned char",
        t: "unsigned short",
        j: "unsigned int",
        m: "unsigned long",
        x: "long long",
        y: "unsigned long long",
        z: "...",
    };
    var subs = [];
    var first = true;
    function dump(x) {
        if (x) Module.print(x);
        Module.print(func);
        var pre = "";
        for (var a = 0; a < i; a++) pre += " ";
        Module.print(pre + "^");
    }
    function parseNested() {
        i++;
        if (func[i] === "K") i++;
        var parts = [];
        while (func[i] !== "E") {
            if (func[i] === "S") {
                i++;
                var next = func.indexOf("_", i);
                var num = func.substring(i, next) || 0;
                parts.push(subs[num] || "?");
                i = next + 1;
                continue;
            }
            if (func[i] === "C") {
                parts.push(parts[parts.length - 1]);
                i += 2;
                continue;
            }
            var size = parseInt(func.substr(i));
            var pre = size.toString().length;
            if (!size || !pre) {
                i--;
                break;
            }
            var curr = func.substr(i + pre, size);
            parts.push(curr);
            subs.push(curr);
            i += pre + size;
        }
        i++;
        return parts;
    }
    function parse(rawList, limit, allowVoid) {
        limit = limit || Infinity;
        var ret = "",
            list = [];
        function flushList() {
            return "(" + list.join(", ") + ")";
        }
        var name;
        if (func[i] === "N") {
            name = parseNested().join("::");
            limit--;
            if (limit === 0) return rawList ? [name] : name;
        } else {
            if (func[i] === "K" || (first && func[i] === "L")) i++;
            var size = parseInt(func.substr(i));
            if (size) {
                var pre = size.toString().length;
                name = func.substr(i + pre, size);
                i += pre + size;
            }
        }
        first = false;
        if (func[i] === "I") {
            i++;
            var iList = parse(true);
            var iRet = parse(true, 1, true);
            ret += iRet[0] + " " + name + "<" + iList.join(", ") + ">";
        } else {
            ret = name;
        }
        paramLoop: while (i < func.length && limit-- > 0) {
            var c = func[i++];
            if (c in basicTypes) {
                list.push(basicTypes[c]);
            } else {
                switch (c) {
                    case "P":
                        list.push(parse(true, 1, true)[0] + "*");
                        break;
                    case "R":
                        list.push(parse(true, 1, true)[0] + "&");
                        break;
                    case "L": {
                        i++;
                        var end = func.indexOf("E", i);
                        var size = end - i;
                        list.push(func.substr(i, size));
                        i += size + 2;
                        break;
                    }
                    case "A": {
                        var size = parseInt(func.substr(i));
                        i += size.toString().length;
                        if (func[i] !== "_") throw "?";
                        i++;
                        list.push(parse(true, 1, true)[0] + " [" + size + "]");
                        break;
                    }
                    case "E":
                        break paramLoop;
                    default:
                        ret += "?" + c;
                        break paramLoop;
                }
            }
        }
        if (!allowVoid && list.length === 1 && list[0] === "void") list = [];
        if (rawList) {
            if (ret) {
                list.push(ret + "?");
            }
            return list;
        } else {
            return ret + flushList();
        }
    }
    var final = func;
    try {
        if (func == "Object._main" || func == "_main") {
            return "main()";
        }
        if (typeof func === "number") func = Pointer_stringify(func);
        if (func[0] !== "_") return func;
        if (func[1] !== "_") return func;
        if (func[2] !== "Z") return func;
        switch (func[3]) {
            case "n":
                return "operator new()";
            case "d":
                return "operator delete()";
        }
        final = parse();
    } catch (e) {
        final += "?";
    }
    if (final.indexOf("?") >= 0 && !hasLibcxxabi) {
        Runtime.warnOnce("warning: a problem occurred in builtin C++ name demangling; build with  -s DEMANGLE_SUPPORT=1  to link in libcxxabi demangling");
    }
    return final;
}
function demangleAll(text) {
    return text.replace(/__Z[\w\d_]+/g, function (x) {
        var y = demangle(x);
        return x === y ? x : x + " [" + y + "]";
    });
}
function jsStackTrace() {
    var err = new Error();
    if (!err.stack) {
        try {
            throw new Error(0);
        } catch (e) {
            err = e;
        }
        if (!err.stack) {
            return "(no stack trace available)";
        }
    }
    return err.stack.toString();
}
function stackTrace() {
    return demangleAll(jsStackTrace());
}
Module["stackTrace"] = stackTrace;
var PAGE_SIZE = 4096;
function alignMemoryPage(x) {
    return (x + 4095) & -4096;
}
var HEAP;
var HEAP8, HEAPU8, HEAP16, HEAPU16, HEAP32, HEAPU32, HEAPF32, HEAPF64;
var STATIC_BASE = 0,
    STATICTOP = 0,
    staticSealed = false;
var STACK_BASE = 0,
    STACKTOP = 0,
    STACK_MAX = 0;
var DYNAMIC_BASE = 0,
    DYNAMICTOP = 0;
function enlargeMemory() {
    abort(
        "Cannot enlarge memory arrays. Either (1) compile with -s TOTAL_MEMORY=X with X higher than the current value " +
            TOTAL_MEMORY +
            ", (2) compile with ALLOW_MEMORY_GROWTH which adjusts the size at runtime but prevents some optimizations, or (3) set Module.TOTAL_MEMORY before the program runs."
    );
}
var TOTAL_STACK = Module["TOTAL_STACK"] || 5242880;
var TOTAL_MEMORY = Module["TOTAL_MEMORY"] || 16777216;
var FAST_MEMORY = Module["FAST_MEMORY"] || 2097152;
var totalMemory = 64 * 1024;
while (totalMemory < TOTAL_MEMORY || totalMemory < 2 * TOTAL_STACK) {
    if (totalMemory < 16 * 1024 * 1024) {
        totalMemory *= 2;
    } else {
        totalMemory += 16 * 1024 * 1024;
    }
}
if (totalMemory !== TOTAL_MEMORY) {
    Module.printErr("increasing TOTAL_MEMORY to " + totalMemory + " to be more reasonable");
    TOTAL_MEMORY = totalMemory;
}
assert(typeof Int32Array !== "undefined" && typeof Float64Array !== "undefined" && !!new Int32Array(1)["subarray"] && !!new Int32Array(1)["set"], "JS engine does not provide full typed array support");
var buffer = new ArrayBuffer(TOTAL_MEMORY);
HEAP8 = new Int8Array(buffer);
HEAP16 = new Int16Array(buffer);
HEAP32 = new Int32Array(buffer);
HEAPU8 = new Uint8Array(buffer);
HEAPU16 = new Uint16Array(buffer);
HEAPU32 = new Uint32Array(buffer);
HEAPF32 = new Float32Array(buffer);
HEAPF64 = new Float64Array(buffer);
HEAP32[0] = 255;
assert(HEAPU8[0] === 255 && HEAPU8[3] === 0, "Typed arrays 2 must be run on a little-endian system");
Module["HEAP"] = HEAP;
Module["HEAP8"] = HEAP8;
Module["HEAP16"] = HEAP16;
Module["HEAP32"] = HEAP32;
Module["HEAPU8"] = HEAPU8;
Module["HEAPU16"] = HEAPU16;
Module["HEAPU32"] = HEAPU32;
Module["HEAPF32"] = HEAPF32;
Module["HEAPF64"] = HEAPF64;
function callRuntimeCallbacks(callbacks) {
    while (callbacks.length > 0) {
        var callback = callbacks.shift();
        if (typeof callback == "function") {
            callback();
            continue;
        }
        var func = callback.func;
        if (typeof func === "number") {
            if (callback.arg === undefined) {
                Runtime.dynCall("v", func);
            } else {
                Runtime.dynCall("vi", func, [callback.arg]);
            }
        } else {
            func(callback.arg === undefined ? null : callback.arg);
        }
    }
}
var __ATPRERUN__ = [];
var __ATINIT__ = [];
var __ATMAIN__ = [];
var __ATEXIT__ = [];
var __ATPOSTRUN__ = [];
var runtimeInitialized = false;
var runtimeExited = false;
function preRun() {
    if (Module["preRun"]) {
        if (typeof Module["preRun"] == "function") Module["preRun"] = [Module["preRun"]];
        while (Module["preRun"].length) {
            addOnPreRun(Module["preRun"].shift());
        }
    }
    callRuntimeCallbacks(__ATPRERUN__);
}
function ensureInitRuntime() {
    if (runtimeInitialized) return;
    runtimeInitialized = true;
    callRuntimeCallbacks(__ATINIT__);
}
function preMain() {
    callRuntimeCallbacks(__ATMAIN__);
}
function exitRuntime() {
    callRuntimeCallbacks(__ATEXIT__);
    runtimeExited = true;
}
function postRun() {
    if (Module["postRun"]) {
        if (typeof Module["postRun"] == "function") Module["postRun"] = [Module["postRun"]];
        while (Module["postRun"].length) {
            addOnPostRun(Module["postRun"].shift());
        }
    }
    callRuntimeCallbacks(__ATPOSTRUN__);
}
function addOnPreRun(cb) {
    __ATPRERUN__.unshift(cb);
}
Module["addOnPreRun"] = Module.addOnPreRun = addOnPreRun;
function addOnInit(cb) {
    __ATINIT__.unshift(cb);
}
Module["addOnInit"] = Module.addOnInit = addOnInit;
function addOnPreMain(cb) {
    __ATMAIN__.unshift(cb);
}
Module["addOnPreMain"] = Module.addOnPreMain = addOnPreMain;
function addOnExit(cb) {
    __ATEXIT__.unshift(cb);
}
Module["addOnExit"] = Module.addOnExit = addOnExit;
function addOnPostRun(cb) {
    __ATPOSTRUN__.unshift(cb);
}
Module["addOnPostRun"] = Module.addOnPostRun = addOnPostRun;
function intArrayFromString(stringy, dontAddNull, length) {
    var ret = new Runtime.UTF8Processor().processJSString(stringy);
    if (length) {
        ret.length = length;
    }
    if (!dontAddNull) {
        ret.push(0);
    }
    return ret;
}
Module["intArrayFromString"] = intArrayFromString;
function intArrayToString(array) {
    var ret = [];
    for (var i = 0; i < array.length; i++) {
        var chr = array[i];
        if (chr > 255) {
            chr &= 255;
        }
        ret.push(String.fromCharCode(chr));
    }
    return ret.join("");
}
Module["intArrayToString"] = intArrayToString;
function writeStringToMemory(string, buffer, dontAddNull) {
    var array = intArrayFromString(string, dontAddNull);
    var i = 0;
    while (i < array.length) {
        var chr = array[i];
        HEAP8[(buffer + i) >> 0] = chr;
        i = i + 1;
    }
}
Module["writeStringToMemory"] = writeStringToMemory;
function writeArrayToMemory(array, buffer) {
    for (var i = 0; i < array.length; i++) {
        HEAP8[(buffer + i) >> 0] = array[i];
    }
}
Module["writeArrayToMemory"] = writeArrayToMemory;
function writeAsciiToMemory(str, buffer, dontAddNull) {
    for (var i = 0; i < str.length; i++) {
        HEAP8[(buffer + i) >> 0] = str.charCodeAt(i);
    }
    if (!dontAddNull) HEAP8[(buffer + str.length) >> 0] = 0;
}
Module["writeAsciiToMemory"] = writeAsciiToMemory;
function unSign(value, bits, ignore) {
    if (value >= 0) {
        return value;
    }
    return bits <= 32 ? 2 * Math.abs(1 << (bits - 1)) + value : Math.pow(2, bits) + value;
}
function reSign(value, bits, ignore) {
    if (value <= 0) {
        return value;
    }
    var half = bits <= 32 ? Math.abs(1 << (bits - 1)) : Math.pow(2, bits - 1);
    if (value >= half && (bits <= 32 || value > half)) {
        value = -2 * half + value;
    }
    return value;
}
if (!Math["imul"] || Math["imul"](4294967295, 5) !== -5)
    Math["imul"] = function imul(a, b) {
        var ah = a >>> 16;
        var al = a & 65535;
        var bh = b >>> 16;
        var bl = b & 65535;
        return (al * bl + ((ah * bl + al * bh) << 16)) | 0;
    };
Math.imul = Math["imul"];
var Math_abs = Math.abs;
var Math_cos = Math.cos;
var Math_sin = Math.sin;
var Math_tan = Math.tan;
var Math_acos = Math.acos;
var Math_asin = Math.asin;
var Math_atan = Math.atan;
var Math_atan2 = Math.atan2;
var Math_exp = Math.exp;
var Math_log = Math.log;
var Math_sqrt = Math.sqrt;
var Math_ceil = Math.ceil;
var Math_floor = Math.floor;
var Math_pow = Math.pow;
var Math_imul = Math.imul;
var Math_fround = Math.fround;
var Math_min = Math.min;
var runDependencies = 0;
var runDependencyWatcher = null;
var dependenciesFulfilled = null;
function addRunDependency(id) {
    runDependencies++;
    if (Module["monitorRunDependencies"]) {
        Module["monitorRunDependencies"](runDependencies);
    }
}
Module["addRunDependency"] = addRunDependency;
function removeRunDependency(id) {
    runDependencies--;
    if (Module["monitorRunDependencies"]) {
        Module["monitorRunDependencies"](runDependencies);
    }
    if (runDependencies == 0) {
        if (runDependencyWatcher !== null) {
            clearInterval(runDependencyWatcher);
            runDependencyWatcher = null;
        }
        if (dependenciesFulfilled) {
            var callback = dependenciesFulfilled;
            dependenciesFulfilled = null;
            callback();
        }
    }
}
Module["removeRunDependency"] = removeRunDependency;
Module["preloadedImages"] = {};
Module["preloadedAudios"] = {};
var memoryInitializer = null;
STATIC_BASE = 8;
STATICTOP = STATIC_BASE + Runtime.alignMemory(3107);
__ATINIT__.push();
var memoryInitializer = "static/js/spc_snes.js.mem";
var tempDoublePtr = Runtime.alignMemory(allocate(12, "i8", ALLOC_STATIC), 8);
assert(tempDoublePtr % 8 == 0);
function copyTempFloat(ptr) {
    HEAP8[tempDoublePtr] = HEAP8[ptr];
    HEAP8[tempDoublePtr + 1] = HEAP8[ptr + 1];
    HEAP8[tempDoublePtr + 2] = HEAP8[ptr + 2];
    HEAP8[tempDoublePtr + 3] = HEAP8[ptr + 3];
}
function copyTempDouble(ptr) {
    HEAP8[tempDoublePtr] = HEAP8[ptr];
    HEAP8[tempDoublePtr + 1] = HEAP8[ptr + 1];
    HEAP8[tempDoublePtr + 2] = HEAP8[ptr + 2];
    HEAP8[tempDoublePtr + 3] = HEAP8[ptr + 3];
    HEAP8[tempDoublePtr + 4] = HEAP8[ptr + 4];
    HEAP8[tempDoublePtr + 5] = HEAP8[ptr + 5];
    HEAP8[tempDoublePtr + 6] = HEAP8[ptr + 6];
    HEAP8[tempDoublePtr + 7] = HEAP8[ptr + 7];
}
function _sbrk(bytes) {
    var self = _sbrk;
    if (!self.called) {
        DYNAMICTOP = alignMemoryPage(DYNAMICTOP);
        self.called = true;
        assert(Runtime.dynamicAlloc);
        self.alloc = Runtime.dynamicAlloc;
        Runtime.dynamicAlloc = function () {
            abort("cannot dynamically allocate, sbrk now has control");
        };
    }
    var ret = DYNAMICTOP;
    if (bytes != 0) self.alloc(bytes);
    return ret;
}
var ___errno_state = 0;
function ___setErrNo(value) {
    HEAP32[___errno_state >> 2] = value;
    return value;
}
var ERRNO_CODES = {
    EPERM: 1,
    ENOENT: 2,
    ESRCH: 3,
    EINTR: 4,
    EIO: 5,
    ENXIO: 6,
    E2BIG: 7,
    ENOEXEC: 8,
    EBADF: 9,
    ECHILD: 10,
    EAGAIN: 11,
    EWOULDBLOCK: 11,
    ENOMEM: 12,
    EACCES: 13,
    EFAULT: 14,
    ENOTBLK: 15,
    EBUSY: 16,
    EEXIST: 17,
    EXDEV: 18,
    ENODEV: 19,
    ENOTDIR: 20,
    EISDIR: 21,
    EINVAL: 22,
    ENFILE: 23,
    EMFILE: 24,
    ENOTTY: 25,
    ETXTBSY: 26,
    EFBIG: 27,
    ENOSPC: 28,
    ESPIPE: 29,
    EROFS: 30,
    EMLINK: 31,
    EPIPE: 32,
    EDOM: 33,
    ERANGE: 34,
    ENOMSG: 42,
    EIDRM: 43,
    ECHRNG: 44,
    EL2NSYNC: 45,
    EL3HLT: 46,
    EL3RST: 47,
    ELNRNG: 48,
    EUNATCH: 49,
    ENOCSI: 50,
    EL2HLT: 51,
    EDEADLK: 35,
    ENOLCK: 37,
    EBADE: 52,
    EBADR: 53,
    EXFULL: 54,
    ENOANO: 55,
    EBADRQC: 56,
    EBADSLT: 57,
    EDEADLOCK: 35,
    EBFONT: 59,
    ENOSTR: 60,
    ENODATA: 61,
    ETIME: 62,
    ENOSR: 63,
    ENONET: 64,
    ENOPKG: 65,
    EREMOTE: 66,
    ENOLINK: 67,
    EADV: 68,
    ESRMNT: 69,
    ECOMM: 70,
    EPROTO: 71,
    EMULTIHOP: 72,
    EDOTDOT: 73,
    EBADMSG: 74,
    ENOTUNIQ: 76,
    EBADFD: 77,
    EREMCHG: 78,
    ELIBACC: 79,
    ELIBBAD: 80,
    ELIBSCN: 81,
    ELIBMAX: 82,
    ELIBEXEC: 83,
    ENOSYS: 38,
    ENOTEMPTY: 39,
    ENAMETOOLONG: 36,
    ELOOP: 40,
    EOPNOTSUPP: 95,
    EPFNOSUPPORT: 96,
    ECONNRESET: 104,
    ENOBUFS: 105,
    EAFNOSUPPORT: 97,
    EPROTOTYPE: 91,
    ENOTSOCK: 88,
    ENOPROTOOPT: 92,
    ESHUTDOWN: 108,
    ECONNREFUSED: 111,
    EADDRINUSE: 98,
    ECONNABORTED: 103,
    ENETUNREACH: 101,
    ENETDOWN: 100,
    ETIMEDOUT: 110,
    EHOSTDOWN: 112,
    EHOSTUNREACH: 113,
    EINPROGRESS: 115,
    EALREADY: 114,
    EDESTADDRREQ: 89,
    EMSGSIZE: 90,
    EPROTONOSUPPORT: 93,
    ESOCKTNOSUPPORT: 94,
    EADDRNOTAVAIL: 99,
    ENETRESET: 102,
    EISCONN: 106,
    ENOTCONN: 107,
    ETOOMANYREFS: 109,
    EUSERS: 87,
    EDQUOT: 122,
    ESTALE: 116,
    ENOTSUP: 95,
    ENOMEDIUM: 123,
    EILSEQ: 84,
    EOVERFLOW: 75,
    ECANCELED: 125,
    ENOTRECOVERABLE: 131,
    EOWNERDEAD: 130,
    ESTRPIPE: 86,
};
function _sysconf(name) {
    switch (name) {
        case 30:
            return PAGE_SIZE;
        case 132:
        case 133:
        case 12:
        case 137:
        case 138:
        case 15:
        case 235:
        case 16:
        case 17:
        case 18:
        case 19:
        case 20:
        case 149:
        case 13:
        case 10:
        case 236:
        case 153:
        case 9:
        case 21:
        case 22:
        case 159:
        case 154:
        case 14:
        case 77:
        case 78:
        case 139:
        case 80:
        case 81:
        case 79:
        case 82:
        case 68:
        case 67:
        case 164:
        case 11:
        case 29:
        case 47:
        case 48:
        case 95:
        case 52:
        case 51:
        case 46:
            return 200809;
        case 27:
        case 246:
        case 127:
        case 128:
        case 23:
        case 24:
        case 160:
        case 161:
        case 181:
        case 182:
        case 242:
        case 183:
        case 184:
        case 243:
        case 244:
        case 245:
        case 165:
        case 178:
        case 179:
        case 49:
        case 50:
        case 168:
        case 169:
        case 175:
        case 170:
        case 171:
        case 172:
        case 97:
        case 76:
        case 32:
        case 173:
        case 35:
            return -1;
        case 176:
        case 177:
        case 7:
        case 155:
        case 8:
        case 157:
        case 125:
        case 126:
        case 92:
        case 93:
        case 129:
        case 130:
        case 131:
        case 94:
        case 91:
            return 1;
        case 74:
        case 60:
        case 69:
        case 70:
        case 4:
            return 1024;
        case 31:
        case 42:
        case 72:
            return 32;
        case 87:
        case 26:
        case 33:
            return 2147483647;
        case 34:
        case 1:
            return 47839;
        case 38:
        case 36:
            return 99;
        case 43:
        case 37:
            return 2048;
        case 0:
            return 2097152;
        case 3:
            return 65536;
        case 28:
            return 32768;
        case 44:
            return 32767;
        case 75:
            return 16384;
        case 39:
            return 1e3;
        case 89:
            return 700;
        case 71:
            return 256;
        case 40:
            return 255;
        case 2:
            return 100;
        case 180:
            return 64;
        case 25:
            return 20;
        case 5:
            return 16;
        case 6:
            return 6;
        case 73:
            return 4;
        case 84: {
            if (typeof navigator === "object") return navigator["hardwareConcurrency"] || 1;
            return 1;
        }
    }
    ___setErrNo(ERRNO_CODES.EINVAL);
    return -1;
}
var ERRNO_MESSAGES = {
    0: "Success",
    1: "Not super-user",
    2: "No such file or directory",
    3: "No such process",
    4: "Interrupted system call",
    5: "I/O error",
    6: "No such device or address",
    7: "Arg list too long",
    8: "Exec format error",
    9: "Bad file number",
    10: "No children",
    11: "No more processes",
    12: "Not enough core",
    13: "Permission denied",
    14: "Bad address",
    15: "Block device required",
    16: "Mount device busy",
    17: "File exists",
    18: "Cross-device link",
    19: "No such device",
    20: "Not a directory",
    21: "Is a directory",
    22: "Invalid argument",
    23: "Too many open files in system",
    24: "Too many open files",
    25: "Not a typewriter",
    26: "Text file busy",
    27: "File too large",
    28: "No space left on device",
    29: "Illegal seek",
    30: "Read only file system",
    31: "Too many links",
    32: "Broken pipe",
    33: "Math arg out of domain of func",
    34: "Math result not representable",
    35: "File locking deadlock error",
    36: "File or path name too long",
    37: "No record locks available",
    38: "Function not implemented",
    39: "Directory not empty",
    40: "Too many symbolic links",
    42: "No message of desired type",
    43: "Identifier removed",
    44: "Channel number out of range",
    45: "Level 2 not synchronized",
    46: "Level 3 halted",
    47: "Level 3 reset",
    48: "Link number out of range",
    49: "Protocol driver not attached",
    50: "No CSI structure available",
    51: "Level 2 halted",
    52: "Invalid exchange",
    53: "Invalid request descriptor",
    54: "Exchange full",
    55: "No anode",
    56: "Invalid request code",
    57: "Invalid slot",
    59: "Bad font file fmt",
    60: "Device not a stream",
    61: "No data (for no delay io)",
    62: "Timer expired",
    63: "Out of streams resources",
    64: "Machine is not on the network",
    65: "Package not installed",
    66: "The object is remote",
    67: "The link has been severed",
    68: "Advertise error",
    69: "Srmount error",
    70: "Communication error on send",
    71: "Protocol error",
    72: "Multihop attempted",
    73: "Cross mount point (not really error)",
    74: "Trying to read unreadable message",
    75: "Value too large for defined data type",
    76: "Given log. name not unique",
    77: "f.d. invalid for this operation",
    78: "Remote address changed",
    79: "Can   access a needed shared lib",
    80: "Accessing a corrupted shared lib",
    81: ".lib section in a.out corrupted",
    82: "Attempting to link in too many libs",
    83: "Attempting to exec a shared library",
    84: "Illegal byte sequence",
    86: "Streams pipe error",
    87: "Too many users",
    88: "Socket operation on non-socket",
    89: "Destination address required",
    90: "Message too long",
    91: "Protocol wrong type for socket",
    92: "Protocol not available",
    93: "Unknown protocol",
    94: "Socket type not supported",
    95: "Not supported",
    96: "Protocol family not supported",
    97: "Address family not supported by protocol family",
    98: "Address already in use",
    99: "Address not available",
    100: "Network interface is not configured",
    101: "Network is unreachable",
    102: "Connection reset by network",
    103: "Connection aborted",
    104: "Connection reset by peer",
    105: "No buffer space available",
    106: "Socket is already connected",
    107: "Socket is not connected",
    108: "Can't send after socket shutdown",
    109: "Too many references",
    110: "Connection timed out",
    111: "Connection refused",
    112: "Host is down",
    113: "Host is unreachable",
    114: "Socket already connected",
    115: "Connection already in progress",
    116: "Stale file handle",
    122: "Quota exceeded",
    123: "No medium (in tape drive)",
    125: "Operation canceled",
    130: "Previous owner died",
    131: "State not recoverable",
};
var PATH = {
    splitPath: function (filename) {
        var splitPathRe = /^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/;
        return splitPathRe.exec(filename).slice(1);
    },
    normalizeArray: function (parts, allowAboveRoot) {
        var up = 0;
        for (var i = parts.length - 1; i >= 0; i--) {
            var last = parts[i];
            if (last === ".") {
                parts.splice(i, 1);
            } else if (last === "..") {
                parts.splice(i, 1);
                up++;
            } else if (up) {
                parts.splice(i, 1);
                up--;
            }
        }
        if (allowAboveRoot) {
            for (; up--; up) {
                parts.unshift("..");
            }
        }
        return parts;
    },
    normalize: function (path) {
        var isAbsolute = path.charAt(0) === "/",
            trailingSlash = path.substr(-1) === "/";
        path = PATH.normalizeArray(
            path.split("/").filter(function (p) {
                return !!p;
            }),
            !isAbsolute
        ).join("/");
        if (!path && !isAbsolute) {
            path = ".";
        }
        if (path && trailingSlash) {
            path += "/";
        }
        return (isAbsolute ? "/" : "") + path;
    },
    dirname: function (path) {
        var result = PATH.splitPath(path),
            root = result[0],
            dir = result[1];
        if (!root && !dir) {
            return ".";
        }
        if (dir) {
            dir = dir.substr(0, dir.length - 1);
        }
        return root + dir;
    },
    basename: function (path) {
        if (path === "/") return "/";
        var lastSlash = path.lastIndexOf("/");
        if (lastSlash === -1) return path;
        return path.substr(lastSlash + 1);
    },
    extname: function (path) {
        return PATH.splitPath(path)[3];
    },
    join: function () {
        var paths = Array.prototype.slice.call(arguments, 0);
        return PATH.normalize(paths.join("/"));
    },
    join2: function (l, r) {
        return PATH.normalize(l + "/" + r);
    },
    resolve: function () {
        var resolvedPath = "",
            resolvedAbsolute = false;
        for (var i = arguments.length - 1; i >= -1 && !resolvedAbsolute; i--) {
            var path = i >= 0 ? arguments[i] : FS.cwd();
            if (typeof path !== "string") {
                throw new TypeError("Arguments to path.resolve must be strings");
            } else if (!path) {
                return "";
            }
            resolvedPath = path + "/" + resolvedPath;
            resolvedAbsolute = path.charAt(0) === "/";
        }
        resolvedPath = PATH.normalizeArray(
            resolvedPath.split("/").filter(function (p) {
                return !!p;
            }),
            !resolvedAbsolute
        ).join("/");
        return (resolvedAbsolute ? "/" : "") + resolvedPath || ".";
    },
    relative: function (from, to) {
        from = PATH.resolve(from).substr(1);
        to = PATH.resolve(to).substr(1);
        function trim(arr) {
            var start = 0;
            for (; start < arr.length; start++) {
                if (arr[start] !== "") break;
            }
            var end = arr.length - 1;
            for (; end >= 0; end--) {
                if (arr[end] !== "") break;
            }
            if (start > end) return [];
            return arr.slice(start, end - start + 1);
        }
        var fromParts = trim(from.split("/"));
        var toParts = trim(to.split("/"));
        var length = Math.min(fromParts.length, toParts.length);
        var samePartsLength = length;
        for (var i = 0; i < length; i++) {
            if (fromParts[i] !== toParts[i]) {
                samePartsLength = i;
                break;
            }
        }
        var outputParts = [];
        for (var i = samePartsLength; i < fromParts.length; i++) {
            outputParts.push("..");
        }
        outputParts = outputParts.concat(toParts.slice(samePartsLength));
        return outputParts.join("/");
    },
};
var TTY = {
    ttys: [],
    init: function () {},
    shutdown: function () {},
    register: function (dev, ops) {
        TTY.ttys[dev] = { input: [], output: [], ops: ops };
        FS.registerDevice(dev, TTY.stream_ops);
    },
    stream_ops: {
        open: function (stream) {
            var tty = TTY.ttys[stream.node.rdev];
            if (!tty) {
                throw new FS.ErrnoError(ERRNO_CODES.ENODEV);
            }
            stream.tty = tty;
            stream.seekable = false;
        },
        close: function (stream) {
            if (stream.tty.output.length) {
                stream.tty.ops.put_char(stream.tty, 10);
            }
        },
        read: function (stream, buffer, offset, length, pos) {
            if (!stream.tty || !stream.tty.ops.get_char) {
                throw new FS.ErrnoError(ERRNO_CODES.ENXIO);
            }
            var bytesRead = 0;
            for (var i = 0; i < length; i++) {
                var result;
                try {
                    result = stream.tty.ops.get_char(stream.tty);
                } catch (e) {
                    throw new FS.ErrnoError(ERRNO_CODES.EIO);
                }
                if (result === undefined && bytesRead === 0) {
                    throw new FS.ErrnoError(ERRNO_CODES.EAGAIN);
                }
                if (result === null || result === undefined) break;
                bytesRead++;
                buffer[offset + i] = result;
            }
            if (bytesRead) {
                stream.node.timestamp = Date.now();
            }
            return bytesRead;
        },
        write: function (stream, buffer, offset, length, pos) {
            if (!stream.tty || !stream.tty.ops.put_char) {
                throw new FS.ErrnoError(ERRNO_CODES.ENXIO);
            }
            for (var i = 0; i < length; i++) {
                try {
                    stream.tty.ops.put_char(stream.tty, buffer[offset + i]);
                } catch (e) {
                    throw new FS.ErrnoError(ERRNO_CODES.EIO);
                }
            }
            if (length) {
                stream.node.timestamp = Date.now();
            }
            return i;
        },
    },
    default_tty_ops: {
        get_char: function (tty) {
            if (!tty.input.length) {
                var result = null;
                if (ENVIRONMENT_IS_NODE) {
                    result = process["stdin"]["read"]();
                    if (!result) {
                        if (process["stdin"]["_readableState"] && process["stdin"]["_readableState"]["ended"]) {
                            return null;
                        }
                        return undefined;
                    }
                } else if (typeof window != "undefined" && typeof window.prompt == "function") {
                    result = window.prompt("Input: ");
                    if (result !== null) {
                        result += "\n";
                    }
                } else if (typeof readline == "function") {
                    result = readline();
                    if (result !== null) {
                        result += "\n";
                    }
                }
                if (!result) {
                    return null;
                }
                tty.input = intArrayFromString(result, true);
            }
            return tty.input.shift();
        },
        put_char: function (tty, val) {
            if (val === null || val === 10) {
                Module["print"](tty.output.join(""));
                tty.output = [];
            } else {
                tty.output.push(TTY.utf8.processCChar(val));
            }
        },
    },
    default_tty1_ops: {
        put_char: function (tty, val) {
            if (val === null || val === 10) {
                Module["printErr"](tty.output.join(""));
                tty.output = [];
            } else {
                tty.output.push(TTY.utf8.processCChar(val));
            }
        },
    },
};
var MEMFS = {
    ops_table: null,
    mount: function (mount) {
        return MEMFS.createNode(null, "/", 16384 | 511, 0);
    },
    createNode: function (parent, name, mode, dev) {
        if (FS.isBlkdev(mode) || FS.isFIFO(mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        if (!MEMFS.ops_table) {
            MEMFS.ops_table = {
                dir: {
                    node: {
                        getattr: MEMFS.node_ops.getattr,
                        setattr: MEMFS.node_ops.setattr,
                        lookup: MEMFS.node_ops.lookup,
                        mknod: MEMFS.node_ops.mknod,
                        rename: MEMFS.node_ops.rename,
                        unlink: MEMFS.node_ops.unlink,
                        rmdir: MEMFS.node_ops.rmdir,
                        readdir: MEMFS.node_ops.readdir,
                        symlink: MEMFS.node_ops.symlink,
                    },
                    stream: { llseek: MEMFS.stream_ops.llseek },
                },
                file: {
                    node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr },
                    stream: { llseek: MEMFS.stream_ops.llseek, read: MEMFS.stream_ops.read, write: MEMFS.stream_ops.write, allocate: MEMFS.stream_ops.allocate, mmap: MEMFS.stream_ops.mmap },
                },
                link: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr, readlink: MEMFS.node_ops.readlink }, stream: {} },
                chrdev: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr }, stream: FS.chrdev_stream_ops },
            };
        }
        var node = FS.createNode(parent, name, mode, dev);
        if (FS.isDir(node.mode)) {
            node.node_ops = MEMFS.ops_table.dir.node;
            node.stream_ops = MEMFS.ops_table.dir.stream;
            node.contents = {};
        } else if (FS.isFile(node.mode)) {
            node.node_ops = MEMFS.ops_table.file.node;
            node.stream_ops = MEMFS.ops_table.file.stream;
            node.usedBytes = 0;
            node.contents = null;
        } else if (FS.isLink(node.mode)) {
            node.node_ops = MEMFS.ops_table.link.node;
            node.stream_ops = MEMFS.ops_table.link.stream;
        } else if (FS.isChrdev(node.mode)) {
            node.node_ops = MEMFS.ops_table.chrdev.node;
            node.stream_ops = MEMFS.ops_table.chrdev.stream;
        }
        node.timestamp = Date.now();
        if (parent) {
            parent.contents[name] = node;
        }
        return node;
    },
    getFileDataAsRegularArray: function (node) {
        if (node.contents && node.contents.subarray) {
            var arr = [];
            for (var i = 0; i < node.usedBytes; ++i) arr.push(node.contents[i]);
            return arr;
        }
        return node.contents;
    },
    getFileDataAsTypedArray: function (node) {
        if (node.contents && node.contents.subarray) return node.contents.subarray(0, node.usedBytes);
        return new Uint8Array(node.contents);
    },
    expandFileStorage: function (node, newCapacity) {
        if (node.contents && node.contents.subarray && newCapacity > node.contents.length) {
            node.contents = MEMFS.getFileDataAsRegularArray(node);
            node.usedBytes = node.contents.length;
        }
        if (!node.contents || node.contents.subarray) {
            var prevCapacity = node.contents ? node.contents.buffer.byteLength : 0;
            if (prevCapacity >= newCapacity) return;
            var CAPACITY_DOUBLING_MAX = 1024 * 1024;
            newCapacity = Math.max(newCapacity, (prevCapacity * (prevCapacity < CAPACITY_DOUBLING_MAX ? 2 : 1.125)) | 0);
            if (prevCapacity != 0) newCapacity = Math.max(newCapacity, 256);
            var oldContents = node.contents;
            node.contents = new Uint8Array(newCapacity);
            if (node.usedBytes > 0) node.contents.set(oldContents.subarray(0, node.usedBytes), 0);
            return;
        }
        if (!node.contents && newCapacity > 0) node.contents = [];
        while (node.contents.length < newCapacity) node.contents.push(0);
    },
    resizeFileStorage: function (node, newSize) {
        if (node.usedBytes == newSize) return;
        if (newSize == 0) {
            node.contents = null;
            node.usedBytes = 0;
            return;
        }
        if (!node.contents || node.contents.subarray) {
            var oldContents = node.contents;
            node.contents = new Uint8Array(new ArrayBuffer(newSize));
            if (oldContents) {
                node.contents.set(oldContents.subarray(0, Math.min(newSize, node.usedBytes)));
            }
            node.usedBytes = newSize;
            return;
        }
        if (!node.contents) node.contents = [];
        if (node.contents.length > newSize) node.contents.length = newSize;
        else while (node.contents.length < newSize) node.contents.push(0);
        node.usedBytes = newSize;
    },
    node_ops: {
        getattr: function (node) {
            var attr = {};
            attr.dev = FS.isChrdev(node.mode) ? node.id : 1;
            attr.ino = node.id;
            attr.mode = node.mode;
            attr.nlink = 1;
            attr.uid = 0;
            attr.gid = 0;
            attr.rdev = node.rdev;
            if (FS.isDir(node.mode)) {
                attr.size = 4096;
            } else if (FS.isFile(node.mode)) {
                attr.size = node.usedBytes;
            } else if (FS.isLink(node.mode)) {
                attr.size = node.link.length;
            } else {
                attr.size = 0;
            }
            attr.atime = new Date(node.timestamp);
            attr.mtime = new Date(node.timestamp);
            attr.ctime = new Date(node.timestamp);
            attr.blksize = 4096;
            attr.blocks = Math.ceil(attr.size / attr.blksize);
            return attr;
        },
        setattr: function (node, attr) {
            if (attr.mode !== undefined) {
                node.mode = attr.mode;
            }
            if (attr.timestamp !== undefined) {
                node.timestamp = attr.timestamp;
            }
            if (attr.size !== undefined) {
                MEMFS.resizeFileStorage(node, attr.size);
            }
        },
        lookup: function (parent, name) {
            throw FS.genericErrors[ERRNO_CODES.ENOENT];
        },
        mknod: function (parent, name, mode, dev) {
            return MEMFS.createNode(parent, name, mode, dev);
        },
        rename: function (old_node, new_dir, new_name) {
            if (FS.isDir(old_node.mode)) {
                var new_node;
                try {
                    new_node = FS.lookupNode(new_dir, new_name);
                } catch (e) {}
                if (new_node) {
                    for (var i in new_node.contents) {
                        throw new FS.ErrnoError(ERRNO_CODES.ENOTEMPTY);
                    }
                }
            }
            delete old_node.parent.contents[old_node.name];
            old_node.name = new_name;
            new_dir.contents[new_name] = old_node;
            old_node.parent = new_dir;
        },
        unlink: function (parent, name) {
            delete parent.contents[name];
        },
        rmdir: function (parent, name) {
            var node = FS.lookupNode(parent, name);
            for (var i in node.contents) {
                throw new FS.ErrnoError(ERRNO_CODES.ENOTEMPTY);
            }
            delete parent.contents[name];
        },
        readdir: function (node) {
            var entries = [".", ".."];
            for (var key in node.contents) {
                if (!node.contents.hasOwnProperty(key)) {
                    continue;
                }
                entries.push(key);
            }
            return entries;
        },
        symlink: function (parent, newname, oldpath) {
            var node = MEMFS.createNode(parent, newname, 511 | 40960, 0);
            node.link = oldpath;
            return node;
        },
        readlink: function (node) {
            if (!FS.isLink(node.mode)) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            return node.link;
        },
    },
    stream_ops: {
        read: function (stream, buffer, offset, length, position) {
            var contents = stream.node.contents;
            if (position >= stream.node.usedBytes) return 0;
            var size = Math.min(stream.node.usedBytes - position, length);
            assert(size >= 0);
            if (size > 8 && contents.subarray) {
                buffer.set(contents.subarray(position, position + size), offset);
            } else {
                for (var i = 0; i < size; i++) buffer[offset + i] = contents[position + i];
            }
            return size;
        },
        write: function (stream, buffer, offset, length, position, canOwn) {
            if (!length) return 0;
            var node = stream.node;
            node.timestamp = Date.now();
            if (buffer.subarray && (!node.contents || node.contents.subarray)) {
                if (canOwn) {
                    node.contents = buffer.subarray(offset, offset + length);
                    node.usedBytes = length;
                    return length;
                } else if (node.usedBytes === 0 && position === 0) {
                    node.contents = new Uint8Array(buffer.subarray(offset, offset + length));
                    node.usedBytes = length;
                    return length;
                } else if (position + length <= node.usedBytes) {
                    node.contents.set(buffer.subarray(offset, offset + length), position);
                    return length;
                }
            }
            MEMFS.expandFileStorage(node, position + length);
            if (node.contents.subarray && buffer.subarray) node.contents.set(buffer.subarray(offset, offset + length), position);
            else
                for (var i = 0; i < length; i++) {
                    node.contents[position + i] = buffer[offset + i];
                }
            node.usedBytes = Math.max(node.usedBytes, position + length);
            return length;
        },
        llseek: function (stream, offset, whence) {
            var position = offset;
            if (whence === 1) {
                position += stream.position;
            } else if (whence === 2) {
                if (FS.isFile(stream.node.mode)) {
                    position += stream.node.usedBytes;
                }
            }
            if (position < 0) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            stream.ungotten = [];
            stream.position = position;
            return position;
        },
        allocate: function (stream, offset, length) {
            MEMFS.expandFileStorage(stream.node, offset + length);
            stream.node.usedBytes = Math.max(stream.node.usedBytes, offset + length);
        },
        mmap: function (stream, buffer, offset, length, position, prot, flags) {
            if (!FS.isFile(stream.node.mode)) {
                throw new FS.ErrnoError(ERRNO_CODES.ENODEV);
            }
            var ptr;
            var allocated;
            var contents = stream.node.contents;
            if (!(flags & 2) && (contents.buffer === buffer || contents.buffer === buffer.buffer)) {
                allocated = false;
                ptr = contents.byteOffset;
            } else {
                if (position > 0 || position + length < stream.node.usedBytes) {
                    if (contents.subarray) {
                        contents = contents.subarray(position, position + length);
                    } else {
                        contents = Array.prototype.slice.call(contents, position, position + length);
                    }
                }
                allocated = true;
                ptr = _malloc(length);
                if (!ptr) {
                    throw new FS.ErrnoError(ERRNO_CODES.ENOMEM);
                }
                buffer.set(contents, ptr);
            }
            return { ptr: ptr, allocated: allocated };
        },
    },
};
var IDBFS = {
    dbs: {},
    indexedDB: function () {
        if (typeof indexedDB !== "undefined") return indexedDB;
        var ret = null;
        if (typeof window === "object") ret = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
        assert(ret, "IDBFS used, but indexedDB not supported");
        return ret;
    },
    DB_VERSION: 21,
    DB_STORE_NAME: "FILE_DATA",
    mount: function (mount) {
        return MEMFS.mount.apply(null, arguments);
    },
    syncfs: function (mount, populate, callback) {
        IDBFS.getLocalSet(mount, function (err, local) {
            if (err) return callback(err);
            IDBFS.getRemoteSet(mount, function (err, remote) {
                if (err) return callback(err);
                var src = populate ? remote : local;
                var dst = populate ? local : remote;
                IDBFS.reconcile(src, dst, callback);
            });
        });
    },
    getDB: function (name, callback) {
        var db = IDBFS.dbs[name];
        if (db) {
            return callback(null, db);
        }
        var req;
        try {
            req = IDBFS.indexedDB().open(name, IDBFS.DB_VERSION);
        } catch (e) {
            return callback(e);
        }
        req.onupgradeneeded = function (e) {
            var db = e.target.result;
            var transaction = e.target.transaction;
            var fileStore;
            if (db.objectStoreNames.contains(IDBFS.DB_STORE_NAME)) {
                fileStore = transaction.objectStore(IDBFS.DB_STORE_NAME);
            } else {
                fileStore = db.createObjectStore(IDBFS.DB_STORE_NAME);
            }
            fileStore.createIndex("timestamp", "timestamp", { unique: false });
        };
        req.onsuccess = function () {
            db = req.result;
            IDBFS.dbs[name] = db;
            callback(null, db);
        };
        req.onerror = function () {
            callback(this.error);
        };
    },
    getLocalSet: function (mount, callback) {
        var entries = {};
        function isRealDir(p) {
            return p !== "." && p !== "..";
        }
        function toAbsolute(root) {
            return function (p) {
                return PATH.join2(root, p);
            };
        }
        var check = FS.readdir(mount.mountpoint).filter(isRealDir).map(toAbsolute(mount.mountpoint));
        while (check.length) {
            var path = check.pop();
            var stat;
            try {
                stat = FS.stat(path);
            } catch (e) {
                return callback(e);
            }
            if (FS.isDir(stat.mode)) {
                check.push.apply(check, FS.readdir(path).filter(isRealDir).map(toAbsolute(path)));
            }
            entries[path] = { timestamp: stat.mtime };
        }
        return callback(null, { type: "local", entries: entries });
    },
    getRemoteSet: function (mount, callback) {
        var entries = {};
        IDBFS.getDB(mount.mountpoint, function (err, db) {
            if (err) return callback(err);
            var transaction = db.transaction([IDBFS.DB_STORE_NAME], "readonly");
            transaction.onerror = function () {
                callback(this.error);
            };
            var store = transaction.objectStore(IDBFS.DB_STORE_NAME);
            var index = store.index("timestamp");
            index.openKeyCursor().onsuccess = function (event) {
                var cursor = event.target.result;
                if (!cursor) {
                    return callback(null, { type: "remote", db: db, entries: entries });
                }
                entries[cursor.primaryKey] = { timestamp: cursor.key };
                cursor.continue();
            };
        });
    },
    loadLocalEntry: function (path, callback) {
        var stat, node;
        try {
            var lookup = FS.lookupPath(path);
            node = lookup.node;
            stat = FS.stat(path);
        } catch (e) {
            return callback(e);
        }
        if (FS.isDir(stat.mode)) {
            return callback(null, { timestamp: stat.mtime, mode: stat.mode });
        } else if (FS.isFile(stat.mode)) {
            node.contents = MEMFS.getFileDataAsTypedArray(node);
            return callback(null, { timestamp: stat.mtime, mode: stat.mode, contents: node.contents });
        } else {
            return callback(new Error("node type not supported"));
        }
    },
    storeLocalEntry: function (path, entry, callback) {
        try {
            if (FS.isDir(entry.mode)) {
                FS.mkdir(path, entry.mode);
            } else if (FS.isFile(entry.mode)) {
                FS.writeFile(path, entry.contents, { encoding: "binary", canOwn: true });
            } else {
                return callback(new Error("node type not supported"));
            }
            FS.utime(path, entry.timestamp, entry.timestamp);
        } catch (e) {
            return callback(e);
        }
        callback(null);
    },
    removeLocalEntry: function (path, callback) {
        try {
            var lookup = FS.lookupPath(path);
            var stat = FS.stat(path);
            if (FS.isDir(stat.mode)) {
                FS.rmdir(path);
            } else if (FS.isFile(stat.mode)) {
                FS.unlink(path);
            }
        } catch (e) {
            return callback(e);
        }
        callback(null);
    },
    loadRemoteEntry: function (store, path, callback) {
        var req = store.get(path);
        req.onsuccess = function (event) {
            callback(null, event.target.result);
        };
        req.onerror = function () {
            callback(this.error);
        };
    },
    storeRemoteEntry: function (store, path, entry, callback) {
        var req = store.put(entry, path);
        req.onsuccess = function () {
            callback(null);
        };
        req.onerror = function () {
            callback(this.error);
        };
    },
    removeRemoteEntry: function (store, path, callback) {
        var req = store.delete(path);
        req.onsuccess = function () {
            callback(null);
        };
        req.onerror = function () {
            callback(this.error);
        };
    },
    reconcile: function (src, dst, callback) {
        var total = 0;
        var create = [];
        Object.keys(src.entries).forEach(function (key) {
            var e = src.entries[key];
            var e2 = dst.entries[key];
            if (!e2 || e.timestamp > e2.timestamp) {
                create.push(key);
                total++;
            }
        });
        var remove = [];
        Object.keys(dst.entries).forEach(function (key) {
            var e = dst.entries[key];
            var e2 = src.entries[key];
            if (!e2) {
                remove.push(key);
                total++;
            }
        });
        if (!total) {
            return callback(null);
        }
        var errored = false;
        var completed = 0;
        var db = src.type === "remote" ? src.db : dst.db;
        var transaction = db.transaction([IDBFS.DB_STORE_NAME], "readwrite");
        var store = transaction.objectStore(IDBFS.DB_STORE_NAME);
        function done(err) {
            if (err) {
                if (!done.errored) {
                    done.errored = true;
                    return callback(err);
                }
                return;
            }
            if (++completed >= total) {
                return callback(null);
            }
        }
        transaction.onerror = function () {
            done(this.error);
        };
        create.sort().forEach(function (path) {
            if (dst.type === "local") {
                IDBFS.loadRemoteEntry(store, path, function (err, entry) {
                    if (err) return done(err);
                    IDBFS.storeLocalEntry(path, entry, done);
                });
            } else {
                IDBFS.loadLocalEntry(path, function (err, entry) {
                    if (err) return done(err);
                    IDBFS.storeRemoteEntry(store, path, entry, done);
                });
            }
        });
        remove
            .sort()
            .reverse()
            .forEach(function (path) {
                if (dst.type === "local") {
                    IDBFS.removeLocalEntry(path, done);
                } else {
                    IDBFS.removeRemoteEntry(store, path, done);
                }
            });
    },
};
var NODEFS = {
    isWindows: false,
    staticInit: function () {
        NODEFS.isWindows = !!process.platform.match(/^win/);
    },
    mount: function (mount) {
        assert(ENVIRONMENT_IS_NODE);
        return NODEFS.createNode(null, "/", NODEFS.getMode(mount.opts.root), 0);
    },
    createNode: function (parent, name, mode, dev) {
        if (!FS.isDir(mode) && !FS.isFile(mode) && !FS.isLink(mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var node = FS.createNode(parent, name, mode);
        node.node_ops = NODEFS.node_ops;
        node.stream_ops = NODEFS.stream_ops;
        return node;
    },
    getMode: function (path) {
        var stat;
        try {
            stat = fs.lstatSync(path);
            if (NODEFS.isWindows) {
                stat.mode = stat.mode | ((stat.mode & 146) >> 1);
            }
        } catch (e) {
            if (!e.code) throw e;
            throw new FS.ErrnoError(ERRNO_CODES[e.code]);
        }
        return stat.mode;
    },
    realPath: function (node) {
        var parts = [];
        while (node.parent !== node) {
            parts.push(node.name);
            node = node.parent;
        }
        parts.push(node.mount.opts.root);
        parts.reverse();
        return PATH.join.apply(null, parts);
    },
    flagsToPermissionStringMap: {
        0: "r",
        1: "r+",
        2: "r+",
        64: "r",
        65: "r+",
        66: "r+",
        129: "rx+",
        193: "rx+",
        514: "w+",
        577: "w",
        578: "w+",
        705: "wx",
        706: "wx+",
        1024: "a",
        1025: "a",
        1026: "a+",
        1089: "a",
        1090: "a+",
        1153: "ax",
        1154: "ax+",
        1217: "ax",
        1218: "ax+",
        4096: "rs",
        4098: "rs+",
    },
    flagsToPermissionString: function (flags) {
        if (flags in NODEFS.flagsToPermissionStringMap) {
            return NODEFS.flagsToPermissionStringMap[flags];
        } else {
            return flags;
        }
    },
    node_ops: {
        getattr: function (node) {
            var path = NODEFS.realPath(node);
            var stat;
            try {
                stat = fs.lstatSync(path);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
            if (NODEFS.isWindows && !stat.blksize) {
                stat.blksize = 4096;
            }
            if (NODEFS.isWindows && !stat.blocks) {
                stat.blocks = ((stat.size + stat.blksize - 1) / stat.blksize) | 0;
            }
            return {
                dev: stat.dev,
                ino: stat.ino,
                mode: stat.mode,
                nlink: stat.nlink,
                uid: stat.uid,
                gid: stat.gid,
                rdev: stat.rdev,
                size: stat.size,
                atime: stat.atime,
                mtime: stat.mtime,
                ctime: stat.ctime,
                blksize: stat.blksize,
                blocks: stat.blocks,
            };
        },
        setattr: function (node, attr) {
            var path = NODEFS.realPath(node);
            try {
                if (attr.mode !== undefined) {
                    fs.chmodSync(path, attr.mode);
                    node.mode = attr.mode;
                }
                if (attr.timestamp !== undefined) {
                    var date = new Date(attr.timestamp);
                    fs.utimesSync(path, date, date);
                }
                if (attr.size !== undefined) {
                    fs.truncateSync(path, attr.size);
                }
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        lookup: function (parent, name) {
            var path = PATH.join2(NODEFS.realPath(parent), name);
            var mode = NODEFS.getMode(path);
            return NODEFS.createNode(parent, name, mode);
        },
        mknod: function (parent, name, mode, dev) {
            var node = NODEFS.createNode(parent, name, mode, dev);
            var path = NODEFS.realPath(node);
            try {
                if (FS.isDir(node.mode)) {
                    fs.mkdirSync(path, node.mode);
                } else {
                    fs.writeFileSync(path, "", { mode: node.mode });
                }
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
            return node;
        },
        rename: function (oldNode, newDir, newName) {
            var oldPath = NODEFS.realPath(oldNode);
            var newPath = PATH.join2(NODEFS.realPath(newDir), newName);
            try {
                fs.renameSync(oldPath, newPath);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        unlink: function (parent, name) {
            var path = PATH.join2(NODEFS.realPath(parent), name);
            try {
                fs.unlinkSync(path);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        rmdir: function (parent, name) {
            var path = PATH.join2(NODEFS.realPath(parent), name);
            try {
                fs.rmdirSync(path);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        readdir: function (node) {
            var path = NODEFS.realPath(node);
            try {
                return fs.readdirSync(path);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        symlink: function (parent, newName, oldPath) {
            var newPath = PATH.join2(NODEFS.realPath(parent), newName);
            try {
                fs.symlinkSync(oldPath, newPath);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        readlink: function (node) {
            var path = NODEFS.realPath(node);
            try {
                return fs.readlinkSync(path);
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
    },
    stream_ops: {
        open: function (stream) {
            var path = NODEFS.realPath(stream.node);
            try {
                if (FS.isFile(stream.node.mode)) {
                    stream.nfd = fs.openSync(path, NODEFS.flagsToPermissionString(stream.flags));
                }
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        close: function (stream) {
            try {
                if (FS.isFile(stream.node.mode) && stream.nfd) {
                    fs.closeSync(stream.nfd);
                }
            } catch (e) {
                if (!e.code) throw e;
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
        },
        read: function (stream, buffer, offset, length, position) {
            var nbuffer = new Buffer(length);
            var res;
            try {
                res = fs.readSync(stream.nfd, nbuffer, 0, length, position);
            } catch (e) {
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
            if (res > 0) {
                for (var i = 0; i < res; i++) {
                    buffer[offset + i] = nbuffer[i];
                }
            }
            return res;
        },
        write: function (stream, buffer, offset, length, position) {
            var nbuffer = new Buffer(buffer.subarray(offset, offset + length));
            var res;
            try {
                res = fs.writeSync(stream.nfd, nbuffer, 0, length, position);
            } catch (e) {
                throw new FS.ErrnoError(ERRNO_CODES[e.code]);
            }
            return res;
        },
        llseek: function (stream, offset, whence) {
            var position = offset;
            if (whence === 1) {
                position += stream.position;
            } else if (whence === 2) {
                if (FS.isFile(stream.node.mode)) {
                    try {
                        var stat = fs.fstatSync(stream.nfd);
                        position += stat.size;
                    } catch (e) {
                        throw new FS.ErrnoError(ERRNO_CODES[e.code]);
                    }
                }
            }
            if (position < 0) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            stream.position = position;
            return position;
        },
    },
};
var _stdin = allocate(1, "i32*", ALLOC_STATIC);
var _stdout = allocate(1, "i32*", ALLOC_STATIC);
var _stderr = allocate(1, "i32*", ALLOC_STATIC);
function _fflush(stream) {}
var FS = {
    root: null,
    mounts: [],
    devices: [null],
    streams: [],
    nextInode: 1,
    nameTable: null,
    currentPath: "/",
    initialized: false,
    ignorePermissions: true,
    trackingDelegate: {},
    tracking: { openFlags: { READ: 1, WRITE: 2 } },
    ErrnoError: null,
    genericErrors: {},
    handleFSError: function (e) {
        if (!(e instanceof FS.ErrnoError)) throw e + " : " + stackTrace();
        return ___setErrNo(e.errno);
    },
    lookupPath: function (path, opts) {
        path = PATH.resolve(FS.cwd(), path);
        opts = opts || {};
        if (!path) return { path: "", node: null };
        var defaults = { follow_mount: true, recurse_count: 0 };
        for (var key in defaults) {
            if (opts[key] === undefined) {
                opts[key] = defaults[key];
            }
        }
        if (opts.recurse_count > 8) {
            throw new FS.ErrnoError(ERRNO_CODES.ELOOP);
        }
        var parts = PATH.normalizeArray(
            path.split("/").filter(function (p) {
                return !!p;
            }),
            false
        );
        var current = FS.root;
        var current_path = "/";
        for (var i = 0; i < parts.length; i++) {
            var islast = i === parts.length - 1;
            if (islast && opts.parent) {
                break;
            }
            current = FS.lookupNode(current, parts[i]);
            current_path = PATH.join2(current_path, parts[i]);
            if (FS.isMountpoint(current)) {
                if (!islast || (islast && opts.follow_mount)) {
                    current = current.mounted.root;
                }
            }
            if (!islast || opts.follow) {
                var count = 0;
                while (FS.isLink(current.mode)) {
                    var link = FS.readlink(current_path);
                    current_path = PATH.resolve(PATH.dirname(current_path), link);
                    var lookup = FS.lookupPath(current_path, { recurse_count: opts.recurse_count });
                    current = lookup.node;
                    if (count++ > 40) {
                        throw new FS.ErrnoError(ERRNO_CODES.ELOOP);
                    }
                }
            }
        }
        return { path: current_path, node: current };
    },
    getPath: function (node) {
        var path;
        while (true) {
            if (FS.isRoot(node)) {
                var mount = node.mount.mountpoint;
                if (!path) return mount;
                return mount[mount.length - 1] !== "/" ? mount + "/" + path : mount + path;
            }
            path = path ? node.name + "/" + path : node.name;
            node = node.parent;
        }
    },
    hashName: function (parentid, name) {
        var hash = 0;
        for (var i = 0; i < name.length; i++) {
            hash = ((hash << 5) - hash + name.charCodeAt(i)) | 0;
        }
        return ((parentid + hash) >>> 0) % FS.nameTable.length;
    },
    hashAddNode: function (node) {
        var hash = FS.hashName(node.parent.id, node.name);
        node.name_next = FS.nameTable[hash];
        FS.nameTable[hash] = node;
    },
    hashRemoveNode: function (node) {
        var hash = FS.hashName(node.parent.id, node.name);
        if (FS.nameTable[hash] === node) {
            FS.nameTable[hash] = node.name_next;
        } else {
            var current = FS.nameTable[hash];
            while (current) {
                if (current.name_next === node) {
                    current.name_next = node.name_next;
                    break;
                }
                current = current.name_next;
            }
        }
    },
    lookupNode: function (parent, name) {
        var err = FS.mayLookup(parent);
        if (err) {
            throw new FS.ErrnoError(err, parent);
        }
        var hash = FS.hashName(parent.id, name);
        for (var node = FS.nameTable[hash]; node; node = node.name_next) {
            var nodeName = node.name;
            if (node.parent.id === parent.id && nodeName === name) {
                return node;
            }
        }
        return FS.lookup(parent, name);
    },
    createNode: function (parent, name, mode, rdev) {
        if (!FS.FSNode) {
            FS.FSNode = function (parent, name, mode, rdev) {
                if (!parent) {
                    parent = this;
                }
                this.parent = parent;
                this.mount = parent.mount;
                this.mounted = null;
                this.id = FS.nextInode++;
                this.name = name;
                this.mode = mode;
                this.node_ops = {};
                this.stream_ops = {};
                this.rdev = rdev;
            };
            FS.FSNode.prototype = {};
            var readMode = 292 | 73;
            var writeMode = 146;
            Object.defineProperties(FS.FSNode.prototype, {
                read: {
                    get: function () {
                        return (this.mode & readMode) === readMode;
                    },
                    set: function (val) {
                        val ? (this.mode |= readMode) : (this.mode &= ~readMode);
                    },
                },
                write: {
                    get: function () {
                        return (this.mode & writeMode) === writeMode;
                    },
                    set: function (val) {
                        val ? (this.mode |= writeMode) : (this.mode &= ~writeMode);
                    },
                },
                isFolder: {
                    get: function () {
                        return FS.isDir(this.mode);
                    },
                },
                isDevice: {
                    get: function () {
                        return FS.isChrdev(this.mode);
                    },
                },
            });
        }
        var node = new FS.FSNode(parent, name, mode, rdev);
        FS.hashAddNode(node);
        return node;
    },
    destroyNode: function (node) {
        FS.hashRemoveNode(node);
    },
    isRoot: function (node) {
        return node === node.parent;
    },
    isMountpoint: function (node) {
        return !!node.mounted;
    },
    isFile: function (mode) {
        return (mode & 61440) === 32768;
    },
    isDir: function (mode) {
        return (mode & 61440) === 16384;
    },
    isLink: function (mode) {
        return (mode & 61440) === 40960;
    },
    isChrdev: function (mode) {
        return (mode & 61440) === 8192;
    },
    isBlkdev: function (mode) {
        return (mode & 61440) === 24576;
    },
    isFIFO: function (mode) {
        return (mode & 61440) === 4096;
    },
    isSocket: function (mode) {
        return (mode & 49152) === 49152;
    },
    flagModes: { r: 0, rs: 1052672, "r+": 2, w: 577, wx: 705, xw: 705, "w+": 578, "wx+": 706, "xw+": 706, a: 1089, ax: 1217, xa: 1217, "a+": 1090, "ax+": 1218, "xa+": 1218 },
    modeStringToFlags: function (str) {
        var flags = FS.flagModes[str];
        if (typeof flags === "undefined") {
            throw new Error("Unknown file open mode: " + str);
        }
        return flags;
    },
    flagsToPermissionString: function (flag) {
        var accmode = flag & 2097155;
        var perms = ["r", "w", "rw"][accmode];
        if (flag & 512) {
            perms += "w";
        }
        return perms;
    },
    nodePermissions: function (node, perms) {
        if (FS.ignorePermissions) {
            return 0;
        }
        if (perms.indexOf("r") !== -1 && !(node.mode & 292)) {
            return ERRNO_CODES.EACCES;
        } else if (perms.indexOf("w") !== -1 && !(node.mode & 146)) {
            return ERRNO_CODES.EACCES;
        } else if (perms.indexOf("x") !== -1 && !(node.mode & 73)) {
            return ERRNO_CODES.EACCES;
        }
        return 0;
    },
    mayLookup: function (dir) {
        var err = FS.nodePermissions(dir, "x");
        if (err) return err;
        if (!dir.node_ops.lookup) return ERRNO_CODES.EACCES;
        return 0;
    },
    mayCreate: function (dir, name) {
        try {
            var node = FS.lookupNode(dir, name);
            return ERRNO_CODES.EEXIST;
        } catch (e) {}
        return FS.nodePermissions(dir, "wx");
    },
    mayDelete: function (dir, name, isdir) {
        var node;
        try {
            node = FS.lookupNode(dir, name);
        } catch (e) {
            return e.errno;
        }
        var err = FS.nodePermissions(dir, "wx");
        if (err) {
            return err;
        }
        if (isdir) {
            if (!FS.isDir(node.mode)) {
                return ERRNO_CODES.ENOTDIR;
            }
            if (FS.isRoot(node) || FS.getPath(node) === FS.cwd()) {
                return ERRNO_CODES.EBUSY;
            }
        } else {
            if (FS.isDir(node.mode)) {
                return ERRNO_CODES.EISDIR;
            }
        }
        return 0;
    },
    mayOpen: function (node, flags) {
        if (!node) {
            return ERRNO_CODES.ENOENT;
        }
        if (FS.isLink(node.mode)) {
            return ERRNO_CODES.ELOOP;
        } else if (FS.isDir(node.mode)) {
            if ((flags & 2097155) !== 0 || flags & 512) {
                return ERRNO_CODES.EISDIR;
            }
        }
        return FS.nodePermissions(node, FS.flagsToPermissionString(flags));
    },
    MAX_OPEN_FDS: 4096,
    nextfd: function (fd_start, fd_end) {
        fd_start = fd_start || 0;
        fd_end = fd_end || FS.MAX_OPEN_FDS;
        for (var fd = fd_start; fd <= fd_end; fd++) {
            if (!FS.streams[fd]) {
                return fd;
            }
        }
        throw new FS.ErrnoError(ERRNO_CODES.EMFILE);
    },
    getStream: function (fd) {
        return FS.streams[fd];
    },
    createStream: function (stream, fd_start, fd_end) {
        if (!FS.FSStream) {
            FS.FSStream = function () {};
            FS.FSStream.prototype = {};
            Object.defineProperties(FS.FSStream.prototype, {
                object: {
                    get: function () {
                        return this.node;
                    },
                    set: function (val) {
                        this.node = val;
                    },
                },
                isRead: {
                    get: function () {
                        return (this.flags & 2097155) !== 1;
                    },
                },
                isWrite: {
                    get: function () {
                        return (this.flags & 2097155) !== 0;
                    },
                },
                isAppend: {
                    get: function () {
                        return this.flags & 1024;
                    },
                },
            });
        }
        var newStream = new FS.FSStream();
        for (var p in stream) {
            newStream[p] = stream[p];
        }
        stream = newStream;
        var fd = FS.nextfd(fd_start, fd_end);
        stream.fd = fd;
        FS.streams[fd] = stream;
        return stream;
    },
    closeStream: function (fd) {
        FS.streams[fd] = null;
    },
    getStreamFromPtr: function (ptr) {
        return FS.streams[ptr - 1];
    },
    getPtrForStream: function (stream) {
        return stream ? stream.fd + 1 : 0;
    },
    chrdev_stream_ops: {
        open: function (stream) {
            var device = FS.getDevice(stream.node.rdev);
            stream.stream_ops = device.stream_ops;
            if (stream.stream_ops.open) {
                stream.stream_ops.open(stream);
            }
        },
        llseek: function () {
            throw new FS.ErrnoError(ERRNO_CODES.ESPIPE);
        },
    },
    major: function (dev) {
        return dev >> 8;
    },
    minor: function (dev) {
        return dev & 255;
    },
    makedev: function (ma, mi) {
        return (ma << 8) | mi;
    },
    registerDevice: function (dev, ops) {
        FS.devices[dev] = { stream_ops: ops };
    },
    getDevice: function (dev) {
        return FS.devices[dev];
    },
    getMounts: function (mount) {
        var mounts = [];
        var check = [mount];
        while (check.length) {
            var m = check.pop();
            mounts.push(m);
            check.push.apply(check, m.mounts);
        }
        return mounts;
    },
    syncfs: function (populate, callback) {
        if (typeof populate === "function") {
            callback = populate;
            populate = false;
        }
        var mounts = FS.getMounts(FS.root.mount);
        var completed = 0;
        function done(err) {
            if (err) {
                if (!done.errored) {
                    done.errored = true;
                    return callback(err);
                }
                return;
            }
            if (++completed >= mounts.length) {
                callback(null);
            }
        }
        mounts.forEach(function (mount) {
            if (!mount.type.syncfs) {
                return done(null);
            }
            mount.type.syncfs(mount, populate, done);
        });
    },
    mount: function (type, opts, mountpoint) {
        var root = mountpoint === "/";
        var pseudo = !mountpoint;
        var node;
        if (root && FS.root) {
            throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
        } else if (!root && !pseudo) {
            var lookup = FS.lookupPath(mountpoint, { follow_mount: false });
            mountpoint = lookup.path;
            node = lookup.node;
            if (FS.isMountpoint(node)) {
                throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
            }
            if (!FS.isDir(node.mode)) {
                throw new FS.ErrnoError(ERRNO_CODES.ENOTDIR);
            }
        }
        var mount = { type: type, opts: opts, mountpoint: mountpoint, mounts: [] };
        var mountRoot = type.mount(mount);
        mountRoot.mount = mount;
        mount.root = mountRoot;
        if (root) {
            FS.root = mountRoot;
        } else if (node) {
            node.mounted = mount;
            if (node.mount) {
                node.mount.mounts.push(mount);
            }
        }
        return mountRoot;
    },
    unmount: function (mountpoint) {
        var lookup = FS.lookupPath(mountpoint, { follow_mount: false });
        if (!FS.isMountpoint(lookup.node)) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var node = lookup.node;
        var mount = node.mounted;
        var mounts = FS.getMounts(mount);
        Object.keys(FS.nameTable).forEach(function (hash) {
            var current = FS.nameTable[hash];
            while (current) {
                var next = current.name_next;
                if (mounts.indexOf(current.mount) !== -1) {
                    FS.destroyNode(current);
                }
                current = next;
            }
        });
        node.mounted = null;
        var idx = node.mount.mounts.indexOf(mount);
        assert(idx !== -1);
        node.mount.mounts.splice(idx, 1);
    },
    lookup: function (parent, name) {
        return parent.node_ops.lookup(parent, name);
    },
    mknod: function (path, mode, dev) {
        var lookup = FS.lookupPath(path, { parent: true });
        var parent = lookup.node;
        var name = PATH.basename(path);
        if (!name || name === "." || name === "..") {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var err = FS.mayCreate(parent, name);
        if (err) {
            throw new FS.ErrnoError(err);
        }
        if (!parent.node_ops.mknod) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        return parent.node_ops.mknod(parent, name, mode, dev);
    },
    create: function (path, mode) {
        mode = mode !== undefined ? mode : 438;
        mode &= 4095;
        mode |= 32768;
        return FS.mknod(path, mode, 0);
    },
    mkdir: function (path, mode) {
        mode = mode !== undefined ? mode : 511;
        mode &= 511 | 512;
        mode |= 16384;
        return FS.mknod(path, mode, 0);
    },
    mkdev: function (path, mode, dev) {
        if (typeof dev === "undefined") {
            dev = mode;
            mode = 438;
        }
        mode |= 8192;
        return FS.mknod(path, mode, dev);
    },
    symlink: function (oldpath, newpath) {
        if (!PATH.resolve(oldpath)) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        var lookup = FS.lookupPath(newpath, { parent: true });
        var parent = lookup.node;
        if (!parent) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        var newname = PATH.basename(newpath);
        var err = FS.mayCreate(parent, newname);
        if (err) {
            throw new FS.ErrnoError(err);
        }
        if (!parent.node_ops.symlink) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        return parent.node_ops.symlink(parent, newname, oldpath);
    },
    rename: function (old_path, new_path) {
        var old_dirname = PATH.dirname(old_path);
        var new_dirname = PATH.dirname(new_path);
        var old_name = PATH.basename(old_path);
        var new_name = PATH.basename(new_path);
        var lookup, old_dir, new_dir;
        try {
            lookup = FS.lookupPath(old_path, { parent: true });
            old_dir = lookup.node;
            lookup = FS.lookupPath(new_path, { parent: true });
            new_dir = lookup.node;
        } catch (e) {
            throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
        }
        if (!old_dir || !new_dir) throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        if (old_dir.mount !== new_dir.mount) {
            throw new FS.ErrnoError(ERRNO_CODES.EXDEV);
        }
        var old_node = FS.lookupNode(old_dir, old_name);
        var relative = PATH.relative(old_path, new_dirname);
        if (relative.charAt(0) !== ".") {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        relative = PATH.relative(new_path, old_dirname);
        if (relative.charAt(0) !== ".") {
            throw new FS.ErrnoError(ERRNO_CODES.ENOTEMPTY);
        }
        var new_node;
        try {
            new_node = FS.lookupNode(new_dir, new_name);
        } catch (e) {}
        if (old_node === new_node) {
            return;
        }
        var isdir = FS.isDir(old_node.mode);
        var err = FS.mayDelete(old_dir, old_name, isdir);
        if (err) {
            throw new FS.ErrnoError(err);
        }
        err = new_node ? FS.mayDelete(new_dir, new_name, isdir) : FS.mayCreate(new_dir, new_name);
        if (err) {
            throw new FS.ErrnoError(err);
        }
        if (!old_dir.node_ops.rename) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        if (FS.isMountpoint(old_node) || (new_node && FS.isMountpoint(new_node))) {
            throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
        }
        if (new_dir !== old_dir) {
            err = FS.nodePermissions(old_dir, "w");
            if (err) {
                throw new FS.ErrnoError(err);
            }
        }
        try {
            if (FS.trackingDelegate["willMovePath"]) {
                FS.trackingDelegate["willMovePath"](old_path, new_path);
            }
        } catch (e) {
            console.log("FS.trackingDelegate['willMovePath']('" + old_path + "', '" + new_path + "') threw an exception: " + e.message);
        }
        FS.hashRemoveNode(old_node);
        try {
            old_dir.node_ops.rename(old_node, new_dir, new_name);
        } catch (e) {
            throw e;
        } finally {
            FS.hashAddNode(old_node);
        }
        try {
            if (FS.trackingDelegate["onMovePath"]) FS.trackingDelegate["onMovePath"](old_path, new_path);
        } catch (e) {
            console.log("FS.trackingDelegate['onMovePath']('" + old_path + "', '" + new_path + "') threw an exception: " + e.message);
        }
    },
    rmdir: function (path) {
        var lookup = FS.lookupPath(path, { parent: true });
        var parent = lookup.node;
        var name = PATH.basename(path);
        var node = FS.lookupNode(parent, name);
        var err = FS.mayDelete(parent, name, true);
        if (err) {
            throw new FS.ErrnoError(err);
        }
        if (!parent.node_ops.rmdir) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        if (FS.isMountpoint(node)) {
            throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
        }
        try {
            if (FS.trackingDelegate["willDeletePath"]) {
                FS.trackingDelegate["willDeletePath"](path);
            }
        } catch (e) {
            console.log("FS.trackingDelegate['willDeletePath']('" + path + "') threw an exception: " + e.message);
        }
        parent.node_ops.rmdir(parent, name);
        FS.destroyNode(node);
        try {
            if (FS.trackingDelegate["onDeletePath"]) FS.trackingDelegate["onDeletePath"](path);
        } catch (e) {
            console.log("FS.trackingDelegate['onDeletePath']('" + path + "') threw an exception: " + e.message);
        }
    },
    readdir: function (path) {
        var lookup = FS.lookupPath(path, { follow: true });
        var node = lookup.node;
        if (!node.node_ops.readdir) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOTDIR);
        }
        return node.node_ops.readdir(node);
    },
    unlink: function (path) {
        var lookup = FS.lookupPath(path, { parent: true });
        var parent = lookup.node;
        var name = PATH.basename(path);
        var node = FS.lookupNode(parent, name);
        var err = FS.mayDelete(parent, name, false);
        if (err) {
            if (err === ERRNO_CODES.EISDIR) err = ERRNO_CODES.EPERM;
            throw new FS.ErrnoError(err);
        }
        if (!parent.node_ops.unlink) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        if (FS.isMountpoint(node)) {
            throw new FS.ErrnoError(ERRNO_CODES.EBUSY);
        }
        try {
            if (FS.trackingDelegate["willDeletePath"]) {
                FS.trackingDelegate["willDeletePath"](path);
            }
        } catch (e) {
            console.log("FS.trackingDelegate['willDeletePath']('" + path + "') threw an exception: " + e.message);
        }
        parent.node_ops.unlink(parent, name);
        FS.destroyNode(node);
        try {
            if (FS.trackingDelegate["onDeletePath"]) FS.trackingDelegate["onDeletePath"](path);
        } catch (e) {
            console.log("FS.trackingDelegate['onDeletePath']('" + path + "') threw an exception: " + e.message);
        }
    },
    readlink: function (path) {
        var lookup = FS.lookupPath(path);
        var link = lookup.node;
        if (!link) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        if (!link.node_ops.readlink) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        return link.node_ops.readlink(link);
    },
    stat: function (path, dontFollow) {
        var lookup = FS.lookupPath(path, { follow: !dontFollow });
        var node = lookup.node;
        if (!node) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        if (!node.node_ops.getattr) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        return node.node_ops.getattr(node);
    },
    lstat: function (path) {
        return FS.stat(path, true);
    },
    chmod: function (path, mode, dontFollow) {
        var node;
        if (typeof path === "string") {
            var lookup = FS.lookupPath(path, { follow: !dontFollow });
            node = lookup.node;
        } else {
            node = path;
        }
        if (!node.node_ops.setattr) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        node.node_ops.setattr(node, { mode: (mode & 4095) | (node.mode & ~4095), timestamp: Date.now() });
    },
    lchmod: function (path, mode) {
        FS.chmod(path, mode, true);
    },
    fchmod: function (fd, mode) {
        var stream = FS.getStream(fd);
        if (!stream) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        FS.chmod(stream.node, mode);
    },
    chown: function (path, uid, gid, dontFollow) {
        var node;
        if (typeof path === "string") {
            var lookup = FS.lookupPath(path, { follow: !dontFollow });
            node = lookup.node;
        } else {
            node = path;
        }
        if (!node.node_ops.setattr) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        node.node_ops.setattr(node, { timestamp: Date.now() });
    },
    lchown: function (path, uid, gid) {
        FS.chown(path, uid, gid, true);
    },
    fchown: function (fd, uid, gid) {
        var stream = FS.getStream(fd);
        if (!stream) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        FS.chown(stream.node, uid, gid);
    },
    truncate: function (path, len) {
        if (len < 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var node;
        if (typeof path === "string") {
            var lookup = FS.lookupPath(path, { follow: true });
            node = lookup.node;
        } else {
            node = path;
        }
        if (!node.node_ops.setattr) {
            throw new FS.ErrnoError(ERRNO_CODES.EPERM);
        }
        if (FS.isDir(node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EISDIR);
        }
        if (!FS.isFile(node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var err = FS.nodePermissions(node, "w");
        if (err) {
            throw new FS.ErrnoError(err);
        }
        node.node_ops.setattr(node, { size: len, timestamp: Date.now() });
    },
    ftruncate: function (fd, len) {
        var stream = FS.getStream(fd);
        if (!stream) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        if ((stream.flags & 2097155) === 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        FS.truncate(stream.node, len);
    },
    utime: function (path, atime, mtime) {
        var lookup = FS.lookupPath(path, { follow: true });
        var node = lookup.node;
        node.node_ops.setattr(node, { timestamp: Math.max(atime, mtime) });
    },
    open: function (path, flags, mode, fd_start, fd_end) {
        if (path === "") {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        flags = typeof flags === "string" ? FS.modeStringToFlags(flags) : flags;
        mode = typeof mode === "undefined" ? 438 : mode;
        if (flags & 64) {
            mode = (mode & 4095) | 32768;
        } else {
            mode = 0;
        }
        var node;
        if (typeof path === "object") {
            node = path;
        } else {
            path = PATH.normalize(path);
            try {
                var lookup = FS.lookupPath(path, { follow: !(flags & 131072) });
                node = lookup.node;
            } catch (e) {}
        }
        var created = false;
        if (flags & 64) {
            if (node) {
                if (flags & 128) {
                    throw new FS.ErrnoError(ERRNO_CODES.EEXIST);
                }
            } else {
                node = FS.mknod(path, mode, 0);
                created = true;
            }
        }
        if (!node) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOENT);
        }
        if (FS.isChrdev(node.mode)) {
            flags &= ~512;
        }
        if (!created) {
            var err = FS.mayOpen(node, flags);
            if (err) {
                throw new FS.ErrnoError(err);
            }
        }
        if (flags & 512) {
            FS.truncate(node, 0);
        }
        flags &= ~(128 | 512);
        var stream = FS.createStream({ node: node, path: FS.getPath(node), flags: flags, seekable: true, position: 0, stream_ops: node.stream_ops, ungotten: [], error: false }, fd_start, fd_end);
        if (stream.stream_ops.open) {
            stream.stream_ops.open(stream);
        }
        if (Module["logReadFiles"] && !(flags & 1)) {
            if (!FS.readFiles) FS.readFiles = {};
            if (!(path in FS.readFiles)) {
                FS.readFiles[path] = 1;
                Module["printErr"]("read file: " + path);
            }
        }
        try {
            if (FS.trackingDelegate["onOpenFile"]) {
                var trackingFlags = 0;
                if ((flags & 2097155) !== 1) {
                    trackingFlags |= FS.tracking.openFlags.READ;
                }
                if ((flags & 2097155) !== 0) {
                    trackingFlags |= FS.tracking.openFlags.WRITE;
                }
                FS.trackingDelegate["onOpenFile"](path, trackingFlags);
            }
        } catch (e) {
            console.log("FS.trackingDelegate['onOpenFile']('" + path + "', flags) threw an exception: " + e.message);
        }
        return stream;
    },
    close: function (stream) {
        try {
            if (stream.stream_ops.close) {
                stream.stream_ops.close(stream);
            }
        } catch (e) {
            throw e;
        } finally {
            FS.closeStream(stream.fd);
        }
    },
    llseek: function (stream, offset, whence) {
        if (!stream.seekable || !stream.stream_ops.llseek) {
            throw new FS.ErrnoError(ERRNO_CODES.ESPIPE);
        }
        return stream.stream_ops.llseek(stream, offset, whence);
    },
    read: function (stream, buffer, offset, length, position) {
        if (length < 0 || position < 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        if ((stream.flags & 2097155) === 1) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        if (FS.isDir(stream.node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EISDIR);
        }
        if (!stream.stream_ops.read) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        var seeking = true;
        if (typeof position === "undefined") {
            position = stream.position;
            seeking = false;
        } else if (!stream.seekable) {
            throw new FS.ErrnoError(ERRNO_CODES.ESPIPE);
        }
        var bytesRead = stream.stream_ops.read(stream, buffer, offset, length, position);
        if (!seeking) stream.position += bytesRead;
        return bytesRead;
    },
    write: function (stream, buffer, offset, length, position, canOwn) {
        if (length < 0 || position < 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        if ((stream.flags & 2097155) === 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        if (FS.isDir(stream.node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.EISDIR);
        }
        if (!stream.stream_ops.write) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        if (stream.flags & 1024) {
            FS.llseek(stream, 0, 2);
        }
        var seeking = true;
        if (typeof position === "undefined") {
            position = stream.position;
            seeking = false;
        } else if (!stream.seekable) {
            throw new FS.ErrnoError(ERRNO_CODES.ESPIPE);
        }
        var bytesWritten = stream.stream_ops.write(stream, buffer, offset, length, position, canOwn);
        if (!seeking) stream.position += bytesWritten;
        try {
            if (stream.path && FS.trackingDelegate["onWriteToFile"]) FS.trackingDelegate["onWriteToFile"](stream.path);
        } catch (e) {
            console.log("FS.trackingDelegate['onWriteToFile']('" + path + "') threw an exception: " + e.message);
        }
        return bytesWritten;
    },
    allocate: function (stream, offset, length) {
        if (offset < 0 || length <= 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
        }
        if ((stream.flags & 2097155) === 0) {
            throw new FS.ErrnoError(ERRNO_CODES.EBADF);
        }
        if (!FS.isFile(stream.node.mode) && !FS.isDir(node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.ENODEV);
        }
        if (!stream.stream_ops.allocate) {
            throw new FS.ErrnoError(ERRNO_CODES.EOPNOTSUPP);
        }
        stream.stream_ops.allocate(stream, offset, length);
    },
    mmap: function (stream, buffer, offset, length, position, prot, flags) {
        if ((stream.flags & 2097155) === 1) {
            throw new FS.ErrnoError(ERRNO_CODES.EACCES);
        }
        if (!stream.stream_ops.mmap) {
            throw new FS.ErrnoError(ERRNO_CODES.ENODEV);
        }
        return stream.stream_ops.mmap(stream, buffer, offset, length, position, prot, flags);
    },
    ioctl: function (stream, cmd, arg) {
        if (!stream.stream_ops.ioctl) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOTTY);
        }
        return stream.stream_ops.ioctl(stream, cmd, arg);
    },
    readFile: function (path, opts) {
        opts = opts || {};
        opts.flags = opts.flags || "r";
        opts.encoding = opts.encoding || "binary";
        if (opts.encoding !== "utf8" && opts.encoding !== "binary") {
            throw new Error('Invalid encoding type "' + opts.encoding + '"');
        }
        var ret;
        var stream = FS.open(path, opts.flags);
        var stat = FS.stat(path);
        var length = stat.size;
        var buf = new Uint8Array(length);
        FS.read(stream, buf, 0, length, 0);
        if (opts.encoding === "utf8") {
            ret = "";
            var utf8 = new Runtime.UTF8Processor();
            for (var i = 0; i < length; i++) {
                ret += utf8.processCChar(buf[i]);
            }
        } else if (opts.encoding === "binary") {
            ret = buf;
        }
        FS.close(stream);
        return ret;
    },
    writeFile: function (path, data, opts) {
        opts = opts || {};
        opts.flags = opts.flags || "w";
        opts.encoding = opts.encoding || "utf8";
        if (opts.encoding !== "utf8" && opts.encoding !== "binary") {
            throw new Error('Invalid encoding type "' + opts.encoding + '"');
        }
        var stream = FS.open(path, opts.flags, opts.mode);
        if (opts.encoding === "utf8") {
            var utf8 = new Runtime.UTF8Processor();
            var buf = new Uint8Array(utf8.processJSString(data));
            FS.write(stream, buf, 0, buf.length, 0, opts.canOwn);
        } else if (opts.encoding === "binary") {
            FS.write(stream, data, 0, data.length, 0, opts.canOwn);
        }
        FS.close(stream);
    },
    cwd: function () {
        return FS.currentPath;
    },
    chdir: function (path) {
        var lookup = FS.lookupPath(path, { follow: true });
        if (!FS.isDir(lookup.node.mode)) {
            throw new FS.ErrnoError(ERRNO_CODES.ENOTDIR);
        }
        var err = FS.nodePermissions(lookup.node, "x");
        if (err) {
            throw new FS.ErrnoError(err);
        }
        FS.currentPath = lookup.path;
    },
    createDefaultDirectories: function () {
        FS.mkdir("/tmp");
        FS.mkdir("/home");
        FS.mkdir("/home/web_user");
    },
    createDefaultDevices: function () {
        FS.mkdir("/dev");
        FS.registerDevice(FS.makedev(1, 3), {
            read: function () {
                return 0;
            },
            write: function () {
                return 0;
            },
        });
        FS.mkdev("/dev/null", FS.makedev(1, 3));
        TTY.register(FS.makedev(5, 0), TTY.default_tty_ops);
        TTY.register(FS.makedev(6, 0), TTY.default_tty1_ops);
        FS.mkdev("/dev/tty", FS.makedev(5, 0));
        FS.mkdev("/dev/tty1", FS.makedev(6, 0));
        var random_device;
        if (typeof crypto !== "undefined") {
            var randomBuffer = new Uint8Array(1);
            random_device = function () {
                crypto.getRandomValues(randomBuffer);
                return randomBuffer[0];
            };
        } else if (ENVIRONMENT_IS_NODE) {
            random_device = function () {
                return require("crypto").randomBytes(1)[0];
            };
        } else {
            random_device = function () {
                return (Math.random() * 256) | 0;
            };
        }
        FS.createDevice("/dev", "random", random_device);
        FS.createDevice("/dev", "urandom", random_device);
        FS.mkdir("/dev/shm");
        FS.mkdir("/dev/shm/tmp");
    },
    createStandardStreams: function () {
        if (Module["stdin"]) {
            FS.createDevice("/dev", "stdin", Module["stdin"]);
        } else {
            FS.symlink("/dev/tty", "/dev/stdin");
        }
        if (Module["stdout"]) {
            FS.createDevice("/dev", "stdout", null, Module["stdout"]);
        } else {
            FS.symlink("/dev/tty", "/dev/stdout");
        }
        if (Module["stderr"]) {
            FS.createDevice("/dev", "stderr", null, Module["stderr"]);
        } else {
            FS.symlink("/dev/tty1", "/dev/stderr");
        }
        var stdin = FS.open("/dev/stdin", "r");
        HEAP32[_stdin >> 2] = FS.getPtrForStream(stdin);
        assert(stdin.fd === 0, "invalid handle for stdin (" + stdin.fd + ")");
        var stdout = FS.open("/dev/stdout", "w");
        HEAP32[_stdout >> 2] = FS.getPtrForStream(stdout);
        assert(stdout.fd === 1, "invalid handle for stdout (" + stdout.fd + ")");
        var stderr = FS.open("/dev/stderr", "w");
        HEAP32[_stderr >> 2] = FS.getPtrForStream(stderr);
        assert(stderr.fd === 2, "invalid handle for stderr (" + stderr.fd + ")");
    },
    ensureErrnoError: function () {
        if (FS.ErrnoError) return;
        FS.ErrnoError = function ErrnoError(errno, node) {
            this.node = node;
            this.setErrno = function (errno) {
                this.errno = errno;
                for (var key in ERRNO_CODES) {
                    if (ERRNO_CODES[key] === errno) {
                        this.code = key;
                        break;
                    }
                }
            };
            this.setErrno(errno);
            this.message = ERRNO_MESSAGES[errno];
        };
        FS.ErrnoError.prototype = new Error();
        FS.ErrnoError.prototype.constructor = FS.ErrnoError;
        [ERRNO_CODES.ENOENT].forEach(function (code) {
            FS.genericErrors[code] = new FS.ErrnoError(code);
            FS.genericErrors[code].stack = "<generic error, no stack>";
        });
    },
    staticInit: function () {
        FS.ensureErrnoError();
        FS.nameTable = new Array(4096);
        FS.mount(MEMFS, {}, "/");
        FS.createDefaultDirectories();
        FS.createDefaultDevices();
    },
    init: function (input, output, error) {
        assert(!FS.init.initialized, "FS.init was previously called. If you want to initialize later with custom parameters, remove any earlier calls (note that one is automatically added to the generated code)");
        FS.init.initialized = true;
        FS.ensureErrnoError();
        Module["stdin"] = input || Module["stdin"];
        Module["stdout"] = output || Module["stdout"];
        Module["stderr"] = error || Module["stderr"];
        FS.createStandardStreams();
    },
    quit: function () {
        FS.init.initialized = false;
        for (var i = 0; i < FS.streams.length; i++) {
            var stream = FS.streams[i];
            if (!stream) {
                continue;
            }
            FS.close(stream);
        }
    },
    getMode: function (canRead, canWrite) {
        var mode = 0;
        if (canRead) mode |= 292 | 73;
        if (canWrite) mode |= 146;
        return mode;
    },
    joinPath: function (parts, forceRelative) {
        var path = PATH.join.apply(null, parts);
        if (forceRelative && path[0] == "/") path = path.substr(1);
        return path;
    },
    absolutePath: function (relative, base) {
        return PATH.resolve(base, relative);
    },
    standardizePath: function (path) {
        return PATH.normalize(path);
    },
    findObject: function (path, dontResolveLastLink) {
        var ret = FS.analyzePath(path, dontResolveLastLink);
        if (ret.exists) {
            return ret.object;
        } else {
            ___setErrNo(ret.error);
            return null;
        }
    },
    analyzePath: function (path, dontResolveLastLink) {
        try {
            var lookup = FS.lookupPath(path, { follow: !dontResolveLastLink });
            path = lookup.path;
        } catch (e) {}
        var ret = { isRoot: false, exists: false, error: 0, name: null, path: null, object: null, parentExists: false, parentPath: null, parentObject: null };
        try {
            var lookup = FS.lookupPath(path, { parent: true });
            ret.parentExists = true;
            ret.parentPath = lookup.path;
            ret.parentObject = lookup.node;
            ret.name = PATH.basename(path);
            lookup = FS.lookupPath(path, { follow: !dontResolveLastLink });
            ret.exists = true;
            ret.path = lookup.path;
            ret.object = lookup.node;
            ret.name = lookup.node.name;
            ret.isRoot = lookup.path === "/";
        } catch (e) {
            ret.error = e.errno;
        }
        return ret;
    },
    createFolder: function (parent, name, canRead, canWrite) {
        var path = PATH.join2(typeof parent === "string" ? parent : FS.getPath(parent), name);
        var mode = FS.getMode(canRead, canWrite);
        return FS.mkdir(path, mode);
    },
    createPath: function (parent, path, canRead, canWrite) {
        parent = typeof parent === "string" ? parent : FS.getPath(parent);
        var parts = path.split("/").reverse();
        while (parts.length) {
            var part = parts.pop();
            if (!part) continue;
            var current = PATH.join2(parent, part);
            try {
                FS.mkdir(current);
            } catch (e) {}
            parent = current;
        }
        return current;
    },
    createFile: function (parent, name, properties, canRead, canWrite) {
        var path = PATH.join2(typeof parent === "string" ? parent : FS.getPath(parent), name);
        var mode = FS.getMode(canRead, canWrite);
        return FS.create(path, mode);
    },
    createDataFile: function (parent, name, data, canRead, canWrite, canOwn) {
        var path = name ? PATH.join2(typeof parent === "string" ? parent : FS.getPath(parent), name) : parent;
        var mode = FS.getMode(canRead, canWrite);
        var node = FS.create(path, mode);
        if (data) {
            if (typeof data === "string") {
                var arr = new Array(data.length);
                for (var i = 0, len = data.length; i < len; ++i) arr[i] = data.charCodeAt(i);
                data = arr;
            }
            FS.chmod(node, mode | 146);
            var stream = FS.open(node, "w");
            FS.write(stream, data, 0, data.length, 0, canOwn);
            FS.close(stream);
            FS.chmod(node, mode);
        }
        return node;
    },
    createDevice: function (parent, name, input, output) {
        var path = PATH.join2(typeof parent === "string" ? parent : FS.getPath(parent), name);
        var mode = FS.getMode(!!input, !!output);
        if (!FS.createDevice.major) FS.createDevice.major = 64;
        var dev = FS.makedev(FS.createDevice.major++, 0);
        FS.registerDevice(dev, {
            open: function (stream) {
                stream.seekable = false;
            },
            close: function (stream) {
                if (output && output.buffer && output.buffer.length) {
                    output(10);
                }
            },
            read: function (stream, buffer, offset, length, pos) {
                var bytesRead = 0;
                for (var i = 0; i < length; i++) {
                    var result;
                    try {
                        result = input();
                    } catch (e) {
                        throw new FS.ErrnoError(ERRNO_CODES.EIO);
                    }
                    if (result === undefined && bytesRead === 0) {
                        throw new FS.ErrnoError(ERRNO_CODES.EAGAIN);
                    }
                    if (result === null || result === undefined) break;
                    bytesRead++;
                    buffer[offset + i] = result;
                }
                if (bytesRead) {
                    stream.node.timestamp = Date.now();
                }
                return bytesRead;
            },
            write: function (stream, buffer, offset, length, pos) {
                for (var i = 0; i < length; i++) {
                    try {
                        output(buffer[offset + i]);
                    } catch (e) {
                        throw new FS.ErrnoError(ERRNO_CODES.EIO);
                    }
                }
                if (length) {
                    stream.node.timestamp = Date.now();
                }
                return i;
            },
        });
        return FS.mkdev(path, mode, dev);
    },
    createLink: function (parent, name, target, canRead, canWrite) {
        var path = PATH.join2(typeof parent === "string" ? parent : FS.getPath(parent), name);
        return FS.symlink(target, path);
    },
    forceLoadFile: function (obj) {
        if (obj.isDevice || obj.isFolder || obj.link || obj.contents) return true;
        var success = true;
        if (typeof XMLHttpRequest !== "undefined") {
            throw new Error("Lazy loading should have been performed (contents set) in createLazyFile, but it was not. Lazy loading only works in web workers. Use --embed-file or --preload-file in emcc on the main thread.");
        } else if (Module["read"]) {
            try {
                obj.contents = intArrayFromString(Module["read"](obj.url), true);
                obj.usedBytes = obj.contents.length;
            } catch (e) {
                success = false;
            }
        } else {
            throw new Error("Cannot load without read() or XMLHttpRequest.");
        }
        if (!success) ___setErrNo(ERRNO_CODES.EIO);
        return success;
    },
    createLazyFile: function (parent, name, url, canRead, canWrite) {
        function LazyUint8Array() {
            this.lengthKnown = false;
            this.chunks = [];
        }
        LazyUint8Array.prototype.get = function LazyUint8Array_get(idx) {
            if (idx > this.length - 1 || idx < 0) {
                return undefined;
            }
            var chunkOffset = idx % this.chunkSize;
            var chunkNum = (idx / this.chunkSize) | 0;
            return this.getter(chunkNum)[chunkOffset];
        };
        LazyUint8Array.prototype.setDataGetter = function LazyUint8Array_setDataGetter(getter) {
            this.getter = getter;
        };
        LazyUint8Array.prototype.cacheLength = function LazyUint8Array_cacheLength() {
            var xhr = new XMLHttpRequest();
            xhr.open("HEAD", url, false);
            xhr.send(null);
            if (!((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304)) throw new Error("Couldn't load " + url + ". Status: " + xhr.status);
            var datalength = Number(xhr.getResponseHeader("Content-length"));
            var header;
            var hasByteServing = (header = xhr.getResponseHeader("Accept-Ranges")) && header === "bytes";
            var chunkSize = 1024 * 1024;
            if (!hasByteServing) chunkSize = datalength;
            var doXHR = function (from, to) {
                if (from > to) throw new Error("invalid range (" + from + ", " + to + ") or no bytes requested!");
                if (to > datalength - 1) throw new Error("only " + datalength + " bytes available! programmer error!");
                var xhr = new XMLHttpRequest();
                xhr.open("GET", url, false);
                if (datalength !== chunkSize) xhr.setRequestHeader("Range", "bytes=" + from + "-" + to);
                if (typeof Uint8Array != "undefined") xhr.responseType = "arraybuffer";
                if (xhr.overrideMimeType) {
                    xhr.overrideMimeType("text/plain; charset=x-user-defined");
                }
                xhr.send(null);
                if (!((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304)) throw new Error("Couldn't load " + url + ". Status: " + xhr.status);
                if (xhr.response !== undefined) {
                    return new Uint8Array(xhr.response || []);
                } else {
                    return intArrayFromString(xhr.responseText || "", true);
                }
            };
            var lazyArray = this;
            lazyArray.setDataGetter(function (chunkNum) {
                var start = chunkNum * chunkSize;
                var end = (chunkNum + 1) * chunkSize - 1;
                end = Math.min(end, datalength - 1);
                if (typeof lazyArray.chunks[chunkNum] === "undefined") {
                    lazyArray.chunks[chunkNum] = doXHR(start, end);
                }
                if (typeof lazyArray.chunks[chunkNum] === "undefined") throw new Error("doXHR failed!");
                return lazyArray.chunks[chunkNum];
            });
            this._length = datalength;
            this._chunkSize = chunkSize;
            this.lengthKnown = true;
        };
        if (typeof XMLHttpRequest !== "undefined") {
            if (!ENVIRONMENT_IS_WORKER) throw "Cannot do synchronous binary XHRs outside webworkers in modern browsers. Use --embed-file or --preload-file in emcc";
            var lazyArray = new LazyUint8Array();
            Object.defineProperty(lazyArray, "length", {
                get: function () {
                    if (!this.lengthKnown) {
                        this.cacheLength();
                    }
                    return this._length;
                },
            });
            Object.defineProperty(lazyArray, "chunkSize", {
                get: function () {
                    if (!this.lengthKnown) {
                        this.cacheLength();
                    }
                    return this._chunkSize;
                },
            });
            var properties = { isDevice: false, contents: lazyArray };
        } else {
            var properties = { isDevice: false, url: url };
        }
        var node = FS.createFile(parent, name, properties, canRead, canWrite);
        if (properties.contents) {
            node.contents = properties.contents;
        } else if (properties.url) {
            node.contents = null;
            node.url = properties.url;
        }
        Object.defineProperty(node, "usedBytes", {
            get: function () {
                return this.contents.length;
            },
        });
        var stream_ops = {};
        var keys = Object.keys(node.stream_ops);
        keys.forEach(function (key) {
            var fn = node.stream_ops[key];
            stream_ops[key] = function forceLoadLazyFile() {
                if (!FS.forceLoadFile(node)) {
                    throw new FS.ErrnoError(ERRNO_CODES.EIO);
                }
                return fn.apply(null, arguments);
            };
        });
        stream_ops.read = function stream_ops_read(stream, buffer, offset, length, position) {
            if (!FS.forceLoadFile(node)) {
                throw new FS.ErrnoError(ERRNO_CODES.EIO);
            }
            var contents = stream.node.contents;
            if (position >= contents.length) return 0;
            var size = Math.min(contents.length - position, length);
            assert(size >= 0);
            if (contents.slice) {
                for (var i = 0; i < size; i++) {
                    buffer[offset + i] = contents[position + i];
                }
            } else {
                for (var i = 0; i < size; i++) {
                    buffer[offset + i] = contents.get(position + i);
                }
            }
            return size;
        };
        node.stream_ops = stream_ops;
        return node;
    },
    createPreloadedFile: function (parent, name, url, canRead, canWrite, onload, onerror, dontCreateFile, canOwn) {
        Browser.init();
        var fullname = name ? PATH.resolve(PATH.join2(parent, name)) : parent;
        function processData(byteArray) {
            function finish(byteArray) {
                if (!dontCreateFile) {
                    FS.createDataFile(parent, name, byteArray, canRead, canWrite, canOwn);
                }
                if (onload) onload();
                removeRunDependency("cp " + fullname);
            }
            var handled = false;
            Module["preloadPlugins"].forEach(function (plugin) {
                if (handled) return;
                if (plugin["canHandle"](fullname)) {
                    plugin["handle"](byteArray, fullname, finish, function () {
                        if (onerror) onerror();
                        removeRunDependency("cp " + fullname);
                    });
                    handled = true;
                }
            });
            if (!handled) finish(byteArray);
        }
        addRunDependency("cp " + fullname);
        if (typeof url == "string") {
            Browser.asyncLoad(
                url,
                function (byteArray) {
                    processData(byteArray);
                },
                onerror
            );
        } else {
            processData(url);
        }
    },
    indexedDB: function () {
        return window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
    },
    DB_NAME: function () {
        return "EM_FS_" + window.location.pathname;
    },
    DB_VERSION: 20,
    DB_STORE_NAME: "FILE_DATA",
    saveFilesToDB: function (paths, onload, onerror) {
        onload = onload || function () {};
        onerror = onerror || function () {};
        var indexedDB = FS.indexedDB();
        try {
            var openRequest = indexedDB.open(FS.DB_NAME(), FS.DB_VERSION);
        } catch (e) {
            return onerror(e);
        }
        openRequest.onupgradeneeded = function openRequest_onupgradeneeded() {
            console.log("creating db");
            var db = openRequest.result;
            db.createObjectStore(FS.DB_STORE_NAME);
        };
        openRequest.onsuccess = function openRequest_onsuccess() {
            var db = openRequest.result;
            var transaction = db.transaction([FS.DB_STORE_NAME], "readwrite");
            var files = transaction.objectStore(FS.DB_STORE_NAME);
            var ok = 0,
                fail = 0,
                total = paths.length;
            function finish() {
                if (fail == 0) onload();
                else onerror();
            }
            paths.forEach(function (path) {
                var putRequest = files.put(FS.analyzePath(path).object.contents, path);
                putRequest.onsuccess = function putRequest_onsuccess() {
                    ok++;
                    if (ok + fail == total) finish();
                };
                putRequest.onerror = function putRequest_onerror() {
                    fail++;
                    if (ok + fail == total) finish();
                };
            });
            transaction.onerror = onerror;
        };
        openRequest.onerror = onerror;
    },
    loadFilesFromDB: function (paths, onload, onerror) {
        onload = onload || function () {};
        onerror = onerror || function () {};
        var indexedDB = FS.indexedDB();
        try {
            var openRequest = indexedDB.open(FS.DB_NAME(), FS.DB_VERSION);
        } catch (e) {
            return onerror(e);
        }
        openRequest.onupgradeneeded = onerror;
        openRequest.onsuccess = function openRequest_onsuccess() {
            var db = openRequest.result;
            try {
                var transaction = db.transaction([FS.DB_STORE_NAME], "readonly");
            } catch (e) {
                onerror(e);
                return;
            }
            var files = transaction.objectStore(FS.DB_STORE_NAME);
            var ok = 0,
                fail = 0,
                total = paths.length;
            function finish() {
                if (fail == 0) onload();
                else onerror();
            }
            paths.forEach(function (path) {
                var getRequest = files.get(path);
                getRequest.onsuccess = function getRequest_onsuccess() {
                    if (FS.analyzePath(path).exists) {
                        FS.unlink(path);
                    }
                    FS.createDataFile(PATH.dirname(path), PATH.basename(path), getRequest.result, true, true, true);
                    ok++;
                    if (ok + fail == total) finish();
                };
                getRequest.onerror = function getRequest_onerror() {
                    fail++;
                    if (ok + fail == total) finish();
                };
            });
            transaction.onerror = onerror;
        };
        openRequest.onerror = onerror;
    },
};
function _mkport() {
    throw "TODO";
}
var SOCKFS = {
    mount: function (mount) {
        Module["websocket"] = Module["websocket"] && "object" === typeof Module["websocket"] ? Module["websocket"] : {};
        Module["websocket"]._callbacks = {};
        Module["websocket"]["on"] = function (event, callback) {
            if ("function" === typeof callback) {
                this._callbacks[event] = callback;
            }
            return this;
        };
        Module["websocket"].emit = function (event, param) {
            if ("function" === typeof this._callbacks[event]) {
                this._callbacks[event].call(this, param);
            }
        };
        return FS.createNode(null, "/", 16384 | 511, 0);
    },
    createSocket: function (family, type, protocol) {
        var streaming = type == 1;
        if (protocol) {
            assert(streaming == (protocol == 6));
        }
        var sock = { family: family, type: type, protocol: protocol, server: null, error: null, peers: {}, pending: [], recv_queue: [], sock_ops: SOCKFS.websocket_sock_ops };
        var name = SOCKFS.nextname();
        var node = FS.createNode(SOCKFS.root, name, 49152, 0);
        node.sock = sock;
        var stream = FS.createStream({ path: name, node: node, flags: FS.modeStringToFlags("r+"), seekable: false, stream_ops: SOCKFS.stream_ops });
        sock.stream = stream;
        return sock;
    },
    getSocket: function (fd) {
        var stream = FS.getStream(fd);
        if (!stream || !FS.isSocket(stream.node.mode)) {
            return null;
        }
        return stream.node.sock;
    },
    stream_ops: {
        poll: function (stream) {
            var sock = stream.node.sock;
            return sock.sock_ops.poll(sock);
        },
        ioctl: function (stream, request, varargs) {
            var sock = stream.node.sock;
            return sock.sock_ops.ioctl(sock, request, varargs);
        },
        read: function (stream, buffer, offset, length, position) {
            var sock = stream.node.sock;
            var msg = sock.sock_ops.recvmsg(sock, length);
            if (!msg) {
                return 0;
            }
            buffer.set(msg.buffer, offset);
            return msg.buffer.length;
        },
        write: function (stream, buffer, offset, length, position) {
            var sock = stream.node.sock;
            return sock.sock_ops.sendmsg(sock, buffer, offset, length);
        },
        close: function (stream) {
            var sock = stream.node.sock;
            sock.sock_ops.close(sock);
        },
    },
    nextname: function () {
        if (!SOCKFS.nextname.current) {
            SOCKFS.nextname.current = 0;
        }
        return "socket[" + SOCKFS.nextname.current++ + "]";
    },
    websocket_sock_ops: {
        createPeer: function (sock, addr, port) {
            var ws;
            if (typeof addr === "object") {
                ws = addr;
                addr = null;
                port = null;
            }
            if (ws) {
                if (ws._socket) {
                    addr = ws._socket.remoteAddress;
                    port = ws._socket.remotePort;
                } else {
                    var result = /ws[s]?:\/\/([^:]+):(\d+)/.exec(ws.url);
                    if (!result) {
                        throw new Error("WebSocket URL must be in the format ws(s)://address:port");
                    }
                    addr = result[1];
                    port = parseInt(result[2], 10);
                }
            } else {
                try {
                    var runtimeConfig = Module["websocket"] && "object" === typeof Module["websocket"];
                    var url = "ws:#".replace("#", "//");
                    if (runtimeConfig) {
                        if ("string" === typeof Module["websocket"]["url"]) {
                            url = Module["websocket"]["url"];
                        }
                    }
                    if (url === "ws://" || url === "wss://") {
                        var parts = addr.split("/");
                        url = url + parts[0] + ":" + port + "/" + parts.slice(1).join("/");
                    }
                    var subProtocols = "binary";
                    if (runtimeConfig) {
                        if ("string" === typeof Module["websocket"]["subprotocol"]) {
                            subProtocols = Module["websocket"]["subprotocol"];
                        }
                    }
                    subProtocols = subProtocols.replace(/^ +| +$/g, "").split(/ *, */);
                    var opts = ENVIRONMENT_IS_NODE ? { protocol: subProtocols.toString() } : subProtocols;
                    var WebSocket = ENVIRONMENT_IS_NODE ? require("ws") : window["WebSocket"];
                    ws = new WebSocket(url, opts);
                    ws.binaryType = "arraybuffer";
                } catch (e) {
                    throw new FS.ErrnoError(ERRNO_CODES.EHOSTUNREACH);
                }
            }
            var peer = { addr: addr, port: port, socket: ws, dgram_send_queue: [] };
            SOCKFS.websocket_sock_ops.addPeer(sock, peer);
            SOCKFS.websocket_sock_ops.handlePeerEvents(sock, peer);
            if (sock.type === 2 && typeof sock.sport !== "undefined") {
                peer.dgram_send_queue.push(new Uint8Array([255, 255, 255, 255, "p".charCodeAt(0), "o".charCodeAt(0), "r".charCodeAt(0), "t".charCodeAt(0), (sock.sport & 65280) >> 8, sock.sport & 255]));
            }
            return peer;
        },
        getPeer: function (sock, addr, port) {
            return sock.peers[addr + ":" + port];
        },
        addPeer: function (sock, peer) {
            sock.peers[peer.addr + ":" + peer.port] = peer;
        },
        removePeer: function (sock, peer) {
            delete sock.peers[peer.addr + ":" + peer.port];
        },
        handlePeerEvents: function (sock, peer) {
            var first = true;
            var handleOpen = function () {
                Module["websocket"].emit("open", sock.stream.fd);
                try {
                    var queued = peer.dgram_send_queue.shift();
                    while (queued) {
                        peer.socket.send(queued);
                        queued = peer.dgram_send_queue.shift();
                    }
                } catch (e) {
                    peer.socket.close();
                }
            };
            function handleMessage(data) {
                assert(typeof data !== "string" && data.byteLength !== undefined);
                data = new Uint8Array(data);
                var wasfirst = first;
                first = false;
                if (
                    wasfirst &&
                    data.length === 10 &&
                    data[0] === 255 &&
                    data[1] === 255 &&
                    data[2] === 255 &&
                    data[3] === 255 &&
                    data[4] === "p".charCodeAt(0) &&
                    data[5] === "o".charCodeAt(0) &&
                    data[6] === "r".charCodeAt(0) &&
                    data[7] === "t".charCodeAt(0)
                ) {
                    var newport = (data[8] << 8) | data[9];
                    SOCKFS.websocket_sock_ops.removePeer(sock, peer);
                    peer.port = newport;
                    SOCKFS.websocket_sock_ops.addPeer(sock, peer);
                    return;
                }
                sock.recv_queue.push({ addr: peer.addr, port: peer.port, data: data });
                Module["websocket"].emit("message", sock.stream.fd);
            }
            if (ENVIRONMENT_IS_NODE) {
                peer.socket.on("open", handleOpen);
                peer.socket.on("message", function (data, flags) {
                    if (!flags.binary) {
                        return;
                    }
                    handleMessage(new Uint8Array(data).buffer);
                });
                peer.socket.on("close", function () {
                    Module["websocket"].emit("close", sock.stream.fd);
                });
                peer.socket.on("error", function (error) {
                    sock.error = ERRNO_CODES.ECONNREFUSED;
                    Module["websocket"].emit("error", [sock.stream.fd, sock.error, "ECONNREFUSED: Connection refused"]);
                });
            } else {
                peer.socket.onopen = handleOpen;
                peer.socket.onclose = function () {
                    Module["websocket"].emit("close", sock.stream.fd);
                };
                peer.socket.onmessage = function peer_socket_onmessage(event) {
                    handleMessage(event.data);
                };
                peer.socket.onerror = function (error) {
                    sock.error = ERRNO_CODES.ECONNREFUSED;
                    Module["websocket"].emit("error", [sock.stream.fd, sock.error, "ECONNREFUSED: Connection refused"]);
                };
            }
        },
        poll: function (sock) {
            if (sock.type === 1 && sock.server) {
                return sock.pending.length ? 64 | 1 : 0;
            }
            var mask = 0;
            var dest = sock.type === 1 ? SOCKFS.websocket_sock_ops.getPeer(sock, sock.daddr, sock.dport) : null;
            if (sock.recv_queue.length || !dest || (dest && dest.socket.readyState === dest.socket.CLOSING) || (dest && dest.socket.readyState === dest.socket.CLOSED)) {
                mask |= 64 | 1;
            }
            if (!dest || (dest && dest.socket.readyState === dest.socket.OPEN)) {
                mask |= 4;
            }
            if ((dest && dest.socket.readyState === dest.socket.CLOSING) || (dest && dest.socket.readyState === dest.socket.CLOSED)) {
                mask |= 16;
            }
            return mask;
        },
        ioctl: function (sock, request, arg) {
            switch (request) {
                case 21531:
                    var bytes = 0;
                    if (sock.recv_queue.length) {
                        bytes = sock.recv_queue[0].data.length;
                    }
                    HEAP32[arg >> 2] = bytes;
                    return 0;
                default:
                    return ERRNO_CODES.EINVAL;
            }
        },
        close: function (sock) {
            if (sock.server) {
                try {
                    sock.server.close();
                } catch (e) {}
                sock.server = null;
            }
            var peers = Object.keys(sock.peers);
            for (var i = 0; i < peers.length; i++) {
                var peer = sock.peers[peers[i]];
                try {
                    peer.socket.close();
                } catch (e) {}
                SOCKFS.websocket_sock_ops.removePeer(sock, peer);
            }
            return 0;
        },
        bind: function (sock, addr, port) {
            if (typeof sock.saddr !== "undefined" || typeof sock.sport !== "undefined") {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            sock.saddr = addr;
            sock.sport = port || _mkport();
            if (sock.type === 2) {
                if (sock.server) {
                    sock.server.close();
                    sock.server = null;
                }
                try {
                    sock.sock_ops.listen(sock, 0);
                } catch (e) {
                    if (!(e instanceof FS.ErrnoError)) throw e;
                    if (e.errno !== ERRNO_CODES.EOPNOTSUPP) throw e;
                }
            }
        },
        connect: function (sock, addr, port) {
            if (sock.server) {
                throw new FS.ErrnoError(ERRNO_CODES.EOPNOTSUPP);
            }
            if (typeof sock.daddr !== "undefined" && typeof sock.dport !== "undefined") {
                var dest = SOCKFS.websocket_sock_ops.getPeer(sock, sock.daddr, sock.dport);
                if (dest) {
                    if (dest.socket.readyState === dest.socket.CONNECTING) {
                        throw new FS.ErrnoError(ERRNO_CODES.EALREADY);
                    } else {
                        throw new FS.ErrnoError(ERRNO_CODES.EISCONN);
                    }
                }
            }
            var peer = SOCKFS.websocket_sock_ops.createPeer(sock, addr, port);
            sock.daddr = peer.addr;
            sock.dport = peer.port;
            throw new FS.ErrnoError(ERRNO_CODES.EINPROGRESS);
        },
        listen: function (sock, backlog) {
            if (!ENVIRONMENT_IS_NODE) {
                throw new FS.ErrnoError(ERRNO_CODES.EOPNOTSUPP);
            }
            if (sock.server) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            var WebSocketServer = require("ws").Server;
            var host = sock.saddr;
            sock.server = new WebSocketServer({ host: host, port: sock.sport });
            Module["websocket"].emit("listen", sock.stream.fd);
            sock.server.on("connection", function (ws) {
                if (sock.type === 1) {
                    var newsock = SOCKFS.createSocket(sock.family, sock.type, sock.protocol);
                    var peer = SOCKFS.websocket_sock_ops.createPeer(newsock, ws);
                    newsock.daddr = peer.addr;
                    newsock.dport = peer.port;
                    sock.pending.push(newsock);
                    Module["websocket"].emit("connection", newsock.stream.fd);
                } else {
                    SOCKFS.websocket_sock_ops.createPeer(sock, ws);
                    Module["websocket"].emit("connection", sock.stream.fd);
                }
            });
            sock.server.on("closed", function () {
                Module["websocket"].emit("close", sock.stream.fd);
                sock.server = null;
            });
            sock.server.on("error", function (error) {
                sock.error = ERRNO_CODES.EHOSTUNREACH;
                Module["websocket"].emit("error", [sock.stream.fd, sock.error, "EHOSTUNREACH: Host is unreachable"]);
            });
        },
        accept: function (listensock) {
            if (!listensock.server) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
            var newsock = listensock.pending.shift();
            newsock.stream.flags = listensock.stream.flags;
            return newsock;
        },
        getname: function (sock, peer) {
            var addr, port;
            if (peer) {
                if (sock.daddr === undefined || sock.dport === undefined) {
                    throw new FS.ErrnoError(ERRNO_CODES.ENOTCONN);
                }
                addr = sock.daddr;
                port = sock.dport;
            } else {
                addr = sock.saddr || 0;
                port = sock.sport || 0;
            }
            return { addr: addr, port: port };
        },
        sendmsg: function (sock, buffer, offset, length, addr, port) {
            if (sock.type === 2) {
                if (addr === undefined || port === undefined) {
                    addr = sock.daddr;
                    port = sock.dport;
                }
                if (addr === undefined || port === undefined) {
                    throw new FS.ErrnoError(ERRNO_CODES.EDESTADDRREQ);
                }
            } else {
                addr = sock.daddr;
                port = sock.dport;
            }
            var dest = SOCKFS.websocket_sock_ops.getPeer(sock, addr, port);
            if (sock.type === 1) {
                if (!dest || dest.socket.readyState === dest.socket.CLOSING || dest.socket.readyState === dest.socket.CLOSED) {
                    throw new FS.ErrnoError(ERRNO_CODES.ENOTCONN);
                } else if (dest.socket.readyState === dest.socket.CONNECTING) {
                    throw new FS.ErrnoError(ERRNO_CODES.EAGAIN);
                }
            }
            var data;
            if (buffer instanceof Array || buffer instanceof ArrayBuffer) {
                data = buffer.slice(offset, offset + length);
            } else {
                data = buffer.buffer.slice(buffer.byteOffset + offset, buffer.byteOffset + offset + length);
            }
            if (sock.type === 2) {
                if (!dest || dest.socket.readyState !== dest.socket.OPEN) {
                    if (!dest || dest.socket.readyState === dest.socket.CLOSING || dest.socket.readyState === dest.socket.CLOSED) {
                        dest = SOCKFS.websocket_sock_ops.createPeer(sock, addr, port);
                    }
                    dest.dgram_send_queue.push(data);
                    return length;
                }
            }
            try {
                dest.socket.send(data);
                return length;
            } catch (e) {
                throw new FS.ErrnoError(ERRNO_CODES.EINVAL);
            }
        },
        recvmsg: function (sock, length) {
            if (sock.type === 1 && sock.server) {
                throw new FS.ErrnoError(ERRNO_CODES.ENOTCONN);
            }
            var queued = sock.recv_queue.shift();
            if (!queued) {
                if (sock.type === 1) {
                    var dest = SOCKFS.websocket_sock_ops.getPeer(sock, sock.daddr, sock.dport);
                    if (!dest) {
                        throw new FS.ErrnoError(ERRNO_CODES.ENOTCONN);
                    } else if (dest.socket.readyState === dest.socket.CLOSING || dest.socket.readyState === dest.socket.CLOSED) {
                        return null;
                    } else {
                        throw new FS.ErrnoError(ERRNO_CODES.EAGAIN);
                    }
                } else {
                    throw new FS.ErrnoError(ERRNO_CODES.EAGAIN);
                }
            }
            var queuedLength = queued.data.byteLength || queued.data.length;
            var queuedOffset = queued.data.byteOffset || 0;
            var queuedBuffer = queued.data.buffer || queued.data;
            var bytesRead = Math.min(length, queuedLength);
            var res = { buffer: new Uint8Array(queuedBuffer, queuedOffset, bytesRead), addr: queued.addr, port: queued.port };
            if (sock.type === 1 && bytesRead < queuedLength) {
                var bytesRemaining = queuedLength - bytesRead;
                queued.data = new Uint8Array(queuedBuffer, queuedOffset + bytesRead, bytesRemaining);
                sock.recv_queue.unshift(queued);
            }
            return res;
        },
    },
};
function _send(fd, buf, len, flags) {
    var sock = SOCKFS.getSocket(fd);
    if (!sock) {
        ___setErrNo(ERRNO_CODES.EBADF);
        return -1;
    }
    return _write(fd, buf, len);
}
function _pwrite(fildes, buf, nbyte, offset) {
    var stream = FS.getStream(fildes);
    if (!stream) {
        ___setErrNo(ERRNO_CODES.EBADF);
        return -1;
    }
    try {
        var slab = HEAP8;
        return FS.write(stream, slab, buf, nbyte, offset);
    } catch (e) {
        FS.handleFSError(e);
        return -1;
    }
}
function _write(fildes, buf, nbyte) {
    var stream = FS.getStream(fildes);
    if (!stream) {
        ___setErrNo(ERRNO_CODES.EBADF);
        return -1;
    }
    try {
        var slab = HEAP8;
        return FS.write(stream, slab, buf, nbyte);
    } catch (e) {
        FS.handleFSError(e);
        return -1;
    }
}
function _fileno(stream) {
    stream = FS.getStreamFromPtr(stream);
    if (!stream) return -1;
    return stream.fd;
}
function _fwrite(ptr, size, nitems, stream) {
    var bytesToWrite = nitems * size;
    if (bytesToWrite == 0) return 0;
    var fd = _fileno(stream);
    var bytesWritten = _write(fd, ptr, bytesToWrite);
    if (bytesWritten == -1) {
        var streamObj = FS.getStreamFromPtr(stream);
        if (streamObj) streamObj.error = true;
        return 0;
    } else {
        return (bytesWritten / size) | 0;
    }
}
Module["_strlen"] = _strlen;
function __reallyNegative(x) {
    return x < 0 || (x === 0 && 1 / x === -Infinity);
}
function __formatString(format, varargs) {
    var textIndex = format;
    var argIndex = 0;
    function getNextArg(type) {
        var ret;
        if (type === "double") {
            ret = ((HEAP32[tempDoublePtr >> 2] = HEAP32[(varargs + argIndex) >> 2]), (HEAP32[(tempDoublePtr + 4) >> 2] = HEAP32[(varargs + (argIndex + 4)) >> 2]), +HEAPF64[tempDoublePtr >> 3]);
        } else if (type == "i64") {
            ret = [HEAP32[(varargs + argIndex) >> 2], HEAP32[(varargs + (argIndex + 4)) >> 2]];
        } else {
            type = "i32";
            ret = HEAP32[(varargs + argIndex) >> 2];
        }
        argIndex += Runtime.getNativeFieldSize(type);
        return ret;
    }
    var ret = [];
    var curr, next, currArg;
    while (1) {
        var startTextIndex = textIndex;
        curr = HEAP8[textIndex >> 0];
        if (curr === 0) break;
        next = HEAP8[(textIndex + 1) >> 0];
        if (curr == 37) {
            var flagAlwaysSigned = false;
            var flagLeftAlign = false;
            var flagAlternative = false;
            var flagZeroPad = false;
            var flagPadSign = false;
            flagsLoop: while (1) {
                switch (next) {
                    case 43:
                        flagAlwaysSigned = true;
                        break;
                    case 45:
                        flagLeftAlign = true;
                        break;
                    case 35:
                        flagAlternative = true;
                        break;
                    case 48:
                        if (flagZeroPad) {
                            break flagsLoop;
                        } else {
                            flagZeroPad = true;
                            break;
                        }
                    case 32:
                        flagPadSign = true;
                        break;
                    default:
                        break flagsLoop;
                }
                textIndex++;
                next = HEAP8[(textIndex + 1) >> 0];
            }
            var width = 0;
            if (next == 42) {
                width = getNextArg("i32");
                textIndex++;
                next = HEAP8[(textIndex + 1) >> 0];
            } else {
                while (next >= 48 && next <= 57) {
                    width = width * 10 + (next - 48);
                    textIndex++;
                    next = HEAP8[(textIndex + 1) >> 0];
                }
            }
            var precisionSet = false,
                precision = -1;
            if (next == 46) {
                precision = 0;
                precisionSet = true;
                textIndex++;
                next = HEAP8[(textIndex + 1) >> 0];
                if (next == 42) {
                    precision = getNextArg("i32");
                    textIndex++;
                } else {
                    while (1) {
                        var precisionChr = HEAP8[(textIndex + 1) >> 0];
                        if (precisionChr < 48 || precisionChr > 57) break;
                        precision = precision * 10 + (precisionChr - 48);
                        textIndex++;
                    }
                }
                next = HEAP8[(textIndex + 1) >> 0];
            }
            if (precision < 0) {
                precision = 6;
                precisionSet = false;
            }
            var argSize;
            switch (String.fromCharCode(next)) {
                case "h":
                    var nextNext = HEAP8[(textIndex + 2) >> 0];
                    if (nextNext == 104) {
                        textIndex++;
                        argSize = 1;
                    } else {
                        argSize = 2;
                    }
                    break;
                case "l":
                    var nextNext = HEAP8[(textIndex + 2) >> 0];
                    if (nextNext == 108) {
                        textIndex++;
                        argSize = 8;
                    } else {
                        argSize = 4;
                    }
                    break;
                case "L":
                case "q":
                case "j":
                    argSize = 8;
                    break;
                case "z":
                case "t":
                case "I":
                    argSize = 4;
                    break;
                default:
                    argSize = null;
            }
            if (argSize) textIndex++;
            next = HEAP8[(textIndex + 1) >> 0];
            switch (String.fromCharCode(next)) {
                case "d":
                case "i":
                case "u":
                case "o":
                case "x":
                case "X":
                case "p": {
                    var signed = next == 100 || next == 105;
                    argSize = argSize || 4;
                    var currArg = getNextArg("i" + argSize * 8);
                    var origArg = currArg;
                    var argText;
                    if (argSize == 8) {
                        currArg = Runtime.makeBigInt(currArg[0], currArg[1], next == 117);
                    }
                    if (argSize <= 4) {
                        var limit = Math.pow(256, argSize) - 1;
                        currArg = (signed ? reSign : unSign)(currArg & limit, argSize * 8);
                    }
                    var currAbsArg = Math.abs(currArg);
                    var prefix = "";
                    if (next == 100 || next == 105) {
                        if (argSize == 8 && i64Math) argText = i64Math.stringify(origArg[0], origArg[1], null);
                        else argText = reSign(currArg, 8 * argSize, 1).toString(10);
                    } else if (next == 117) {
                        if (argSize == 8 && i64Math) argText = i64Math.stringify(origArg[0], origArg[1], true);
                        else argText = unSign(currArg, 8 * argSize, 1).toString(10);
                        currArg = Math.abs(currArg);
                    } else if (next == 111) {
                        argText = (flagAlternative ? "0" : "") + currAbsArg.toString(8);
                    } else if (next == 120 || next == 88) {
                        prefix = flagAlternative && currArg != 0 ? "0x" : "";
                        if (argSize == 8 && i64Math) {
                            if (origArg[1]) {
                                argText = (origArg[1] >>> 0).toString(16);
                                var lower = (origArg[0] >>> 0).toString(16);
                                while (lower.length < 8) lower = "0" + lower;
                                argText += lower;
                            } else {
                                argText = (origArg[0] >>> 0).toString(16);
                            }
                        } else if (currArg < 0) {
                            currArg = -currArg;
                            argText = (currAbsArg - 1).toString(16);
                            var buffer = [];
                            for (var i = 0; i < argText.length; i++) {
                                buffer.push((15 - parseInt(argText[i], 16)).toString(16));
                            }
                            argText = buffer.join("");
                            while (argText.length < argSize * 2) argText = "f" + argText;
                        } else {
                            argText = currAbsArg.toString(16);
                        }
                        if (next == 88) {
                            prefix = prefix.toUpperCase();
                            argText = argText.toUpperCase();
                        }
                    } else if (next == 112) {
                        if (currAbsArg === 0) {
                            argText = "(nil)";
                        } else {
                            prefix = "0x";
                            argText = currAbsArg.toString(16);
                        }
                    }
                    if (precisionSet) {
                        while (argText.length < precision) {
                            argText = "0" + argText;
                        }
                    }
                    if (currArg >= 0) {
                        if (flagAlwaysSigned) {
                            prefix = "+" + prefix;
                        } else if (flagPadSign) {
                            prefix = " " + prefix;
                        }
                    }
                    if (argText.charAt(0) == "-") {
                        prefix = "-" + prefix;
                        argText = argText.substr(1);
                    }
                    while (prefix.length + argText.length < width) {
                        if (flagLeftAlign) {
                            argText += " ";
                        } else {
                            if (flagZeroPad) {
                                argText = "0" + argText;
                            } else {
                                prefix = " " + prefix;
                            }
                        }
                    }
                    argText = prefix + argText;
                    argText.split("").forEach(function (chr) {
                        ret.push(chr.charCodeAt(0));
                    });
                    break;
                }
                case "f":
                case "F":
                case "e":
                case "E":
                case "g":
                case "G": {
                    var currArg = getNextArg("double");
                    var argText;
                    if (isNaN(currArg)) {
                        argText = "nan";
                        flagZeroPad = false;
                    } else if (!isFinite(currArg)) {
                        argText = (currArg < 0 ? "-" : "") + "inf";
                        flagZeroPad = false;
                    } else {
                        var isGeneral = false;
                        var effectivePrecision = Math.min(precision, 20);
                        if (next == 103 || next == 71) {
                            isGeneral = true;
                            precision = precision || 1;
                            var exponent = parseInt(currArg.toExponential(effectivePrecision).split("e")[1], 10);
                            if (precision > exponent && exponent >= -4) {
                                next = (next == 103 ? "f" : "F").charCodeAt(0);
                                precision -= exponent + 1;
                            } else {
                                next = (next == 103 ? "e" : "E").charCodeAt(0);
                                precision--;
                            }
                            effectivePrecision = Math.min(precision, 20);
                        }
                        if (next == 101 || next == 69) {
                            argText = currArg.toExponential(effectivePrecision);
                            if (/[eE][-+]\d$/.test(argText)) {
                                argText = argText.slice(0, -1) + "0" + argText.slice(-1);
                            }
                        } else if (next == 102 || next == 70) {
                            argText = currArg.toFixed(effectivePrecision);
                            if (currArg === 0 && __reallyNegative(currArg)) {
                                argText = "-" + argText;
                            }
                        }
                        var parts = argText.split("e");
                        if (isGeneral && !flagAlternative) {
                            while (parts[0].length > 1 && parts[0].indexOf(".") != -1 && (parts[0].slice(-1) == "0" || parts[0].slice(-1) == ".")) {
                                parts[0] = parts[0].slice(0, -1);
                            }
                        } else {
                            if (flagAlternative && argText.indexOf(".") == -1) parts[0] += ".";
                            while (precision > effectivePrecision++) parts[0] += "0";
                        }
                        argText = parts[0] + (parts.length > 1 ? "e" + parts[1] : "");
                        if (next == 69) argText = argText.toUpperCase();
                        if (currArg >= 0) {
                            if (flagAlwaysSigned) {
                                argText = "+" + argText;
                            } else if (flagPadSign) {
                                argText = " " + argText;
                            }
                        }
                    }
                    while (argText.length < width) {
                        if (flagLeftAlign) {
                            argText += " ";
                        } else {
                            if (flagZeroPad && (argText[0] == "-" || argText[0] == "+")) {
                                argText = argText[0] + "0" + argText.slice(1);
                            } else {
                                argText = (flagZeroPad ? "0" : " ") + argText;
                            }
                        }
                    }
                    if (next < 97) argText = argText.toUpperCase();
                    argText.split("").forEach(function (chr) {
                        ret.push(chr.charCodeAt(0));
                    });
                    break;
                }
                case "s": {
                    var arg = getNextArg("i8*");
                    var argLength = arg ? _strlen(arg) : "(null)".length;
                    if (precisionSet) argLength = Math.min(argLength, precision);
                    if (!flagLeftAlign) {
                        while (argLength < width--) {
                            ret.push(32);
                        }
                    }
                    if (arg) {
                        for (var i = 0; i < argLength; i++) {
                            ret.push(HEAPU8[arg++ >> 0]);
                        }
                    } else {
                        ret = ret.concat(intArrayFromString("(null)".substr(0, argLength), true));
                    }
                    if (flagLeftAlign) {
                        while (argLength < width--) {
                            ret.push(32);
                        }
                    }
                    break;
                }
                case "c": {
                    if (flagLeftAlign) ret.push(getNextArg("i8"));
                    while (--width > 0) {
                        ret.push(32);
                    }
                    if (!flagLeftAlign) ret.push(getNextArg("i8"));
                    break;
                }
                case "n": {
                    var ptr = getNextArg("i32*");
                    HEAP32[ptr >> 2] = ret.length;
                    break;
                }
                case "%": {
                    ret.push(curr);
                    break;
                }
                default: {
                    for (var i = startTextIndex; i < textIndex + 2; i++) {
                        ret.push(HEAP8[i >> 0]);
                    }
                }
            }
            textIndex += 2;
        } else {
            ret.push(curr);
            textIndex += 1;
        }
    }
    return ret;
}
function _fprintf(stream, format, varargs) {
    var result = __formatString(format, varargs);
    var stack = Runtime.stackSave();
    var ret = _fwrite(allocate(result, "i8", ALLOC_STACK), 1, result.length, stream);
    Runtime.stackRestore(stack);
    return ret;
}
Module["_memset"] = _memset;
function ___errno_location() {
    return ___errno_state;
}
function _abort() {
    Module["abort"]();
}
function __exit(status) {
    Module["exit"](status);
}
function _exit(status) {
    __exit(status);
}
function ___assert_fail(condition, filename, line, func) {
    ABORT = true;
    throw "Assertion failed: " + Pointer_stringify(condition) + ", at: " + [filename ? Pointer_stringify(filename) : "unknown filename", line, func ? Pointer_stringify(func) : "unknown function"] + " at " + stackTrace();
}
function _time(ptr) {
    var ret = (Date.now() / 1e3) | 0;
    if (ptr) {
        HEAP32[ptr >> 2] = ret;
    }
    return ret;
}
var Browser = {
    mainLoop: {
        scheduler: null,
        method: "",
        shouldPause: false,
        paused: false,
        queue: [],
        pause: function () {
            Browser.mainLoop.shouldPause = true;
        },
        resume: function () {
            if (Browser.mainLoop.paused) {
                Browser.mainLoop.paused = false;
                Browser.mainLoop.scheduler();
            }
            Browser.mainLoop.shouldPause = false;
        },
        updateStatus: function () {
            if (Module["setStatus"]) {
                var message = Module["statusMessage"] || "Please wait...";
                var remaining = Browser.mainLoop.remainingBlockers;
                var expected = Browser.mainLoop.expectedBlockers;
                if (remaining) {
                    if (remaining < expected) {
                        Module["setStatus"](message + " (" + (expected - remaining) + "/" + expected + ")");
                    } else {
                        Module["setStatus"](message);
                    }
                } else {
                    Module["setStatus"]("");
                }
            }
        },
        runIter: function (func) {
            if (ABORT) return;
            if (Module["preMainLoop"]) {
                var preRet = Module["preMainLoop"]();
                if (preRet === false) {
                    return;
                }
            }
            try {
                func();
            } catch (e) {
                if (e instanceof ExitStatus) {
                    return;
                } else {
                    if (e && typeof e === "object" && e.stack) Module.printErr("exception thrown: " + [e, e.stack]);
                    throw e;
                }
            }
            if (Module["postMainLoop"]) Module["postMainLoop"]();
        },
    },
    isFullScreen: false,
    pointerLock: false,
    moduleContextCreatedCallbacks: [],
    workers: [],
    init: function () {
        if (!Module["preloadPlugins"]) Module["preloadPlugins"] = [];
        if (Browser.initted) return;
        Browser.initted = true;
        try {
            new Blob();
            Browser.hasBlobConstructor = true;
        } catch (e) {
            Browser.hasBlobConstructor = false;
            console.log("warning: no blob constructor, cannot create blobs with mimetypes");
        }
        Browser.BlobBuilder = typeof MozBlobBuilder != "undefined" ? MozBlobBuilder : typeof WebKitBlobBuilder != "undefined" ? WebKitBlobBuilder : !Browser.hasBlobConstructor ? console.log("warning: no BlobBuilder") : null;
        Browser.URLObject = typeof window != "undefined" ? (window.URL ? window.URL : window.webkitURL) : undefined;
        if (!Module.noImageDecoding && typeof Browser.URLObject === "undefined") {
            console.log("warning: Browser does not support creating object URLs. Built-in browser image decoding will not be available.");
            Module.noImageDecoding = true;
        }
        var imagePlugin = {};
        imagePlugin["canHandle"] = function imagePlugin_canHandle(name) {
            return !Module.noImageDecoding && /\.(jpg|jpeg|png|bmp)$/i.test(name);
        };
        imagePlugin["handle"] = function imagePlugin_handle(byteArray, name, onload, onerror) {
            var b = null;
            if (Browser.hasBlobConstructor) {
                try {
                    b = new Blob([byteArray], { type: Browser.getMimetype(name) });
                    if (b.size !== byteArray.length) {
                        b = new Blob([new Uint8Array(byteArray).buffer], { type: Browser.getMimetype(name) });
                    }
                } catch (e) {
                    Runtime.warnOnce("Blob constructor present but fails: " + e + "; falling back to blob builder");
                }
            }
            if (!b) {
                var bb = new Browser.BlobBuilder();
                bb.append(new Uint8Array(byteArray).buffer);
                b = bb.getBlob();
            }
            var url = Browser.URLObject.createObjectURL(b);
            var img = new Image();
            img.onload = function img_onload() {
                assert(img.complete, "Image " + name + " could not be decoded");
                var canvas = document.createElement("canvas");
                canvas.width = img.width;
                canvas.height = img.height;
                var ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0);
                Module["preloadedImages"][name] = canvas;
                Browser.URLObject.revokeObjectURL(url);
                if (onload) onload(byteArray);
            };
            img.onerror = function img_onerror(event) {
                console.log("Image " + url + " could not be decoded");
                if (onerror) onerror();
            };
            img.src = url;
        };
        Module["preloadPlugins"].push(imagePlugin);
        var audioPlugin = {};
        audioPlugin["canHandle"] = function audioPlugin_canHandle(name) {
            return !Module.noAudioDecoding && name.substr(-4) in { ".ogg": 1, ".wav": 1, ".mp3": 1 };
        };
        audioPlugin["handle"] = function audioPlugin_handle(byteArray, name, onload, onerror) {
            var done = false;
            function finish(audio) {
                if (done) return;
                done = true;
                Module["preloadedAudios"][name] = audio;
                if (onload) onload(byteArray);
            }
            function fail() {
                if (done) return;
                done = true;
                Module["preloadedAudios"][name] = new Audio();
                if (onerror) onerror();
            }
            if (Browser.hasBlobConstructor) {
                try {
                    var b = new Blob([byteArray], { type: Browser.getMimetype(name) });
                } catch (e) {
                    return fail();
                }
                var url = Browser.URLObject.createObjectURL(b);
                var audio = new Audio();
                audio.addEventListener(
                    "canplaythrough",
                    function () {
                        finish(audio);
                    },
                    false
                );
                audio.onerror = function audio_onerror(event) {
                    if (done) return;
                    console.log("warning: browser could not fully decode audio " + name + ", trying slower base64 approach");
                    function encode64(data) {
                        var BASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
                        var PAD = "=";
                        var ret = "";
                        var leftchar = 0;
                        var leftbits = 0;
                        for (var i = 0; i < data.length; i++) {
                            leftchar = (leftchar << 8) | data[i];
                            leftbits += 8;
                            while (leftbits >= 6) {
                                var curr = (leftchar >> (leftbits - 6)) & 63;
                                leftbits -= 6;
                                ret += BASE[curr];
                            }
                        }
                        if (leftbits == 2) {
                            ret += BASE[(leftchar & 3) << 4];
                            ret += PAD + PAD;
                        } else if (leftbits == 4) {
                            ret += BASE[(leftchar & 15) << 2];
                            ret += PAD;
                        }
                        return ret;
                    }
                    audio.src = "data:audio/x-" + name.substr(-3) + ";base64," + encode64(byteArray);
                    finish(audio);
                };
                audio.src = url;
                Browser.safeSetTimeout(function () {
                    finish(audio);
                }, 1e4);
            } else {
                return fail();
            }
        };
        Module["preloadPlugins"].push(audioPlugin);
        var canvas = Module["canvas"];
        function pointerLockChange() {
            Browser.pointerLock = document["pointerLockElement"] === canvas || document["mozPointerLockElement"] === canvas || document["webkitPointerLockElement"] === canvas || document["msPointerLockElement"] === canvas;
        }
        if (canvas) {
            canvas.requestPointerLock = canvas["requestPointerLock"] || canvas["mozRequestPointerLock"] || canvas["webkitRequestPointerLock"] || canvas["msRequestPointerLock"] || function () {};
            canvas.exitPointerLock = document["exitPointerLock"] || document["mozExitPointerLock"] || document["webkitExitPointerLock"] || document["msExitPointerLock"] || function () {};
            canvas.exitPointerLock = canvas.exitPointerLock.bind(document);
            document.addEventListener("pointerlockchange", pointerLockChange, false);
            document.addEventListener("mozpointerlockchange", pointerLockChange, false);
            document.addEventListener("webkitpointerlockchange", pointerLockChange, false);
            document.addEventListener("mspointerlockchange", pointerLockChange, false);
            if (Module["elementPointerLock"]) {
                canvas.addEventListener(
                    "click",
                    function (ev) {
                        if (!Browser.pointerLock && canvas.requestPointerLock) {
                            canvas.requestPointerLock();
                            ev.preventDefault();
                        }
                    },
                    false
                );
            }
        }
    },
    createContext: function (canvas, useWebGL, setInModule, webGLContextAttributes) {
        if (useWebGL && Module.ctx && canvas == Module.canvas) return Module.ctx;
        var ctx;
        var contextHandle;
        if (useWebGL) {
            var contextAttributes = { antialias: false, alpha: false };
            if (webGLContextAttributes) {
                for (var attribute in webGLContextAttributes) {
                    contextAttributes[attribute] = webGLContextAttributes[attribute];
                }
            }
            contextHandle = GL.createContext(canvas, contextAttributes);
            ctx = GL.getContext(contextHandle).GLctx;
            canvas.style.backgroundColor = "black";
        } else {
            ctx = canvas.getContext("2d");
        }
        if (!ctx) return null;
        if (setInModule) {
            if (!useWebGL) assert(typeof GLctx === "undefined", "cannot set in module if GLctx is used, but we are a non-GL context that would replace it");
            Module.ctx = ctx;
            if (useWebGL) GL.makeContextCurrent(contextHandle);
            Module.useWebGL = useWebGL;
            Browser.moduleContextCreatedCallbacks.forEach(function (callback) {
                callback();
            });
            Browser.init();
        }
        return ctx;
    },
    destroyContext: function (canvas, useWebGL, setInModule) {},
    fullScreenHandlersInstalled: false,
    lockPointer: undefined,
    resizeCanvas: undefined,
    requestFullScreen: function (lockPointer, resizeCanvas) {
        Browser.lockPointer = lockPointer;
        Browser.resizeCanvas = resizeCanvas;
        if (typeof Browser.lockPointer === "undefined") Browser.lockPointer = true;
        if (typeof Browser.resizeCanvas === "undefined") Browser.resizeCanvas = false;
        var canvas = Module["canvas"];
        function fullScreenChange() {
            Browser.isFullScreen = false;
            var canvasContainer = canvas.parentNode;
            if (
                (document["webkitFullScreenElement"] ||
                    document["webkitFullscreenElement"] ||
                    document["mozFullScreenElement"] ||
                    document["mozFullscreenElement"] ||
                    document["fullScreenElement"] ||
                    document["fullscreenElement"] ||
                    document["msFullScreenElement"] ||
                    document["msFullscreenElement"] ||
                    document["webkitCurrentFullScreenElement"]) === canvasContainer
            ) {
                canvas.cancelFullScreen = document["cancelFullScreen"] || document["mozCancelFullScreen"] || document["webkitCancelFullScreen"] || document["msExitFullscreen"] || document["exitFullscreen"] || function () {};
                canvas.cancelFullScreen = canvas.cancelFullScreen.bind(document);
                if (Browser.lockPointer) canvas.requestPointerLock();
                Browser.isFullScreen = true;
                if (Browser.resizeCanvas) Browser.setFullScreenCanvasSize();
            } else {
                canvasContainer.parentNode.insertBefore(canvas, canvasContainer);
                canvasContainer.parentNode.removeChild(canvasContainer);
                if (Browser.resizeCanvas) Browser.setWindowedCanvasSize();
            }
            if (Module["onFullScreen"]) Module["onFullScreen"](Browser.isFullScreen);
            Browser.updateCanvasDimensions(canvas);
        }
        if (!Browser.fullScreenHandlersInstalled) {
            Browser.fullScreenHandlersInstalled = true;
            document.addEventListener("fullscreenchange", fullScreenChange, false);
            document.addEventListener("mozfullscreenchange", fullScreenChange, false);
            document.addEventListener("webkitfullscreenchange", fullScreenChange, false);
            document.addEventListener("MSFullscreenChange", fullScreenChange, false);
        }
        var canvasContainer = document.createElement("div");
        canvas.parentNode.insertBefore(canvasContainer, canvas);
        canvasContainer.appendChild(canvas);
        canvasContainer.requestFullScreen =
            canvasContainer["requestFullScreen"] ||
            canvasContainer["mozRequestFullScreen"] ||
            canvasContainer["msRequestFullscreen"] ||
            (canvasContainer["webkitRequestFullScreen"]
                ? function () {
                      canvasContainer["webkitRequestFullScreen"](Element["ALLOW_KEYBOARD_INPUT"]);
                  }
                : null);
        canvasContainer.requestFullScreen();
    },
    nextRAF: 0,
    fakeRequestAnimationFrame: function (func) {
        var now = Date.now();
        if (Browser.nextRAF === 0) {
            Browser.nextRAF = now + 1e3 / 60;
        } else {
            while (now + 2 >= Browser.nextRAF) {
                Browser.nextRAF += 1e3 / 60;
            }
        }
        var delay = Math.max(Browser.nextRAF - now, 0);
        setTimeout(func, delay);
    },
    requestAnimationFrame: function requestAnimationFrame(func) {
        if (typeof window === "undefined") {
            Browser.fakeRequestAnimationFrame(func);
        } else {
            if (!window.requestAnimationFrame) {
                window.requestAnimationFrame =
                    window["requestAnimationFrame"] ||
                    window["mozRequestAnimationFrame"] ||
                    window["webkitRequestAnimationFrame"] ||
                    window["msRequestAnimationFrame"] ||
                    window["oRequestAnimationFrame"] ||
                    Browser.fakeRequestAnimationFrame;
            }
            window.requestAnimationFrame(func);
        }
    },
    safeCallback: function (func) {
        return function () {
            if (!ABORT) return func.apply(null, arguments);
        };
    },
    safeRequestAnimationFrame: function (func) {
        return Browser.requestAnimationFrame(function () {
            if (!ABORT) func();
        });
    },
    safeSetTimeout: function (func, timeout) {
        Module["noExitRuntime"] = true;
        return setTimeout(function () {
            if (!ABORT) func();
        }, timeout);
    },
    safeSetInterval: function (func, timeout) {
        Module["noExitRuntime"] = true;
        return setInterval(function () {
            if (!ABORT) func();
        }, timeout);
    },
    getMimetype: function (name) {
        return { jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", bmp: "image/bmp", ogg: "audio/ogg", wav: "audio/wav", mp3: "audio/mpeg" }[name.substr(name.lastIndexOf(".") + 1)];
    },
    getUserMedia: function (func) {
        if (!window.getUserMedia) {
            window.getUserMedia = navigator["getUserMedia"] || navigator["mozGetUserMedia"];
        }
        window.getUserMedia(func);
    },
    getMovementX: function (event) {
        return event["movementX"] || event["mozMovementX"] || event["webkitMovementX"] || 0;
    },
    getMovementY: function (event) {
        return event["movementY"] || event["mozMovementY"] || event["webkitMovementY"] || 0;
    },
    getMouseWheelDelta: function (event) {
        var delta = 0;
        switch (event.type) {
            case "DOMMouseScroll":
                delta = event.detail;
                break;
            case "mousewheel":
                delta = -event.wheelDelta;
                break;
            case "wheel":
                delta = event.deltaY;
                break;
            default:
                throw "unrecognized mouse wheel event: " + event.type;
        }
        return Math.max(-1, Math.min(1, delta));
    },
    mouseX: 0,
    mouseY: 0,
    mouseMovementX: 0,
    mouseMovementY: 0,
    touches: {},
    lastTouches: {},
    calculateMouseEvent: function (event) {
        if (Browser.pointerLock) {
            if (event.type != "mousemove" && "mozMovementX" in event) {
                Browser.mouseMovementX = Browser.mouseMovementY = 0;
            } else {
                Browser.mouseMovementX = Browser.getMovementX(event);
                Browser.mouseMovementY = Browser.getMovementY(event);
            }
            if (typeof SDL != "undefined") {
                Browser.mouseX = SDL.mouseX + Browser.mouseMovementX;
                Browser.mouseY = SDL.mouseY + Browser.mouseMovementY;
            } else {
                Browser.mouseX += Browser.mouseMovementX;
                Browser.mouseY += Browser.mouseMovementY;
            }
        } else {
            var rect = Module["canvas"].getBoundingClientRect();
            var cw = Module["canvas"].width;
            var ch = Module["canvas"].height;
            var scrollX = typeof window.scrollX !== "undefined" ? window.scrollX : window.pageXOffset;
            var scrollY = typeof window.scrollY !== "undefined" ? window.scrollY : window.pageYOffset;
            if (event.type === "touchstart" || event.type === "touchend" || event.type === "touchmove") {
                var touch = event.touch;
                if (touch === undefined) {
                    return;
                }
                var adjustedX = touch.pageX - (scrollX + rect.left);
                var adjustedY = touch.pageY - (scrollY + rect.top);
                adjustedX = adjustedX * (cw / rect.width);
                adjustedY = adjustedY * (ch / rect.height);
                var coords = { x: adjustedX, y: adjustedY };
                if (event.type === "touchstart") {
                    Browser.lastTouches[touch.identifier] = coords;
                    Browser.touches[touch.identifier] = coords;
                } else if (event.type === "touchend" || event.type === "touchmove") {
                    Browser.lastTouches[touch.identifier] = Browser.touches[touch.identifier];
                    Browser.touches[touch.identifier] = { x: adjustedX, y: adjustedY };
                }
                return;
            }
            var x = event.pageX - (scrollX + rect.left);
            var y = event.pageY - (scrollY + rect.top);
            x = x * (cw / rect.width);
            y = y * (ch / rect.height);
            Browser.mouseMovementX = x - Browser.mouseX;
            Browser.mouseMovementY = y - Browser.mouseY;
            Browser.mouseX = x;
            Browser.mouseY = y;
        }
    },
    xhrLoad: function (url, onload, onerror) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.responseType = "arraybuffer";
        xhr.onload = function xhr_onload() {
            if (xhr.status == 200 || (xhr.status == 0 && xhr.response)) {
                onload(xhr.response);
            } else {
                onerror();
            }
        };
        xhr.onerror = onerror;
        xhr.send(null);
    },
    asyncLoad: function (url, onload, onerror, noRunDep) {
        Browser.xhrLoad(
            url,
            function (arrayBuffer) {
                assert(arrayBuffer, 'Loading data file "' + url + '" failed (no arrayBuffer).');
                onload(new Uint8Array(arrayBuffer));
                if (!noRunDep) removeRunDependency("al " + url);
            },
            function (event) {
                if (onerror) {
                    onerror();
                } else {
                    throw 'Loading data file "' + url + '" failed.';
                }
            }
        );
        if (!noRunDep) addRunDependency("al " + url);
    },
    resizeListeners: [],
    updateResizeListeners: function () {
        var canvas = Module["canvas"];
        Browser.resizeListeners.forEach(function (listener) {
            listener(canvas.width, canvas.height);
        });
    },
    setCanvasSize: function (width, height, noUpdates) {
        var canvas = Module["canvas"];
        Browser.updateCanvasDimensions(canvas, width, height);
        if (!noUpdates) Browser.updateResizeListeners();
    },
    windowedWidth: 0,
    windowedHeight: 0,
    setFullScreenCanvasSize: function () {
        if (typeof SDL != "undefined") {
            var flags = HEAPU32[(SDL.screen + Runtime.QUANTUM_SIZE * 0) >> 2];
            flags = flags | 8388608;
            HEAP32[(SDL.screen + Runtime.QUANTUM_SIZE * 0) >> 2] = flags;
        }
        Browser.updateResizeListeners();
    },
    setWindowedCanvasSize: function () {
        if (typeof SDL != "undefined") {
            var flags = HEAPU32[(SDL.screen + Runtime.QUANTUM_SIZE * 0) >> 2];
            flags = flags & ~8388608;
            HEAP32[(SDL.screen + Runtime.QUANTUM_SIZE * 0) >> 2] = flags;
        }
        Browser.updateResizeListeners();
    },
    updateCanvasDimensions: function (canvas, wNative, hNative) {
        if (wNative && hNative) {
            canvas.widthNative = wNative;
            canvas.heightNative = hNative;
        } else {
            wNative = canvas.widthNative;
            hNative = canvas.heightNative;
        }
        var w = wNative;
        var h = hNative;
        if (Module["forcedAspectRatio"] && Module["forcedAspectRatio"] > 0) {
            if (w / h < Module["forcedAspectRatio"]) {
                w = Math.round(h * Module["forcedAspectRatio"]);
            } else {
                h = Math.round(w / Module["forcedAspectRatio"]);
            }
        }
        if (
            (document["webkitFullScreenElement"] ||
                document["webkitFullscreenElement"] ||
                document["mozFullScreenElement"] ||
                document["mozFullscreenElement"] ||
                document["fullScreenElement"] ||
                document["fullscreenElement"] ||
                document["msFullScreenElement"] ||
                document["msFullscreenElement"] ||
                document["webkitCurrentFullScreenElement"]) === canvas.parentNode &&
            typeof screen != "undefined"
        ) {
            var factor = Math.min(screen.width / w, screen.height / h);
            w = Math.round(w * factor);
            h = Math.round(h * factor);
        }
        if (Browser.resizeCanvas) {
            if (canvas.width != w) canvas.width = w;
            if (canvas.height != h) canvas.height = h;
            if (typeof canvas.style != "undefined") {
                canvas.style.removeProperty("width");
                canvas.style.removeProperty("height");
            }
        } else {
            if (canvas.width != wNative) canvas.width = wNative;
            if (canvas.height != hNative) canvas.height = hNative;
            if (typeof canvas.style != "undefined") {
                if (w != wNative || h != hNative) {
                    canvas.style.setProperty("width", w + "px", "important");
                    canvas.style.setProperty("height", h + "px", "important");
                } else {
                    canvas.style.removeProperty("width");
                    canvas.style.removeProperty("height");
                }
            }
        }
    },
    wgetRequests: {},
    nextWgetRequestHandle: 0,
    getNextWgetRequestHandle: function () {
        var handle = Browser.nextWgetRequestHandle;
        Browser.nextWgetRequestHandle++;
        return handle;
    },
};
function _emscripten_memcpy_big(dest, src, num) {
    HEAPU8.set(HEAPU8.subarray(src, src + num), dest);
    return dest;
}
Module["_memcpy"] = _memcpy;
___errno_state = Runtime.staticAlloc(4);
HEAP32[___errno_state >> 2] = 0;
FS.staticInit();
__ATINIT__.unshift({
    func: function () {
        if (!Module["noFSInit"] && !FS.init.initialized) FS.init();
    },
});
__ATMAIN__.push({
    func: function () {
        FS.ignorePermissions = false;
    },
});
__ATEXIT__.push({
    func: function () {
        FS.quit();
    },
});
Module["FS_createFolder"] = FS.createFolder;
Module["FS_createPath"] = FS.createPath;
Module["FS_createDataFile"] = FS.createDataFile;
Module["FS_createPreloadedFile"] = FS.createPreloadedFile;
Module["FS_createLazyFile"] = FS.createLazyFile;
Module["FS_createLink"] = FS.createLink;
Module["FS_createDevice"] = FS.createDevice;
__ATINIT__.unshift({
    func: function () {
        TTY.init();
    },
});
__ATEXIT__.push({
    func: function () {
        TTY.shutdown();
    },
});
TTY.utf8 = new Runtime.UTF8Processor();
if (ENVIRONMENT_IS_NODE) {
    var fs = require("fs");
    NODEFS.staticInit();
}
__ATINIT__.push({
    func: function () {
        SOCKFS.root = FS.mount(SOCKFS, {}, null);
    },
});
Module["requestFullScreen"] = function Module_requestFullScreen(lockPointer, resizeCanvas) {
    Browser.requestFullScreen(lockPointer, resizeCanvas);
};
Module["requestAnimationFrame"] = function Module_requestAnimationFrame(func) {
    Browser.requestAnimationFrame(func);
};
Module["setCanvasSize"] = function Module_setCanvasSize(width, height, noUpdates) {
    Browser.setCanvasSize(width, height, noUpdates);
};
Module["pauseMainLoop"] = function Module_pauseMainLoop() {
    Browser.mainLoop.pause();
};
Module["resumeMainLoop"] = function Module_resumeMainLoop() {
    Browser.mainLoop.resume();
};
Module["getUserMedia"] = function Module_getUserMedia() {
    Browser.getUserMedia();
};
STACK_BASE = STACKTOP = Runtime.alignMemory(STATICTOP);
staticSealed = true;
STACK_MAX = STACK_BASE + 5242880;
DYNAMIC_BASE = DYNAMICTOP = Runtime.alignMemory(STACK_MAX);
assert(DYNAMIC_BASE < TOTAL_MEMORY, "TOTAL_MEMORY not big enough for stack");
var Math_min = Math.min;
function asmPrintInt(x, y) {
    Module.print("int " + x + "," + y);
}
function asmPrintFloat(x, y) {
    Module.print("float " + x + "," + y);
}
var asm = (function (global, env, buffer) {
    // EMSCRIPTEN_START_ASM
    "use asm";
    var a = new global.Int8Array(buffer);
    var b = new global.Int16Array(buffer);
    var c = new global.Int32Array(buffer);
    var d = new global.Uint8Array(buffer);
    var e = new global.Uint16Array(buffer);
    var f = new global.Uint32Array(buffer);
    var g = new global.Float32Array(buffer);
    var h = new global.Float64Array(buffer);
    var i = env.STACKTOP | 0;
    var j = env.STACK_MAX | 0;
    var k = env.tempDoublePtr | 0;
    var l = env.ABORT | 0;
    var m = env._stderr | 0;
    var n = 0;
    var o = 0;
    var p = 0;
    var q = 0;
    var r = +env.NaN,
        s = +env.Infinity;
    var t = 0,
        u = 0,
        v = 0,
        w = 0,
        x = 0.0,
        y = 0,
        z = 0,
        A = 0,
        B = 0.0;
    var C = 0;
    var D = 0;
    var E = 0;
    var F = 0;
    var G = 0;
    var H = 0;
    var I = 0;
    var J = 0;
    var K = 0;
    var L = 0;
    var M = global.Math.floor;
    var N = global.Math.abs;
    var O = global.Math.sqrt;
    var P = global.Math.pow;
    var Q = global.Math.cos;
    var R = global.Math.sin;
    var S = global.Math.tan;
    var T = global.Math.acos;
    var U = global.Math.asin;
    var V = global.Math.atan;
    var W = global.Math.atan2;
    var X = global.Math.exp;
    var Y = global.Math.log;
    var Z = global.Math.ceil;
    var _ = global.Math.imul;
    var $ = env.abort;
    var aa = env.assert;
    var ba = env.asmPrintInt;
    var ca = env.asmPrintFloat;
    var da = env.min;
    var ea = env._fflush;
    var fa = env.__formatString;
    var ga = env._time;
    var ha = env._send;
    var ia = env._pwrite;
    var ja = env._fileno;
    var ka = env.__exit;
    var la = env._abort;
    var ma = env.___setErrNo;
    var na = env._fwrite;
    var oa = env._sbrk;
    var pa = env._mkport;
    var qa = env._fprintf;
    var ra = env.___assert_fail;
    var sa = env._emscripten_memcpy_big;
    var ta = env.__reallyNegative;
    var ua = env._write;
    var va = env._sysconf;
    var wa = env._exit;
    var xa = env.___errno_location;
    var ya = 0.0;
    // EMSCRIPTEN_START_FUNCS
    function za(a) {
        a = a | 0;
        var b = 0;
        b = i;
        i = (i + a) | 0;
        i = (i + 7) & -8;
        return b | 0;
    }
    function Aa() {
        return i | 0;
    }
    function Ba(a) {
        a = a | 0;
        i = a;
    }
    function Ca(a, b) {
        a = a | 0;
        b = b | 0;
        if ((n | 0) == 0) {
            n = a;
            o = b;
        }
    }
    function Da(b) {
        b = b | 0;
        a[k >> 0] = a[b >> 0];
        a[(k + 1) >> 0] = a[(b + 1) >> 0];
        a[(k + 2) >> 0] = a[(b + 2) >> 0];
        a[(k + 3) >> 0] = a[(b + 3) >> 0];
    }
    function Ea(b) {
        b = b | 0;
        a[k >> 0] = a[b >> 0];
        a[(k + 1) >> 0] = a[(b + 1) >> 0];
        a[(k + 2) >> 0] = a[(b + 2) >> 0];
        a[(k + 3) >> 0] = a[(b + 3) >> 0];
        a[(k + 4) >> 0] = a[(b + 4) >> 0];
        a[(k + 5) >> 0] = a[(b + 5) >> 0];
        a[(k + 6) >> 0] = a[(b + 6) >> 0];
        a[(k + 7) >> 0] = a[(b + 7) >> 0];
    }
    function Fa(a) {
        a = a | 0;
        C = a;
    }
    function Ga() {
        return C | 0;
    }
    function Ha(a) {
        a = a | 0;
        var b = 0,
            d = 0;
        b = i;
        i = (i + 16) | 0;
        d = b;
        if ((a | 0) == 0) {
            i = b;
            return;
        } else {
            b = c[m >> 2] | 0;
            c[d >> 2] = a;
            qa(b | 0, 8, d | 0) | 0;
            wa(1);
        }
    }
    function Ia(a, b) {
        a = a | 0;
        b = b | 0;
        return 0;
    }
    function Ja(a, b) {
        a = a | 0;
        b = b | 0;
        var d = 0,
            e = 0,
            f = 0,
            g = 0;
        d = i;
        c[6] = _a() | 0;
        e = eb() | 0;
        c[8] = e;
        f = c[6] | 0;
        if (((f | 0) != 0) & ((e | 0) != 0)) {
            g = f;
        } else {
            Ha(40);
            g = c[6] | 0;
        }
        Ha(bb(g, a, b) | 0);
        cb(c[6] | 0);
        gb(c[8] | 0);
        i = d;
        return;
    }
    function Ka(a, b) {
        a = a | 0;
        b = b | 0;
        var d = 0;
        d = i;
        Ha(db(c[6] | 0, b, a) | 0);
        fb(c[8] | 0, a, b);
        i = d;
        return;
    }
    function La(b, d) {
        b = b | 0;
        d = d | 0;
        var e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0;
        e = i;
        f = (b + 2072) | 0;
        if ((c[f >> 2] | 0) == (d | 0)) {
            i = e;
            return;
        }
        c[f >> 2] = d;
        f = (d | 0) != 0;
        if (f) {
            d = (b + 68188) | 0;
            g = (b + 2140) | 0;
            h = (d + 0) | 0;
            j = (g + 64) | 0;
            do {
                a[g >> 0] = a[h >> 0] | 0;
                g = (g + 1) | 0;
                h = (h + 1) | 0;
            } while ((g | 0) < (j | 0));
            k = d;
        } else {
            k = (b + 68188) | 0;
        }
        g = (k + 0) | 0;
        h = ((f ? (b + 2076) | 0 : (b + 2140) | 0) + 0) | 0;
        j = (g + 64) | 0;
        do {
            a[g >> 0] = a[h >> 0] | 0;
            g = (g + 1) | 0;
            h = (h + 1) | 0;
        } while ((g | 0) < (j | 0));
        i = e;
        return;
    }
    function Ma(b, d, e, f) {
        b = b | 0;
        d = d | 0;
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0,
            w = 0,
            x = 0,
            y = 0;
        g = i;
        switch (f | 0) {
            case 15:
            case 14:
            case 13: {
                if ((d | 0) >= 4096) {
                    i = g;
                    return;
                }
                h = (f + -13) | 0;
                j = (e + -1) | 0;
                k = (b + ((h * 24) | 0) + 1868) | 0;
                l = c[k >> 2] | 0;
                if ((l | 0) <= (j | 0) ? ((m = c[(b + ((h * 24) | 0) + 1872) >> 2] | 0), (n = (((j - l) | 0) / (m | 0)) | 0), (j = (n + 1) | 0), (c[k >> 2] = (_(j, m) | 0) + l), (c[(b + ((h * 24) | 0) + 1884) >> 2] | 0) != 0) : 0) {
                    l = c[(b + ((h * 24) | 0) + 1876) >> 2] | 0;
                    m = (b + ((h * 24) | 0) + 1880) | 0;
                    k = c[m >> 2] | 0;
                    o = (n - ((l + 255 - k) & 255)) | 0;
                    if ((o | 0) > -1) {
                        n = ((o | 0) / (l | 0)) | 0;
                        p = (b + ((h * 24) | 0) + 1888) | 0;
                        c[p >> 2] = (n + 1 + (c[p >> 2] | 0)) & 15;
                        q = (o - (_(n, l) | 0)) | 0;
                    } else {
                        q = (k + j) | 0;
                    }
                    c[m >> 2] = q & 255;
                }
                c[(b + ((h * 24) | 0) + 1888) >> 2] = 0;
                i = g;
                return;
            }
            case 12:
            case 11:
            case 10: {
                h = (f + -10) | 0;
                q = (((d + 255) & 255) + 1) | 0;
                m = (b + ((h * 24) | 0) + 1876) | 0;
                j = c[m >> 2] | 0;
                if ((j | 0) == (q | 0)) {
                    i = g;
                    return;
                }
                k = (b + ((h * 24) | 0) + 1868) | 0;
                l = c[k >> 2] | 0;
                if ((l | 0) <= (e | 0) ? ((n = c[(b + ((h * 24) | 0) + 1872) >> 2] | 0), (o = (((e - l) | 0) / (n | 0)) | 0), (p = (o + 1) | 0), (c[k >> 2] = (_(p, n) | 0) + l), (c[(b + ((h * 24) | 0) + 1884) >> 2] | 0) != 0) : 0) {
                    l = (b + ((h * 24) | 0) + 1880) | 0;
                    n = c[l >> 2] | 0;
                    k = (o - ((j + 255 - n) & 255)) | 0;
                    if ((k | 0) > -1) {
                        o = ((k | 0) / (j | 0)) | 0;
                        r = (b + ((h * 24) | 0) + 1888) | 0;
                        c[r >> 2] = (o + 1 + (c[r >> 2] | 0)) & 15;
                        s = (k - (_(o, j) | 0)) | 0;
                    } else {
                        s = (n + p) | 0;
                    }
                    c[l >> 2] = s & 255;
                }
                c[m >> 2] = q;
                i = g;
                return;
            }
            case 9:
            case 8: {
                a[(b + f + 1956) >> 0] = d;
                i = g;
                return;
            }
            case 1: {
                if (((d & 16) | 0) != 0) {
                    a[(b + 1960) >> 0] = 0;
                    a[(b + 1961) >> 0] = 0;
                }
                if (((d & 32) | 0) == 0) {
                    t = 0;
                } else {
                    a[(b + 1962) >> 0] = 0;
                    a[(b + 1963) >> 0] = 0;
                    t = 0;
                }
                do {
                    f = (d >>> t) & 1;
                    q = (b + ((t * 24) | 0) + 1884) | 0;
                    m = c[q >> 2] | 0;
                    if ((m | 0) != (f | 0)) {
                        s = (b + ((t * 24) | 0) + 1868) | 0;
                        l = c[s >> 2] | 0;
                        if ((l | 0) <= (e | 0) ? ((p = c[(b + ((t * 24) | 0) + 1872) >> 2] | 0), (n = (((e - l) | 0) / (p | 0)) | 0), (j = (n + 1) | 0), (c[s >> 2] = (_(j, p) | 0) + l), (m | 0) != 0) : 0) {
                            m = c[(b + ((t * 24) | 0) + 1876) >> 2] | 0;
                            l = (b + ((t * 24) | 0) + 1880) | 0;
                            p = c[l >> 2] | 0;
                            s = (n - ((m + 255 - p) & 255)) | 0;
                            if ((s | 0) > -1) {
                                n = ((s | 0) / (m | 0)) | 0;
                                o = (b + ((t * 24) | 0) + 1888) | 0;
                                c[o >> 2] = (n + 1 + (c[o >> 2] | 0)) & 15;
                                u = (s - (_(n, m) | 0)) | 0;
                            } else {
                                u = (p + j) | 0;
                            }
                            c[l >> 2] = u & 255;
                        }
                        c[q >> 2] = f;
                        if ((f | 0) != 0) {
                            c[(b + ((t * 24) | 0) + 1880) >> 2] = 0;
                            c[(b + ((t * 24) | 0) + 1888) >> 2] = 0;
                        }
                    }
                    t = (t + 1) | 0;
                } while ((t | 0) != 3);
                t = d & 128;
                d = (b + 2072) | 0;
                if ((c[d >> 2] | 0) == (t | 0)) {
                    i = g;
                    return;
                }
                c[d >> 2] = t;
                d = (t | 0) != 0;
                if (d) {
                    t = (b + 68188) | 0;
                    v = (b + 2140) | 0;
                    w = (t + 0) | 0;
                    x = (v + 64) | 0;
                    do {
                        a[v >> 0] = a[w >> 0] | 0;
                        v = (v + 1) | 0;
                        w = (w + 1) | 0;
                    } while ((v | 0) < (x | 0));
                    y = t;
                } else {
                    y = (b + 68188) | 0;
                }
                v = (y + 0) | 0;
                w = ((d ? (b + 2076) | 0 : (b + 2140) | 0) + 0) | 0;
                x = (v + 64) | 0;
                do {
                    a[v >> 0] = a[w >> 0] | 0;
                    v = (v + 1) | 0;
                    w = (w + 1) | 0;
                } while ((v | 0) < (x | 0));
                i = g;
                return;
            }
            default: {
                i = g;
                return;
            }
        }
    }
    function Na(b, e, f) {
        b = b | 0;
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0;
        g = i;
        h = (b + 1942) | 0;
        j = a[h >> 0] | 0;
        k = (b + 1996) | 0;
        l = c[k >> 2] | 0;
        m = (f - (a[(b + (j & 255) + 1612) >> 0] | 0) - l) | 0;
        do {
            if (!((m | 0) > -1)) {
                if ((l | 0) == 127) {
                    if ((j << 24) >> 24 == 76) {
                        f = (b + 2012) | 0;
                        c[f >> 2] = (~d[(b + 92) >> 0] & e) | c[f >> 2];
                        n = 76;
                        break;
                    } else if ((j << 24) >> 24 == 92) {
                        f = (b + 2016) | 0;
                        c[f >> 2] = c[f >> 2] | e;
                        f = (b + 2012) | 0;
                        c[f >> 2] = c[f >> 2] & ~e;
                        n = 92;
                        break;
                    } else {
                        o = j;
                        p = 7;
                        break;
                    }
                } else {
                    o = j;
                    p = 7;
                }
            } else {
                f = (m + 32) & -32;
                c[k >> 2] = f + l;
                ib(b, f);
                o = a[h >> 0] | 0;
                p = 7;
            }
        } while (0);
        if ((p | 0) == 7) {
            if ((o << 24) >> 24 > -1) {
                n = o;
            } else {
                i = g;
                return;
            }
        }
        o = n & 255;
        a[(b + o) >> 0] = e;
        n = o & 15;
        if (n >>> 0 < 2) {
            p = n ^ o;
            h = a[(b + p) >> 0] | 0;
            l = a[(b + (p + 1)) >> 0] | 0;
            p = _(l, h) | 0;
            if ((p | 0) < (c[(b + 1564) >> 2] | 0)) {
                q = (h >> 7) ^ h;
                r = (l >> 7) ^ l;
            } else {
                q = h;
                r = l;
            }
            l = o >>> 4;
            h = c[(b + ((l * 140) | 0) + 444) >> 2] | 0;
            c[(b + ((l * 140) | 0) + 436) >> 2] = h & q;
            c[(b + ((l * 140) | 0) + 440) >> 2] = h & r;
            i = g;
            return;
        }
        if ((n | 0) != 12) {
            i = g;
            return;
        }
        if ((o | 0) == 76) {
            c[(b + 300) >> 2] = e & 255;
            i = g;
            return;
        } else if ((o | 0) == 124) {
            a[(b + 124) >> 0] = 0;
            i = g;
            return;
        } else {
            i = g;
            return;
        }
    }
    function Oa(b, d, e, f) {
        b = b | 0;
        d = d | 0;
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0;
        g = i;
        h = d & 255;
        j = e;
        while (1) {
            if ((j | 0) < 64) {
                k = 3;
                break;
            }
            e = (b + (j + 65472) + 2716) | 0;
            if (!((a[e >> 0] | 0) == (h << 24) >> 24)) {
                k = 6;
                break;
            }
            a[e >> 0] = -1;
            a[(b + (j + -64) + 2716) >> 0] = h;
            l = (j + -304) | 0;
            if (!((l | 0) > -1)) {
                k = 14;
                break;
            }
            if ((l | 0) < 16) {
                k = 9;
                break;
            }
            e = (j + -65536) | 0;
            if ((e | 0) > -1) {
                j = e;
            } else {
                k = 14;
                break;
            }
        }
        if ((k | 0) == 3) {
            a[(b + j + 2140) >> 0] = h;
            if ((c[(b + 2072) >> 2] | 0) == 0) {
                i = g;
                return;
            }
            a[(b + (j + 65472) + 2716) >> 0] = a[(b + j + 2076) >> 0] | 0;
            i = g;
            return;
        } else if ((k | 0) == 6) {
            ra(312, 352, 405, 384);
        } else if ((k | 0) == 9) {
            a[(b + l + 1940) >> 0] = h;
            if (((-788594688 << l) | 0) >= 0) {
                i = g;
                return;
            }
            if ((l | 0) == 3) {
                Na(b, d, f);
                i = g;
                return;
            } else {
                Ma(b, d, f, l);
                i = g;
                return;
            }
        } else if ((k | 0) == 14) {
            i = g;
            return;
        }
    }
    function Pa(b, e, f) {
        b = b | 0;
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0;
        g = i;
        h = e;
        while (1) {
            j = (h + -240) | 0;
            if (!(((j | 0) > -1) & (((h + -256) | 0) >>> 0 > 65279))) {
                k = 18;
                break;
            }
            l = (h + -253) | 0;
            if (l >>> 0 < 3) {
                k = 4;
                break;
            }
            if ((l | 0) < 0) {
                k = 11;
                break;
            }
            e = (h + -65536) | 0;
            if ((e | 0) < 256) {
                h = e;
            } else {
                k = 17;
                break;
            }
        }
        if ((k | 0) == 4) {
            e = (b + ((l * 24) | 0) + 1868) | 0;
            m = c[e >> 2] | 0;
            if ((m | 0) <= (f | 0) ? ((n = c[(b + ((l * 24) | 0) + 1872) >> 2] | 0), (o = (((f - m) | 0) / (n | 0)) | 0), (p = (o + 1) | 0), (c[e >> 2] = (_(p, n) | 0) + m), (c[(b + ((l * 24) | 0) + 1884) >> 2] | 0) != 0) : 0) {
                m = c[(b + ((l * 24) | 0) + 1876) >> 2] | 0;
                n = (b + ((l * 24) | 0) + 1880) | 0;
                e = c[n >> 2] | 0;
                q = (o - ((m + 255 - e) & 255)) | 0;
                if ((q | 0) > -1) {
                    o = ((q | 0) / (m | 0)) | 0;
                    r = (b + ((l * 24) | 0) + 1888) | 0;
                    c[r >> 2] = (o + 1 + (c[r >> 2] | 0)) & 15;
                    s = (q - (_(o, m) | 0)) | 0;
                } else {
                    s = (e + p) | 0;
                }
                c[n >> 2] = s & 255;
            }
            s = (b + ((l * 24) | 0) + 1888) | 0;
            l = c[s >> 2] | 0;
            c[s >> 2] = 0;
            t = l;
            i = g;
            return t | 0;
        } else if ((k | 0) == 11) {
            l = (h + -242) | 0;
            if (!(l >>> 0 < 2)) {
                t = d[(b + j + 1956) >> 0] | 0;
                i = g;
                return t | 0;
            }
            j = (b + 1942) | 0;
            s = a[j >> 0] | 0;
            n = s & 255;
            if ((l | 0) != 1) {
                t = n;
                i = g;
                return t | 0;
            }
            l = (b + 1996) | 0;
            p = c[l >> 2] | 0;
            e = (f - (a[(b + (n & 127) + 1612) >> 0] | 0) - p) | 0;
            if ((e | 0) > -1) {
                n = (e + 32) & -32;
                c[l >> 2] = n + p;
                ib(b, n);
                u = a[j >> 0] | 0;
            } else {
                u = s;
            }
            t = d[(b + (u & 127)) >> 0] | 0;
            i = g;
            return t | 0;
        } else if ((k | 0) == 17) {
            ra(400, 352, 497, 448);
        } else if ((k | 0) == 18) {
            t = d[(b + h + 2716) >> 0] | 0;
            i = g;
            return t | 0;
        }
        return 0;
    }
    function Qa(a, b) {
        a = a | 0;
        b = b | 0;
        var d = 0,
            e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0;
        d = i;
        e = (a + 2e3) | 0;
        f = c[e >> 2] | 0;
        if ((f | 0) < (b | 0)) {
            Ra(a, b) | 0;
            g = c[e >> 2] | 0;
        } else {
            g = f;
        }
        f = (g - b) | 0;
        c[e >> 2] = f;
        e = (a + 2024) | 0;
        c[e >> 2] = (c[e >> 2] | 0) + b;
        if (!(((f + 11) | 0) >>> 0 < 12)) {
            ra(464, 352, 546, 512);
        }
        f = (a + 1868) | 0;
        b = c[f >> 2] | 0;
        if ((b | 0) <= 0 ? ((e = c[(a + 1872) >> 2] | 0), (g = (((0 - b) | 0) / (e | 0)) | 0), (h = (g + 1) | 0), (c[f >> 2] = (_(h, e) | 0) + b), (c[(a + 1884) >> 2] | 0) != 0) : 0) {
            b = c[(a + 1876) >> 2] | 0;
            e = (a + 1880) | 0;
            f = c[e >> 2] | 0;
            j = (g - ((b + 255 - f) & 255)) | 0;
            if ((j | 0) > -1) {
                g = ((j | 0) / (b | 0)) | 0;
                k = (a + 1888) | 0;
                c[k >> 2] = (g + 1 + (c[k >> 2] | 0)) & 15;
                l = (j - (_(g, b) | 0)) | 0;
            } else {
                l = (f + h) | 0;
            }
            c[e >> 2] = l & 255;
        }
        l = (a + 1892) | 0;
        e = c[l >> 2] | 0;
        if ((e | 0) <= 0 ? ((h = c[(a + 1896) >> 2] | 0), (f = (((0 - e) | 0) / (h | 0)) | 0), (b = (f + 1) | 0), (c[l >> 2] = (_(b, h) | 0) + e), (c[(a + 1908) >> 2] | 0) != 0) : 0) {
            e = c[(a + 1900) >> 2] | 0;
            h = (a + 1904) | 0;
            l = c[h >> 2] | 0;
            g = (f - ((e + 255 - l) & 255)) | 0;
            if ((g | 0) > -1) {
                f = ((g | 0) / (e | 0)) | 0;
                j = (a + 1912) | 0;
                c[j >> 2] = (f + 1 + (c[j >> 2] | 0)) & 15;
                m = (g - (_(f, e) | 0)) | 0;
            } else {
                m = (l + b) | 0;
            }
            c[h >> 2] = m & 255;
        }
        m = (a + 1916) | 0;
        h = c[m >> 2] | 0;
        if ((h | 0) <= 0 ? ((b = c[(a + 1920) >> 2] | 0), (l = (((0 - h) | 0) / (b | 0)) | 0), (e = (l + 1) | 0), (c[m >> 2] = (_(e, b) | 0) + h), (c[(a + 1932) >> 2] | 0) != 0) : 0) {
            h = c[(a + 1924) >> 2] | 0;
            b = (a + 1928) | 0;
            m = c[b >> 2] | 0;
            f = (l - ((h + 255 - m) & 255)) | 0;
            if ((f | 0) > -1) {
                l = ((f | 0) / (h | 0)) | 0;
                g = (a + 1936) | 0;
                c[g >> 2] = (l + 1 + (c[g >> 2] | 0)) & 15;
                n = (f - (_(l, h) | 0)) | 0;
            } else {
                n = (m + e) | 0;
            }
            c[b >> 2] = n & 255;
        }
        n = (a + 1996) | 0;
        b = c[n >> 2] | 0;
        if ((b | 0) < 0 ? ((e = (-29 - b) | 0), (e | 0) > -1) : 0) {
            m = (e + 32) & -32;
            c[n >> 2] = m + b;
            ib(a, m);
        }
        if ((c[(a + 2028) >> 2] | 0) == 0) {
            i = d;
            return;
        }
        Ya(a);
        i = d;
        return;
    }
    function Ra(b, e) {
        b = b | 0;
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0,
            w = 0,
            x = 0,
            y = 0,
            z = 0,
            A = 0,
            B = 0,
            C = 0,
            D = 0,
            E = 0,
            F = 0,
            G = 0,
            H = 0,
            I = 0,
            J = 0,
            K = 0,
            L = 0,
            M = 0,
            N = 0,
            O = 0,
            P = 0,
            Q = 0,
            R = 0,
            S = 0,
            T = 0,
            U = 0,
            V = 0,
            W = 0,
            X = 0,
            Y = 0,
            Z = 0,
            $ = 0,
            aa = 0,
            ba = 0,
            ca = 0,
            da = 0,
            ea = 0,
            fa = 0,
            ga = 0,
            ha = 0,
            ia = 0,
            ja = 0,
            ka = 0,
            la = 0,
            ma = 0,
            na = 0,
            oa = 0,
            pa = 0,
            qa = 0,
            sa = 0,
            ta = 0,
            ua = 0,
            va = 0,
            wa = 0,
            xa = 0,
            ya = 0,
            za = 0,
            Aa = 0,
            Ba = 0,
            Ca = 0,
            Da = 0,
            Ea = 0,
            Fa = 0,
            Ga = 0,
            Ha = 0,
            Ia = 0,
            Ja = 0,
            Ka = 0,
            La = 0,
            Qa = 0,
            Ra = 0,
            Sa = 0,
            Ta = 0,
            Ua = 0,
            Va = 0,
            Wa = 0,
            Xa = 0,
            Ya = 0,
            Za = 0,
            _a = 0,
            $a = 0,
            ab = 0,
            bb = 0,
            cb = 0,
            db = 0,
            eb = 0,
            fb = 0,
            gb = 0,
            hb = 0,
            jb = 0,
            kb = 0,
            lb = 0,
            mb = 0,
            nb = 0,
            ob = 0,
            pb = 0,
            qb = 0,
            rb = 0,
            sb = 0,
            tb = 0,
            ub = 0,
            vb = 0,
            wb = 0,
            xb = 0,
            yb = 0,
            zb = 0,
            Ab = 0,
            Bb = 0,
            Cb = 0,
            Db = 0,
            Eb = 0,
            Fb = 0,
            Gb = 0,
            Hb = 0,
            Ib = 0,
            Jb = 0,
            Kb = 0,
            Lb = 0,
            Mb = 0,
            Nb = 0,
            Ob = 0,
            Pb = 0,
            Qb = 0,
            Rb = 0,
            Sb = 0,
            Tb = 0,
            Ub = 0,
            Vb = 0,
            Wb = 0,
            Xb = 0,
            Yb = 0,
            Zb = 0,
            _b = 0,
            $b = 0,
            ac = 0,
            bc = 0,
            cc = 0,
            dc = 0,
            ec = 0,
            fc = 0,
            gc = 0,
            hc = 0,
            ic = 0,
            jc = 0,
            kc = 0,
            lc = 0,
            mc = 0,
            nc = 0,
            oc = 0,
            pc = 0,
            qc = 0,
            rc = 0,
            sc = 0,
            tc = 0,
            uc = 0,
            vc = 0,
            wc = 0,
            xc = 0,
            yc = 0,
            zc = 0,
            Ac = 0,
            Bc = 0,
            Cc = 0,
            Dc = 0,
            Ec = 0,
            Fc = 0,
            Gc = 0,
            Hc = 0,
            Ic = 0,
            Jc = 0,
            Kc = 0,
            Lc = 0,
            Mc = 0,
            Nc = 0,
            Oc = 0,
            Pc = 0,
            Qc = 0,
            Rc = 0,
            Sc = 0,
            Tc = 0,
            Uc = 0,
            Vc = 0,
            Wc = 0,
            Xc = 0,
            Yc = 0,
            Zc = 0,
            _c = 0,
            $c = 0,
            ad = 0,
            bd = 0;
        f = i;
        g = (b + 2e3) | 0;
        h = ((c[g >> 2] | 0) - e) | 0;
        if ((h | 0) >= 1) {
            ra(528, 544, 163, 568);
        }
        c[g >> 2] = e;
        j = (b + 1996) | 0;
        c[j >> 2] = (c[j >> 2] | 0) + h;
        k = (b + 1868) | 0;
        c[k >> 2] = (c[k >> 2] | 0) + h;
        l = (b + 1892) | 0;
        c[l >> 2] = (c[l >> 2] | 0) + h;
        m = (b + 1916) | 0;
        c[m >> 2] = (c[m >> 2] | 0) + h;
        n = (b + 1976) | 0;
        o = c[n >> 2] | 0;
        p = (b + 1980) | 0;
        q = c[p >> 2] | 0;
        r = (b + 1984) | 0;
        s = c[r >> 2] | 0;
        t = (b + 1972) | 0;
        u = (b + (c[t >> 2] | 0) + 2716) | 0;
        v = (b + 1992) | 0;
        w = (b + ((c[v >> 2] | 0) + 257) + 2716) | 0;
        x = (b + 1988) | 0;
        y = c[x >> 2] | 0;
        z = y << 8;
        A = (y << 3) & 256;
        B = (((y << 4) & 2048) | (y & 2)) ^ 2;
        C = a[u >> 0] | 0;
        D = C & 255;
        E = ((d[(b + D + 2204) >> 0] | 0) + h) | 0;
        F = (b + 2716) | 0;
        a: do {
            if ((E | 0) <= 0) {
                G = (b + 1942) | 0;
                H = (b + 68218) | 0;
                I = (b + 68219) | 0;
                J = D;
                K = E;
                L = C;
                M = o;
                N = z;
                O = A;
                P = B;
                Q = u;
                R = y;
                S = w;
                T = q;
                U = s;
                b: while (1) {
                    V = (Q + 1) | 0;
                    W = a[V >> 0] | 0;
                    X = W & 255;
                    c: do {
                        switch (J | 0) {
                            case 0: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 63: {
                                ha = (V - F + 2) | 0;
                                ia = (b + ((d[(Q + 2) >> 0] << 8) | X) + 2716) | 0;
                                ja = (S + -2) | 0;
                                ka = (ja - F) | 0;
                                if ((ka | 0) > 256) {
                                    a[(S + -1) >> 0] = ha >>> 8;
                                    a[ja >> 0] = ha;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ia;
                                    ca = R;
                                    da = K;
                                    ea = ja;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    a[(b + ((ka & 255) | 256) + 2716) >> 0] = ha;
                                    a[(S + -1) >> 0] = ha >>> 8;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ia;
                                    ca = R;
                                    da = K;
                                    ea = (S + 254) | 0;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 232: {
                                la = X;
                                ma = N;
                                na = X;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                                break;
                            }
                            case 240: {
                                if (((P & 255) << 24) >> 24 == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 111: {
                                ia = (S - F) | 0;
                                if ((ia | 0) < 511) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (b + ((d[(S + 1) >> 0] << 8) | d[S >> 0]) + 2716) | 0;
                                    ca = R;
                                    da = K;
                                    ea = (S + 2) | 0;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (b + ((d[(S + -255) >> 0] << 8) | d[(b + ((ia & 255) | 256) + 2716) >> 0]) + 2716) | 0;
                                    ca = R;
                                    da = K;
                                    ea = (S + -254) | 0;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 208: {
                                if (((P & 255) << 24) >> 24 == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 228: {
                                ia = (Q + 2) | 0;
                                ha = X | O;
                                ka = (ha + -253) | 0;
                                if (ka >>> 0 < 3) {
                                    ja = (b + ((ka * 24) | 0) + 1868) | 0;
                                    va = c[ja >> 2] | 0;
                                    if (
                                        (K | 0) >= (va | 0)
                                            ? ((wa = c[(b + ((ka * 24) | 0) + 1872) >> 2] | 0),
                                              (xa = (((K - va) | 0) / (wa | 0)) | 0),
                                              (ya = (xa + 1) | 0),
                                              (c[ja >> 2] = (_(ya, wa) | 0) + va),
                                              (c[(b + ((ka * 24) | 0) + 1884) >> 2] | 0) != 0)
                                            : 0
                                    ) {
                                        va = c[(b + ((ka * 24) | 0) + 1876) >> 2] | 0;
                                        wa = (b + ((ka * 24) | 0) + 1880) | 0;
                                        ja = c[wa >> 2] | 0;
                                        za = (xa - ((va + 255 - ja) & 255)) | 0;
                                        if ((za | 0) > -1) {
                                            xa = ((za | 0) / (va | 0)) | 0;
                                            Aa = (b + ((ka * 24) | 0) + 1888) | 0;
                                            c[Aa >> 2] = (xa + 1 + (c[Aa >> 2] | 0)) & 15;
                                            Ba = (za - (_(xa, va) | 0)) | 0;
                                        } else {
                                            Ba = (ja + ya) | 0;
                                        }
                                        c[wa >> 2] = Ba & 255;
                                    }
                                    wa = (b + ((ka * 24) | 0) + 1888) | 0;
                                    ka = c[wa >> 2] | 0;
                                    c[wa >> 2] = 0;
                                    Y = ka;
                                    Z = N;
                                    $ = O;
                                    aa = ka;
                                    ba = ia;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    ka = d[(b + ha + 2716) >> 0] | 0;
                                    wa = (ha + -240) | 0;
                                    if (!(wa >>> 0 < 16)) {
                                        Y = ka;
                                        Z = N;
                                        $ = O;
                                        aa = ka;
                                        ba = ia;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                    ka = d[(b + wa + 1956) >> 0] | 0;
                                    wa = (ha + -242) | 0;
                                    if (!(wa >>> 0 < 2)) {
                                        Y = ka;
                                        Z = N;
                                        $ = O;
                                        aa = ka;
                                        ba = ia;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                    ka = a[G >> 0] | 0;
                                    ha = ka & 255;
                                    if ((wa | 0) != 1) {
                                        Y = ha;
                                        Z = N;
                                        $ = O;
                                        aa = ha;
                                        ba = ia;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                    wa = c[j >> 2] | 0;
                                    ya = (K - (a[(b + (ha & 127) + 1612) >> 0] | 0) - wa) | 0;
                                    if ((ya | 0) > -1) {
                                        ha = (ya + 32) & -32;
                                        c[j >> 2] = ha + wa;
                                        ib(b, ha);
                                        Ca = a[G >> 0] | 0;
                                    } else {
                                        Ca = ka;
                                    }
                                    ka = d[(b + (Ca & 127)) >> 0] | 0;
                                    Y = ka;
                                    Z = N;
                                    $ = O;
                                    aa = ka;
                                    ba = ia;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 250: {
                                ia = (K + -2) | 0;
                                ka = X | O;
                                ha = (ka + -253) | 0;
                                if (!(ha >>> 0 < 3)) {
                                    wa = d[(b + ka + 2716) >> 0] | 0;
                                    ya = (ka + -240) | 0;
                                    if (ya >>> 0 < 16) {
                                        ja = d[(b + ya + 1956) >> 0] | 0;
                                        ya = (ka + -242) | 0;
                                        if (ya >>> 0 < 2) {
                                            ka = a[G >> 0] | 0;
                                            va = ka & 255;
                                            if ((ya | 0) == 1) {
                                                ya = c[j >> 2] | 0;
                                                xa = (ia - (a[(b + (va & 127) + 1612) >> 0] | 0) - ya) | 0;
                                                if ((xa | 0) > -1) {
                                                    za = (xa + 32) & -32;
                                                    c[j >> 2] = za + ya;
                                                    ib(b, za);
                                                    Da = a[G >> 0] | 0;
                                                } else {
                                                    Da = ka;
                                                }
                                                Ea = d[(b + (Da & 127)) >> 0] | 0;
                                            } else {
                                                Ea = va;
                                            }
                                        } else {
                                            Ea = ja;
                                        }
                                    } else {
                                        Ea = wa;
                                    }
                                } else {
                                    wa = (b + ((ha * 24) | 0) + 1868) | 0;
                                    ja = c[wa >> 2] | 0;
                                    if (
                                        (ia | 0) >= (ja | 0)
                                            ? ((va = c[(b + ((ha * 24) | 0) + 1872) >> 2] | 0),
                                              (ka = (((ia - ja) | 0) / (va | 0)) | 0),
                                              (ia = (ka + 1) | 0),
                                              (c[wa >> 2] = (_(ia, va) | 0) + ja),
                                              (c[(b + ((ha * 24) | 0) + 1884) >> 2] | 0) != 0)
                                            : 0
                                    ) {
                                        ja = c[(b + ((ha * 24) | 0) + 1876) >> 2] | 0;
                                        va = (b + ((ha * 24) | 0) + 1880) | 0;
                                        wa = c[va >> 2] | 0;
                                        za = (ka - ((ja + 255 - wa) & 255)) | 0;
                                        if ((za | 0) > -1) {
                                            ka = ((za | 0) / (ja | 0)) | 0;
                                            ya = (b + ((ha * 24) | 0) + 1888) | 0;
                                            c[ya >> 2] = (ka + 1 + (c[ya >> 2] | 0)) & 15;
                                            Fa = (za - (_(ka, ja) | 0)) | 0;
                                        } else {
                                            Fa = (wa + ia) | 0;
                                        }
                                        c[va >> 2] = Fa & 255;
                                    }
                                    va = (b + ((ha * 24) | 0) + 1888) | 0;
                                    ha = c[va >> 2] | 0;
                                    c[va >> 2] = 0;
                                    Ea = ha;
                                }
                                Ga = (Ea + 8192) | 0;
                                ua = 48;
                                break;
                            }
                            case 143: {
                                Ga = X;
                                ua = 48;
                                break;
                            }
                            case 196: {
                                ha = (Q + 2) | 0;
                                va = X | O;
                                ia = M & 255;
                                a[(b + va + 2716) >> 0] = ia;
                                wa = (va + -240) | 0;
                                if (wa >>> 0 < 16) {
                                    ja = (va + -242) | 0;
                                    a[(b + wa + 1940) >> 0] = ia;
                                    if ((ja | 0) == 1) {
                                        Na(b, M, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = ha;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                    if (ja >>> 0 > 1) {
                                        Ma(b, M, K, wa);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = ha;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                    } else {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = ha;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ha;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                                break;
                            }
                            case 230: {
                                Ha = (T + O) | 0;
                                Ia = Q;
                                ua = 65;
                                break;
                            }
                            case 247: {
                                ha = X | O;
                                Ha = (((d[(b + (ha + 1) + 2716) >> 0] << 8) | d[(b + ha + 2716) >> 0]) + U) | 0;
                                Ia = V;
                                ua = 65;
                                break;
                            }
                            case 246: {
                                Ja = (X + U) | 0;
                                ua = 63;
                                break;
                            }
                            case 231: {
                                ha = ((X + T) & 255) | O;
                                Ha = (d[(b + (ha + 1) + 2716) >> 0] << 8) | d[(b + ha + 2716) >> 0];
                                Ia = V;
                                ua = 65;
                                break;
                            }
                            case 245: {
                                Ja = (X + T) | 0;
                                ua = 63;
                                break;
                            }
                            case 229: {
                                Ja = X;
                                ua = 63;
                                break;
                            }
                            case 244: {
                                Ha = ((X + T) & 255) | O;
                                Ia = V;
                                ua = 65;
                                break;
                            }
                            case 191: {
                                ha = Pa(b, (T + O) | 0, (K + -1) | 0) | 0;
                                Y = ha;
                                Z = N;
                                $ = O;
                                aa = ha;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = (T + 1) & 255;
                                ga = U;
                                break;
                            }
                            case 249: {
                                Ka = (X + U) & 255;
                                ua = 68;
                                break;
                            }
                            case 248: {
                                Ka = X;
                                ua = 68;
                                break;
                            }
                            case 233: {
                                ha = (Q + 2) | 0;
                                La = Pa(b, (d[ha >> 0] << 8) | X, K) | 0;
                                Qa = ha;
                                ua = 82;
                                break;
                            }
                            case 205: {
                                La = X;
                                Qa = V;
                                ua = 82;
                                break;
                            }
                            case 251: {
                                Ra = (X + T) & 255;
                                ua = 84;
                                break;
                            }
                            case 235: {
                                Ra = X;
                                ua = 84;
                                break;
                            }
                            case 236: {
                                ha = (d[(Q + 2) >> 0] << 8) | X;
                                wa = (Q + 3) | 0;
                                ja = (ha + -253) | 0;
                                if (ja >>> 0 < 3) {
                                    ia = (b + ((ja * 24) | 0) + 1868) | 0;
                                    va = c[ia >> 2] | 0;
                                    if (
                                        (K | 0) >= (va | 0)
                                            ? ((ka = c[(b + ((ja * 24) | 0) + 1872) >> 2] | 0),
                                              (za = (((K - va) | 0) / (ka | 0)) | 0),
                                              (ya = (za + 1) | 0),
                                              (c[ia >> 2] = (_(ya, ka) | 0) + va),
                                              (c[(b + ((ja * 24) | 0) + 1884) >> 2] | 0) != 0)
                                            : 0
                                    ) {
                                        va = c[(b + ((ja * 24) | 0) + 1876) >> 2] | 0;
                                        ka = (b + ((ja * 24) | 0) + 1880) | 0;
                                        ia = c[ka >> 2] | 0;
                                        xa = (za - ((va + 255 - ia) & 255)) | 0;
                                        if ((xa | 0) > -1) {
                                            za = ((xa | 0) / (va | 0)) | 0;
                                            Aa = (b + ((ja * 24) | 0) + 1888) | 0;
                                            c[Aa >> 2] = (za + 1 + (c[Aa >> 2] | 0)) & 15;
                                            Sa = (xa - (_(za, va) | 0)) | 0;
                                        } else {
                                            Sa = (ia + ya) | 0;
                                        }
                                        c[ka >> 2] = Sa & 255;
                                    }
                                    ka = (b + ((ja * 24) | 0) + 1888) | 0;
                                    ja = c[ka >> 2] | 0;
                                    c[ka >> 2] = 0;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ja;
                                    ba = wa;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = ja;
                                    break c;
                                } else {
                                    ja = d[(b + ha + 2716) >> 0] | 0;
                                    ka = (ha + -240) | 0;
                                    if (!(ka >>> 0 < 16)) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ja;
                                        ba = wa;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = ja;
                                        break c;
                                    }
                                    ja = d[(b + ka + 1956) >> 0] | 0;
                                    ka = (ha + -242) | 0;
                                    if (!(ka >>> 0 < 2)) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ja;
                                        ba = wa;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = ja;
                                        break c;
                                    }
                                    ja = a[G >> 0] | 0;
                                    ha = ja & 255;
                                    if ((ka | 0) != 1) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ha;
                                        ba = wa;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = ha;
                                        break c;
                                    }
                                    ka = c[j >> 2] | 0;
                                    ya = (K - (a[(b + (ha & 127) + 1612) >> 0] | 0) - ka) | 0;
                                    if ((ya | 0) > -1) {
                                        ha = (ya + 32) & -32;
                                        c[j >> 2] = ha + ka;
                                        ib(b, ha);
                                        Ta = a[G >> 0] | 0;
                                    } else {
                                        Ta = ja;
                                    }
                                    ja = d[(b + (Ta & 127)) >> 0] | 0;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ja;
                                    ba = wa;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = ja;
                                    break c;
                                }
                                break;
                            }
                            case 141: {
                                la = M;
                                ma = N;
                                na = X;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = X;
                                ua = 6;
                                break;
                            }
                            case 198: {
                                Ua = (T + O) | 0;
                                Va = Q;
                                ua = 118;
                                break;
                            }
                            case 215: {
                                ja = X | O;
                                Ua = (((d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0]) + U) | 0;
                                Va = V;
                                ua = 118;
                                break;
                            }
                            case 214: {
                                Wa = (X + U) | 0;
                                ua = 116;
                                break;
                            }
                            case 199: {
                                ja = ((X + T) & 255) | O;
                                Ua = (d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0];
                                Va = V;
                                ua = 118;
                                break;
                            }
                            case 201: {
                                Xa = T;
                                ua = 127;
                                break;
                            }
                            case 213: {
                                Wa = (X + T) | 0;
                                ua = 116;
                                break;
                            }
                            case 197: {
                                Wa = X;
                                ua = 116;
                                break;
                            }
                            case 212: {
                                Ua = ((X + T) & 255) | O;
                                Va = V;
                                ua = 118;
                                break;
                            }
                            case 217: {
                                Ya = (X + U) & 255;
                                ua = 137;
                                break;
                            }
                            case 216: {
                                Ya = X;
                                ua = 137;
                                break;
                            }
                            case 204: {
                                Xa = U;
                                ua = 127;
                                break;
                            }
                            case 203: {
                                Za = X;
                                ua = 143;
                                break;
                            }
                            case 125: {
                                Y = T;
                                Z = N;
                                $ = O;
                                aa = T;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 221: {
                                Y = U;
                                Z = N;
                                $ = O;
                                aa = U;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 93: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = M;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = M;
                                ga = U;
                                break;
                            }
                            case 253: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = M;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = M;
                                break;
                            }
                            case 157: {
                                ja = (S + -257 - F) | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = ja;
                                ga = U;
                                break;
                            }
                            case 189: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = (b + (T + 257) + 2716) | 0;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 219: {
                                Za = (X + T) & 255;
                                ua = 143;
                                break;
                            }
                            case 38: {
                                _a = (T + O) | 0;
                                $a = Q;
                                ua = 171;
                                break;
                            }
                            case 175: {
                                ja = (M + 8192) | 0;
                                wa = (T + O) | 0;
                                ha = ja & 255;
                                a[(b + wa + 2716) >> 0] = ha;
                                ka = (wa + -240) | 0;
                                do {
                                    if ((ka | 0) > -1) {
                                        if ((ka | 0) >= 16) {
                                            ya = (wa + -65472) | 0;
                                            if (!((ya | 0) > -1)) {
                                                break;
                                            }
                                            Oa(b, ja, ya, K);
                                            break;
                                        }
                                        a[(b + ka + 1940) >> 0] = ha;
                                        if (((-788594688 << ka) | 0) < 0) {
                                            if ((ka | 0) == 3) {
                                                Na(b, ja, K);
                                                break;
                                            } else {
                                                Ma(b, ja, K, ka);
                                                break;
                                            }
                                        }
                                    }
                                } while (0);
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = (T + 1) | 0;
                                ga = U;
                                break;
                            }
                            case 37: {
                                ab = X;
                                ua = 168;
                                break;
                            }
                            case 52: {
                                bb = (X + T) & 255;
                                ua = 170;
                                break;
                            }
                            case 36: {
                                bb = X;
                                ua = 170;
                                break;
                            }
                            case 40: {
                                cb = X;
                                db = V;
                                ua = 172;
                                break;
                            }
                            case 57: {
                                eb = (T + O) | 0;
                                fb = Pa(b, (U + O) | 0, (K + -2) | 0) | 0;
                                gb = V;
                                ua = 176;
                                break;
                            }
                            case 41: {
                                hb = Pa(b, X | O, (K + -3) | 0) | 0;
                                ua = 175;
                                break;
                            }
                            case 55: {
                                ka = X | O;
                                _a = (((d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0]) + U) | 0;
                                $a = V;
                                ua = 171;
                                break;
                            }
                            case 39: {
                                ka = ((X + T) & 255) | O;
                                _a = (d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0];
                                $a = V;
                                ua = 171;
                                break;
                            }
                            case 54: {
                                ab = (X + U) | 0;
                                ua = 168;
                                break;
                            }
                            case 53: {
                                ab = (X + T) | 0;
                                ua = 168;
                                break;
                            }
                            case 6: {
                                jb = (T + O) | 0;
                                kb = Q;
                                ua = 192;
                                break;
                            }
                            case 56: {
                                hb = X;
                                ua = 175;
                                break;
                            }
                            case 5: {
                                lb = X;
                                ua = 189;
                                break;
                            }
                            case 20: {
                                mb = (X + T) & 255;
                                ua = 191;
                                break;
                            }
                            case 4: {
                                mb = X;
                                ua = 191;
                                break;
                            }
                            case 8: {
                                nb = X;
                                ob = V;
                                ua = 193;
                                break;
                            }
                            case 25: {
                                pb = (T + O) | 0;
                                qb = Pa(b, (U + O) | 0, (K + -2) | 0) | 0;
                                rb = V;
                                ua = 197;
                                break;
                            }
                            case 9: {
                                sb = Pa(b, X | O, (K + -3) | 0) | 0;
                                ua = 196;
                                break;
                            }
                            case 23: {
                                ka = X | O;
                                jb = (((d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0]) + U) | 0;
                                kb = V;
                                ua = 192;
                                break;
                            }
                            case 7: {
                                ka = ((X + T) & 255) | O;
                                jb = (d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0];
                                kb = V;
                                ua = 192;
                                break;
                            }
                            case 22: {
                                lb = (X + U) | 0;
                                ua = 189;
                                break;
                            }
                            case 21: {
                                lb = (X + T) | 0;
                                ua = 189;
                                break;
                            }
                            case 70: {
                                tb = (T + O) | 0;
                                ub = Q;
                                ua = 213;
                                break;
                            }
                            case 24: {
                                sb = X;
                                ua = 196;
                                break;
                            }
                            case 69: {
                                vb = X;
                                ua = 210;
                                break;
                            }
                            case 84: {
                                wb = (X + T) & 255;
                                ua = 212;
                                break;
                            }
                            case 68: {
                                wb = X;
                                ua = 212;
                                break;
                            }
                            case 72: {
                                xb = X;
                                yb = V;
                                ua = 214;
                                break;
                            }
                            case 89: {
                                zb = (T + O) | 0;
                                Ab = Pa(b, (U + O) | 0, (K + -2) | 0) | 0;
                                Bb = V;
                                ua = 218;
                                break;
                            }
                            case 73: {
                                Cb = Pa(b, X | O, (K + -3) | 0) | 0;
                                ua = 217;
                                break;
                            }
                            case 87: {
                                ka = X | O;
                                tb = (((d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0]) + U) | 0;
                                ub = V;
                                ua = 213;
                                break;
                            }
                            case 71: {
                                ka = ((X + T) & 255) | O;
                                tb = (d[(b + (ka + 1) + 2716) >> 0] << 8) | d[(b + ka + 2716) >> 0];
                                ub = V;
                                ua = 213;
                                break;
                            }
                            case 86: {
                                vb = (X + U) | 0;
                                ua = 210;
                                break;
                            }
                            case 85: {
                                vb = (X + T) | 0;
                                ua = 210;
                                break;
                            }
                            case 102: {
                                Db = (T + O) | 0;
                                Eb = Q;
                                ua = 234;
                                break;
                            }
                            case 88: {
                                Cb = X;
                                ua = 217;
                                break;
                            }
                            case 101: {
                                Fb = X;
                                ua = 231;
                                break;
                            }
                            case 116: {
                                Gb = (X + T) & 255;
                                ua = 233;
                                break;
                            }
                            case 100: {
                                Gb = X;
                                ua = 233;
                                break;
                            }
                            case 104: {
                                Hb = X;
                                Ib = V;
                                ua = 235;
                                break;
                            }
                            case 121: {
                                ka = Pa(b, (U + O) | 0, (K + -2) | 0) | 0;
                                ja = ((Pa(b, (T + O) | 0, (K + -1) | 0) | 0) - ka) | 0;
                                Y = M;
                                Z = ~ja;
                                $ = O;
                                aa = ja & 255;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 119: {
                                ja = X | O;
                                Db = (((d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0]) + U) | 0;
                                Eb = V;
                                ua = 234;
                                break;
                            }
                            case 103: {
                                ja = ((X + T) & 255) | O;
                                Db = (d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0];
                                Eb = V;
                                ua = 234;
                                break;
                            }
                            case 118: {
                                Fb = (X + U) | 0;
                                ua = 231;
                                break;
                            }
                            case 117: {
                                Fb = (X + T) | 0;
                                ua = 231;
                                break;
                            }
                            case 62: {
                                Jb = X | O;
                                Kb = V;
                                ua = 241;
                                break;
                            }
                            case 120: {
                                Lb = X;
                                ua = 238;
                                break;
                            }
                            case 30: {
                                ja = (Q + 2) | 0;
                                Jb = (d[ja >> 0] << 8) | X;
                                Kb = ja;
                                ua = 241;
                                break;
                            }
                            case 200: {
                                Mb = X;
                                Nb = V;
                                ua = 242;
                                break;
                            }
                            case 126: {
                                Ob = X | O;
                                Pb = V;
                                ua = 245;
                                break;
                            }
                            case 105: {
                                Lb = Pa(b, X | O, (K + -3) | 0) | 0;
                                ua = 238;
                                break;
                            }
                            case 173: {
                                Qb = X;
                                Rb = V;
                                ua = 246;
                                break;
                            }
                            case 153:
                            case 185: {
                                Sb = (T + O) | 0;
                                Tb = Pa(b, (U + O) | 0, (K + -2) | 0) | 0;
                                Ub = Q;
                                ua = 250;
                                break;
                            }
                            case 137:
                            case 169: {
                                Vb = Pa(b, X | O, (K + -3) | 0) | 0;
                                ua = 249;
                                break;
                            }
                            case 152:
                            case 184: {
                                Vb = X;
                                ua = 249;
                                break;
                            }
                            case 166:
                            case 134: {
                                Wb = (T + O) | 0;
                                Xb = Q;
                                ua = 259;
                                break;
                            }
                            case 94: {
                                ja = (Q + 2) | 0;
                                Ob = (d[ja >> 0] << 8) | X;
                                Pb = ja;
                                ua = 245;
                                break;
                            }
                            case 165:
                            case 133: {
                                Yb = X;
                                ua = 256;
                                break;
                            }
                            case 180:
                            case 148: {
                                Zb = (X + T) & 255;
                                ua = 258;
                                break;
                            }
                            case 164:
                            case 132: {
                                Zb = X;
                                ua = 258;
                                break;
                            }
                            case 183:
                            case 151: {
                                ja = X | O;
                                Wb = (((d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0]) + U) | 0;
                                Xb = V;
                                ua = 259;
                                break;
                            }
                            case 167:
                            case 135: {
                                ja = ((X + T) & 255) | O;
                                Wb = (d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0];
                                Xb = V;
                                ua = 259;
                                break;
                            }
                            case 182:
                            case 150: {
                                Yb = (X + U) | 0;
                                ua = 256;
                                break;
                            }
                            case 181:
                            case 149: {
                                Yb = (X + T) | 0;
                                ua = 256;
                                break;
                            }
                            case 188: {
                                ja = (M + 1) | 0;
                                Y = ja & 255;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 61: {
                                ja = (T + 1) | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = ja & 255;
                                ga = U;
                                break;
                            }
                            case 252: {
                                ja = (U + 1) | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = ja & 255;
                                break;
                            }
                            case 156: {
                                ja = (M + -1) | 0;
                                Y = ja & 255;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 29: {
                                ja = (T + -1) | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = ja & 255;
                                ga = U;
                                break;
                            }
                            case 220: {
                                ja = (U + -1) | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = ja & 255;
                                break;
                            }
                            case 187:
                            case 155: {
                                _b = (X + T) & 255;
                                ua = 277;
                                break;
                            }
                            case 136:
                            case 168: {
                                $b = -1;
                                ac = X;
                                bc = M;
                                cc = V;
                                ua = 260;
                                break;
                            }
                            case 172:
                            case 140: {
                                ja = (Q + 2) | 0;
                                dc = (d[ja >> 0] << 8) | X;
                                ec = ja;
                                ua = 279;
                                break;
                            }
                            case 171:
                            case 139: {
                                _b = X;
                                ua = 277;
                                break;
                            }
                            case 92: {
                                fc = 0;
                                ua = 288;
                                break;
                            }
                            case 124: {
                                fc = N;
                                ua = 288;
                                break;
                            }
                            case 28: {
                                gc = 0;
                                ua = 290;
                                break;
                            }
                            case 60: {
                                gc = N;
                                ua = 290;
                                break;
                            }
                            case 11: {
                                hc = 0;
                                ic = X | O;
                                jc = V;
                                ua = 297;
                                break;
                            }
                            case 27: {
                                kc = 0;
                                ua = 293;
                                break;
                            }
                            case 59: {
                                kc = N;
                                ua = 293;
                                break;
                            }
                            case 43: {
                                lc = N;
                                mc = X;
                                ua = 294;
                                break;
                            }
                            case 12: {
                                nc = 0;
                                ua = 296;
                                break;
                            }
                            case 75: {
                                oc = 0;
                                pc = X | O;
                                qc = V;
                                ua = 311;
                                break;
                            }
                            case 44: {
                                nc = N;
                                ua = 296;
                                break;
                            }
                            case 91: {
                                rc = 0;
                                ua = 307;
                                break;
                            }
                            case 107: {
                                sc = N;
                                tc = X;
                                ua = 308;
                                break;
                            }
                            case 76: {
                                uc = 0;
                                ua = 310;
                                break;
                            }
                            case 108: {
                                uc = N;
                                ua = 310;
                                break;
                            }
                            case 123: {
                                rc = N;
                                ua = 307;
                                break;
                            }
                            case 159: {
                                ja = ((M << 4) & 240) | (M >> 4);
                                Y = ja;
                                Z = N;
                                $ = O;
                                aa = ja;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 186: {
                                ja = Pa(b, X | O, (K + -2) | 0) | 0;
                                ka = Pa(b, ((X + 1) & 255) | O, K) | 0;
                                la = ja;
                                ma = N;
                                na = (ja & 127) | (ja >> 1) | ka;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = ka;
                                ua = 6;
                                break;
                            }
                            case 218: {
                                ka = X | O;
                                ja = (K + -1) | 0;
                                ha = M & 255;
                                a[(b + ka + 2716) >> 0] = ha;
                                wa = (ka + -240) | 0;
                                do {
                                    if (wa >>> 0 < 16 ? ((a[(b + wa + 1940) >> 0] = ha), ((-788594688 << wa) | 0) < 0) : 0) {
                                        if ((wa | 0) == 3) {
                                            Na(b, M, ja);
                                            break;
                                        } else {
                                            Ma(b, M, ja, wa);
                                            break;
                                        }
                                    }
                                } while (0);
                                wa = (U + 8192) | 0;
                                ja = ((X + 1) & 255) | O;
                                ha = wa & 255;
                                a[(b + ja + 2716) >> 0] = ha;
                                ka = (ja + -240) | 0;
                                if (ka >>> 0 < 16 ? ((a[(b + ka + 1940) >> 0] = ha), ((-788594688 << ka) | 0) < 0) : 0) {
                                    if ((ka | 0) == 3) {
                                        Na(b, wa, K);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    } else {
                                        Ma(b, wa, K, ka);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    }
                                } else {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                                break;
                            }
                            case 26:
                            case 58: {
                                ka = X | O;
                                wa = (((J >>> 4) & 2) + -1 + (Pa(b, ka, (K + -3) | 0) | 0)) | 0;
                                ha = ((wa >>> 1) | wa) & 127;
                                ja = (K + -2) | 0;
                                ya = wa & 255;
                                a[(b + ka + 2716) >> 0] = ya;
                                ia = (ka + -240) | 0;
                                do {
                                    if (ia >>> 0 < 16 ? ((a[(b + ia + 1940) >> 0] = ya), ((-788594688 << ia) | 0) < 0) : 0) {
                                        if ((ia | 0) == 3) {
                                            Na(b, wa, ja);
                                            break;
                                        } else {
                                            Ma(b, wa, ja, ia);
                                            break;
                                        }
                                    }
                                } while (0);
                                ia = ((X + 1) & 255) | O;
                                ja = ((Pa(b, ia, (K + -1) | 0) | 0) + (wa >>> 8)) | 0;
                                ya = ja & 255;
                                ka = ya | ha;
                                va = ja & 255;
                                a[(b + ia + 2716) >> 0] = va;
                                ja = (ia + -240) | 0;
                                if (ja >>> 0 < 16 ? ((a[(b + ja + 1940) >> 0] = va), ((-788594688 << ja) | 0) < 0) : 0) {
                                    if ((ja | 0) == 3) {
                                        Na(b, ya, K);
                                        la = M;
                                        ma = N;
                                        na = ka;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    } else {
                                        Ma(b, ya, K, ja);
                                        la = M;
                                        ma = N;
                                        na = ka;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    }
                                } else {
                                    la = M;
                                    ma = N;
                                    na = ka;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                                break;
                            }
                            case 154:
                            case 122: {
                                ka = Pa(b, X | O, (K + -2) | 0) | 0;
                                ja = Pa(b, ((X + 1) & 255) | O, K) | 0;
                                if ((L << 24) >> 24 == -102) {
                                    vc = ja ^ 255;
                                    wc = ((ka ^ 255) + 1) | 0;
                                } else {
                                    vc = ja;
                                    wc = ka;
                                }
                                ka = (wc + M) | 0;
                                ja = (vc + U + (ka >> 8)) | 0;
                                ya = vc ^ U ^ ja;
                                va = ja & 255;
                                la = ka & 255;
                                ma = ja;
                                na = (((ka >>> 1) | ka) & 127) | va;
                                oa = V;
                                pa = ((ya >>> 1) & 8) | (R & -73) | ((((ya + 128) | 0) >>> 2) & 64);
                                qa = K;
                                sa = T;
                                ta = va;
                                ua = 6;
                                break;
                            }
                            case 158: {
                                va = (M + (U << 8)) | 0;
                                ya = R & -73;
                                ka = (U | 0) < (T | 0) ? ya : ya | 64;
                                if ((U | 0) < ((T << 1) | 0)) {
                                    ya = ((va >>> 0) / (T >>> 0)) | 0;
                                    xc = ya;
                                    yc = (va - (_(ya, T) | 0)) | 0;
                                } else {
                                    ya = (va - (T << 9)) | 0;
                                    va = (256 - T) | 0;
                                    xc = (255 - (((ya >>> 0) / (va >>> 0)) | 0)) | 0;
                                    yc = (((ya >>> 0) % (va >>> 0) | 0) + T) | 0;
                                }
                                va = xc & 255;
                                Y = va;
                                Z = N;
                                $ = O;
                                aa = va;
                                ba = V;
                                ca = (U & 15) >>> 0 < (T & 15) >>> 0 ? ka : ka | 8;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = yc;
                                break;
                            }
                            case 223: {
                                if ((M | 0) <= 153 ? ((N & 256) | 0) == 0 : 0) {
                                    zc = M;
                                    Ac = N;
                                } else {
                                    zc = (M + 96) | 0;
                                    Ac = 256;
                                }
                                if (!((zc & 14) >>> 0 > 9) ? ((R & 8) | 0) == 0 : 0) {
                                    Bc = zc;
                                } else {
                                    Bc = (zc + 6) | 0;
                                }
                                Y = Bc & 255;
                                Z = Ac;
                                $ = O;
                                aa = Bc;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 90: {
                                ka = (M - (Pa(b, X | O, (K + -1) | 0) | 0)) | 0;
                                va = (U - (Pa(b, ((X + 1) & 255) | O, K) | 0) + (ka >> 8)) | 0;
                                la = M;
                                ma = ~va;
                                na = (((ka >>> 1) | ka) & 127) | (va & 255);
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                                break;
                            }
                            case 207: {
                                va = _(M, U) | 0;
                                ka = va >>> 8;
                                Y = va & 255;
                                Z = N;
                                $ = O;
                                aa = (((va >>> 1) | va) & 127) | ka;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = ka;
                                break;
                            }
                            case 190: {
                                if ((M | 0) <= 153 ? ((N & 256) | 0) != 0 : 0) {
                                    Cc = M;
                                    Dc = N;
                                } else {
                                    Cc = (M + -96) | 0;
                                    Dc = 0;
                                }
                                if (!((Cc & 14) >>> 0 > 9) ? ((R & 8) | 0) != 0 : 0) {
                                    Ec = Cc;
                                } else {
                                    Ec = (Cc + -6) | 0;
                                }
                                Y = Ec & 255;
                                Z = Dc;
                                $ = O;
                                aa = Ec;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 47: {
                                la = M;
                                ma = N;
                                na = P;
                                oa = (Q + (((W << 24) >> 24) + 1)) | 0;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                                break;
                            }
                            case 48: {
                                if (((P & 2176) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 16: {
                                if (((P & 2176) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 176: {
                                if (((N & 256) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 144: {
                                if (((N & 256) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 112: {
                                if (((R & 64) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 80: {
                                if (((R & 64) | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 243:
                            case 211:
                            case 179:
                            case 147:
                            case 115:
                            case 83:
                            case 51:
                            case 19: {
                                ka = (Q + 2) | 0;
                                if ((((Pa(b, X | O, (K + -4) | 0) | 0) & (1 << (J >>> 5))) | 0) == 0) {
                                    Fc = ka;
                                    ua = 5;
                                } else {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = ka;
                                    pa = R;
                                    qa = (K + -2) | 0;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                                break;
                            }
                            case 222: {
                                Gc = (X + T) & 255;
                                ua = 388;
                                break;
                            }
                            case 46: {
                                Gc = X;
                                ua = 388;
                                break;
                            }
                            case 227:
                            case 195:
                            case 163:
                            case 131:
                            case 99:
                            case 67:
                            case 35:
                            case 3: {
                                ka = (Q + 2) | 0;
                                if ((((Pa(b, X | O, (K + -4) | 0) | 0) & (1 << (J >>> 5))) | 0) == 0) {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = ka;
                                    pa = R;
                                    qa = (K + -2) | 0;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                } else {
                                    Fc = ka;
                                    ua = 5;
                                }
                                break;
                            }
                            case 110: {
                                ka = X | O;
                                va = Pa(b, ka, (K + -4) | 0) | 0;
                                ya = (va + 8191) | 0;
                                ja = (K + -3) | 0;
                                ia = ya & 255;
                                a[(b + ka + 2716) >> 0] = ia;
                                za = (ka + -240) | 0;
                                do {
                                    if (za >>> 0 < 16 ? ((a[(b + za + 1940) >> 0] = ia), ((-788594688 << za) | 0) < 0) : 0) {
                                        if ((za | 0) == 3) {
                                            Na(b, ya, ja);
                                            break;
                                        } else {
                                            Ma(b, ya, ja, za);
                                            break;
                                        }
                                    }
                                } while (0);
                                za = (Q + 2) | 0;
                                if ((va | 0) == 1) {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = za;
                                    pa = R;
                                    qa = (K + -2) | 0;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                } else {
                                    Fc = za;
                                    ua = 5;
                                }
                                break;
                            }
                            case 31: {
                                za = (b + (((d[(Q + 2) >> 0] << 8) | X) + T) + 2716) | 0;
                                Hc = a[za >> 0] | 0;
                                Ic = za;
                                ua = 414;
                                break;
                            }
                            case 95: {
                                Hc = W;
                                Ic = V;
                                ua = 414;
                                break;
                            }
                            case 254: {
                                za = (U + 255) & 255;
                                if ((za | 0) == 0) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + 2) | 0;
                                    ca = R;
                                    da = (K + -2) | 0;
                                    ea = S;
                                    fa = T;
                                    ga = 0;
                                    break c;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = (Q + (((W << 24) >> 24) + 2)) | 0;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = za;
                                    break c;
                                }
                                break;
                            }
                            case 241:
                            case 225:
                            case 209:
                            case 193:
                            case 177:
                            case 161:
                            case 145:
                            case 129:
                            case 113:
                            case 97:
                            case 81:
                            case 65:
                            case 49:
                            case 33:
                            case 17:
                            case 1: {
                                za = (V - F) | 0;
                                ja = (65502 - (J >>> 3)) | 0;
                                ya = (b + ((d[(b + (ja + 1) + 2716) >> 0] << 8) | d[(b + ja + 2716) >> 0]) + 2716) | 0;
                                ja = (S + -2) | 0;
                                ia = (ja - F) | 0;
                                if ((ia | 0) > 256) {
                                    a[(S + -1) >> 0] = za >>> 8;
                                    a[ja >> 0] = za;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ya;
                                    ca = R;
                                    da = K;
                                    ea = ja;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    a[(b + ((ia & 255) | 256) + 2716) >> 0] = za;
                                    a[(S + -1) >> 0] = za >>> 8;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ya;
                                    ca = R;
                                    da = K;
                                    ea = (S + 254) | 0;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 15: {
                                ya = (V - F) | 0;
                                za = (b + ((d[I >> 0] << 8) | d[H >> 0]) + 2716) | 0;
                                ia = (S + -2) | 0;
                                ja = (ia - F) | 0;
                                if ((ja | 0) > 256) {
                                    a[(S + -1) >> 0] = ya >>> 8;
                                    a[ia >> 0] = ya;
                                    Jc = ia;
                                } else {
                                    a[(b + ((ja & 255) | 256) + 2716) >> 0] = ya;
                                    a[(S + -1) >> 0] = ya >>> 8;
                                    Jc = (S + 254) | 0;
                                }
                                ya = ((N >>> 8) & 1) | (O >>> 3) | (R & -164) | (((P >>> 4) | P) & 128);
                                ja = (Jc + -1) | 0;
                                a[ja >> 0] = ((P & 255) << 24) >> 24 == 0 ? ya | 2 : ya;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = za;
                                ca = (R & -21) | 16;
                                da = K;
                                ea = ((ja - F) | 0) == 256 ? (Jc + 255) | 0 : ja;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 79: {
                                ja = (V - F + 1) | 0;
                                za = (b + (X | 65280) + 2716) | 0;
                                ya = (S + -2) | 0;
                                ia = (ya - F) | 0;
                                if ((ia | 0) > 256) {
                                    a[(S + -1) >> 0] = ja >>> 8;
                                    a[ya >> 0] = ja;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = za;
                                    ca = R;
                                    da = K;
                                    ea = ya;
                                    fa = T;
                                    ga = U;
                                    break c;
                                } else {
                                    a[(b + ((ia & 255) | 256) + 2716) >> 0] = ja;
                                    a[(S + -1) >> 0] = ja >>> 8;
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = za;
                                    ca = R;
                                    da = K;
                                    ea = (S + 254) | 0;
                                    fa = T;
                                    ga = U;
                                    break c;
                                }
                                break;
                            }
                            case 78:
                            case 14: {
                                za = (d[(Q + 2) >> 0] << 8) | X;
                                ja = (Q + 3) | 0;
                                ia = Pa(b, za, (K + -2) | 0) | 0;
                                ya = (M - ia) & 255;
                                ha = (ia & ~M) | ((L << 24) >> 24 == 14 ? M : 0);
                                ia = ha & 255;
                                a[(b + za + 2716) >> 0] = ia;
                                wa = (za + -240) | 0;
                                if ((wa | 0) > -1) {
                                    if ((wa | 0) >= 16) {
                                        ka = (za + -65472) | 0;
                                        if (!((ka | 0) > -1)) {
                                            Y = M;
                                            Z = N;
                                            $ = O;
                                            aa = ya;
                                            ba = ja;
                                            ca = R;
                                            da = K;
                                            ea = S;
                                            fa = T;
                                            ga = U;
                                            break c;
                                        }
                                        Oa(b, ha, ka, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = ja;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                    a[(b + wa + 1940) >> 0] = ia;
                                    if (((-788594688 << wa) | 0) < 0) {
                                        if ((wa | 0) == 3) {
                                            Na(b, ha, K);
                                            Y = M;
                                            Z = N;
                                            $ = O;
                                            aa = ya;
                                            ba = ja;
                                            ca = R;
                                            da = K;
                                            ea = S;
                                            fa = T;
                                            ga = U;
                                            break c;
                                        } else {
                                            Ma(b, ha, K, wa);
                                            Y = M;
                                            Z = N;
                                            $ = O;
                                            aa = ya;
                                            ba = ja;
                                            ca = R;
                                            da = K;
                                            ea = S;
                                            fa = T;
                                            ga = U;
                                            break c;
                                        }
                                    } else {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = ja;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = ja;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                                break;
                            }
                            case 127: {
                                Kc = (b + ((d[(S + 2) >> 0] << 8) | d[(S + 1) >> 0]) + 2716) | 0;
                                Lc = (S + 3) | 0;
                                Mc = d[S >> 0] | 0;
                                ua = 428;
                                break;
                            }
                            case 142: {
                                ja = (S + 1) | 0;
                                if (((ja - F) | 0) == 513) {
                                    Kc = V;
                                    Lc = (S + -255) | 0;
                                    Mc = d[(S + -256) >> 0] | 0;
                                    ua = 428;
                                } else {
                                    Kc = V;
                                    Lc = ja;
                                    Mc = d[S >> 0] | 0;
                                    ua = 428;
                                }
                                break;
                            }
                            case 13: {
                                ja = ((N >>> 8) & 1) | (O >>> 3) | (R & -164) | (((P >>> 4) | P) & 128);
                                ya = (S + -1) | 0;
                                a[ya >> 0] = ((P & 255) << 24) >> 24 == 0 ? ja | 2 : ja;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = ((ya - F) | 0) == 256 ? (S + 255) | 0 : ya;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 45: {
                                ya = (S + -1) | 0;
                                a[ya >> 0] = M;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = ((ya - F) | 0) == 256 ? (S + 255) | 0 : ya;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 77: {
                                ya = (S + -1) | 0;
                                a[ya >> 0] = T;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = ((ya - F) | 0) == 256 ? (S + 255) | 0 : ya;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 109: {
                                ya = (S + -1) | 0;
                                a[ya >> 0] = U;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = ((ya - F) | 0) == 256 ? (S + 255) | 0 : ya;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 174: {
                                ya = (S + 1) | 0;
                                if (((ya - F) | 0) == 513) {
                                    Y = d[(S + -256) >> 0] | 0;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = (S + -255) | 0;
                                    fa = T;
                                    ga = U;
                                } else {
                                    Y = d[S >> 0] | 0;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = ya;
                                    fa = T;
                                    ga = U;
                                }
                                break;
                            }
                            case 206: {
                                ya = (S + 1) | 0;
                                if (((ya - F) | 0) == 513) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = (S + -255) | 0;
                                    fa = d[(S + -256) >> 0] | 0;
                                    ga = U;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = ya;
                                    fa = d[S >> 0] | 0;
                                    ga = U;
                                }
                                break;
                            }
                            case 238: {
                                ya = (S + 1) | 0;
                                if (((ya - F) | 0) == 513) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = (S + -255) | 0;
                                    fa = T;
                                    ga = d[(S + -256) >> 0] | 0;
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = V;
                                    ca = R;
                                    da = K;
                                    ea = ya;
                                    fa = T;
                                    ga = d[S >> 0] | 0;
                                }
                                break;
                            }
                            case 242:
                            case 210:
                            case 178:
                            case 146:
                            case 114:
                            case 82:
                            case 50:
                            case 18:
                            case 226:
                            case 194:
                            case 162:
                            case 130:
                            case 98:
                            case 66:
                            case 34:
                            case 2: {
                                ya = 1 << (J >>> 5);
                                ja = X | O;
                                wa = ((Pa(b, ja, (K + -1) | 0) | 0) & ~ya) | (((J & 16) | 0) == 0 ? ya : 0);
                                ya = wa & 255;
                                a[(b + ja + 2716) >> 0] = ya;
                                ha = (ja + -240) | 0;
                                if (ha >>> 0 < 16 ? ((a[(b + ha + 1940) >> 0] = ya), ((-788594688 << ha) | 0) < 0) : 0) {
                                    if ((ha | 0) == 3) {
                                        Na(b, wa, K);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    } else {
                                        Ma(b, wa, K, ha);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = V;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break c;
                                    }
                                } else {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                                break;
                            }
                            case 74: {
                                ha = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = N & 256 & (((Pa(b, ((ha << 8) & 7936) | X, K) | 0) >>> (ha >>> 5)) << 8);
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 202: {
                                ha = d[(Q + 2) >> 0] | 0;
                                wa = (Q + 3) | 0;
                                ya = ((ha << 8) & 7936) | X;
                                ja = ha >>> 5;
                                ha = ((((Pa(b, ya, (K + -2) | 0) | 0) & ~(1 << ja)) | (((N >>> 8) & 1) << ja)) + 8192) | 0;
                                ja = ha & 255;
                                a[(b + ya + 2716) >> 0] = ja;
                                ia = (ya + -240) | 0;
                                if (ia >>> 0 < 16 ? ((a[(b + ia + 1940) >> 0] = ja), ((-788594688 << ia) | 0) < 0) : 0) {
                                    if ((ia | 0) == 3) {
                                        Na(b, ha, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = wa;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    } else {
                                        Ma(b, ha, K, ia);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = wa;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = wa;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                                break;
                            }
                            case 106: {
                                wa = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = (((((Pa(b, ((wa << 8) & 7936) | X, K) | 0) >>> (wa >>> 5)) << 8) | -257) ^ 256) & N;
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 10: {
                                wa = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = ((((Pa(b, ((wa << 8) & 7936) | X, (K + -1) | 0) | 0) >>> (wa >>> 5)) << 8) & 256) | N;
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 42: {
                                wa = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = (((((Pa(b, ((wa << 8) & 7936) | X, (K + -1) | 0) | 0) >>> (wa >>> 5)) << 8) | -257) ^ 256) | N;
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 138: {
                                wa = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = ((((Pa(b, ((wa << 8) & 7936) | X, (K + -1) | 0) | 0) >>> (wa >>> 5)) << 8) & 256) ^ N;
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 234: {
                                wa = d[(Q + 2) >> 0] | 0;
                                ia = (Q + 3) | 0;
                                ha = ((wa << 8) & 7936) | X;
                                ja = (1 << (wa >>> 5)) ^ (Pa(b, ha, (K + -1) | 0) | 0);
                                wa = ja & 255;
                                a[(b + ha + 2716) >> 0] = wa;
                                ya = (ha + -240) | 0;
                                if (ya >>> 0 < 16 ? ((a[(b + ya + 1940) >> 0] = wa), ((-788594688 << ya) | 0) < 0) : 0) {
                                    if ((ya | 0) == 3) {
                                        Na(b, ja, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = ia;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    } else {
                                        Ma(b, ja, K, ya);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = P;
                                        ba = ia;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break c;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = ia;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                                break;
                            }
                            case 96: {
                                Y = M;
                                Z = 0;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 170: {
                                ia = d[(Q + 2) >> 0] | 0;
                                Y = M;
                                Z = (((Pa(b, ((ia << 8) & 7936) | X, K) | 0) >>> (ia >>> 5)) << 8) & 256;
                                $ = O;
                                aa = P;
                                ba = (Q + 3) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 128: {
                                Y = M;
                                Z = -1;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 237: {
                                Y = M;
                                Z = N ^ 256;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 224: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R & -73;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 32: {
                                Y = M;
                                Z = N;
                                $ = 0;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 64: {
                                Y = M;
                                Z = N;
                                $ = 256;
                                aa = P;
                                ba = V;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 160: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R | 4;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 192: {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = V;
                                ca = R & -5;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            case 239: {
                                ua = 478;
                                break b;
                                break;
                            }
                            case 255: {
                                ia = (V - F + -1) | 0;
                                if (!(ia >>> 0 > 65535)) {
                                    ua = 478;
                                    break b;
                                }
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = (b + (ia & 65535) + 2716) | 0;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                                break;
                            }
                            default: {
                                ua = 479;
                                break b;
                            }
                        }
                    } while (0);
                    switch (ua | 0) {
                        case 48: {
                            ua = 0;
                            W = (Q + 3) | 0;
                            ia = d[(Q + 2) >> 0] | O;
                            ya = Ga & 255;
                            a[(b + ia + 2716) >> 0] = ya;
                            ja = (ia + -240) | 0;
                            if (ja >>> 0 < 16 ? ((a[(b + ja + 1940) >> 0] = ya), ((-788594688 << ja) | 0) < 0) : 0) {
                                if ((ja | 0) == 3) {
                                    Na(b, Ga, K);
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = W;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break;
                                } else {
                                    Ma(b, Ga, K, ja);
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = P;
                                    ba = W;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break;
                                }
                            } else {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = P;
                                ba = W;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                            }
                            break;
                        }
                        case 63: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            Ha = ((d[W >> 0] << 8) + Ja) | 0;
                            Ia = W;
                            ua = 65;
                            break;
                        }
                        case 68: {
                            ua = 0;
                            W = Ka | O;
                            ja = (W + -253) | 0;
                            if (ja >>> 0 < 3) {
                                ya = (b + ((ja * 24) | 0) + 1868) | 0;
                                ia = c[ya >> 2] | 0;
                                if (
                                    (K | 0) >= (ia | 0)
                                        ? ((wa = c[(b + ((ja * 24) | 0) + 1872) >> 2] | 0), (ha = (((K - ia) | 0) / (wa | 0)) | 0), (ka = (ha + 1) | 0), (c[ya >> 2] = (_(ka, wa) | 0) + ia), (c[(b + ((ja * 24) | 0) + 1884) >> 2] | 0) != 0)
                                        : 0
                                ) {
                                    ia = c[(b + ((ja * 24) | 0) + 1876) >> 2] | 0;
                                    wa = (b + ((ja * 24) | 0) + 1880) | 0;
                                    ya = c[wa >> 2] | 0;
                                    za = (ha - ((ia + 255 - ya) & 255)) | 0;
                                    if ((za | 0) > -1) {
                                        ha = ((za | 0) / (ia | 0)) | 0;
                                        xa = (b + ((ja * 24) | 0) + 1888) | 0;
                                        c[xa >> 2] = (ha + 1 + (c[xa >> 2] | 0)) & 15;
                                        Nc = (za - (_(ha, ia) | 0)) | 0;
                                    } else {
                                        Nc = (ya + ka) | 0;
                                    }
                                    c[wa >> 2] = Nc & 255;
                                }
                                wa = (b + ((ja * 24) | 0) + 1888) | 0;
                                ja = c[wa >> 2] | 0;
                                c[wa >> 2] = 0;
                                la = M;
                                ma = N;
                                na = ja;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = ja;
                                ta = U;
                                ua = 6;
                                break;
                            } else {
                                ja = d[(b + W + 2716) >> 0] | 0;
                                wa = (W + -240) | 0;
                                if (!(wa >>> 0 < 16)) {
                                    la = M;
                                    ma = N;
                                    na = ja;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = ja;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                ja = d[(b + wa + 1956) >> 0] | 0;
                                wa = (W + -242) | 0;
                                if (!(wa >>> 0 < 2)) {
                                    la = M;
                                    ma = N;
                                    na = ja;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = ja;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                ja = a[G >> 0] | 0;
                                W = ja & 255;
                                if ((wa | 0) != 1) {
                                    la = M;
                                    ma = N;
                                    na = W;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = W;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                wa = c[j >> 2] | 0;
                                ka = (K - (a[(b + (W & 127) + 1612) >> 0] | 0) - wa) | 0;
                                if ((ka | 0) > -1) {
                                    W = (ka + 32) & -32;
                                    c[j >> 2] = W + wa;
                                    ib(b, W);
                                    Oc = a[G >> 0] | 0;
                                } else {
                                    Oc = ja;
                                }
                                ja = d[(b + (Oc & 127)) >> 0] | 0;
                                la = M;
                                ma = N;
                                na = ja;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = ja;
                                ta = U;
                                ua = 6;
                                break;
                            }
                            break;
                        }
                        case 82: {
                            ua = 0;
                            la = M;
                            ma = N;
                            na = La;
                            oa = Qa;
                            pa = R;
                            qa = K;
                            sa = La;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 84: {
                            ua = 0;
                            ja = (Q + 2) | 0;
                            W = Ra | O;
                            wa = (W + -253) | 0;
                            if (wa >>> 0 < 3) {
                                ka = (b + ((wa * 24) | 0) + 1868) | 0;
                                ya = c[ka >> 2] | 0;
                                if (
                                    (K | 0) >= (ya | 0)
                                        ? ((ia = c[(b + ((wa * 24) | 0) + 1872) >> 2] | 0), (ha = (((K - ya) | 0) / (ia | 0)) | 0), (za = (ha + 1) | 0), (c[ka >> 2] = (_(za, ia) | 0) + ya), (c[(b + ((wa * 24) | 0) + 1884) >> 2] | 0) != 0)
                                        : 0
                                ) {
                                    ya = c[(b + ((wa * 24) | 0) + 1876) >> 2] | 0;
                                    ia = (b + ((wa * 24) | 0) + 1880) | 0;
                                    ka = c[ia >> 2] | 0;
                                    xa = (ha - ((ya + 255 - ka) & 255)) | 0;
                                    if ((xa | 0) > -1) {
                                        ha = ((xa | 0) / (ya | 0)) | 0;
                                        Aa = (b + ((wa * 24) | 0) + 1888) | 0;
                                        c[Aa >> 2] = (ha + 1 + (c[Aa >> 2] | 0)) & 15;
                                        Pc = (xa - (_(ha, ya) | 0)) | 0;
                                    } else {
                                        Pc = (ka + za) | 0;
                                    }
                                    c[ia >> 2] = Pc & 255;
                                }
                                ia = (b + ((wa * 24) | 0) + 1888) | 0;
                                wa = c[ia >> 2] | 0;
                                c[ia >> 2] = 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = wa;
                                ba = ja;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = wa;
                                break;
                            } else {
                                wa = d[(b + W + 2716) >> 0] | 0;
                                ia = (W + -240) | 0;
                                if (!(ia >>> 0 < 16)) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = wa;
                                    ba = ja;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = wa;
                                    break;
                                }
                                wa = d[(b + ia + 1956) >> 0] | 0;
                                ia = (W + -242) | 0;
                                if (!(ia >>> 0 < 2)) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = wa;
                                    ba = ja;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = wa;
                                    break;
                                }
                                wa = a[G >> 0] | 0;
                                W = wa & 255;
                                if ((ia | 0) != 1) {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = W;
                                    ba = ja;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = W;
                                    break;
                                }
                                ia = c[j >> 2] | 0;
                                za = (K - (a[(b + (W & 127) + 1612) >> 0] | 0) - ia) | 0;
                                if ((za | 0) > -1) {
                                    W = (za + 32) & -32;
                                    c[j >> 2] = W + ia;
                                    ib(b, W);
                                    Qc = a[G >> 0] | 0;
                                } else {
                                    Qc = wa;
                                }
                                wa = d[(b + (Qc & 127)) >> 0] | 0;
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = wa;
                                ba = ja;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = wa;
                                break;
                            }
                            break;
                        }
                        case 116: {
                            ua = 0;
                            wa = (Q + 2) | 0;
                            Ua = ((d[wa >> 0] << 8) + Wa) | 0;
                            Va = wa;
                            ua = 118;
                            break;
                        }
                        case 127: {
                            ua = 0;
                            wa = (d[(Q + 2) >> 0] << 8) | X;
                            ja = Xa & 255;
                            a[(b + wa + 2716) >> 0] = ja;
                            W = (wa + -240) | 0;
                            do {
                                if ((W | 0) > -1) {
                                    if ((W | 0) >= 16) {
                                        ia = (wa + -65472) | 0;
                                        if (!((ia | 0) > -1)) {
                                            break;
                                        }
                                        Oa(b, Xa, ia, K);
                                        break;
                                    }
                                    a[(b + W + 1940) >> 0] = ja;
                                    if (((-788594688 << W) | 0) < 0) {
                                        if ((W | 0) == 3) {
                                            Na(b, Xa, K);
                                            break;
                                        } else {
                                            Ma(b, Xa, K, W);
                                            break;
                                        }
                                    }
                                }
                            } while (0);
                            Y = M;
                            Z = N;
                            $ = O;
                            aa = P;
                            ba = (Q + 3) | 0;
                            ca = R;
                            da = K;
                            ea = S;
                            fa = T;
                            ga = U;
                            break;
                        }
                        case 137: {
                            ua = 0;
                            W = Ya | O;
                            ja = T & 255;
                            a[(b + W + 2716) >> 0] = ja;
                            wa = (W + -240) | 0;
                            if (wa >>> 0 < 16 ? ((a[(b + wa + 1940) >> 0] = ja), ((-788594688 << wa) | 0) < 0) : 0) {
                                if ((wa | 0) == 3) {
                                    Na(b, T, K);
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                } else {
                                    Ma(b, T, K, wa);
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                            } else {
                                la = M;
                                ma = N;
                                na = P;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                            break;
                        }
                        case 143: {
                            ua = 0;
                            wa = Za | O;
                            ja = U & 255;
                            a[(b + wa + 2716) >> 0] = ja;
                            W = (wa + -240) | 0;
                            if (W >>> 0 < 16 ? ((a[(b + W + 1940) >> 0] = ja), ((-788594688 << W) | 0) < 0) : 0) {
                                if ((W | 0) == 3) {
                                    Na(b, U, K);
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                } else {
                                    Ma(b, U, K, W);
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = V;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                            } else {
                                la = M;
                                ma = N;
                                na = P;
                                oa = V;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                            break;
                        }
                        case 168: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            _a = ((d[W >> 0] << 8) + ab) | 0;
                            $a = W;
                            ua = 171;
                            break;
                        }
                        case 170: {
                            ua = 0;
                            _a = bb | O;
                            $a = V;
                            ua = 171;
                            break;
                        }
                        case 175: {
                            ua = 0;
                            eb = d[(Q + 2) >> 0] | O;
                            fb = hb;
                            gb = (Q + 3) | 0;
                            ua = 176;
                            break;
                        }
                        case 189: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            jb = ((d[W >> 0] << 8) + lb) | 0;
                            kb = W;
                            ua = 192;
                            break;
                        }
                        case 191: {
                            ua = 0;
                            jb = mb | O;
                            kb = V;
                            ua = 192;
                            break;
                        }
                        case 196: {
                            ua = 0;
                            pb = d[(Q + 2) >> 0] | O;
                            qb = sb;
                            rb = (Q + 3) | 0;
                            ua = 197;
                            break;
                        }
                        case 210: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            tb = ((d[W >> 0] << 8) + vb) | 0;
                            ub = W;
                            ua = 213;
                            break;
                        }
                        case 212: {
                            ua = 0;
                            tb = wb | O;
                            ub = V;
                            ua = 213;
                            break;
                        }
                        case 217: {
                            ua = 0;
                            zb = d[(Q + 2) >> 0] | O;
                            Ab = Cb;
                            Bb = (Q + 3) | 0;
                            ua = 218;
                            break;
                        }
                        case 231: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            Db = ((d[W >> 0] << 8) + Fb) | 0;
                            Eb = W;
                            ua = 234;
                            break;
                        }
                        case 233: {
                            ua = 0;
                            Db = Gb | O;
                            Eb = V;
                            ua = 234;
                            break;
                        }
                        case 238: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            ja = ((Pa(b, d[W >> 0] | O, (K + -1) | 0) | 0) - Lb) | 0;
                            la = M;
                            ma = ~ja;
                            na = ja & 255;
                            oa = W;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 241: {
                            ua = 0;
                            Mb = Pa(b, Jb, K) | 0;
                            Nb = Kb;
                            ua = 242;
                            break;
                        }
                        case 245: {
                            ua = 0;
                            Qb = Pa(b, Ob, K) | 0;
                            Rb = Pb;
                            ua = 246;
                            break;
                        }
                        case 249: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            Sb = d[W >> 0] | O;
                            Tb = Vb;
                            Ub = W;
                            ua = 250;
                            break;
                        }
                        case 256: {
                            ua = 0;
                            W = (Q + 2) | 0;
                            Wb = ((d[W >> 0] << 8) + Yb) | 0;
                            Xb = W;
                            ua = 259;
                            break;
                        }
                        case 258: {
                            ua = 0;
                            Wb = Zb | O;
                            Xb = V;
                            ua = 259;
                            break;
                        }
                        case 277: {
                            ua = 0;
                            dc = _b | O;
                            ec = V;
                            ua = 279;
                            break;
                        }
                        case 288: {
                            ua = 0;
                            W = ((fc >>> 1) & 128) | (M >> 1);
                            Y = W;
                            Z = M << 8;
                            $ = O;
                            aa = W;
                            ba = V;
                            ca = R;
                            da = K;
                            ea = S;
                            fa = T;
                            ga = U;
                            break;
                        }
                        case 290: {
                            ua = 0;
                            W = M << 1;
                            ja = ((gc >>> 8) & 1) | W;
                            Y = ja & 255;
                            Z = W;
                            $ = O;
                            aa = ja;
                            ba = V;
                            ca = R;
                            da = K;
                            ea = S;
                            fa = T;
                            ga = U;
                            break;
                        }
                        case 293: {
                            ua = 0;
                            lc = kc;
                            mc = (X + T) & 255;
                            ua = 294;
                            break;
                        }
                        case 296: {
                            ua = 0;
                            ja = (Q + 2) | 0;
                            hc = nc;
                            ic = (d[ja >> 0] << 8) | X;
                            jc = ja;
                            ua = 297;
                            break;
                        }
                        case 307: {
                            ua = 0;
                            sc = rc;
                            tc = (X + T) & 255;
                            ua = 308;
                            break;
                        }
                        case 310: {
                            ua = 0;
                            ja = (Q + 2) | 0;
                            oc = uc;
                            pc = (d[ja >> 0] << 8) | X;
                            qc = ja;
                            ua = 311;
                            break;
                        }
                        case 388: {
                            ua = 0;
                            ja = (K + -4) | 0;
                            W = Gc | O;
                            wa = (W + -253) | 0;
                            if (!(wa >>> 0 < 3)) {
                                ia = d[(b + W + 2716) >> 0] | 0;
                                za = (W + -240) | 0;
                                if (za >>> 0 < 16) {
                                    ka = d[(b + za + 1956) >> 0] | 0;
                                    za = (W + -242) | 0;
                                    if (za >>> 0 < 2) {
                                        W = a[G >> 0] | 0;
                                        ya = W & 255;
                                        if ((za | 0) == 1) {
                                            za = c[j >> 2] | 0;
                                            ha = (ja - (a[(b + (ya & 127) + 1612) >> 0] | 0) - za) | 0;
                                            if ((ha | 0) > -1) {
                                                xa = (ha + 32) & -32;
                                                c[j >> 2] = xa + za;
                                                ib(b, xa);
                                                Rc = a[G >> 0] | 0;
                                            } else {
                                                Rc = W;
                                            }
                                            Sc = d[(b + (Rc & 127)) >> 0] | 0;
                                        } else {
                                            Sc = ya;
                                        }
                                    } else {
                                        Sc = ka;
                                    }
                                } else {
                                    Sc = ia;
                                }
                            } else {
                                ia = (b + ((wa * 24) | 0) + 1868) | 0;
                                ka = c[ia >> 2] | 0;
                                if (
                                    (ja | 0) >= (ka | 0)
                                        ? ((ya = c[(b + ((wa * 24) | 0) + 1872) >> 2] | 0), (W = (((ja - ka) | 0) / (ya | 0)) | 0), (ja = (W + 1) | 0), (c[ia >> 2] = (_(ja, ya) | 0) + ka), (c[(b + ((wa * 24) | 0) + 1884) >> 2] | 0) != 0)
                                        : 0
                                ) {
                                    ka = c[(b + ((wa * 24) | 0) + 1876) >> 2] | 0;
                                    ya = (b + ((wa * 24) | 0) + 1880) | 0;
                                    ia = c[ya >> 2] | 0;
                                    xa = (W - ((ka + 255 - ia) & 255)) | 0;
                                    if ((xa | 0) > -1) {
                                        W = ((xa | 0) / (ka | 0)) | 0;
                                        za = (b + ((wa * 24) | 0) + 1888) | 0;
                                        c[za >> 2] = (W + 1 + (c[za >> 2] | 0)) & 15;
                                        Tc = (xa - (_(W, ka) | 0)) | 0;
                                    } else {
                                        Tc = (ia + ja) | 0;
                                    }
                                    c[ya >> 2] = Tc & 255;
                                }
                                ya = (b + ((wa * 24) | 0) + 1888) | 0;
                                wa = c[ya >> 2] | 0;
                                c[ya >> 2] = 0;
                                Sc = wa;
                            }
                            wa = (Q + 2) | 0;
                            if ((Sc | 0) == (M | 0)) {
                                la = M;
                                ma = N;
                                na = P;
                                oa = wa;
                                pa = R;
                                qa = (K + -2) | 0;
                                sa = T;
                                ta = U;
                                ua = 6;
                            } else {
                                Fc = wa;
                                ua = 5;
                            }
                            break;
                        }
                        case 414: {
                            ua = 0;
                            Y = M;
                            Z = N;
                            $ = O;
                            aa = P;
                            ba = (b + ((d[(Ic + 1) >> 0] << 8) | (Hc & 255)) + 2716) | 0;
                            ca = R;
                            da = K;
                            ea = S;
                            fa = T;
                            ga = U;
                            break;
                        }
                        case 428: {
                            ua = 0;
                            Y = M;
                            Z = Mc << 8;
                            $ = (Mc << 3) & 256;
                            aa = (((Mc << 4) & 2048) | (Mc & 2)) ^ 2;
                            ba = Kc;
                            ca = Mc;
                            da = K;
                            ea = Lc;
                            fa = T;
                            ga = U;
                            break;
                        }
                    }
                    switch (ua | 0) {
                        case 5: {
                            ua = 0;
                            la = M;
                            ma = N;
                            na = P;
                            oa = (Fc + (a[Fc >> 0] | 0)) | 0;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 65: {
                            ua = 0;
                            wa = Pa(b, Ha, K) | 0;
                            la = wa;
                            ma = N;
                            na = wa;
                            oa = Ia;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 118: {
                            ua = 0;
                            wa = M & 255;
                            a[(b + Ua + 2716) >> 0] = wa;
                            ya = (Ua + -240) | 0;
                            if ((ya | 0) > -1) {
                                if ((ya | 0) >= 16) {
                                    ja = (Ua + -65472) | 0;
                                    if (!((ja | 0) > -1)) {
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = Va;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                    Oa(b, M, ja, K);
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = Va;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                a[(b + ya + 1940) >> 0] = wa;
                                if (((-788594688 << ya) | 0) < 0) {
                                    if ((ya | 0) == 3) {
                                        Na(b, M, K);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = Va;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    } else {
                                        Ma(b, M, K, ya);
                                        la = M;
                                        ma = N;
                                        na = P;
                                        oa = Va;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                } else {
                                    la = M;
                                    ma = N;
                                    na = P;
                                    oa = Va;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                            } else {
                                la = M;
                                ma = N;
                                na = P;
                                oa = Va;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                            break;
                        }
                        case 171: {
                            ua = 0;
                            cb = Pa(b, _a, K) | 0;
                            db = $a;
                            ua = 172;
                            break;
                        }
                        case 176: {
                            ua = 0;
                            ya = (Pa(b, eb, (K + -1) | 0) | 0) & fb;
                            wa = ya & 255;
                            a[(b + eb + 2716) >> 0] = wa;
                            ja = (eb + -240) | 0;
                            if ((ja | 0) > -1) {
                                if ((ja | 0) >= 16) {
                                    ia = (eb + -65472) | 0;
                                    if (!((ia | 0) > -1)) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = gb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                    Oa(b, ya, ia, K);
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = gb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break;
                                }
                                a[(b + ja + 1940) >> 0] = wa;
                                if (((-788594688 << ja) | 0) < 0) {
                                    if ((ja | 0) == 3) {
                                        Na(b, ya, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = gb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    } else {
                                        Ma(b, ya, K, ja);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = gb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = gb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                            } else {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ya;
                                ba = gb;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                            }
                            break;
                        }
                        case 192: {
                            ua = 0;
                            nb = Pa(b, jb, K) | 0;
                            ob = kb;
                            ua = 193;
                            break;
                        }
                        case 197: {
                            ua = 0;
                            ya = Pa(b, pb, (K + -1) | 0) | 0 | qb;
                            ja = ya & 255;
                            a[(b + pb + 2716) >> 0] = ja;
                            wa = (pb + -240) | 0;
                            if ((wa | 0) > -1) {
                                if ((wa | 0) >= 16) {
                                    ia = (pb + -65472) | 0;
                                    if (!((ia | 0) > -1)) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = rb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                    Oa(b, ya, ia, K);
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = rb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break;
                                }
                                a[(b + wa + 1940) >> 0] = ja;
                                if (((-788594688 << wa) | 0) < 0) {
                                    if ((wa | 0) == 3) {
                                        Na(b, ya, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = rb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    } else {
                                        Ma(b, ya, K, wa);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = rb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = rb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                            } else {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ya;
                                ba = rb;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                            }
                            break;
                        }
                        case 213: {
                            ua = 0;
                            xb = Pa(b, tb, K) | 0;
                            yb = ub;
                            ua = 214;
                            break;
                        }
                        case 218: {
                            ua = 0;
                            ya = (Pa(b, zb, (K + -1) | 0) | 0) ^ Ab;
                            wa = ya & 255;
                            a[(b + zb + 2716) >> 0] = wa;
                            ja = (zb + -240) | 0;
                            if ((ja | 0) > -1) {
                                if ((ja | 0) >= 16) {
                                    ia = (zb + -65472) | 0;
                                    if (!((ia | 0) > -1)) {
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = Bb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                    Oa(b, ya, ia, K);
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = Bb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                    break;
                                }
                                a[(b + ja + 1940) >> 0] = wa;
                                if (((-788594688 << ja) | 0) < 0) {
                                    if ((ja | 0) == 3) {
                                        Na(b, ya, K);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = Bb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    } else {
                                        Ma(b, ya, K, ja);
                                        Y = M;
                                        Z = N;
                                        $ = O;
                                        aa = ya;
                                        ba = Bb;
                                        ca = R;
                                        da = K;
                                        ea = S;
                                        fa = T;
                                        ga = U;
                                        break;
                                    }
                                } else {
                                    Y = M;
                                    Z = N;
                                    $ = O;
                                    aa = ya;
                                    ba = Bb;
                                    ca = R;
                                    da = K;
                                    ea = S;
                                    fa = T;
                                    ga = U;
                                }
                            } else {
                                Y = M;
                                Z = N;
                                $ = O;
                                aa = ya;
                                ba = Bb;
                                ca = R;
                                da = K;
                                ea = S;
                                fa = T;
                                ga = U;
                            }
                            break;
                        }
                        case 234: {
                            ua = 0;
                            Hb = Pa(b, Db, K) | 0;
                            Ib = Eb;
                            ua = 235;
                            break;
                        }
                        case 242: {
                            ua = 0;
                            ya = (T - Mb) | 0;
                            la = M;
                            ma = ~ya;
                            na = ya & 255;
                            oa = Nb;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 246: {
                            ua = 0;
                            ya = (U - Qb) | 0;
                            la = M;
                            ma = ~ya;
                            na = ya & 255;
                            oa = Rb;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                            break;
                        }
                        case 250: {
                            ua = 0;
                            $b = Sb;
                            ac = Tb;
                            bc = Pa(b, Sb, (K + -1) | 0) | 0;
                            cc = Ub;
                            ua = 260;
                            break;
                        }
                        case 259: {
                            ua = 0;
                            $b = -1;
                            ac = Pa(b, Wb, K) | 0;
                            bc = M;
                            cc = Xb;
                            ua = 260;
                            break;
                        }
                        case 279: {
                            ua = 0;
                            ya = (((J >>> 4) & 2) + -1 + (Pa(b, dc, (K + -1) | 0) | 0)) | 0;
                            ja = ya & 255;
                            a[(b + dc + 2716) >> 0] = ja;
                            wa = (dc + -240) | 0;
                            if ((wa | 0) > -1) {
                                if ((wa | 0) >= 16) {
                                    ia = (dc + -65472) | 0;
                                    if (!((ia | 0) > -1)) {
                                        la = M;
                                        ma = N;
                                        na = ya;
                                        oa = ec;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                    Oa(b, ya, ia, K);
                                    la = M;
                                    ma = N;
                                    na = ya;
                                    oa = ec;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                a[(b + wa + 1940) >> 0] = ja;
                                if (((-788594688 << wa) | 0) < 0) {
                                    if ((wa | 0) == 3) {
                                        Na(b, ya, K);
                                        la = M;
                                        ma = N;
                                        na = ya;
                                        oa = ec;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    } else {
                                        Ma(b, ya, K, wa);
                                        la = M;
                                        ma = N;
                                        na = ya;
                                        oa = ec;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                } else {
                                    la = M;
                                    ma = N;
                                    na = ya;
                                    oa = ec;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                            } else {
                                la = M;
                                ma = N;
                                na = ya;
                                oa = ec;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                            break;
                        }
                        case 294: {
                            ua = 0;
                            hc = lc;
                            ic = mc | O;
                            jc = V;
                            ua = 297;
                            break;
                        }
                        case 308: {
                            ua = 0;
                            oc = sc;
                            pc = tc | O;
                            qc = V;
                            ua = 311;
                            break;
                        }
                    }
                    do {
                        if ((ua | 0) == 172) {
                            ua = 0;
                            ya = cb & M;
                            la = ya;
                            ma = N;
                            na = ya;
                            oa = db;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                        } else if ((ua | 0) == 193) {
                            ua = 0;
                            ya = nb | M;
                            la = ya;
                            ma = N;
                            na = ya;
                            oa = ob;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                        } else if ((ua | 0) == 214) {
                            ua = 0;
                            ya = xb ^ M;
                            la = ya;
                            ma = N;
                            na = ya;
                            oa = yb;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                        } else if ((ua | 0) == 235) {
                            ua = 0;
                            ya = (M - Hb) | 0;
                            la = M;
                            ma = ~ya;
                            na = ya & 255;
                            oa = Ib;
                            pa = R;
                            qa = K;
                            sa = T;
                            ta = U;
                            ua = 6;
                        } else if ((ua | 0) == 260) {
                            ua = 0;
                            ya = (L & 255) > 159 ? ac ^ 255 : ac;
                            wa = (bc + ((N >>> 8) & 1) + ya) | 0;
                            ja = ya ^ bc ^ wa;
                            ya = ((ja >>> 1) & 8) | (R & -73) | ((((ja + 128) | 0) >>> 2) & 64);
                            if (($b | 0) < 0) {
                                la = wa & 255;
                                ma = wa;
                                na = wa;
                                oa = cc;
                                pa = ya;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                                break;
                            }
                            ja = wa & 255;
                            a[(b + $b + 2716) >> 0] = ja;
                            ia = ($b + -240) | 0;
                            if ((ia | 0) > -1) {
                                if ((ia | 0) >= 16) {
                                    ka = ($b + -65472) | 0;
                                    if (!((ka | 0) > -1)) {
                                        la = M;
                                        ma = wa;
                                        na = wa;
                                        oa = cc;
                                        pa = ya;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                    Oa(b, wa, ka, K);
                                    la = M;
                                    ma = wa;
                                    na = wa;
                                    oa = cc;
                                    pa = ya;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                a[(b + ia + 1940) >> 0] = ja;
                                if (((-788594688 << ia) | 0) < 0) {
                                    if ((ia | 0) == 3) {
                                        Na(b, wa, K);
                                        la = M;
                                        ma = wa;
                                        na = wa;
                                        oa = cc;
                                        pa = ya;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    } else {
                                        Ma(b, wa, K, ia);
                                        la = M;
                                        ma = wa;
                                        na = wa;
                                        oa = cc;
                                        pa = ya;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                } else {
                                    la = M;
                                    ma = wa;
                                    na = wa;
                                    oa = cc;
                                    pa = ya;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                            } else {
                                la = M;
                                ma = wa;
                                na = wa;
                                oa = cc;
                                pa = ya;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                        } else if ((ua | 0) == 297) {
                            ua = 0;
                            ya = (Pa(b, ic, (K + -1) | 0) | 0) << 1;
                            wa = ya | ((hc >>> 8) & 1);
                            ia = wa & 255;
                            a[(b + ic + 2716) >> 0] = ia;
                            ja = (ic + -240) | 0;
                            if ((ja | 0) > -1) {
                                if ((ja | 0) >= 16) {
                                    ka = (ic + -65472) | 0;
                                    if (!((ka | 0) > -1)) {
                                        la = M;
                                        ma = ya;
                                        na = wa;
                                        oa = jc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                    Oa(b, wa, ka, K);
                                    la = M;
                                    ma = ya;
                                    na = wa;
                                    oa = jc;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                a[(b + ja + 1940) >> 0] = ia;
                                if (((-788594688 << ja) | 0) < 0) {
                                    if ((ja | 0) == 3) {
                                        Na(b, wa, K);
                                        la = M;
                                        ma = ya;
                                        na = wa;
                                        oa = jc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    } else {
                                        Ma(b, wa, K, ja);
                                        la = M;
                                        ma = ya;
                                        na = wa;
                                        oa = jc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                } else {
                                    la = M;
                                    ma = ya;
                                    na = wa;
                                    oa = jc;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                            } else {
                                la = M;
                                ma = ya;
                                na = wa;
                                oa = jc;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                        } else if ((ua | 0) == 311) {
                            ua = 0;
                            wa = Pa(b, pc, (K + -1) | 0) | 0;
                            ya = (wa >> 1) | ((oc >>> 1) & 128);
                            ja = wa << 8;
                            wa = ya & 255;
                            a[(b + pc + 2716) >> 0] = wa;
                            ia = (pc + -240) | 0;
                            if ((ia | 0) > -1) {
                                if ((ia | 0) >= 16) {
                                    ka = (pc + -65472) | 0;
                                    if (!((ka | 0) > -1)) {
                                        la = M;
                                        ma = ja;
                                        na = ya;
                                        oa = qc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                    Oa(b, ya, ka, K);
                                    la = M;
                                    ma = ja;
                                    na = ya;
                                    oa = qc;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                    break;
                                }
                                a[(b + ia + 1940) >> 0] = wa;
                                if (((-788594688 << ia) | 0) < 0) {
                                    if ((ia | 0) == 3) {
                                        Na(b, ya, K);
                                        la = M;
                                        ma = ja;
                                        na = ya;
                                        oa = qc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    } else {
                                        Ma(b, ya, K, ia);
                                        la = M;
                                        ma = ja;
                                        na = ya;
                                        oa = qc;
                                        pa = R;
                                        qa = K;
                                        sa = T;
                                        ta = U;
                                        ua = 6;
                                        break;
                                    }
                                } else {
                                    la = M;
                                    ma = ja;
                                    na = ya;
                                    oa = qc;
                                    pa = R;
                                    qa = K;
                                    sa = T;
                                    ta = U;
                                    ua = 6;
                                }
                            } else {
                                la = M;
                                ma = ja;
                                na = ya;
                                oa = qc;
                                pa = R;
                                qa = K;
                                sa = T;
                                ta = U;
                                ua = 6;
                            }
                        }
                    } while (0);
                    if ((ua | 0) == 6) {
                        ua = 0;
                        Y = la;
                        Z = ma;
                        $ = O;
                        aa = na;
                        ba = (oa + 1) | 0;
                        ca = pa;
                        da = qa;
                        ea = S;
                        fa = sa;
                        ga = ta;
                    }
                    L = a[ba >> 0] | 0;
                    J = L & 255;
                    K = ((d[(b + J + 2204) >> 0] | 0) + da) | 0;
                    if ((K | 0) > 0) {
                        Uc = Y;
                        Vc = Z;
                        Wc = $;
                        Xc = aa;
                        Yc = ba;
                        Zc = ca;
                        _c = da;
                        $c = ea;
                        ad = fa;
                        bd = ga;
                        break a;
                    } else {
                        M = Y;
                        N = Z;
                        O = $;
                        P = aa;
                        Q = ba;
                        R = ca;
                        S = ea;
                        T = fa;
                        U = ga;
                    }
                }
                if ((ua | 0) == 478) {
                    c[(b + 2020) >> 2] = 584;
                    Uc = M;
                    Vc = N;
                    Wc = O;
                    Xc = P;
                    Yc = Q;
                    Zc = R;
                    _c = 0;
                    $c = S;
                    ad = T;
                    bd = U;
                    break;
                } else if ((ua | 0) == 479) {
                    ra(608, 544, 1200, 568);
                }
            } else {
                Uc = o;
                Vc = z;
                Wc = A;
                Xc = B;
                Yc = u;
                Zc = y;
                _c = h;
                $c = w;
                ad = q;
                bd = s;
            }
        } while (0);
        c[t >> 2] = (Yc - F) & 65535;
        c[v >> 2] = ($c + -257 - F) & 255;
        c[n >> 2] = Uc & 255;
        c[p >> 2] = ad & 255;
        c[r >> 2] = bd & 255;
        bd = ((Vc >>> 8) & 1) | (Wc >>> 3) | (Zc & -164) | (((Xc >>> 4) | Xc) & 128);
        c[x >> 2] = (((Xc & 255) << 24) >> 24 == 0 ? bd | 2 : bd) & 255;
        bd = ((c[g >> 2] | 0) + _c) | 0;
        c[g >> 2] = bd;
        c[j >> 2] = (c[j >> 2] | 0) - _c;
        c[k >> 2] = (c[k >> 2] | 0) - _c;
        c[l >> 2] = (c[l >> 2] | 0) - _c;
        c[m >> 2] = (c[m >> 2] | 0) - _c;
        if ((bd | 0) > (e | 0)) {
            ra(616, 544, 1220, 568);
        } else {
            i = f;
            return (b + 1944) | 0;
        }
        return 0;
    }
    function Sa(b) {
        b = b | 0;
        var d = 0,
            e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0;
        d = i;
        ub((b + 1868) | 0, 0, 66640) | 0;
        e = (b + 2716) | 0;
        jb(b, e);
        c[(b + 2008) >> 2] = 256;
        a[(b + 2138) >> 0] = -1;
        a[(b + 2139) >> 0] = -64;
        f = 0;
        do {
            g = a[(640 + f) >> 0] | 0;
            h = f << 1;
            a[(b + h + 2204) >> 0] = (g & 255) >>> 4;
            a[(b + (h | 1) + 2204) >> 0] = g & 15;
            f = (f + 1) | 0;
        } while ((f | 0) != 128);
        vb((b + 1612) | 0, 56, 256) | 0;
        ub(e | 0, -1, 65536) | 0;
        c[(b + 2072) >> 2] = 0;
        e = (b + 2460) | 0;
        f = (b + 2956) | 0;
        g = (b + 1940) | 0;
        h = (g + 0) | 0;
        j = (f + 0) | 0;
        k = (h + 16) | 0;
        do {
            a[h >> 0] = a[j >> 0] | 0;
            h = (h + 1) | 0;
            j = (j + 1) | 0;
        } while ((h | 0) < (k | 0));
        l = (b + 1956) | 0;
        h = (l + 0) | 0;
        j = (f + 0) | 0;
        k = (h + 12) | 0;
        do {
            a[h >> 0] = a[j >> 0] | 0;
            h = (h + 1) | 0;
            j = (j + 1) | 0;
        } while ((h | 0) < (k | 0));
        a[l >> 0] = 0;
        a[(b + 1957) >> 0] = 0;
        a[(b + 1966) >> 0] = 0;
        a[(b + 1967) >> 0] = 0;
        a[(b + 1968) >> 0] = 0;
        ub(e | 0, -1, 256) | 0;
        ub((b + 68252) | 0, -1, 256) | 0;
        e = (b + 1969) | 0;
        a[(e + 0) >> 0] = 15;
        a[(e + 1) >> 0] = 15;
        a[(e + 2) >> 0] = 15;
        e = (b + 1972) | 0;
        c[(e + 0) >> 2] = 0;
        c[(e + 4) >> 2] = 0;
        c[(e + 8) >> 2] = 0;
        c[(e + 12) >> 2] = 0;
        c[(e + 16) >> 2] = 0;
        c[(e + 20) >> 2] = 0;
        c[e >> 2] = 65472;
        a[g >> 0] = 10;
        a[(b + 1941) >> 0] = -80;
        g = (b + 1960) | 0;
        a[g >> 0] = 0;
        a[(g + 1) >> 0] = 0;
        a[(g + 2) >> 0] = 0;
        a[(g + 3) >> 0] = 0;
        Ua(b);
        kb(b);
        i = d;
        return 0;
    }
    function Ta(a, b) {
        a = a | 0;
        b = b | 0;
        var d = 0;
        c[(a + 2008) >> 2] = b;
        d = (b | 0) == 0 ? 1 : b;
        b = ((((d >> 1) + 4096) | 0) / (d | 0)) | 0;
        d = (b | 0) < 4 ? 4 : b;
        c[(a + 1920) >> 2] = d;
        b = d << 3;
        c[(a + 1896) >> 2] = b;
        c[(a + 1872) >> 2] = b;
        return;
    }
    function Ua(e) {
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            j = 0;
        f = i;
        c[(e + 2020) >> 2] = 0;
        a[(e + 2004) >> 0] = 0;
        c[(e + 2e3) >> 2] = 0;
        c[(e + 1996) >> 2] = 33;
        c[(e + 1868) >> 2] = 1;
        c[(e + 1880) >> 2] = 0;
        c[(e + 1892) >> 2] = 1;
        c[(e + 1904) >> 2] = 0;
        c[(e + 1916) >> 2] = 1;
        c[(e + 1928) >> 2] = 0;
        g = (e + 1941) | 0;
        La(e, (d[g >> 0] | 0) & 128);
        c[(e + 1876) >> 2] = (((d[(e + 1950) >> 0] | 0) + 255) & 255) + 1;
        h = d[g >> 0] | 0;
        c[(e + 1884) >> 2] = h & 1;
        c[(e + 1888) >> 2] = (d[(e + 1969) >> 0] | 0) & 15;
        c[(e + 1900) >> 2] = (((d[(e + 1951) >> 0] | 0) + 255) & 255) + 1;
        c[(e + 1908) >> 2] = (h >>> 1) & 1;
        c[(e + 1912) >> 2] = (d[(e + 1970) >> 0] | 0) & 15;
        c[(e + 1924) >> 2] = (((d[(e + 1952) >> 0] | 0) + 255) & 255) + 1;
        c[(e + 1932) >> 2] = (h >>> 2) & 1;
        c[(e + 1936) >> 2] = (d[(e + 1971) >> 0] | 0) & 15;
        h = c[(e + 2008) >> 2] | 0;
        g = (h | 0) == 0 ? 1 : h;
        h = ((((g >> 1) + 4096) | 0) / (g | 0)) | 0;
        g = (h | 0) < 4 ? 4 : h;
        c[(e + 1920) >> 2] = g;
        h = g << 3;
        c[(e + 1896) >> 2] = h;
        c[(e + 1872) >> 2] = h;
        c[(e + 2024) >> 2] = 0;
        h = (e + 2056) | 0;
        g = (e + 2040) | 0;
        do {
            j = g;
            g = (g + 2) | 0;
            b[j >> 1] = 0;
        } while (g >>> 0 < h >>> 0);
        c[(e + 2036) >> 2] = g;
        c[(e + 2028) >> 2] = 0;
        hb(e, 0, 0);
        i = f;
        return;
    }
    function Va(b, e, f) {
        b = b | 0;
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0;
        g = i;
        if ((f | 0) < 35) {
            h = 808;
            i = g;
            return h | 0;
        }
        if ((rb(e, 768, 27) | 0) != 0) {
            h = 808;
            i = g;
            return h | 0;
        }
        if ((f | 0) < 65920) {
            h = 824;
            i = g;
            return h | 0;
        }
        c[(b + 1972) >> 2] = ((d[(e + 38) >> 0] | 0) << 8) | (d[(e + 37) >> 0] | 0);
        c[(b + 1976) >> 2] = d[(e + 39) >> 0];
        c[(b + 1980) >> 2] = d[(e + 40) >> 0];
        c[(b + 1984) >> 2] = d[(e + 41) >> 0];
        c[(b + 1988) >> 2] = d[(e + 42) >> 0];
        c[(b + 1992) >> 2] = d[(e + 43) >> 0];
        vb((b + 2716) | 0, (e + 256) | 0, 65536) | 0;
        c[(b + 2072) >> 2] = 0;
        f = (b + 2460) | 0;
        j = (b + 2956) | 0;
        k = (b + 1940) | 0;
        l = (j + 0) | 0;
        m = (k + 16) | 0;
        do {
            a[k >> 0] = a[l >> 0] | 0;
            k = (k + 1) | 0;
            l = (l + 1) | 0;
        } while ((k | 0) < (m | 0));
        n = (b + 1956) | 0;
        k = (n + 0) | 0;
        l = (j + 0) | 0;
        m = (k + 16) | 0;
        do {
            a[k >> 0] = a[l >> 0] | 0;
            k = (k + 1) | 0;
            l = (l + 1) | 0;
        } while ((k | 0) < (m | 0));
        a[n >> 0] = 0;
        a[(b + 1957) >> 0] = 0;
        a[(b + 1966) >> 0] = 0;
        a[(b + 1967) >> 0] = 0;
        a[(b + 1968) >> 0] = 0;
        ub(f | 0, -1, 256) | 0;
        ub((b + 68252) | 0, -1, 256) | 0;
        lb(b, (e + 65792) | 0);
        Ua(b);
        h = 0;
        i = g;
        return h | 0;
    }
    function Wa(b) {
        b = b | 0;
        var c = 0,
            e = 0,
            f = 0;
        c = i;
        if (!((a[(b + 108) >> 0] & 32) == 0)) {
            i = c;
            return;
        }
        e = (d[(b + 109) >> 0] | 0) << 8;
        f = ((((d[(b + 125) >> 0] | 0) << 11) & 30720) + e) | 0;
        ub((b + e + 2716) | 0, -1, (((f | 0) > 65536 ? 65536 : f) - e) | 0) | 0;
        i = c;
        return;
    }
    function Xa(a, d, e) {
        a = a | 0;
        d = d | 0;
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0;
        f = i;
        if (((e & 1) | 0) != 0) {
            ra(848, 864, 279, 896);
        }
        g = (a + 2024) | 0;
        c[g >> 2] = c[g >> 2] & 31;
        if ((d | 0) == 0) {
            g = (a + 2056) | 0;
            h = (a + 2040) | 0;
            do {
                j = h;
                h = (h + 2) | 0;
                b[j >> 1] = 0;
            } while (h >>> 0 < g >>> 0);
            c[(a + 2036) >> 2] = h;
            c[(a + 2028) >> 2] = 0;
            hb(a, 0, 0);
            i = f;
            return;
        }
        h = (d + (e << 1)) | 0;
        c[(a + 2028) >> 2] = d;
        c[(a + 2032) >> 2] = h;
        g = (a + 2040) | 0;
        j = c[(a + 2036) >> 2] | 0;
        k = (e | 0) > 0;
        if ((g >>> 0 < j >>> 0) & k) {
            e = d;
            l = g;
            while (1) {
                m = (l + 2) | 0;
                n = (e + 2) | 0;
                b[e >> 1] = b[l >> 1] | 0;
                o = n >>> 0 < h >>> 0;
                if ((m >>> 0 < j >>> 0) & o) {
                    e = n;
                    l = m;
                } else {
                    p = n;
                    q = o;
                    r = m;
                    break;
                }
            }
        } else {
            p = d;
            q = k;
            r = g;
        }
        if (!q) {
            q = (a + 1580) | 0;
            g = (a + 1612) | 0;
            if (r >>> 0 < j >>> 0) {
                k = q;
                d = r;
                do {
                    r = d;
                    d = (d + 2) | 0;
                    l = k;
                    k = (k + 2) | 0;
                    b[l >> 1] = b[r >> 1] | 0;
                } while (d >>> 0 < j >>> 0);
                if (k >>> 0 > g >>> 0) {
                    ra(912, 864, 303, 896);
                } else {
                    s = k;
                    t = g;
                }
            } else {
                s = q;
                t = g;
            }
        } else {
            s = p;
            t = h;
        }
        hb(a, s, (t - s) >> 1);
        i = f;
        return;
    }
    function Ya(a) {
        a = a | 0;
        var d = 0,
            e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0;
        d = i;
        e = c[(a + 2032) >> 2] | 0;
        f = c[(a + 1568) >> 2] | 0;
        g = c[(a + 2028) >> 2] | 0;
        h = (g >>> 0 > f >>> 0) | (f >>> 0 > e >>> 0);
        j = (a + 1580) | 0;
        k = h ? e : f;
        e = h ? f : j;
        f = (a + 2040) | 0;
        h = (g + (((c[(a + 2024) >> 2] >> 5) << 1) << 1)) | 0;
        if (h >>> 0 < k >>> 0) {
            g = h;
            h = f;
            while (1) {
                l = (h + 2) | 0;
                b[h >> 1] = b[g >> 1] | 0;
                g = (g + 2) | 0;
                if (!(g >>> 0 < k >>> 0)) {
                    m = l;
                    break;
                } else {
                    h = l;
                }
            }
        } else {
            m = f;
        }
        if (j >>> 0 < e >>> 0) {
            f = j;
            j = m;
            while (1) {
                h = (j + 2) | 0;
                b[j >> 1] = b[f >> 1] | 0;
                f = (f + 2) | 0;
                if (!(f >>> 0 < e >>> 0)) {
                    n = h;
                    break;
                } else {
                    j = h;
                }
            }
        } else {
            n = m;
        }
        c[(a + 2036) >> 2] = n;
        if (n >>> 0 > ((a + 2072) | 0) >>> 0) {
            ra(928, 864, 334, 968);
        } else {
            i = d;
            return;
        }
    }
    function Za(a, b, d) {
        a = a | 0;
        b = b | 0;
        d = d | 0;
        var e = 0;
        e = i;
        if (((b & 1) | 0) != 0) {
            ra(984, 864, 339, 1008);
        }
        if ((b | 0) != 0) {
            Xa(a, d, b);
            Qa(a, b << 4);
        }
        b = (a + 2020) | 0;
        a = c[b >> 2] | 0;
        c[b >> 2] = 0;
        i = e;
        return a | 0;
    }
    function _a() {
        var a = 0,
            b = 0,
            c = 0;
        a = i;
        b = pb(68508) | 0;
        if ((b | 0) != 0) {
            if ((Sa(b) | 0) == 0) {
                c = b;
            } else {
                qb(b);
                c = 0;
            }
        } else {
            c = 0;
        }
        i = a;
        return c | 0;
    }
    function $a(a, b, c) {
        a = a | 0;
        b = b | 0;
        c = c | 0;
        var d = 0;
        d = i;
        Xa(a, b, c);
        i = d;
        return;
    }
    function ab(a, b) {
        a = a | 0;
        b = b | 0;
        var c = 0;
        c = i;
        Ta(a, b);
        i = c;
        return;
    }
    function bb(a, b, c) {
        a = a | 0;
        b = b | 0;
        c = c | 0;
        var d = 0,
            e = 0;
        d = i;
        e = Va(a, b, c) | 0;
        i = d;
        return e | 0;
    }
    function cb(a) {
        a = a | 0;
        var b = 0;
        b = i;
        Wa(a);
        i = b;
        return;
    }
    function db(a, b, c) {
        a = a | 0;
        b = b | 0;
        c = c | 0;
        var d = 0,
            e = 0;
        d = i;
        e = Za(a, b, c) | 0;
        i = d;
        return e | 0;
    }
    function eb() {
        var a = 0,
            b = 0,
            c = 0;
        a = i;
        b = pb(32) | 0;
        if ((b | 0) == 0) {
            c = 0;
        } else {
            nb(b);
            c = b;
        }
        i = a;
        return c | 0;
    }
    function fb(a, b, c) {
        a = a | 0;
        b = b | 0;
        c = c | 0;
        var d = 0;
        d = i;
        ob(a, b, c);
        i = d;
        return;
    }
    function gb(a) {
        a = a | 0;
        var b = 0;
        b = i;
        mb(a);
        i = b;
        return;
    }
    function hb(a, b, d) {
        a = a | 0;
        b = b | 0;
        d = d | 0;
        var e = 0,
            f = 0;
        if (((d & 1) | 0) == 0) {
            e = (b | 0) == 0;
            f = e ? (a + 1580) | 0 : b;
            c[(a + 1576) >> 2] = f;
            c[(a + 1568) >> 2] = f;
            c[(a + 1572) >> 2] = f + ((e ? 16 : d) << 1);
            return;
        } else {
            ra(1016, 1032, 78, 1056);
        }
    }
    function ib(e, f) {
        e = e | 0;
        f = f | 0;
        var g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0,
            w = 0,
            x = 0,
            y = 0,
            z = 0,
            A = 0,
            B = 0,
            C = 0,
            D = 0,
            E = 0,
            F = 0,
            G = 0,
            H = 0,
            I = 0,
            J = 0,
            K = 0,
            L = 0,
            M = 0,
            N = 0,
            O = 0,
            P = 0,
            Q = 0,
            R = 0,
            S = 0,
            T = 0,
            U = 0,
            V = 0,
            W = 0,
            X = 0,
            Y = 0,
            Z = 0,
            $ = 0,
            aa = 0,
            ba = 0,
            ca = 0,
            da = 0,
            ea = 0,
            fa = 0,
            ga = 0,
            ha = 0,
            ia = 0,
            ja = 0,
            ka = 0,
            la = 0,
            ma = 0,
            na = 0,
            oa = 0,
            pa = 0,
            qa = 0,
            sa = 0,
            ta = 0,
            ua = 0,
            va = 0,
            wa = 0,
            xa = 0,
            ya = 0,
            za = 0,
            Aa = 0,
            Ba = 0,
            Ca = 0,
            Da = 0,
            Ea = 0,
            Fa = 0,
            Ga = 0,
            Ha = 0,
            Ia = 0,
            Ja = 0,
            Ka = 0,
            La = 0,
            Ma = 0,
            Na = 0,
            Oa = 0,
            Pa = 0,
            Qa = 0,
            Ra = 0,
            Sa = 0,
            Ta = 0,
            Ua = 0,
            Va = 0,
            Wa = 0,
            Xa = 0,
            Ya = 0,
            Za = 0,
            _a = 0,
            $a = 0,
            ab = 0,
            bb = 0,
            cb = 0;
        g = i;
        h = (e + 280) | 0;
        j = ((c[h >> 2] | 0) + f) | 0;
        f = j >> 5;
        c[h >> 2] = j & 31;
        if ((f | 0) == 0) {
            i = g;
            return;
        }
        j = c[(e + 1556) >> 2] | 0;
        h = d[(e + 93) >> 0] << 8;
        k = (e + 45) | 0;
        l = (e + 61) | 0;
        m = ((d[k >> 0] | 0) >>> 1) | d[l >> 0];
        n = (e + 108) | 0;
        o = d[n >> 0] & 31;
        p = a[(e + 12) >> 0] | 0;
        q = a[(e + 28) >> 0] | 0;
        r = _(q, p) | 0;
        s = (r | 0) < (c[(e + 1564) >> 2] | 0) ? (0 - p) | 0 : p;
        p = (e + 260) | 0;
        r = (e + 288) | 0;
        t = (e + 292) | 0;
        u = (e + 296) | 0;
        v = (e + (o << 2) + 1428) | 0;
        w = c[(1072 + (o << 2)) >> 2] | 0;
        o = (e + 268) | 0;
        x = (e + 308) | 0;
        y = (e + 124) | 0;
        z = (e + 304) | 0;
        A = (e + 264) | 0;
        B = (e + 77) | 0;
        C = (e + 272) | 0;
        D = (e + 109) | 0;
        E = (e + 125) | 0;
        F = (e + 276) | 0;
        G = (e + 256) | 0;
        H = (e + 192) | 0;
        I = (e + 128) | 0;
        J = (e + 127) | 0;
        K = (e + 15) | 0;
        L = (e + 31) | 0;
        M = (e + 47) | 0;
        N = (e + 63) | 0;
        O = (e + 79) | 0;
        P = (e + 95) | 0;
        Q = (e + 111) | 0;
        R = (e + 13) | 0;
        S = (e + 44) | 0;
        T = (e + 60) | 0;
        U = (e + 1568) | 0;
        V = (e + 1572) | 0;
        W = (e + 1580) | 0;
        X = (e + 1612) | 0;
        Y = (e + 300) | 0;
        Z = (e + 92) | 0;
        $ = f;
        a: while (1) {
            f = c[p >> 2] | 0;
            c[p >> 2] = f ^ 1;
            if ((f | 0) != 1) {
                f = c[Y >> 2] & ~c[A >> 2];
                c[Y >> 2] = f;
                c[A >> 2] = f;
                c[z >> 2] = d[Z >> 0];
            }
            f = c[r >> 2] | 0;
            c[r >> 2] = (((f & 7) | 0) == 0 ? -6 : -1) + f;
            f = c[t >> 2] | 0;
            c[t >> 2] = (((f & 7) | 0) == 0 ? -5 : -1) + f;
            f = c[u >> 2] | 0;
            c[u >> 2] = (((f & 7) | 0) == 0 ? -4 : -1) + f;
            if (((w & c[c[v >> 2] >> 2]) | 0) == 0) {
                f = c[o >> 2] | 0;
                c[o >> 2] = (((f << 13) ^ (f << 14)) & 16384) ^ (f >> 1);
                aa = 0;
                ba = 0;
                ca = 0;
                da = 0;
                ea = 0;
                fa = x;
                ga = e;
                ha = 1;
            } else {
                aa = 0;
                ba = 0;
                ca = 0;
                da = 0;
                ea = 0;
                fa = x;
                ga = e;
                ha = 1;
            }
            while (1) {
                f = (fa + 104) | 0;
                ia = d[(j + (c[f >> 2] | 0)) >> 0] | 0;
                ja = (fa + 112) | 0;
                ka = c[ja >> 2] | 0;
                la = ((d[(ga + 3) >> 0] << 8) & 16128) | d[(ga + 2) >> 0];
                if (((d[k >> 0] & ha) | 0) == 0) {
                    ma = la;
                } else {
                    ma = (((_(la, ea >> 5) | 0) >> 10) + la) | 0;
                }
                la = (ka + -1) | 0;
                if ((ka | 0) <= 0) {
                    ka = c[(fa + 120) >> 2] | 0;
                    na = (fa + 120) | 0;
                    a[(ga + 8) >> 0] = ka >>> 4;
                    if ((ka | 0) != 0) {
                        oa = c[(fa + 100) >> 2] | 0;
                        pa = (oa >>> 3) & 510;
                        qa = (1200 + (pa << 1)) | 0;
                        sa = (510 - pa) | 0;
                        ta = (1200 + (sa << 1)) | 0;
                        ua = oa >>> 12;
                        oa = c[(fa + 96) >> 2] | 0;
                        va = (oa + (ua << 2)) | 0;
                        if (((ha & m) | 0) == 0) {
                            wa = _(b[qa >> 1] | 0, c[va >> 2] | 0) | 0;
                            xa = ((_(b[(1200 + ((pa | 1) << 1)) >> 1] | 0, c[(oa + ((ua + 1) << 2)) >> 2] | 0) | 0) + wa) | 0;
                            wa = (xa + (_(b[(1200 + ((sa | 1) << 1)) >> 1] | 0, c[(oa + ((ua + 2) << 2)) >> 2] | 0) | 0)) | 0;
                            ya = (_((wa + (_(b[ta >> 1] | 0, c[(oa + ((ua + 3) << 2)) >> 2] | 0) | 0)) >> 11, ka) | 0) >> 11;
                        } else {
                            wa = (c[o >> 2] << 17) >> 16;
                            if (((d[l >> 0] & ha) | 0) == 0) {
                                xa = (_(b[qa >> 1] | 0, c[va >> 2] | 0) | 0) >>> 11;
                                va = (((_(b[(1200 + ((pa | 1) << 1)) >> 1] | 0, c[(oa + ((ua + 1) << 2)) >> 2] | 0) | 0) >>> 11) + xa) | 0;
                                xa = ((va + ((_(b[(1200 + ((sa | 1) << 1)) >> 1] | 0, c[(oa + ((ua + 2) << 2)) >> 2] | 0) | 0) >>> 11)) << 16) >> 16;
                                sa = (xa + ((_(b[ta >> 1] | 0, c[(oa + ((ua + 3) << 2)) >> 2] | 0) | 0) >> 11)) | 0;
                                if ((((sa << 16) >> 16) | 0) == (sa | 0)) {
                                    za = sa;
                                } else {
                                    za = (sa >> 31) ^ 32767;
                                }
                                Aa = za & -2;
                            } else {
                                Aa = wa;
                            }
                            ya = ((_(Aa, ka) | 0) >> 11) & -2;
                        }
                        wa = _(c[(fa + 128) >> 2] | 0, ya) | 0;
                        sa = _(c[(fa + 132) >> 2] | 0, ya) | 0;
                        ua = (wa + ca) | 0;
                        oa = (sa + da) | 0;
                        if (((d[B >> 0] & ha) | 0) == 0) {
                            Ba = na;
                            Ca = ka;
                            Da = ia;
                            Ea = aa;
                            Fa = ba;
                            Ga = ua;
                            Ha = oa;
                            Ia = ya;
                            Ja = ma;
                        } else {
                            Ba = na;
                            Ca = ka;
                            Da = ia;
                            Ea = (wa + aa) | 0;
                            Fa = (sa + ba) | 0;
                            Ga = ua;
                            Ha = oa;
                            Ia = ya;
                            Ja = ma;
                        }
                    } else {
                        Ba = na;
                        Ca = 0;
                        Da = ia;
                        Ea = aa;
                        Fa = ba;
                        Ga = ca;
                        Ha = da;
                        Ia = 0;
                        Ja = ma;
                    }
                } else {
                    c[ja >> 2] = la;
                    if ((la | 0) == 4) {
                        na = ((d[(ga + 4) >> 0] << 2) + h) | 0;
                        c[f >> 2] = (d[(j + (na | 1)) >> 0] << 8) | d[(j + na) >> 0];
                        c[(fa + 108) >> 2] = 1;
                        c[(fa + 96) >> 2] = fa;
                        Ka = 0;
                    } else {
                        Ka = ia;
                    }
                    c[(fa + 120) >> 2] = 0;
                    c[(fa + 124) >> 2] = 0;
                    c[(fa + 100) >> 2] = ((la & 3) | 0) != 0 ? 16384 : 0;
                    a[(ga + 8) >> 0] = 0;
                    Ba = (fa + 120) | 0;
                    Ca = 0;
                    Da = Ka;
                    Ea = aa;
                    Fa = ba;
                    Ga = ca;
                    Ha = da;
                    Ia = 0;
                    Ja = 0;
                }
                a[(ga + 9) >> 0] = Ia >>> 8;
                if ((a[n >> 0] | 0) >= 0 ? ((Da & 3) | 0) != 1 : 0) {
                    La = Ca;
                } else {
                    c[(fa + 116) >> 2] = 0;
                    La = 0;
                }
                if ((c[p >> 2] | 0) != 0) {
                    if (((c[z >> 2] & ha) | 0) != 0) {
                        c[(fa + 116) >> 2] = 0;
                    }
                    if (((c[A >> 2] & ha) | 0) != 0) {
                        c[ja >> 2] = 5;
                        c[(fa + 116) >> 2] = 1;
                        a[y >> 0] = d[y >> 0] & (ha ^ 255);
                    }
                }
                la = (c[ja >> 2] | 0) == 0;
                b: do {
                    if (la) {
                        ja = (fa + 116) | 0;
                        ia = c[ja >> 2] | 0;
                        if ((ia | 0) == 0) {
                            na = (La + -8) | 0;
                            c[Ba >> 2] = na;
                            if ((na | 0) >= 1) {
                                Ma = 57;
                                break;
                            }
                            c[Ba >> 2] = 0;
                            break;
                        }
                        na = a[(ga + 5) >> 0] | 0;
                        oa = na & 255;
                        ua = d[(ga + 6) >> 0] | 0;
                        do {
                            if ((na << 24) >> 24 < 0) {
                                if ((ia | 0) > 2) {
                                    sa = (La + -1) | 0;
                                    wa = (sa - (sa >> 8)) | 0;
                                    sa = ua & 31;
                                    c[(fa + 124) >> 2] = wa;
                                    if (((c[(1072 + (sa << 2)) >> 2] & c[c[(e + (sa << 2) + 1428) >> 2] >> 2]) | 0) != 0) {
                                        Ma = 57;
                                        break b;
                                    }
                                    c[Ba >> 2] = wa;
                                    Ma = 57;
                                    break b;
                                }
                                if ((ia | 0) == 2) {
                                    wa = (La + -1) | 0;
                                    Na = (wa - (wa >> 8)) | 0;
                                    Oa = ua;
                                    Pa = ((oa >>> 3) & 14) | 16;
                                    break;
                                } else {
                                    wa = ((oa << 1) & 30) | 1;
                                    Na = (((wa | 0) != 31 ? 32 : 1024) + La) | 0;
                                    Oa = ua;
                                    Pa = wa;
                                    break;
                                }
                            } else {
                                wa = a[(ga + 7) >> 0] | 0;
                                sa = wa & 255;
                                ka = sa >>> 5;
                                if ((wa << 24) >> 24 > -1) {
                                    Na = sa << 4;
                                    Oa = sa;
                                    Pa = 31;
                                    break;
                                }
                                ta = sa & 31;
                                if ((ka | 0) == 4) {
                                    Na = (La + -32) | 0;
                                    Oa = sa;
                                    Pa = ta;
                                    break;
                                }
                                if ((wa & 255) < 192) {
                                    wa = (La + -1) | 0;
                                    Na = (wa - (wa >> 8)) | 0;
                                    Oa = sa;
                                    Pa = ta;
                                    break;
                                }
                                wa = (La + 32) | 0;
                                if ((ka | 0) == 7) {
                                    Na = (c[(fa + 124) >> 2] | 0) >>> 0 > 1535 ? (La + 8) | 0 : wa;
                                    Oa = sa;
                                    Pa = ta;
                                } else {
                                    Na = wa;
                                    Oa = sa;
                                    Pa = ta;
                                }
                            }
                        } while (0);
                        if ((((Na >> 8) | 0) == ((Oa >>> 5) | 0)) & ((ia | 0) == 2)) {
                            c[ja >> 2] = 3;
                            Qa = 3;
                        } else {
                            Qa = ia;
                        }
                        c[(fa + 124) >> 2] = Na;
                        if (Na >>> 0 > 2047) {
                            ua = (((Na >> 31) & -2047) + 2047) | 0;
                            if ((Qa | 0) == 1) {
                                c[ja >> 2] = 2;
                                Ra = ua;
                            } else {
                                Ra = ua;
                            }
                        } else {
                            Ra = Na;
                        }
                        if (((c[(1072 + (Pa << 2)) >> 2] & c[c[(e + (Pa << 2) + 1428) >> 2] >> 2]) | 0) == 0) {
                            c[Ba >> 2] = Ra;
                            Ma = 57;
                        } else {
                            Ma = 57;
                        }
                    } else {
                        Ma = 57;
                    }
                } while (0);
                if ((Ma | 0) == 57 ? ((Ma = 0), (ua = (fa + 100) | 0), (oa = c[ua >> 2] | 0), (na = ((oa & 16383) + Ja) | 0), (c[ua >> 2] = (na | 0) > 32767 ? 32767 : na), (oa | 0) > 16383) : 0) {
                    oa = c[f >> 2] | 0;
                    na = (fa + 108) | 0;
                    ua = c[na >> 2] | 0;
                    ta = (ua + oa) | 0;
                    sa = (d[(j + (ta & 65535)) >> 0] << 8) | d[(j + ((ta + 1) & 65535)) >> 0];
                    ta = (ua + 2) | 0;
                    if ((ta | 0) > 8) {
                        if ((ta | 0) != 9) {
                            Ma = 60;
                            break a;
                        }
                        if (((Da & 1) | 0) != 0) {
                            ua = (((d[(ga + 4) >> 0] << 2) | 2) + h) | 0;
                            wa = (d[(j + (ua | 1)) >> 0] << 8) | d[(j + ua) >> 0];
                            if (la) {
                                a[y >> 0] = d[y >> 0] | ha;
                                Sa = wa;
                            } else {
                                Sa = wa;
                            }
                        } else {
                            Sa = (oa + 9) & 65535;
                        }
                        c[f >> 2] = Sa;
                        Ta = 1;
                    } else {
                        Ta = ta;
                    }
                    c[na >> 2] = Ta;
                    na = Da >> 4;
                    ta = d[(2264 + na) >> 0] | 0;
                    oa = d[(na + 2280) >> 0] | 0;
                    na = (fa + 96) | 0;
                    wa = c[na >> 2] | 0;
                    ua = (wa + 16) | 0;
                    ka = Da & 12;
                    xa = (ka | 0) == 8;
                    if (!(ka >>> 0 > 7)) {
                        if ((ka | 0) == 0) {
                            ka = sa;
                            va = wa;
                            while (1) {
                                pa = (((ka << 16) >> 16) >> ta) << oa;
                                if ((((pa << 16) >> 16) | 0) == (pa | 0)) {
                                    Ua = pa;
                                } else {
                                    Ua = (pa >> 31) ^ 32767;
                                }
                                pa = (Ua << 17) >> 16;
                                c[va >> 2] = pa;
                                c[(va + 48) >> 2] = pa;
                                pa = (va + 4) | 0;
                                if (pa >>> 0 < ua >>> 0) {
                                    ka = ka << 4;
                                    va = pa;
                                } else {
                                    Va = pa;
                                    break;
                                }
                            }
                        } else {
                            va = sa;
                            ka = wa;
                            while (1) {
                                f = c[(ka + 44) >> 2] | 0;
                                la = ((f >> 1) + ((((va << 16) >> 16) >> ta) << oa) + ((0 - f) >> 5)) | 0;
                                if ((((la << 16) >> 16) | 0) == (la | 0)) {
                                    Wa = la;
                                } else {
                                    Wa = (la >> 31) ^ 32767;
                                }
                                la = (Wa << 17) >> 16;
                                c[ka >> 2] = la;
                                c[(ka + 48) >> 2] = la;
                                la = (ka + 4) | 0;
                                if (la >>> 0 < ua >>> 0) {
                                    va = va << 4;
                                    ka = la;
                                } else {
                                    Va = la;
                                    break;
                                }
                            }
                        }
                    } else {
                        ka = sa;
                        va = wa;
                        while (1) {
                            la = c[(va + 44) >> 2] | 0;
                            f = c[(va + 40) >> 2] | 0;
                            pa = f >> 1;
                            qa = (la + ((((ka << 16) >> 16) >> ta) << oa) - pa) | 0;
                            if (xa) {
                                Xa = (((_(la, -3) | 0) >> 6) + (f >> 5) + qa) | 0;
                            } else {
                                Xa = (qa + ((_(la, -13) | 0) >> 7) + ((pa * 3) >> 4)) | 0;
                            }
                            if ((((Xa << 16) >> 16) | 0) == (Xa | 0)) {
                                Ya = Xa;
                            } else {
                                Ya = (Xa >> 31) ^ 32767;
                            }
                            pa = (Ya << 17) >> 16;
                            c[va >> 2] = pa;
                            c[(va + 48) >> 2] = pa;
                            pa = (va + 4) | 0;
                            if (pa >>> 0 < ua >>> 0) {
                                ka = ka << 4;
                                va = pa;
                            } else {
                                Va = pa;
                                break;
                            }
                        }
                    }
                    c[na >> 2] = Va >>> 0 < ((fa + 48) | 0) >>> 0 ? Va : fa;
                }
                va = ha << 1;
                if ((va | 0) >= 256) {
                    break;
                }
                aa = Ea;
                ba = Fa;
                ca = Ga;
                da = Ha;
                ea = Ia;
                fa = (fa + 140) | 0;
                ga = (ga + 16) | 0;
                ha = va;
            }
            va = c[C >> 2] | 0;
            ka = ((d[D >> 0] << 8) + va) & 65535;
            ua = (j + ka) | 0;
            if ((va | 0) == 0) {
                xa = (d[E >> 0] << 11) & 30720;
                c[F >> 2] = xa;
                Za = xa;
            } else {
                Za = c[F >> 2] | 0;
            }
            xa = (va + 4) | 0;
            c[C >> 2] = (xa | 0) >= (Za | 0) ? 0 : xa;
            xa = (j + (ka + 1)) | 0;
            va = (((d[xa >> 0] << 8) | d[ua >> 0]) << 16) >> 16;
            oa = (j + (ka + 2)) | 0;
            ta = (j + (ka + 3)) | 0;
            ka = (((d[ta >> 0] << 8) | d[oa >> 0]) << 16) >> 16;
            wa = ((c[G >> 2] | 0) + 8) | 0;
            sa = wa >>> 0 < H >>> 0 ? wa : I;
            c[G >> 2] = sa;
            c[(sa + 64) >> 2] = va;
            c[sa >> 2] = va;
            c[(sa + 68) >> 2] = ka;
            c[(sa + 4) >> 2] = ka;
            wa = a[J >> 0] | 0;
            pa = _(wa, va) | 0;
            va = _(ka, wa) | 0;
            wa = a[K >> 0] | 0;
            ka = ((_(wa, c[(sa + 8) >> 2] | 0) | 0) + pa) | 0;
            pa = ((_(c[(sa + 12) >> 2] | 0, wa) | 0) + va) | 0;
            va = a[L >> 0] | 0;
            wa = (ka + (_(va, c[(sa + 16) >> 2] | 0) | 0)) | 0;
            ka = (pa + (_(c[(sa + 20) >> 2] | 0, va) | 0)) | 0;
            va = a[M >> 0] | 0;
            pa = (wa + (_(va, c[(sa + 24) >> 2] | 0) | 0)) | 0;
            wa = (ka + (_(c[(sa + 28) >> 2] | 0, va) | 0)) | 0;
            va = a[N >> 0] | 0;
            ka = (pa + (_(va, c[(sa + 32) >> 2] | 0) | 0)) | 0;
            pa = (wa + (_(c[(sa + 36) >> 2] | 0, va) | 0)) | 0;
            va = a[O >> 0] | 0;
            wa = (ka + (_(va, c[(sa + 40) >> 2] | 0) | 0)) | 0;
            ka = (pa + (_(c[(sa + 44) >> 2] | 0, va) | 0)) | 0;
            va = a[P >> 0] | 0;
            pa = (wa + (_(va, c[(sa + 48) >> 2] | 0) | 0)) | 0;
            wa = (ka + (_(c[(sa + 52) >> 2] | 0, va) | 0)) | 0;
            va = a[Q >> 0] | 0;
            ka = (pa + (_(va, c[(sa + 56) >> 2] | 0) | 0)) | 0;
            pa = (wa + (_(c[(sa + 60) >> 2] | 0, va) | 0)) | 0;
            if ((a[n >> 0] & 32) == 0) {
                va = a[R >> 0] | 0;
                sa = (((_(va, ka) | 0) >> 14) + (Ea >> 7)) | 0;
                wa = (((_(va, pa) | 0) >> 14) + (Fa >> 7)) | 0;
                if ((((sa << 16) >> 16) | 0) == (sa | 0)) {
                    _a = sa;
                } else {
                    _a = (sa >> 31) ^ 32767;
                }
                if ((((wa << 16) >> 16) | 0) == (wa | 0)) {
                    $a = wa;
                } else {
                    $a = (wa >> 31) ^ 32767;
                }
                a[xa >> 0] = _a >>> 8;
                a[ua >> 0] = _a;
                a[ta >> 0] = $a >>> 8;
                a[oa >> 0] = $a;
            }
            oa = _(Ga, s) | 0;
            ta = ((_(a[S >> 0] | 0, ka) | 0) + oa) | 0;
            oa = ta >> 14;
            ka = _(Ha, q) | 0;
            ua = ((_(a[T >> 0] | 0, pa) | 0) + ka) | 0;
            ka = ua >> 14;
            if ((((oa << 16) >> 16) | 0) == (oa | 0)) {
                ab = oa;
            } else {
                ab = (ta >> 31) ^ 32767;
            }
            if ((((ka << 16) >> 16) | 0) == (ka | 0)) {
                bb = ka;
            } else {
                bb = (ua >> 31) ^ 32767;
            }
            ua = (a[n >> 0] & 64) == 0;
            ka = c[U >> 2] | 0;
            b[ka >> 1] = ua ? ab & 65535 : 0;
            b[(ka + 2) >> 1] = ua ? bb & 65535 : 0;
            ua = (ka + 4) | 0;
            if (ua >>> 0 < (c[V >> 2] | 0) >>> 0) {
                cb = ua;
            } else {
                c[V >> 2] = X;
                cb = W;
            }
            c[U >> 2] = cb;
            $ = ($ + -1) | 0;
            if (($ | 0) == 0) {
                Ma = 98;
                break;
            }
        }
        if ((Ma | 0) == 60) {
            ra(2224, 1032, 471, 2256);
        } else if ((Ma | 0) == 98) {
            i = g;
            return;
        }
    }
    function jb(b, d) {
        b = b | 0;
        d = d | 0;
        var e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0;
        e = i;
        i = (i + 16) | 0;
        f = e;
        c[(b + 1556) >> 2] = d;
        c[(b + 1560) >> 2] = 0;
        d = (b + 1564) | 0;
        g = 0;
        do {
            c[(b + ((g * 140) | 0) + 444) >> 2] = -1;
            h = g << 4;
            j = a[(b + h) >> 0] | 0;
            k = a[(b + (h | 1)) >> 0] | 0;
            h = _(k, j) | 0;
            if ((h | 0) < (c[d >> 2] | 0)) {
                l = (j >> 7) ^ j;
                m = (k >> 7) ^ k;
            } else {
                l = j;
                m = k;
            }
            c[(b + ((g * 140) | 0) + 436) >> 2] = l;
            c[(b + ((g * 140) | 0) + 440) >> 2] = m;
            g = (g + 1) | 0;
        } while ((g | 0) != 8);
        c[d >> 2] = -16384;
        d = (b + 1580) | 0;
        c[(b + 1576) >> 2] = d;
        c[(b + 1568) >> 2] = d;
        c[(b + 1572) >> 2] = b + 1612;
        lb(b, 2328);
        c[f >> 2] = 1;
        if ((a[f >> 0] | 0) == 0) {
            ra(2456, 2488, 63, 2520);
        } else {
            i = e;
            return;
        }
    }
    function kb(a) {
        a = a | 0;
        var b = 0;
        b = i;
        lb(a, 2328);
        i = b;
        return;
    }
    function lb(b, e) {
        b = b | 0;
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0;
        f = i;
        g = (b + 0) | 0;
        h = (e + 0) | 0;
        e = (g + 128) | 0;
        do {
            a[g >> 0] = a[h >> 0] | 0;
            g = (g + 1) | 0;
            h = (h + 1) | 0;
        } while ((g | 0) < (e | 0));
        ub((b + 128) | 0, 0, 1428) | 0;
        c[(b + 1396) >> 2] = 1;
        c[(b + 1384) >> 2] = b + 1288;
        c[(b + 1256) >> 2] = 1;
        c[(b + 1244) >> 2] = b + 1148;
        c[(b + 1116) >> 2] = 1;
        c[(b + 1104) >> 2] = b + 1008;
        c[(b + 976) >> 2] = 1;
        c[(b + 964) >> 2] = b + 868;
        c[(b + 836) >> 2] = 1;
        c[(b + 824) >> 2] = b + 728;
        c[(b + 696) >> 2] = 1;
        c[(b + 684) >> 2] = b + 588;
        c[(b + 556) >> 2] = 1;
        c[(b + 544) >> 2] = b + 448;
        c[(b + 416) >> 2] = 1;
        c[(b + 404) >> 2] = b + 308;
        c[(b + 300) >> 2] = d[(b + 76) >> 0];
        h = c[(b + 1560) >> 2] | 0;
        g = (b + 1564) | 0;
        e = 0;
        do {
            j = (((h >>> e) & 1) + -1) | 0;
            c[(b + ((e * 140) | 0) + 444) >> 2] = j;
            k = e << 4;
            l = a[(b + k) >> 0] | 0;
            m = a[(b + (k | 1)) >> 0] | 0;
            k = _(m, l) | 0;
            if ((k | 0) < (c[g >> 2] | 0)) {
                n = (l >> 7) ^ l;
                o = (m >> 7) ^ m;
            } else {
                n = l;
                o = m;
            }
            c[(b + ((e * 140) | 0) + 436) >> 2] = n & j;
            c[(b + ((e * 140) | 0) + 440) >> 2] = o & j;
            e = (e + 1) | 0;
        } while ((e | 0) != 8);
        if ((c[(b + 1556) >> 2] | 0) == 0) {
            ra(2296, 1032, 667, 2304);
        }
        c[(b + 268) >> 2] = 16384;
        c[(b + 256) >> 2] = b + 128;
        c[(b + 260) >> 2] = 1;
        c[(b + 272) >> 2] = 0;
        c[(b + 280) >> 2] = 0;
        e = (b + 284) | 0;
        c[e >> 2] = 1;
        c[(b + 288) >> 2] = 0;
        o = (b + 292) | 0;
        c[o >> 2] = -32;
        c[(b + 296) >> 2] = 11;
        n = 1;
        g = 2;
        while (1) {
            c[(b + (n << 2) + 1428) >> 2] = b + (g << 2) + 284;
            h = (g + -1) | 0;
            n = (n + 1) | 0;
            if ((n | 0) == 32) {
                break;
            } else {
                g = (h | 0) != 0 ? h : 3;
            }
        }
        c[(b + 1428) >> 2] = e;
        c[(b + 1548) >> 2] = o;
        i = f;
        return;
    }
    function mb(a) {
        a = a | 0;
        var b = 0,
            d = 0;
        b = i;
        d = (a + 8) | 0;
        c[(d + 0) >> 2] = 0;
        c[(d + 4) >> 2] = 0;
        c[(d + 8) >> 2] = 0;
        c[(d + 12) >> 2] = 0;
        c[(d + 16) >> 2] = 0;
        c[(d + 20) >> 2] = 0;
        i = b;
        return;
    }
    function nb(a) {
        a = a | 0;
        var b = 0,
            d = 0;
        b = i;
        c[a >> 2] = 256;
        c[(a + 4) >> 2] = 8;
        d = (a + 8) | 0;
        c[(d + 0) >> 2] = 0;
        c[(d + 4) >> 2] = 0;
        c[(d + 8) >> 2] = 0;
        c[(d + 12) >> 2] = 0;
        c[(d + 16) >> 2] = 0;
        c[(d + 20) >> 2] = 0;
        i = b;
        return;
    }
    function ob(a, d, e) {
        a = a | 0;
        d = d | 0;
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0;
        f = i;
        if (((e & 1) | 0) != 0) {
            ra(2552, 2576, 31, 2608);
        }
        g = c[a >> 2] | 0;
        h = c[(a + 4) >> 2] | 0;
        if ((e | 0) <= 0) {
            i = f;
            return;
        }
        j = (a + 28) | 0;
        k = (a + 24) | 0;
        l = (a + 20) | 0;
        m = 0;
        n = c[l >> 2] | 0;
        o = c[k >> 2] | 0;
        p = c[j >> 2] | 0;
        do {
            q = (d + (m << 1)) | 0;
            r = b[q >> 1] | 0;
            s = o;
            o = (r + n) | 0;
            n = (r * 3) | 0;
            r = p >> 10;
            t = p;
            p = (p - (p >> h) + (_((o - s) | 0, g) | 0)) | 0;
            if ((((r << 16) >> 16) | 0) == (r | 0)) {
                u = r;
            } else {
                u = (t >> 31) ^ 32767;
            }
            b[q >> 1] = u;
            m = (m + 2) | 0;
        } while ((m | 0) < (e | 0));
        c[l >> 2] = n;
        c[k >> 2] = o;
        c[j >> 2] = p;
        p = (a + 16) | 0;
        j = (a + 12) | 0;
        o = (a + 8) | 0;
        a = 0;
        k = c[o >> 2] | 0;
        n = c[j >> 2] | 0;
        l = c[p >> 2] | 0;
        do {
            m = (d + ((a | 1) << 1)) | 0;
            u = b[m >> 1] | 0;
            q = n;
            n = (u + k) | 0;
            k = (u * 3) | 0;
            u = l >> 10;
            t = l;
            l = (l - (l >> h) + (_((n - q) | 0, g) | 0)) | 0;
            if ((((u << 16) >> 16) | 0) == (u | 0)) {
                v = u;
            } else {
                v = (t >> 31) ^ 32767;
            }
            b[m >> 1] = v;
            a = (a + 2) | 0;
        } while ((a | 0) < (e | 0));
        c[o >> 2] = k;
        c[j >> 2] = n;
        c[p >> 2] = l;
        i = f;
        return;
    }
    function pb(a) {
        a = a | 0;
        var b = 0,
            d = 0,
            e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0,
            w = 0,
            x = 0,
            y = 0,
            z = 0,
            A = 0,
            B = 0,
            C = 0,
            D = 0,
            E = 0,
            F = 0,
            G = 0,
            H = 0,
            I = 0,
            J = 0,
            K = 0,
            L = 0,
            M = 0,
            N = 0,
            O = 0,
            P = 0,
            Q = 0,
            R = 0,
            S = 0,
            T = 0,
            U = 0,
            V = 0,
            W = 0,
            X = 0,
            Y = 0,
            Z = 0,
            _ = 0,
            $ = 0,
            aa = 0,
            ba = 0,
            ca = 0,
            da = 0,
            ea = 0,
            fa = 0,
            ha = 0,
            ia = 0,
            ja = 0,
            ka = 0,
            ma = 0,
            na = 0,
            pa = 0,
            qa = 0,
            ra = 0,
            sa = 0,
            ta = 0,
            ua = 0,
            wa = 0,
            ya = 0,
            za = 0,
            Aa = 0,
            Ba = 0,
            Ca = 0,
            Da = 0,
            Ea = 0,
            Fa = 0,
            Ga = 0,
            Ha = 0,
            Ia = 0,
            Ja = 0,
            Ka = 0,
            La = 0,
            Ma = 0,
            Na = 0,
            Oa = 0;
        b = i;
        do {
            if (a >>> 0 < 245) {
                if (a >>> 0 < 11) {
                    d = 16;
                } else {
                    d = (a + 11) & -8;
                }
                e = d >>> 3;
                f = c[654] | 0;
                g = f >>> e;
                if (((g & 3) | 0) != 0) {
                    h = (((g & 1) ^ 1) + e) | 0;
                    j = h << 1;
                    k = (2656 + (j << 2)) | 0;
                    l = (2656 + ((j + 2) << 2)) | 0;
                    j = c[l >> 2] | 0;
                    m = (j + 8) | 0;
                    n = c[m >> 2] | 0;
                    do {
                        if ((k | 0) != (n | 0)) {
                            if (n >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            }
                            o = (n + 12) | 0;
                            if ((c[o >> 2] | 0) == (j | 0)) {
                                c[o >> 2] = k;
                                c[l >> 2] = n;
                                break;
                            } else {
                                la();
                            }
                        } else {
                            c[654] = f & ~(1 << h);
                        }
                    } while (0);
                    n = h << 3;
                    c[(j + 4) >> 2] = n | 3;
                    l = (j + (n | 4)) | 0;
                    c[l >> 2] = c[l >> 2] | 1;
                    p = m;
                    i = b;
                    return p | 0;
                }
                if (d >>> 0 > (c[656] | 0) >>> 0) {
                    if ((g | 0) != 0) {
                        l = 2 << e;
                        n = (g << e) & (l | (0 - l));
                        l = ((n & (0 - n)) + -1) | 0;
                        n = (l >>> 12) & 16;
                        k = l >>> n;
                        l = (k >>> 5) & 8;
                        o = k >>> l;
                        k = (o >>> 2) & 4;
                        q = o >>> k;
                        o = (q >>> 1) & 2;
                        r = q >>> o;
                        q = (r >>> 1) & 1;
                        s = ((l | n | k | o | q) + (r >>> q)) | 0;
                        q = s << 1;
                        r = (2656 + (q << 2)) | 0;
                        o = (2656 + ((q + 2) << 2)) | 0;
                        q = c[o >> 2] | 0;
                        k = (q + 8) | 0;
                        n = c[k >> 2] | 0;
                        do {
                            if ((r | 0) != (n | 0)) {
                                if (n >>> 0 < (c[658] | 0) >>> 0) {
                                    la();
                                }
                                l = (n + 12) | 0;
                                if ((c[l >> 2] | 0) == (q | 0)) {
                                    c[l >> 2] = r;
                                    c[o >> 2] = n;
                                    break;
                                } else {
                                    la();
                                }
                            } else {
                                c[654] = f & ~(1 << s);
                            }
                        } while (0);
                        f = s << 3;
                        n = (f - d) | 0;
                        c[(q + 4) >> 2] = d | 3;
                        o = (q + d) | 0;
                        c[(q + (d | 4)) >> 2] = n | 1;
                        c[(q + f) >> 2] = n;
                        f = c[656] | 0;
                        if ((f | 0) != 0) {
                            r = c[659] | 0;
                            e = f >>> 3;
                            f = e << 1;
                            g = (2656 + (f << 2)) | 0;
                            m = c[654] | 0;
                            j = 1 << e;
                            if (((m & j) | 0) != 0) {
                                e = (2656 + ((f + 2) << 2)) | 0;
                                h = c[e >> 2] | 0;
                                if (h >>> 0 < (c[658] | 0) >>> 0) {
                                    la();
                                } else {
                                    t = e;
                                    u = h;
                                }
                            } else {
                                c[654] = m | j;
                                t = (2656 + ((f + 2) << 2)) | 0;
                                u = g;
                            }
                            c[t >> 2] = r;
                            c[(u + 12) >> 2] = r;
                            c[(r + 8) >> 2] = u;
                            c[(r + 12) >> 2] = g;
                        }
                        c[656] = n;
                        c[659] = o;
                        p = k;
                        i = b;
                        return p | 0;
                    }
                    o = c[655] | 0;
                    if ((o | 0) != 0) {
                        n = ((o & (0 - o)) + -1) | 0;
                        o = (n >>> 12) & 16;
                        g = n >>> o;
                        n = (g >>> 5) & 8;
                        r = g >>> n;
                        g = (r >>> 2) & 4;
                        f = r >>> g;
                        r = (f >>> 1) & 2;
                        j = f >>> r;
                        f = (j >>> 1) & 1;
                        m = c[(2920 + (((n | o | g | r | f) + (j >>> f)) << 2)) >> 2] | 0;
                        f = ((c[(m + 4) >> 2] & -8) - d) | 0;
                        j = m;
                        r = m;
                        while (1) {
                            m = c[(j + 16) >> 2] | 0;
                            if ((m | 0) == 0) {
                                g = c[(j + 20) >> 2] | 0;
                                if ((g | 0) == 0) {
                                    break;
                                } else {
                                    v = g;
                                }
                            } else {
                                v = m;
                            }
                            m = ((c[(v + 4) >> 2] & -8) - d) | 0;
                            g = m >>> 0 < f >>> 0;
                            f = g ? m : f;
                            j = v;
                            r = g ? v : r;
                        }
                        j = c[658] | 0;
                        if (r >>> 0 < j >>> 0) {
                            la();
                        }
                        k = (r + d) | 0;
                        if (!(r >>> 0 < k >>> 0)) {
                            la();
                        }
                        q = c[(r + 24) >> 2] | 0;
                        s = c[(r + 12) >> 2] | 0;
                        do {
                            if ((s | 0) == (r | 0)) {
                                g = (r + 20) | 0;
                                m = c[g >> 2] | 0;
                                if ((m | 0) == 0) {
                                    o = (r + 16) | 0;
                                    n = c[o >> 2] | 0;
                                    if ((n | 0) == 0) {
                                        w = 0;
                                        break;
                                    } else {
                                        x = n;
                                        y = o;
                                    }
                                } else {
                                    x = m;
                                    y = g;
                                }
                                while (1) {
                                    g = (x + 20) | 0;
                                    m = c[g >> 2] | 0;
                                    if ((m | 0) != 0) {
                                        x = m;
                                        y = g;
                                        continue;
                                    }
                                    g = (x + 16) | 0;
                                    m = c[g >> 2] | 0;
                                    if ((m | 0) == 0) {
                                        break;
                                    } else {
                                        x = m;
                                        y = g;
                                    }
                                }
                                if (y >>> 0 < j >>> 0) {
                                    la();
                                } else {
                                    c[y >> 2] = 0;
                                    w = x;
                                    break;
                                }
                            } else {
                                g = c[(r + 8) >> 2] | 0;
                                if (g >>> 0 < j >>> 0) {
                                    la();
                                }
                                m = (g + 12) | 0;
                                if ((c[m >> 2] | 0) != (r | 0)) {
                                    la();
                                }
                                o = (s + 8) | 0;
                                if ((c[o >> 2] | 0) == (r | 0)) {
                                    c[m >> 2] = s;
                                    c[o >> 2] = g;
                                    w = s;
                                    break;
                                } else {
                                    la();
                                }
                            }
                        } while (0);
                        do {
                            if ((q | 0) != 0) {
                                s = c[(r + 28) >> 2] | 0;
                                j = (2920 + (s << 2)) | 0;
                                if ((r | 0) == (c[j >> 2] | 0)) {
                                    c[j >> 2] = w;
                                    if ((w | 0) == 0) {
                                        c[655] = c[655] & ~(1 << s);
                                        break;
                                    }
                                } else {
                                    if (q >>> 0 < (c[658] | 0) >>> 0) {
                                        la();
                                    }
                                    s = (q + 16) | 0;
                                    if ((c[s >> 2] | 0) == (r | 0)) {
                                        c[s >> 2] = w;
                                    } else {
                                        c[(q + 20) >> 2] = w;
                                    }
                                    if ((w | 0) == 0) {
                                        break;
                                    }
                                }
                                if (w >>> 0 < (c[658] | 0) >>> 0) {
                                    la();
                                }
                                c[(w + 24) >> 2] = q;
                                s = c[(r + 16) >> 2] | 0;
                                do {
                                    if ((s | 0) != 0) {
                                        if (s >>> 0 < (c[658] | 0) >>> 0) {
                                            la();
                                        } else {
                                            c[(w + 16) >> 2] = s;
                                            c[(s + 24) >> 2] = w;
                                            break;
                                        }
                                    }
                                } while (0);
                                s = c[(r + 20) >> 2] | 0;
                                if ((s | 0) != 0) {
                                    if (s >>> 0 < (c[658] | 0) >>> 0) {
                                        la();
                                    } else {
                                        c[(w + 20) >> 2] = s;
                                        c[(s + 24) >> 2] = w;
                                        break;
                                    }
                                }
                            }
                        } while (0);
                        if (f >>> 0 < 16) {
                            q = (f + d) | 0;
                            c[(r + 4) >> 2] = q | 3;
                            s = (r + (q + 4)) | 0;
                            c[s >> 2] = c[s >> 2] | 1;
                        } else {
                            c[(r + 4) >> 2] = d | 3;
                            c[(r + (d | 4)) >> 2] = f | 1;
                            c[(r + (f + d)) >> 2] = f;
                            s = c[656] | 0;
                            if ((s | 0) != 0) {
                                q = c[659] | 0;
                                j = s >>> 3;
                                s = j << 1;
                                g = (2656 + (s << 2)) | 0;
                                o = c[654] | 0;
                                m = 1 << j;
                                if (((o & m) | 0) != 0) {
                                    j = (2656 + ((s + 2) << 2)) | 0;
                                    n = c[j >> 2] | 0;
                                    if (n >>> 0 < (c[658] | 0) >>> 0) {
                                        la();
                                    } else {
                                        z = j;
                                        A = n;
                                    }
                                } else {
                                    c[654] = o | m;
                                    z = (2656 + ((s + 2) << 2)) | 0;
                                    A = g;
                                }
                                c[z >> 2] = q;
                                c[(A + 12) >> 2] = q;
                                c[(q + 8) >> 2] = A;
                                c[(q + 12) >> 2] = g;
                            }
                            c[656] = f;
                            c[659] = k;
                        }
                        p = (r + 8) | 0;
                        i = b;
                        return p | 0;
                    } else {
                        B = d;
                    }
                } else {
                    B = d;
                }
            } else {
                if (!(a >>> 0 > 4294967231)) {
                    g = (a + 11) | 0;
                    q = g & -8;
                    s = c[655] | 0;
                    if ((s | 0) != 0) {
                        m = (0 - q) | 0;
                        o = g >>> 8;
                        if ((o | 0) != 0) {
                            if (q >>> 0 > 16777215) {
                                C = 31;
                            } else {
                                g = (((o + 1048320) | 0) >>> 16) & 8;
                                n = o << g;
                                o = (((n + 520192) | 0) >>> 16) & 4;
                                j = n << o;
                                n = (((j + 245760) | 0) >>> 16) & 2;
                                h = (14 - (o | g | n) + ((j << n) >>> 15)) | 0;
                                C = ((q >>> ((h + 7) | 0)) & 1) | (h << 1);
                            }
                        } else {
                            C = 0;
                        }
                        h = c[(2920 + (C << 2)) >> 2] | 0;
                        a: do {
                            if ((h | 0) == 0) {
                                D = m;
                                E = 0;
                                F = 0;
                            } else {
                                if ((C | 0) == 31) {
                                    G = 0;
                                } else {
                                    G = (25 - (C >>> 1)) | 0;
                                }
                                n = m;
                                j = 0;
                                g = q << G;
                                o = h;
                                e = 0;
                                while (1) {
                                    l = c[(o + 4) >> 2] & -8;
                                    H = (l - q) | 0;
                                    if (H >>> 0 < n >>> 0) {
                                        if ((l | 0) == (q | 0)) {
                                            D = H;
                                            E = o;
                                            F = o;
                                            break a;
                                        } else {
                                            I = H;
                                            J = o;
                                        }
                                    } else {
                                        I = n;
                                        J = e;
                                    }
                                    H = c[(o + 20) >> 2] | 0;
                                    o = c[(o + ((g >>> 31) << 2) + 16) >> 2] | 0;
                                    l = ((H | 0) == 0) | ((H | 0) == (o | 0)) ? j : H;
                                    if ((o | 0) == 0) {
                                        D = I;
                                        E = l;
                                        F = J;
                                        break;
                                    } else {
                                        n = I;
                                        j = l;
                                        g = g << 1;
                                        e = J;
                                    }
                                }
                            }
                        } while (0);
                        if (((E | 0) == 0) & ((F | 0) == 0)) {
                            h = 2 << C;
                            m = s & (h | (0 - h));
                            if ((m | 0) == 0) {
                                B = q;
                                break;
                            }
                            h = ((m & (0 - m)) + -1) | 0;
                            m = (h >>> 12) & 16;
                            r = h >>> m;
                            h = (r >>> 5) & 8;
                            k = r >>> h;
                            r = (k >>> 2) & 4;
                            f = k >>> r;
                            k = (f >>> 1) & 2;
                            e = f >>> k;
                            f = (e >>> 1) & 1;
                            K = c[(2920 + (((h | m | r | k | f) + (e >>> f)) << 2)) >> 2] | 0;
                        } else {
                            K = E;
                        }
                        if ((K | 0) == 0) {
                            L = D;
                            M = F;
                        } else {
                            f = D;
                            e = K;
                            k = F;
                            while (1) {
                                r = ((c[(e + 4) >> 2] & -8) - q) | 0;
                                m = r >>> 0 < f >>> 0;
                                h = m ? r : f;
                                r = m ? e : k;
                                m = c[(e + 16) >> 2] | 0;
                                if ((m | 0) != 0) {
                                    f = h;
                                    e = m;
                                    k = r;
                                    continue;
                                }
                                e = c[(e + 20) >> 2] | 0;
                                if ((e | 0) == 0) {
                                    L = h;
                                    M = r;
                                    break;
                                } else {
                                    f = h;
                                    k = r;
                                }
                            }
                        }
                        if ((M | 0) != 0 ? L >>> 0 < (((c[656] | 0) - q) | 0) >>> 0 : 0) {
                            k = c[658] | 0;
                            if (M >>> 0 < k >>> 0) {
                                la();
                            }
                            f = (M + q) | 0;
                            if (!(M >>> 0 < f >>> 0)) {
                                la();
                            }
                            e = c[(M + 24) >> 2] | 0;
                            s = c[(M + 12) >> 2] | 0;
                            do {
                                if ((s | 0) == (M | 0)) {
                                    r = (M + 20) | 0;
                                    h = c[r >> 2] | 0;
                                    if ((h | 0) == 0) {
                                        m = (M + 16) | 0;
                                        g = c[m >> 2] | 0;
                                        if ((g | 0) == 0) {
                                            N = 0;
                                            break;
                                        } else {
                                            O = g;
                                            P = m;
                                        }
                                    } else {
                                        O = h;
                                        P = r;
                                    }
                                    while (1) {
                                        r = (O + 20) | 0;
                                        h = c[r >> 2] | 0;
                                        if ((h | 0) != 0) {
                                            O = h;
                                            P = r;
                                            continue;
                                        }
                                        r = (O + 16) | 0;
                                        h = c[r >> 2] | 0;
                                        if ((h | 0) == 0) {
                                            break;
                                        } else {
                                            O = h;
                                            P = r;
                                        }
                                    }
                                    if (P >>> 0 < k >>> 0) {
                                        la();
                                    } else {
                                        c[P >> 2] = 0;
                                        N = O;
                                        break;
                                    }
                                } else {
                                    r = c[(M + 8) >> 2] | 0;
                                    if (r >>> 0 < k >>> 0) {
                                        la();
                                    }
                                    h = (r + 12) | 0;
                                    if ((c[h >> 2] | 0) != (M | 0)) {
                                        la();
                                    }
                                    m = (s + 8) | 0;
                                    if ((c[m >> 2] | 0) == (M | 0)) {
                                        c[h >> 2] = s;
                                        c[m >> 2] = r;
                                        N = s;
                                        break;
                                    } else {
                                        la();
                                    }
                                }
                            } while (0);
                            do {
                                if ((e | 0) != 0) {
                                    s = c[(M + 28) >> 2] | 0;
                                    k = (2920 + (s << 2)) | 0;
                                    if ((M | 0) == (c[k >> 2] | 0)) {
                                        c[k >> 2] = N;
                                        if ((N | 0) == 0) {
                                            c[655] = c[655] & ~(1 << s);
                                            break;
                                        }
                                    } else {
                                        if (e >>> 0 < (c[658] | 0) >>> 0) {
                                            la();
                                        }
                                        s = (e + 16) | 0;
                                        if ((c[s >> 2] | 0) == (M | 0)) {
                                            c[s >> 2] = N;
                                        } else {
                                            c[(e + 20) >> 2] = N;
                                        }
                                        if ((N | 0) == 0) {
                                            break;
                                        }
                                    }
                                    if (N >>> 0 < (c[658] | 0) >>> 0) {
                                        la();
                                    }
                                    c[(N + 24) >> 2] = e;
                                    s = c[(M + 16) >> 2] | 0;
                                    do {
                                        if ((s | 0) != 0) {
                                            if (s >>> 0 < (c[658] | 0) >>> 0) {
                                                la();
                                            } else {
                                                c[(N + 16) >> 2] = s;
                                                c[(s + 24) >> 2] = N;
                                                break;
                                            }
                                        }
                                    } while (0);
                                    s = c[(M + 20) >> 2] | 0;
                                    if ((s | 0) != 0) {
                                        if (s >>> 0 < (c[658] | 0) >>> 0) {
                                            la();
                                        } else {
                                            c[(N + 20) >> 2] = s;
                                            c[(s + 24) >> 2] = N;
                                            break;
                                        }
                                    }
                                }
                            } while (0);
                            b: do {
                                if (!(L >>> 0 < 16)) {
                                    c[(M + 4) >> 2] = q | 3;
                                    c[(M + (q | 4)) >> 2] = L | 1;
                                    c[(M + (L + q)) >> 2] = L;
                                    e = L >>> 3;
                                    if (L >>> 0 < 256) {
                                        s = e << 1;
                                        k = (2656 + (s << 2)) | 0;
                                        r = c[654] | 0;
                                        m = 1 << e;
                                        do {
                                            if (((r & m) | 0) == 0) {
                                                c[654] = r | m;
                                                Q = (2656 + ((s + 2) << 2)) | 0;
                                                R = k;
                                            } else {
                                                e = (2656 + ((s + 2) << 2)) | 0;
                                                h = c[e >> 2] | 0;
                                                if (!(h >>> 0 < (c[658] | 0) >>> 0)) {
                                                    Q = e;
                                                    R = h;
                                                    break;
                                                }
                                                la();
                                            }
                                        } while (0);
                                        c[Q >> 2] = f;
                                        c[(R + 12) >> 2] = f;
                                        c[(M + (q + 8)) >> 2] = R;
                                        c[(M + (q + 12)) >> 2] = k;
                                        break;
                                    }
                                    s = L >>> 8;
                                    if ((s | 0) != 0) {
                                        if (L >>> 0 > 16777215) {
                                            S = 31;
                                        } else {
                                            m = (((s + 1048320) | 0) >>> 16) & 8;
                                            r = s << m;
                                            s = (((r + 520192) | 0) >>> 16) & 4;
                                            h = r << s;
                                            r = (((h + 245760) | 0) >>> 16) & 2;
                                            e = (14 - (s | m | r) + ((h << r) >>> 15)) | 0;
                                            S = ((L >>> ((e + 7) | 0)) & 1) | (e << 1);
                                        }
                                    } else {
                                        S = 0;
                                    }
                                    e = (2920 + (S << 2)) | 0;
                                    c[(M + (q + 28)) >> 2] = S;
                                    c[(M + (q + 20)) >> 2] = 0;
                                    c[(M + (q + 16)) >> 2] = 0;
                                    r = c[655] | 0;
                                    h = 1 << S;
                                    if (((r & h) | 0) == 0) {
                                        c[655] = r | h;
                                        c[e >> 2] = f;
                                        c[(M + (q + 24)) >> 2] = e;
                                        c[(M + (q + 12)) >> 2] = f;
                                        c[(M + (q + 8)) >> 2] = f;
                                        break;
                                    }
                                    h = c[e >> 2] | 0;
                                    if ((S | 0) == 31) {
                                        T = 0;
                                    } else {
                                        T = (25 - (S >>> 1)) | 0;
                                    }
                                    c: do {
                                        if (((c[(h + 4) >> 2] & -8) | 0) != (L | 0)) {
                                            e = L << T;
                                            r = h;
                                            while (1) {
                                                U = (r + ((e >>> 31) << 2) + 16) | 0;
                                                m = c[U >> 2] | 0;
                                                if ((m | 0) == 0) {
                                                    break;
                                                }
                                                if (((c[(m + 4) >> 2] & -8) | 0) == (L | 0)) {
                                                    V = m;
                                                    break c;
                                                } else {
                                                    e = e << 1;
                                                    r = m;
                                                }
                                            }
                                            if (U >>> 0 < (c[658] | 0) >>> 0) {
                                                la();
                                            } else {
                                                c[U >> 2] = f;
                                                c[(M + (q + 24)) >> 2] = r;
                                                c[(M + (q + 12)) >> 2] = f;
                                                c[(M + (q + 8)) >> 2] = f;
                                                break b;
                                            }
                                        } else {
                                            V = h;
                                        }
                                    } while (0);
                                    h = (V + 8) | 0;
                                    k = c[h >> 2] | 0;
                                    e = c[658] | 0;
                                    if (V >>> 0 < e >>> 0) {
                                        la();
                                    }
                                    if (k >>> 0 < e >>> 0) {
                                        la();
                                    } else {
                                        c[(k + 12) >> 2] = f;
                                        c[h >> 2] = f;
                                        c[(M + (q + 8)) >> 2] = k;
                                        c[(M + (q + 12)) >> 2] = V;
                                        c[(M + (q + 24)) >> 2] = 0;
                                        break;
                                    }
                                } else {
                                    k = (L + q) | 0;
                                    c[(M + 4) >> 2] = k | 3;
                                    h = (M + (k + 4)) | 0;
                                    c[h >> 2] = c[h >> 2] | 1;
                                }
                            } while (0);
                            p = (M + 8) | 0;
                            i = b;
                            return p | 0;
                        } else {
                            B = q;
                        }
                    } else {
                        B = q;
                    }
                } else {
                    B = -1;
                }
            }
        } while (0);
        M = c[656] | 0;
        if (!(B >>> 0 > M >>> 0)) {
            L = (M - B) | 0;
            V = c[659] | 0;
            if (L >>> 0 > 15) {
                c[659] = V + B;
                c[656] = L;
                c[(V + (B + 4)) >> 2] = L | 1;
                c[(V + M) >> 2] = L;
                c[(V + 4) >> 2] = B | 3;
            } else {
                c[656] = 0;
                c[659] = 0;
                c[(V + 4) >> 2] = M | 3;
                L = (V + (M + 4)) | 0;
                c[L >> 2] = c[L >> 2] | 1;
            }
            p = (V + 8) | 0;
            i = b;
            return p | 0;
        }
        V = c[657] | 0;
        if (B >>> 0 < V >>> 0) {
            L = (V - B) | 0;
            c[657] = L;
            V = c[660] | 0;
            c[660] = V + B;
            c[(V + (B + 4)) >> 2] = L | 1;
            c[(V + 4) >> 2] = B | 3;
            p = (V + 8) | 0;
            i = b;
            return p | 0;
        }
        do {
            if ((c[772] | 0) == 0) {
                V = va(30) | 0;
                if ((((V + -1) & V) | 0) == 0) {
                    c[774] = V;
                    c[773] = V;
                    c[775] = -1;
                    c[776] = -1;
                    c[777] = 0;
                    c[765] = 0;
                    c[772] = ((ga(0) | 0) & -16) ^ 1431655768;
                    break;
                } else {
                    la();
                }
            }
        } while (0);
        V = (B + 48) | 0;
        L = c[774] | 0;
        M = (B + 47) | 0;
        U = (L + M) | 0;
        T = (0 - L) | 0;
        L = U & T;
        if (!(L >>> 0 > B >>> 0)) {
            p = 0;
            i = b;
            return p | 0;
        }
        S = c[764] | 0;
        if ((S | 0) != 0 ? ((R = c[762] | 0), (Q = (R + L) | 0), (Q >>> 0 <= R >>> 0) | (Q >>> 0 > S >>> 0)) : 0) {
            p = 0;
            i = b;
            return p | 0;
        }
        d: do {
            if (((c[765] & 4) | 0) == 0) {
                S = c[660] | 0;
                e: do {
                    if ((S | 0) != 0) {
                        Q = 3064 | 0;
                        while (1) {
                            R = c[Q >> 2] | 0;
                            if (!(R >>> 0 > S >>> 0) ? ((W = (Q + 4) | 0), ((R + (c[W >> 2] | 0)) | 0) >>> 0 > S >>> 0) : 0) {
                                break;
                            }
                            R = c[(Q + 8) >> 2] | 0;
                            if ((R | 0) == 0) {
                                X = 182;
                                break e;
                            } else {
                                Q = R;
                            }
                        }
                        if ((Q | 0) != 0) {
                            R = (U - (c[657] | 0)) & T;
                            if (R >>> 0 < 2147483647) {
                                N = oa(R | 0) | 0;
                                O = (N | 0) == (((c[Q >> 2] | 0) + (c[W >> 2] | 0)) | 0);
                                Y = N;
                                Z = R;
                                _ = O ? N : -1;
                                $ = O ? R : 0;
                                X = 191;
                            } else {
                                aa = 0;
                            }
                        } else {
                            X = 182;
                        }
                    } else {
                        X = 182;
                    }
                } while (0);
                do {
                    if ((X | 0) == 182) {
                        S = oa(0) | 0;
                        if ((S | 0) != (-1 | 0)) {
                            q = S;
                            R = c[773] | 0;
                            O = (R + -1) | 0;
                            if (((O & q) | 0) == 0) {
                                ba = L;
                            } else {
                                ba = (L - q + ((O + q) & (0 - R))) | 0;
                            }
                            R = c[762] | 0;
                            q = (R + ba) | 0;
                            if ((ba >>> 0 > B >>> 0) & (ba >>> 0 < 2147483647)) {
                                O = c[764] | 0;
                                if ((O | 0) != 0 ? (q >>> 0 <= R >>> 0) | (q >>> 0 > O >>> 0) : 0) {
                                    aa = 0;
                                    break;
                                }
                                O = oa(ba | 0) | 0;
                                q = (O | 0) == (S | 0);
                                Y = O;
                                Z = ba;
                                _ = q ? S : -1;
                                $ = q ? ba : 0;
                                X = 191;
                            } else {
                                aa = 0;
                            }
                        } else {
                            aa = 0;
                        }
                    }
                } while (0);
                f: do {
                    if ((X | 0) == 191) {
                        q = (0 - Z) | 0;
                        if ((_ | 0) != (-1 | 0)) {
                            ca = _;
                            da = $;
                            X = 202;
                            break d;
                        }
                        do {
                            if (((Y | 0) != (-1 | 0)) & (Z >>> 0 < 2147483647) & (Z >>> 0 < V >>> 0) ? ((S = c[774] | 0), (O = (M - Z + S) & (0 - S)), O >>> 0 < 2147483647) : 0) {
                                if ((oa(O | 0) | 0) == (-1 | 0)) {
                                    oa(q | 0) | 0;
                                    aa = $;
                                    break f;
                                } else {
                                    ea = (O + Z) | 0;
                                    break;
                                }
                            } else {
                                ea = Z;
                            }
                        } while (0);
                        if ((Y | 0) == (-1 | 0)) {
                            aa = $;
                        } else {
                            ca = Y;
                            da = ea;
                            X = 202;
                            break d;
                        }
                    }
                } while (0);
                c[765] = c[765] | 4;
                fa = aa;
                X = 199;
            } else {
                fa = 0;
                X = 199;
            }
        } while (0);
        if (
            (((X | 0) == 199 ? L >>> 0 < 2147483647 : 0) ? ((aa = oa(L | 0) | 0), (L = oa(0) | 0), ((L | 0) != (-1 | 0)) & ((aa | 0) != (-1 | 0)) & (aa >>> 0 < L >>> 0)) : 0)
                ? ((ea = (L - aa) | 0), (L = ea >>> 0 > ((B + 40) | 0) >>> 0), L)
                : 0
        ) {
            ca = aa;
            da = L ? ea : fa;
            X = 202;
        }
        if ((X | 0) == 202) {
            fa = ((c[762] | 0) + da) | 0;
            c[762] = fa;
            if (fa >>> 0 > (c[763] | 0) >>> 0) {
                c[763] = fa;
            }
            fa = c[660] | 0;
            g: do {
                if ((fa | 0) != 0) {
                    ea = 3064 | 0;
                    while (1) {
                        ha = c[ea >> 2] | 0;
                        ia = (ea + 4) | 0;
                        ja = c[ia >> 2] | 0;
                        if ((ca | 0) == ((ha + ja) | 0)) {
                            X = 214;
                            break;
                        }
                        L = c[(ea + 8) >> 2] | 0;
                        if ((L | 0) == 0) {
                            break;
                        } else {
                            ea = L;
                        }
                    }
                    if (((X | 0) == 214 ? ((c[(ea + 12) >> 2] & 8) | 0) == 0 : 0) ? (fa >>> 0 >= ha >>> 0) & (fa >>> 0 < ca >>> 0) : 0) {
                        c[ia >> 2] = ja + da;
                        L = ((c[657] | 0) + da) | 0;
                        aa = (fa + 8) | 0;
                        if (((aa & 7) | 0) == 0) {
                            ka = 0;
                        } else {
                            ka = (0 - aa) & 7;
                        }
                        aa = (L - ka) | 0;
                        c[660] = fa + ka;
                        c[657] = aa;
                        c[(fa + (ka + 4)) >> 2] = aa | 1;
                        c[(fa + (L + 4)) >> 2] = 40;
                        c[661] = c[776];
                        break;
                    }
                    if (ca >>> 0 < (c[658] | 0) >>> 0) {
                        c[658] = ca;
                    }
                    L = (ca + da) | 0;
                    aa = 3064 | 0;
                    while (1) {
                        if ((c[aa >> 2] | 0) == (L | 0)) {
                            X = 224;
                            break;
                        }
                        Y = c[(aa + 8) >> 2] | 0;
                        if ((Y | 0) == 0) {
                            break;
                        } else {
                            aa = Y;
                        }
                    }
                    if ((X | 0) == 224 ? ((c[(aa + 12) >> 2] & 8) | 0) == 0 : 0) {
                        c[aa >> 2] = ca;
                        L = (aa + 4) | 0;
                        c[L >> 2] = (c[L >> 2] | 0) + da;
                        L = (ca + 8) | 0;
                        if (((L & 7) | 0) == 0) {
                            ma = 0;
                        } else {
                            ma = (0 - L) & 7;
                        }
                        L = (ca + (da + 8)) | 0;
                        if (((L & 7) | 0) == 0) {
                            na = 0;
                        } else {
                            na = (0 - L) & 7;
                        }
                        L = (ca + (na + da)) | 0;
                        ea = (ma + B) | 0;
                        Y = (ca + ea) | 0;
                        $ = (L - (ca + ma) - B) | 0;
                        c[(ca + (ma + 4)) >> 2] = B | 3;
                        h: do {
                            if ((L | 0) != (c[660] | 0)) {
                                if ((L | 0) == (c[659] | 0)) {
                                    Z = ((c[656] | 0) + $) | 0;
                                    c[656] = Z;
                                    c[659] = Y;
                                    c[(ca + (ea + 4)) >> 2] = Z | 1;
                                    c[(ca + (Z + ea)) >> 2] = Z;
                                    break;
                                }
                                Z = (da + 4) | 0;
                                M = c[(ca + (Z + na)) >> 2] | 0;
                                if (((M & 3) | 0) == 1) {
                                    V = M & -8;
                                    _ = M >>> 3;
                                    i: do {
                                        if (!(M >>> 0 < 256)) {
                                            ba = c[(ca + ((na | 24) + da)) >> 2] | 0;
                                            W = c[(ca + (da + 12 + na)) >> 2] | 0;
                                            do {
                                                if ((W | 0) == (L | 0)) {
                                                    T = na | 16;
                                                    U = (ca + (Z + T)) | 0;
                                                    q = c[U >> 2] | 0;
                                                    if ((q | 0) == 0) {
                                                        Q = (ca + (T + da)) | 0;
                                                        T = c[Q >> 2] | 0;
                                                        if ((T | 0) == 0) {
                                                            pa = 0;
                                                            break;
                                                        } else {
                                                            qa = T;
                                                            ra = Q;
                                                        }
                                                    } else {
                                                        qa = q;
                                                        ra = U;
                                                    }
                                                    while (1) {
                                                        U = (qa + 20) | 0;
                                                        q = c[U >> 2] | 0;
                                                        if ((q | 0) != 0) {
                                                            qa = q;
                                                            ra = U;
                                                            continue;
                                                        }
                                                        U = (qa + 16) | 0;
                                                        q = c[U >> 2] | 0;
                                                        if ((q | 0) == 0) {
                                                            break;
                                                        } else {
                                                            qa = q;
                                                            ra = U;
                                                        }
                                                    }
                                                    if (ra >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    } else {
                                                        c[ra >> 2] = 0;
                                                        pa = qa;
                                                        break;
                                                    }
                                                } else {
                                                    U = c[(ca + ((na | 8) + da)) >> 2] | 0;
                                                    if (U >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    }
                                                    q = (U + 12) | 0;
                                                    if ((c[q >> 2] | 0) != (L | 0)) {
                                                        la();
                                                    }
                                                    Q = (W + 8) | 0;
                                                    if ((c[Q >> 2] | 0) == (L | 0)) {
                                                        c[q >> 2] = W;
                                                        c[Q >> 2] = U;
                                                        pa = W;
                                                        break;
                                                    } else {
                                                        la();
                                                    }
                                                }
                                            } while (0);
                                            if ((ba | 0) == 0) {
                                                break;
                                            }
                                            W = c[(ca + (da + 28 + na)) >> 2] | 0;
                                            r = (2920 + (W << 2)) | 0;
                                            do {
                                                if ((L | 0) != (c[r >> 2] | 0)) {
                                                    if (ba >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    }
                                                    U = (ba + 16) | 0;
                                                    if ((c[U >> 2] | 0) == (L | 0)) {
                                                        c[U >> 2] = pa;
                                                    } else {
                                                        c[(ba + 20) >> 2] = pa;
                                                    }
                                                    if ((pa | 0) == 0) {
                                                        break i;
                                                    }
                                                } else {
                                                    c[r >> 2] = pa;
                                                    if ((pa | 0) != 0) {
                                                        break;
                                                    }
                                                    c[655] = c[655] & ~(1 << W);
                                                    break i;
                                                }
                                            } while (0);
                                            if (pa >>> 0 < (c[658] | 0) >>> 0) {
                                                la();
                                            }
                                            c[(pa + 24) >> 2] = ba;
                                            W = na | 16;
                                            r = c[(ca + (W + da)) >> 2] | 0;
                                            do {
                                                if ((r | 0) != 0) {
                                                    if (r >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    } else {
                                                        c[(pa + 16) >> 2] = r;
                                                        c[(r + 24) >> 2] = pa;
                                                        break;
                                                    }
                                                }
                                            } while (0);
                                            r = c[(ca + (Z + W)) >> 2] | 0;
                                            if ((r | 0) == 0) {
                                                break;
                                            }
                                            if (r >>> 0 < (c[658] | 0) >>> 0) {
                                                la();
                                            } else {
                                                c[(pa + 20) >> 2] = r;
                                                c[(r + 24) >> 2] = pa;
                                                break;
                                            }
                                        } else {
                                            r = c[(ca + ((na | 8) + da)) >> 2] | 0;
                                            ba = c[(ca + (da + 12 + na)) >> 2] | 0;
                                            U = (2656 + ((_ << 1) << 2)) | 0;
                                            do {
                                                if ((r | 0) != (U | 0)) {
                                                    if (r >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    }
                                                    if ((c[(r + 12) >> 2] | 0) == (L | 0)) {
                                                        break;
                                                    }
                                                    la();
                                                }
                                            } while (0);
                                            if ((ba | 0) == (r | 0)) {
                                                c[654] = c[654] & ~(1 << _);
                                                break;
                                            }
                                            do {
                                                if ((ba | 0) == (U | 0)) {
                                                    sa = (ba + 8) | 0;
                                                } else {
                                                    if (ba >>> 0 < (c[658] | 0) >>> 0) {
                                                        la();
                                                    }
                                                    W = (ba + 8) | 0;
                                                    if ((c[W >> 2] | 0) == (L | 0)) {
                                                        sa = W;
                                                        break;
                                                    }
                                                    la();
                                                }
                                            } while (0);
                                            c[(r + 12) >> 2] = ba;
                                            c[sa >> 2] = r;
                                        }
                                    } while (0);
                                    ta = (ca + ((V | na) + da)) | 0;
                                    ua = (V + $) | 0;
                                } else {
                                    ta = L;
                                    ua = $;
                                }
                                _ = (ta + 4) | 0;
                                c[_ >> 2] = c[_ >> 2] & -2;
                                c[(ca + (ea + 4)) >> 2] = ua | 1;
                                c[(ca + (ua + ea)) >> 2] = ua;
                                _ = ua >>> 3;
                                if (ua >>> 0 < 256) {
                                    Z = _ << 1;
                                    M = (2656 + (Z << 2)) | 0;
                                    U = c[654] | 0;
                                    W = 1 << _;
                                    do {
                                        if (((U & W) | 0) == 0) {
                                            c[654] = U | W;
                                            wa = (2656 + ((Z + 2) << 2)) | 0;
                                            ya = M;
                                        } else {
                                            _ = (2656 + ((Z + 2) << 2)) | 0;
                                            Q = c[_ >> 2] | 0;
                                            if (!(Q >>> 0 < (c[658] | 0) >>> 0)) {
                                                wa = _;
                                                ya = Q;
                                                break;
                                            }
                                            la();
                                        }
                                    } while (0);
                                    c[wa >> 2] = Y;
                                    c[(ya + 12) >> 2] = Y;
                                    c[(ca + (ea + 8)) >> 2] = ya;
                                    c[(ca + (ea + 12)) >> 2] = M;
                                    break;
                                }
                                Z = ua >>> 8;
                                do {
                                    if ((Z | 0) == 0) {
                                        za = 0;
                                    } else {
                                        if (ua >>> 0 > 16777215) {
                                            za = 31;
                                            break;
                                        }
                                        W = (((Z + 1048320) | 0) >>> 16) & 8;
                                        U = Z << W;
                                        V = (((U + 520192) | 0) >>> 16) & 4;
                                        Q = U << V;
                                        U = (((Q + 245760) | 0) >>> 16) & 2;
                                        _ = (14 - (V | W | U) + ((Q << U) >>> 15)) | 0;
                                        za = ((ua >>> ((_ + 7) | 0)) & 1) | (_ << 1);
                                    }
                                } while (0);
                                Z = (2920 + (za << 2)) | 0;
                                c[(ca + (ea + 28)) >> 2] = za;
                                c[(ca + (ea + 20)) >> 2] = 0;
                                c[(ca + (ea + 16)) >> 2] = 0;
                                M = c[655] | 0;
                                _ = 1 << za;
                                if (((M & _) | 0) == 0) {
                                    c[655] = M | _;
                                    c[Z >> 2] = Y;
                                    c[(ca + (ea + 24)) >> 2] = Z;
                                    c[(ca + (ea + 12)) >> 2] = Y;
                                    c[(ca + (ea + 8)) >> 2] = Y;
                                    break;
                                }
                                _ = c[Z >> 2] | 0;
                                if ((za | 0) == 31) {
                                    Aa = 0;
                                } else {
                                    Aa = (25 - (za >>> 1)) | 0;
                                }
                                j: do {
                                    if (((c[(_ + 4) >> 2] & -8) | 0) != (ua | 0)) {
                                        Z = ua << Aa;
                                        M = _;
                                        while (1) {
                                            Ba = (M + ((Z >>> 31) << 2) + 16) | 0;
                                            U = c[Ba >> 2] | 0;
                                            if ((U | 0) == 0) {
                                                break;
                                            }
                                            if (((c[(U + 4) >> 2] & -8) | 0) == (ua | 0)) {
                                                Ca = U;
                                                break j;
                                            } else {
                                                Z = Z << 1;
                                                M = U;
                                            }
                                        }
                                        if (Ba >>> 0 < (c[658] | 0) >>> 0) {
                                            la();
                                        } else {
                                            c[Ba >> 2] = Y;
                                            c[(ca + (ea + 24)) >> 2] = M;
                                            c[(ca + (ea + 12)) >> 2] = Y;
                                            c[(ca + (ea + 8)) >> 2] = Y;
                                            break h;
                                        }
                                    } else {
                                        Ca = _;
                                    }
                                } while (0);
                                _ = (Ca + 8) | 0;
                                Z = c[_ >> 2] | 0;
                                r = c[658] | 0;
                                if (Ca >>> 0 < r >>> 0) {
                                    la();
                                }
                                if (Z >>> 0 < r >>> 0) {
                                    la();
                                } else {
                                    c[(Z + 12) >> 2] = Y;
                                    c[_ >> 2] = Y;
                                    c[(ca + (ea + 8)) >> 2] = Z;
                                    c[(ca + (ea + 12)) >> 2] = Ca;
                                    c[(ca + (ea + 24)) >> 2] = 0;
                                    break;
                                }
                            } else {
                                Z = ((c[657] | 0) + $) | 0;
                                c[657] = Z;
                                c[660] = Y;
                                c[(ca + (ea + 4)) >> 2] = Z | 1;
                            }
                        } while (0);
                        p = (ca + (ma | 8)) | 0;
                        i = b;
                        return p | 0;
                    }
                    ea = 3064 | 0;
                    while (1) {
                        Da = c[ea >> 2] | 0;
                        if (!(Da >>> 0 > fa >>> 0) ? ((Ea = c[(ea + 4) >> 2] | 0), (Fa = (Da + Ea) | 0), Fa >>> 0 > fa >>> 0) : 0) {
                            break;
                        }
                        ea = c[(ea + 8) >> 2] | 0;
                    }
                    ea = (Da + (Ea + -39)) | 0;
                    if (((ea & 7) | 0) == 0) {
                        Ga = 0;
                    } else {
                        Ga = (0 - ea) & 7;
                    }
                    ea = (Da + (Ea + -47 + Ga)) | 0;
                    Y = ea >>> 0 < ((fa + 16) | 0) >>> 0 ? fa : ea;
                    ea = (Y + 8) | 0;
                    $ = (ca + 8) | 0;
                    if ((($ & 7) | 0) == 0) {
                        Ha = 0;
                    } else {
                        Ha = (0 - $) & 7;
                    }
                    $ = (da + -40 - Ha) | 0;
                    c[660] = ca + Ha;
                    c[657] = $;
                    c[(ca + (Ha + 4)) >> 2] = $ | 1;
                    c[(ca + (da + -36)) >> 2] = 40;
                    c[661] = c[776];
                    c[(Y + 4) >> 2] = 27;
                    c[(ea + 0) >> 2] = c[766];
                    c[(ea + 4) >> 2] = c[767];
                    c[(ea + 8) >> 2] = c[768];
                    c[(ea + 12) >> 2] = c[769];
                    c[766] = ca;
                    c[767] = da;
                    c[769] = 0;
                    c[768] = ea;
                    ea = (Y + 28) | 0;
                    c[ea >> 2] = 7;
                    if (((Y + 32) | 0) >>> 0 < Fa >>> 0) {
                        $ = ea;
                        do {
                            ea = $;
                            $ = ($ + 4) | 0;
                            c[$ >> 2] = 7;
                        } while (((ea + 8) | 0) >>> 0 < Fa >>> 0);
                    }
                    if ((Y | 0) != (fa | 0)) {
                        $ = (Y - fa) | 0;
                        ea = (fa + ($ + 4)) | 0;
                        c[ea >> 2] = c[ea >> 2] & -2;
                        c[(fa + 4) >> 2] = $ | 1;
                        c[(fa + $) >> 2] = $;
                        ea = $ >>> 3;
                        if ($ >>> 0 < 256) {
                            L = ea << 1;
                            aa = (2656 + (L << 2)) | 0;
                            Z = c[654] | 0;
                            _ = 1 << ea;
                            do {
                                if (((Z & _) | 0) == 0) {
                                    c[654] = Z | _;
                                    Ia = (2656 + ((L + 2) << 2)) | 0;
                                    Ja = aa;
                                } else {
                                    ea = (2656 + ((L + 2) << 2)) | 0;
                                    r = c[ea >> 2] | 0;
                                    if (!(r >>> 0 < (c[658] | 0) >>> 0)) {
                                        Ia = ea;
                                        Ja = r;
                                        break;
                                    }
                                    la();
                                }
                            } while (0);
                            c[Ia >> 2] = fa;
                            c[(Ja + 12) >> 2] = fa;
                            c[(fa + 8) >> 2] = Ja;
                            c[(fa + 12) >> 2] = aa;
                            break;
                        }
                        L = $ >>> 8;
                        if ((L | 0) != 0) {
                            if ($ >>> 0 > 16777215) {
                                Ka = 31;
                            } else {
                                _ = (((L + 1048320) | 0) >>> 16) & 8;
                                Z = L << _;
                                L = (((Z + 520192) | 0) >>> 16) & 4;
                                Y = Z << L;
                                Z = (((Y + 245760) | 0) >>> 16) & 2;
                                r = (14 - (L | _ | Z) + ((Y << Z) >>> 15)) | 0;
                                Ka = (($ >>> ((r + 7) | 0)) & 1) | (r << 1);
                            }
                        } else {
                            Ka = 0;
                        }
                        r = (2920 + (Ka << 2)) | 0;
                        c[(fa + 28) >> 2] = Ka;
                        c[(fa + 20) >> 2] = 0;
                        c[(fa + 16) >> 2] = 0;
                        Z = c[655] | 0;
                        Y = 1 << Ka;
                        if (((Z & Y) | 0) == 0) {
                            c[655] = Z | Y;
                            c[r >> 2] = fa;
                            c[(fa + 24) >> 2] = r;
                            c[(fa + 12) >> 2] = fa;
                            c[(fa + 8) >> 2] = fa;
                            break;
                        }
                        Y = c[r >> 2] | 0;
                        if ((Ka | 0) == 31) {
                            La = 0;
                        } else {
                            La = (25 - (Ka >>> 1)) | 0;
                        }
                        k: do {
                            if (((c[(Y + 4) >> 2] & -8) | 0) != ($ | 0)) {
                                r = $ << La;
                                Z = Y;
                                while (1) {
                                    Ma = (Z + ((r >>> 31) << 2) + 16) | 0;
                                    _ = c[Ma >> 2] | 0;
                                    if ((_ | 0) == 0) {
                                        break;
                                    }
                                    if (((c[(_ + 4) >> 2] & -8) | 0) == ($ | 0)) {
                                        Na = _;
                                        break k;
                                    } else {
                                        r = r << 1;
                                        Z = _;
                                    }
                                }
                                if (Ma >>> 0 < (c[658] | 0) >>> 0) {
                                    la();
                                } else {
                                    c[Ma >> 2] = fa;
                                    c[(fa + 24) >> 2] = Z;
                                    c[(fa + 12) >> 2] = fa;
                                    c[(fa + 8) >> 2] = fa;
                                    break g;
                                }
                            } else {
                                Na = Y;
                            }
                        } while (0);
                        Y = (Na + 8) | 0;
                        $ = c[Y >> 2] | 0;
                        aa = c[658] | 0;
                        if (Na >>> 0 < aa >>> 0) {
                            la();
                        }
                        if ($ >>> 0 < aa >>> 0) {
                            la();
                        } else {
                            c[($ + 12) >> 2] = fa;
                            c[Y >> 2] = fa;
                            c[(fa + 8) >> 2] = $;
                            c[(fa + 12) >> 2] = Na;
                            c[(fa + 24) >> 2] = 0;
                            break;
                        }
                    }
                } else {
                    $ = c[658] | 0;
                    if ((($ | 0) == 0) | (ca >>> 0 < $ >>> 0)) {
                        c[658] = ca;
                    }
                    c[766] = ca;
                    c[767] = da;
                    c[769] = 0;
                    c[663] = c[772];
                    c[662] = -1;
                    $ = 0;
                    do {
                        Y = $ << 1;
                        aa = (2656 + (Y << 2)) | 0;
                        c[(2656 + ((Y + 3) << 2)) >> 2] = aa;
                        c[(2656 + ((Y + 2) << 2)) >> 2] = aa;
                        $ = ($ + 1) | 0;
                    } while (($ | 0) != 32);
                    $ = (ca + 8) | 0;
                    if ((($ & 7) | 0) == 0) {
                        Oa = 0;
                    } else {
                        Oa = (0 - $) & 7;
                    }
                    $ = (da + -40 - Oa) | 0;
                    c[660] = ca + Oa;
                    c[657] = $;
                    c[(ca + (Oa + 4)) >> 2] = $ | 1;
                    c[(ca + (da + -36)) >> 2] = 40;
                    c[661] = c[776];
                }
            } while (0);
            da = c[657] | 0;
            if (da >>> 0 > B >>> 0) {
                ca = (da - B) | 0;
                c[657] = ca;
                da = c[660] | 0;
                c[660] = da + B;
                c[(da + (B + 4)) >> 2] = ca | 1;
                c[(da + 4) >> 2] = B | 3;
                p = (da + 8) | 0;
                i = b;
                return p | 0;
            }
        }
        c[(xa() | 0) >> 2] = 12;
        p = 0;
        i = b;
        return p | 0;
    }
    function qb(a) {
        a = a | 0;
        var b = 0,
            d = 0,
            e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0,
            m = 0,
            n = 0,
            o = 0,
            p = 0,
            q = 0,
            r = 0,
            s = 0,
            t = 0,
            u = 0,
            v = 0,
            w = 0,
            x = 0,
            y = 0,
            z = 0,
            A = 0,
            B = 0,
            C = 0,
            D = 0,
            E = 0,
            F = 0,
            G = 0,
            H = 0,
            I = 0,
            J = 0,
            K = 0;
        b = i;
        if ((a | 0) == 0) {
            i = b;
            return;
        }
        d = (a + -8) | 0;
        e = c[658] | 0;
        if (d >>> 0 < e >>> 0) {
            la();
        }
        f = c[(a + -4) >> 2] | 0;
        g = f & 3;
        if ((g | 0) == 1) {
            la();
        }
        h = f & -8;
        j = (a + (h + -8)) | 0;
        do {
            if (((f & 1) | 0) == 0) {
                k = c[d >> 2] | 0;
                if ((g | 0) == 0) {
                    i = b;
                    return;
                }
                l = (-8 - k) | 0;
                m = (a + l) | 0;
                n = (k + h) | 0;
                if (m >>> 0 < e >>> 0) {
                    la();
                }
                if ((m | 0) == (c[659] | 0)) {
                    o = (a + (h + -4)) | 0;
                    if (((c[o >> 2] & 3) | 0) != 3) {
                        p = m;
                        q = n;
                        break;
                    }
                    c[656] = n;
                    c[o >> 2] = c[o >> 2] & -2;
                    c[(a + (l + 4)) >> 2] = n | 1;
                    c[j >> 2] = n;
                    i = b;
                    return;
                }
                o = k >>> 3;
                if (k >>> 0 < 256) {
                    k = c[(a + (l + 8)) >> 2] | 0;
                    r = c[(a + (l + 12)) >> 2] | 0;
                    s = (2656 + ((o << 1) << 2)) | 0;
                    if ((k | 0) != (s | 0)) {
                        if (k >>> 0 < e >>> 0) {
                            la();
                        }
                        if ((c[(k + 12) >> 2] | 0) != (m | 0)) {
                            la();
                        }
                    }
                    if ((r | 0) == (k | 0)) {
                        c[654] = c[654] & ~(1 << o);
                        p = m;
                        q = n;
                        break;
                    }
                    if ((r | 0) != (s | 0)) {
                        if (r >>> 0 < e >>> 0) {
                            la();
                        }
                        s = (r + 8) | 0;
                        if ((c[s >> 2] | 0) == (m | 0)) {
                            t = s;
                        } else {
                            la();
                        }
                    } else {
                        t = (r + 8) | 0;
                    }
                    c[(k + 12) >> 2] = r;
                    c[t >> 2] = k;
                    p = m;
                    q = n;
                    break;
                }
                k = c[(a + (l + 24)) >> 2] | 0;
                r = c[(a + (l + 12)) >> 2] | 0;
                do {
                    if ((r | 0) == (m | 0)) {
                        s = (a + (l + 20)) | 0;
                        o = c[s >> 2] | 0;
                        if ((o | 0) == 0) {
                            u = (a + (l + 16)) | 0;
                            v = c[u >> 2] | 0;
                            if ((v | 0) == 0) {
                                w = 0;
                                break;
                            } else {
                                x = v;
                                y = u;
                            }
                        } else {
                            x = o;
                            y = s;
                        }
                        while (1) {
                            s = (x + 20) | 0;
                            o = c[s >> 2] | 0;
                            if ((o | 0) != 0) {
                                x = o;
                                y = s;
                                continue;
                            }
                            s = (x + 16) | 0;
                            o = c[s >> 2] | 0;
                            if ((o | 0) == 0) {
                                break;
                            } else {
                                x = o;
                                y = s;
                            }
                        }
                        if (y >>> 0 < e >>> 0) {
                            la();
                        } else {
                            c[y >> 2] = 0;
                            w = x;
                            break;
                        }
                    } else {
                        s = c[(a + (l + 8)) >> 2] | 0;
                        if (s >>> 0 < e >>> 0) {
                            la();
                        }
                        o = (s + 12) | 0;
                        if ((c[o >> 2] | 0) != (m | 0)) {
                            la();
                        }
                        u = (r + 8) | 0;
                        if ((c[u >> 2] | 0) == (m | 0)) {
                            c[o >> 2] = r;
                            c[u >> 2] = s;
                            w = r;
                            break;
                        } else {
                            la();
                        }
                    }
                } while (0);
                if ((k | 0) != 0) {
                    r = c[(a + (l + 28)) >> 2] | 0;
                    s = (2920 + (r << 2)) | 0;
                    if ((m | 0) == (c[s >> 2] | 0)) {
                        c[s >> 2] = w;
                        if ((w | 0) == 0) {
                            c[655] = c[655] & ~(1 << r);
                            p = m;
                            q = n;
                            break;
                        }
                    } else {
                        if (k >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        }
                        r = (k + 16) | 0;
                        if ((c[r >> 2] | 0) == (m | 0)) {
                            c[r >> 2] = w;
                        } else {
                            c[(k + 20) >> 2] = w;
                        }
                        if ((w | 0) == 0) {
                            p = m;
                            q = n;
                            break;
                        }
                    }
                    if (w >>> 0 < (c[658] | 0) >>> 0) {
                        la();
                    }
                    c[(w + 24) >> 2] = k;
                    r = c[(a + (l + 16)) >> 2] | 0;
                    do {
                        if ((r | 0) != 0) {
                            if (r >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            } else {
                                c[(w + 16) >> 2] = r;
                                c[(r + 24) >> 2] = w;
                                break;
                            }
                        }
                    } while (0);
                    r = c[(a + (l + 20)) >> 2] | 0;
                    if ((r | 0) != 0) {
                        if (r >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        } else {
                            c[(w + 20) >> 2] = r;
                            c[(r + 24) >> 2] = w;
                            p = m;
                            q = n;
                            break;
                        }
                    } else {
                        p = m;
                        q = n;
                    }
                } else {
                    p = m;
                    q = n;
                }
            } else {
                p = d;
                q = h;
            }
        } while (0);
        if (!(p >>> 0 < j >>> 0)) {
            la();
        }
        d = (a + (h + -4)) | 0;
        w = c[d >> 2] | 0;
        if (((w & 1) | 0) == 0) {
            la();
        }
        if (((w & 2) | 0) == 0) {
            if ((j | 0) == (c[660] | 0)) {
                e = ((c[657] | 0) + q) | 0;
                c[657] = e;
                c[660] = p;
                c[(p + 4) >> 2] = e | 1;
                if ((p | 0) != (c[659] | 0)) {
                    i = b;
                    return;
                }
                c[659] = 0;
                c[656] = 0;
                i = b;
                return;
            }
            if ((j | 0) == (c[659] | 0)) {
                e = ((c[656] | 0) + q) | 0;
                c[656] = e;
                c[659] = p;
                c[(p + 4) >> 2] = e | 1;
                c[(p + e) >> 2] = e;
                i = b;
                return;
            }
            e = ((w & -8) + q) | 0;
            x = w >>> 3;
            do {
                if (!(w >>> 0 < 256)) {
                    y = c[(a + (h + 16)) >> 2] | 0;
                    t = c[(a + (h | 4)) >> 2] | 0;
                    do {
                        if ((t | 0) == (j | 0)) {
                            g = (a + (h + 12)) | 0;
                            f = c[g >> 2] | 0;
                            if ((f | 0) == 0) {
                                r = (a + (h + 8)) | 0;
                                k = c[r >> 2] | 0;
                                if ((k | 0) == 0) {
                                    z = 0;
                                    break;
                                } else {
                                    A = k;
                                    B = r;
                                }
                            } else {
                                A = f;
                                B = g;
                            }
                            while (1) {
                                g = (A + 20) | 0;
                                f = c[g >> 2] | 0;
                                if ((f | 0) != 0) {
                                    A = f;
                                    B = g;
                                    continue;
                                }
                                g = (A + 16) | 0;
                                f = c[g >> 2] | 0;
                                if ((f | 0) == 0) {
                                    break;
                                } else {
                                    A = f;
                                    B = g;
                                }
                            }
                            if (B >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            } else {
                                c[B >> 2] = 0;
                                z = A;
                                break;
                            }
                        } else {
                            g = c[(a + h) >> 2] | 0;
                            if (g >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            }
                            f = (g + 12) | 0;
                            if ((c[f >> 2] | 0) != (j | 0)) {
                                la();
                            }
                            r = (t + 8) | 0;
                            if ((c[r >> 2] | 0) == (j | 0)) {
                                c[f >> 2] = t;
                                c[r >> 2] = g;
                                z = t;
                                break;
                            } else {
                                la();
                            }
                        }
                    } while (0);
                    if ((y | 0) != 0) {
                        t = c[(a + (h + 20)) >> 2] | 0;
                        n = (2920 + (t << 2)) | 0;
                        if ((j | 0) == (c[n >> 2] | 0)) {
                            c[n >> 2] = z;
                            if ((z | 0) == 0) {
                                c[655] = c[655] & ~(1 << t);
                                break;
                            }
                        } else {
                            if (y >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            }
                            t = (y + 16) | 0;
                            if ((c[t >> 2] | 0) == (j | 0)) {
                                c[t >> 2] = z;
                            } else {
                                c[(y + 20) >> 2] = z;
                            }
                            if ((z | 0) == 0) {
                                break;
                            }
                        }
                        if (z >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        }
                        c[(z + 24) >> 2] = y;
                        t = c[(a + (h + 8)) >> 2] | 0;
                        do {
                            if ((t | 0) != 0) {
                                if (t >>> 0 < (c[658] | 0) >>> 0) {
                                    la();
                                } else {
                                    c[(z + 16) >> 2] = t;
                                    c[(t + 24) >> 2] = z;
                                    break;
                                }
                            }
                        } while (0);
                        t = c[(a + (h + 12)) >> 2] | 0;
                        if ((t | 0) != 0) {
                            if (t >>> 0 < (c[658] | 0) >>> 0) {
                                la();
                            } else {
                                c[(z + 20) >> 2] = t;
                                c[(t + 24) >> 2] = z;
                                break;
                            }
                        }
                    }
                } else {
                    t = c[(a + h) >> 2] | 0;
                    y = c[(a + (h | 4)) >> 2] | 0;
                    n = (2656 + ((x << 1) << 2)) | 0;
                    if ((t | 0) != (n | 0)) {
                        if (t >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        }
                        if ((c[(t + 12) >> 2] | 0) != (j | 0)) {
                            la();
                        }
                    }
                    if ((y | 0) == (t | 0)) {
                        c[654] = c[654] & ~(1 << x);
                        break;
                    }
                    if ((y | 0) != (n | 0)) {
                        if (y >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        }
                        n = (y + 8) | 0;
                        if ((c[n >> 2] | 0) == (j | 0)) {
                            C = n;
                        } else {
                            la();
                        }
                    } else {
                        C = (y + 8) | 0;
                    }
                    c[(t + 12) >> 2] = y;
                    c[C >> 2] = t;
                }
            } while (0);
            c[(p + 4) >> 2] = e | 1;
            c[(p + e) >> 2] = e;
            if ((p | 0) == (c[659] | 0)) {
                c[656] = e;
                i = b;
                return;
            } else {
                D = e;
            }
        } else {
            c[d >> 2] = w & -2;
            c[(p + 4) >> 2] = q | 1;
            c[(p + q) >> 2] = q;
            D = q;
        }
        q = D >>> 3;
        if (D >>> 0 < 256) {
            w = q << 1;
            d = (2656 + (w << 2)) | 0;
            e = c[654] | 0;
            C = 1 << q;
            if (((e & C) | 0) != 0) {
                q = (2656 + ((w + 2) << 2)) | 0;
                j = c[q >> 2] | 0;
                if (j >>> 0 < (c[658] | 0) >>> 0) {
                    la();
                } else {
                    E = q;
                    F = j;
                }
            } else {
                c[654] = e | C;
                E = (2656 + ((w + 2) << 2)) | 0;
                F = d;
            }
            c[E >> 2] = p;
            c[(F + 12) >> 2] = p;
            c[(p + 8) >> 2] = F;
            c[(p + 12) >> 2] = d;
            i = b;
            return;
        }
        d = D >>> 8;
        if ((d | 0) != 0) {
            if (D >>> 0 > 16777215) {
                G = 31;
            } else {
                F = (((d + 1048320) | 0) >>> 16) & 8;
                E = d << F;
                d = (((E + 520192) | 0) >>> 16) & 4;
                w = E << d;
                E = (((w + 245760) | 0) >>> 16) & 2;
                C = (14 - (d | F | E) + ((w << E) >>> 15)) | 0;
                G = ((D >>> ((C + 7) | 0)) & 1) | (C << 1);
            }
        } else {
            G = 0;
        }
        C = (2920 + (G << 2)) | 0;
        c[(p + 28) >> 2] = G;
        c[(p + 20) >> 2] = 0;
        c[(p + 16) >> 2] = 0;
        E = c[655] | 0;
        w = 1 << G;
        a: do {
            if (((E & w) | 0) != 0) {
                F = c[C >> 2] | 0;
                if ((G | 0) == 31) {
                    H = 0;
                } else {
                    H = (25 - (G >>> 1)) | 0;
                }
                b: do {
                    if (((c[(F + 4) >> 2] & -8) | 0) != (D | 0)) {
                        d = D << H;
                        e = F;
                        while (1) {
                            I = (e + ((d >>> 31) << 2) + 16) | 0;
                            j = c[I >> 2] | 0;
                            if ((j | 0) == 0) {
                                break;
                            }
                            if (((c[(j + 4) >> 2] & -8) | 0) == (D | 0)) {
                                J = j;
                                break b;
                            } else {
                                d = d << 1;
                                e = j;
                            }
                        }
                        if (I >>> 0 < (c[658] | 0) >>> 0) {
                            la();
                        } else {
                            c[I >> 2] = p;
                            c[(p + 24) >> 2] = e;
                            c[(p + 12) >> 2] = p;
                            c[(p + 8) >> 2] = p;
                            break a;
                        }
                    } else {
                        J = F;
                    }
                } while (0);
                F = (J + 8) | 0;
                d = c[F >> 2] | 0;
                j = c[658] | 0;
                if (J >>> 0 < j >>> 0) {
                    la();
                }
                if (d >>> 0 < j >>> 0) {
                    la();
                } else {
                    c[(d + 12) >> 2] = p;
                    c[F >> 2] = p;
                    c[(p + 8) >> 2] = d;
                    c[(p + 12) >> 2] = J;
                    c[(p + 24) >> 2] = 0;
                    break;
                }
            } else {
                c[655] = E | w;
                c[C >> 2] = p;
                c[(p + 24) >> 2] = C;
                c[(p + 12) >> 2] = p;
                c[(p + 8) >> 2] = p;
            }
        } while (0);
        p = ((c[662] | 0) + -1) | 0;
        c[662] = p;
        if ((p | 0) == 0) {
            K = 3072 | 0;
        } else {
            i = b;
            return;
        }
        while (1) {
            p = c[K >> 2] | 0;
            if ((p | 0) == 0) {
                break;
            } else {
                K = (p + 8) | 0;
            }
        }
        c[662] = -1;
        i = b;
        return;
    }
    function rb(b, c, d) {
        b = b | 0;
        c = c | 0;
        d = d | 0;
        var e = 0,
            f = 0,
            g = 0,
            h = 0,
            j = 0,
            k = 0,
            l = 0;
        e = i;
        a: do {
            if ((d | 0) == 0) {
                f = 0;
            } else {
                g = d;
                h = b;
                j = c;
                while (1) {
                    k = a[h >> 0] | 0;
                    l = a[j >> 0] | 0;
                    if (!((k << 24) >> 24 == (l << 24) >> 24)) {
                        break;
                    }
                    g = (g + -1) | 0;
                    if ((g | 0) == 0) {
                        f = 0;
                        break a;
                    } else {
                        h = (h + 1) | 0;
                        j = (j + 1) | 0;
                    }
                }
                f = ((k & 255) - (l & 255)) | 0;
            }
        } while (0);
        i = e;
        return f | 0;
    }
    function sb() {}
    function tb(b) {
        b = b | 0;
        var c = 0;
        c = b;
        while (a[c >> 0] | 0) {
            c = (c + 1) | 0;
        }
        return (c - b) | 0;
    }
    function ub(b, d, e) {
        b = b | 0;
        d = d | 0;
        e = e | 0;
        var f = 0,
            g = 0,
            h = 0,
            i = 0;
        f = (b + e) | 0;
        if ((e | 0) >= 20) {
            d = d & 255;
            g = b & 3;
            h = d | (d << 8) | (d << 16) | (d << 24);
            i = f & ~3;
            if (g) {
                g = (b + 4 - g) | 0;
                while ((b | 0) < (g | 0)) {
                    a[b >> 0] = d;
                    b = (b + 1) | 0;
                }
            }
            while ((b | 0) < (i | 0)) {
                c[b >> 2] = h;
                b = (b + 4) | 0;
            }
        }
        while ((b | 0) < (f | 0)) {
            a[b >> 0] = d;
            b = (b + 1) | 0;
        }
        return (b - e) | 0;
    }
    function vb(b, d, e) {
        b = b | 0;
        d = d | 0;
        e = e | 0;
        var f = 0;
        if ((e | 0) >= 4096) return sa(b | 0, d | 0, e | 0) | 0;
        f = b | 0;
        if ((b & 3) == (d & 3)) {
            while (b & 3) {
                if ((e | 0) == 0) return f | 0;
                a[b >> 0] = a[d >> 0] | 0;
                b = (b + 1) | 0;
                d = (d + 1) | 0;
                e = (e - 1) | 0;
            }
            while ((e | 0) >= 4) {
                c[b >> 2] = c[d >> 2];
                b = (b + 4) | 0;
                d = (d + 4) | 0;
                e = (e - 4) | 0;
            }
        }
        while ((e | 0) > 0) {
            a[b >> 0] = a[d >> 0] | 0;
            b = (b + 1) | 0;
            d = (d + 1) | 0;
            e = (e - 1) | 0;
        }
        return f | 0;
    }

    // EMSCRIPTEN_END_FUNCS
    return {
        _my_init: Ja,
        _spc_set_output: $a,
        _free: qb,
        _main: Ia,
        _spc_set_tempo: ab,
        _spc_filter_clear: gb,
        _spc_filter_run: fb,
        _strlen: tb,
        _memset: ub,
        _malloc: pb,
        _spc_filter_new: eb,
        _memcpy: vb,
        _spc_play: db,
        _my_decode: Ka,
        _spc_new: _a,
        _spc_load_spc: bb,
        _spc_clear_echo: cb,
        runPostSets: sb,
        stackAlloc: za,
        stackSave: Aa,
        stackRestore: Ba,
        setThrew: Ca,
        setTempRet0: Fa,
        getTempRet0: Ga,
    };
    // EMSCRIPTEN_END_ASM
})(
    { Math: Math, Int8Array: Int8Array, Int16Array: Int16Array, Int32Array: Int32Array, Uint8Array: Uint8Array, Uint16Array: Uint16Array, Uint32Array: Uint32Array, Float32Array: Float32Array, Float64Array: Float64Array },
    {
        abort: abort,
        assert: assert,
        asmPrintInt: asmPrintInt,
        asmPrintFloat: asmPrintFloat,
        min: Math_min,
        _fflush: _fflush,
        __formatString: __formatString,
        _time: _time,
        _send: _send,
        _pwrite: _pwrite,
        _fileno: _fileno,
        __exit: __exit,
        _abort: _abort,
        ___setErrNo: ___setErrNo,
        _fwrite: _fwrite,
        _sbrk: _sbrk,
        _mkport: _mkport,
        _fprintf: _fprintf,
        ___assert_fail: ___assert_fail,
        _emscripten_memcpy_big: _emscripten_memcpy_big,
        __reallyNegative: __reallyNegative,
        _write: _write,
        _sysconf: _sysconf,
        _exit: _exit,
        ___errno_location: ___errno_location,
        STACKTOP: STACKTOP,
        STACK_MAX: STACK_MAX,
        tempDoublePtr: tempDoublePtr,
        ABORT: ABORT,
        NaN: NaN,
        Infinity: Infinity,
        _stderr: _stderr,
    },
    buffer
);
var _my_init = (Module["_my_init"] = asm["_my_init"]);
var _spc_set_output = (Module["_spc_set_output"] = asm["_spc_set_output"]);
var _free = (Module["_free"] = asm["_free"]);
var _main = (Module["_main"] = asm["_main"]);
var _spc_set_tempo = (Module["_spc_set_tempo"] = asm["_spc_set_tempo"]);
var _spc_filter_clear = (Module["_spc_filter_clear"] = asm["_spc_filter_clear"]);
var _spc_filter_run = (Module["_spc_filter_run"] = asm["_spc_filter_run"]);
var _strlen = (Module["_strlen"] = asm["_strlen"]);
var _memset = (Module["_memset"] = asm["_memset"]);
var _malloc = (Module["_malloc"] = asm["_malloc"]);
var _spc_filter_new = (Module["_spc_filter_new"] = asm["_spc_filter_new"]);
var _memcpy = (Module["_memcpy"] = asm["_memcpy"]);
var _spc_play = (Module["_spc_play"] = asm["_spc_play"]);
var _my_decode = (Module["_my_decode"] = asm["_my_decode"]);
var _spc_new = (Module["_spc_new"] = asm["_spc_new"]);
var _spc_load_spc = (Module["_spc_load_spc"] = asm["_spc_load_spc"]);
var _spc_clear_echo = (Module["_spc_clear_echo"] = asm["_spc_clear_echo"]);
var runPostSets = (Module["runPostSets"] = asm["runPostSets"]);
Runtime.stackAlloc = asm["stackAlloc"];
Runtime.stackSave = asm["stackSave"];
Runtime.stackRestore = asm["stackRestore"];
Runtime.setTempRet0 = asm["setTempRet0"];
Runtime.getTempRet0 = asm["getTempRet0"];
var i64Math = null;
if (memoryInitializer) {
    if (Module["memoryInitializerPrefixURL"]) {
        memoryInitializer = Module["memoryInitializerPrefixURL"] + memoryInitializer;
    }
    if (ENVIRONMENT_IS_NODE || ENVIRONMENT_IS_SHELL) {
        var data = Module["readBinary"](memoryInitializer);
        HEAPU8.set(data, STATIC_BASE);
    } else {
        addRunDependency("memory initializer");
        Browser.asyncLoad(
            memoryInitializer,
            function (data) {
                HEAPU8.set(data, STATIC_BASE);
                removeRunDependency("memory initializer");
            },
            function (data) {
                throw "could not load memory initializer " + memoryInitializer;
            }
        );
    }
}
function ExitStatus(status) {
    this.name = "ExitStatus";
    this.message = "Program terminated with exit(" + status + ")";
    this.status = status;
}
ExitStatus.prototype = new Error();
ExitStatus.prototype.constructor = ExitStatus;
var initialStackTop;
var preloadStartTime = null;
var calledMain = false;
dependenciesFulfilled = function runCaller() {
    if (!Module["calledRun"] && shouldRunNow) run();
    if (!Module["calledRun"]) dependenciesFulfilled = runCaller;
};
Module["callMain"] = Module.callMain = function callMain(args) {
    assert(runDependencies == 0, "cannot call main when async dependencies remain! (listen on __ATMAIN__)");
    assert(__ATPRERUN__.length == 0, "cannot call main when preRun functions remain to be called");
    args = args || [];
    ensureInitRuntime();
    var argc = args.length + 1;
    function pad() {
        for (var i = 0; i < 4 - 1; i++) {
            argv.push(0);
        }
    }
    var argv = [allocate(intArrayFromString(Module["thisProgram"]), "i8", ALLOC_NORMAL)];
    pad();
    for (var i = 0; i < argc - 1; i = i + 1) {
        argv.push(allocate(intArrayFromString(args[i]), "i8", ALLOC_NORMAL));
        pad();
    }
    argv.push(0);
    argv = allocate(argv, "i32", ALLOC_NORMAL);
    initialStackTop = STACKTOP;
    try {
        var ret = Module["_main"](argc, argv, 0);
        exit(ret);
    } catch (e) {
        if (e instanceof ExitStatus) {
            return;
        } else if (e == "SimulateInfiniteLoop") {
            Module["noExitRuntime"] = true;
            return;
        } else {
            if (e && typeof e === "object" && e.stack) Module.printErr("exception thrown: " + [e, e.stack]);
            throw e;
        }
    } finally {
        calledMain = true;
    }
};
function run(args) {
    args = args || Module["arguments"];
    if (preloadStartTime === null) preloadStartTime = Date.now();
    if (runDependencies > 0) {
        Module.printErr("run() called, but dependencies remain, so not running");
        return;
    }
    preRun();
    if (runDependencies > 0) return;
    if (Module["calledRun"]) return;
    function doRun() {
        if (Module["calledRun"]) return;
        Module["calledRun"] = true;
        if (ABORT) return;
        ensureInitRuntime();
        preMain();
        if (ENVIRONMENT_IS_WEB && preloadStartTime !== null) {
            Module.printErr("pre-main prep time: " + (Date.now() - preloadStartTime) + " ms");
        }
        if (Module["_main"] && shouldRunNow) {
            Module["callMain"](args);
        }
        postRun();
    }
    if (Module["setStatus"]) {
        Module["setStatus"]("Running...");
        setTimeout(function () {
            setTimeout(function () {
                Module["setStatus"]("");
            }, 1);
            doRun();
        }, 1);
    } else {
        doRun();
    }
}
Module["run"] = Module.run = run;
function exit(status) {
    if (Module["noExitRuntime"]) {
        return;
    }
    ABORT = true;
    EXITSTATUS = status;
    STACKTOP = initialStackTop;
    exitRuntime();
    if (ENVIRONMENT_IS_NODE) {
        process["stdout"]["once"]("drain", function () {
            process["exit"](status);
        });
        console.log(" ");
        setTimeout(function () {
            process["exit"](status);
        }, 500);
    } else if (ENVIRONMENT_IS_SHELL && typeof quit === "function") {
        quit(status);
    }
    throw new ExitStatus(status);
}
Module["exit"] = Module.exit = exit;
function abort(text) {
    if (text) {
        Module.print(text);
        Module.printErr(text);
    }
    ABORT = true;
    EXITSTATUS = 1;
    var extra = "\nIf this abort() is unexpected, build with -s ASSERTIONS=1 which can give more information.";
    throw "abort() at " + stackTrace() + extra;
}
Module["abort"] = Module.abort = abort;
if (Module["preInit"]) {
    if (typeof Module["preInit"] == "function") Module["preInit"] = [Module["preInit"]];
    while (Module["preInit"].length > 0) {
        Module["preInit"].pop()();
    }
}
var shouldRunNow = true;
if (Module["noInitialRun"]) {
    shouldRunNow = false;
}
Module["noExitRuntime"] = true;
run();
