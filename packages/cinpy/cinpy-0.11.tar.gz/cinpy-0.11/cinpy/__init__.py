import configparser
import ctypes
import importlib
import re
import subprocess
import sys
from flexible_partial import FlexiblePartialOwnName
import numpy as np
import os
import collections
from touchtouch import touch

c_functions = sys.modules[__name__]


d_types2 = collections.namedtuple("d_types", "np c ct use comment code alias")
d_typesall = []
d_typesall.append(
    d_types2(
        np="np.bool_",
        c="bool",
        ct="ctypes.c_bool",
        use=True,
        comment="The bool_ type is not a subclass of the int_ type (the bool_ is not even a number type). T",
        code="?",
        alias="numpy.bool8",
    )
)
d_typesall.append(
    d_types2(
        np="np.byte",
        c="signed char",
        ct="ctypes.c_byte",
        use=True,
        comment="Signed integer type, compatible with C char",
        code="b",
        alias="numpy.int8: 8-bit signed integer (-128 to 127).",
    )
)
d_typesall.append(
    d_types2(
        np="np.ubyte",
        c="unsigned char",
        ct="ctypes.c_ubyte",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned char. ",
        code="B",
        alias="numpy.uint8: 8-bit unsigned integer (0 to 255).",
    )
)
d_typesall.append(
    d_types2(
        np="np.short",
        c="short",
        ct="ctypes.c_short",
        use=True,
        comment="Signed integer type, compatible with C short.",
        code="h",
        alias="numpy.int16: 16-bit signed integer (-32_768 to 32_767)",
    )
)
d_typesall.append(
    d_types2(
        np="np.ushort",
        c="unsigned short",
        ct="ctypes.c_ushort",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned short",
        code="H",
        alias="numpy.uint16: 16-bit unsigned integer (0 to 65_535)",
    )
)
d_typesall.append(
    d_types2(
        np="np.intc",
        c="int",
        ct="ctypes.c_int",
        use=True,
        comment="Signed integer type, compatible with C int",
        code="i",
        alias="numpy.int32: 32-bit signed integer (-2_147_483_648 to 2_147_483_647)",
    )
)
d_typesall.append(
    d_types2(
        np="np.uintc",
        c="unsigned int",
        ct="ctypes.c_uint",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned int",
        code="I",
        alias="numpy.uint32: 32-bit unsigned integer (0 to 4_294_967_295)",
    )
)
d_typesall.append(
    d_types2(
        np="np.int_",
        c="long",
        ct="ctypes.c_long",
        use=True,
        comment="Signed integer type, compatible with Python int and C long",
        code="l",
        alias="numpy.int64: 64-bit signed integer (-9_223_372_036_854_775_808 to 9_223_372_036_854_775_807) / numpy.intp: Signed integer large enough to fit pointer, compatible with C intptr_t.",
    )
)
d_typesall.append(
    d_types2(
        np="np.uint",
        c="unsigned long",
        ct="ctypes.c_ulong",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned long",
        code="L",
        alias="numpy.uint32: 32-bit unsigned integer (0 to 4_294_967_295)",
    )
)
d_typesall.append(
    d_types2(
        np="np.longlong",
        c="long long",
        ct="ctypes.c_longlong",
        use=True,
        comment="Signed integer type, compatible with C long long",
        code="q",
        alias="",
    )
)
d_typesall.append(
    d_types2(
        np="np.ulonglong",
        c="unsigned long long",
        ct="ctypes.c_ulonglong",
        use=True,
        comment="Signed integer type, compatible with C unsigned long long",
        code="Q",
        alias="",
    )
)
d_typesall.append(
    d_types2(
        np="np.single",
        c="float",
        ct="ctypes.c_float",
        use=True,
        comment="Single-precision floating-point number type, compatible with C float",
        code="f",
        alias="numpy.float32: 32-bit-precision floating-point number type: sign bit, 8 bits exponent, 23 bits mantissa.",
    )
)
d_typesall.append(
    d_types2(
        np="np.double",
        c="double",
        ct="ctypes.c_double",
        use=True,
        comment="Double-precision floating-point number type, compatible with Python float and C double",
        code="d",
        alias="numpy.float64: 64-bit precision floating-point number type: sign bit, 11 bits exponent, 52 bits mantissa.",
    )
)
d_typesall.append(
    d_types2(
        np="np.longdouble",
        c="long double",
        ct="ctypes.c_longdouble",
        use=True,
        comment="Extended-precision floating-point number type, compatible with C long double but not necessarily with IEEE 754 quadruple-precision.",
        code="g",
        alias="numpy.float128: 128-bit extended-precision floating-point number type.",
    )
)
d_typesall.append(
    d_types2(
        np="np.csingle",
        c="float complex",
        ct="ctypes.c_double",
        use=True,
        comment="Complex number type composed of two single-precision floating-point numbers",
        code="F",
        alias="numpy.complex64: Complex number type composed of 2 32-bit-precision floating-point numbers.",
    )
)
d_typesall.append(
    d_types2(
        np="np.cdouble",
        c="double complex",
        ct="ctypes.c_double",
        use=True,
        comment="Complex number type composed of two double-precision floating-point numbers, compatible with Python complex.",
        code="D",
        alias="numpy.complex128: Complex number type composed of 2 64-bit-precision floating-point numbers.",
    )
)
d_typesall.append(
    d_types2(
        np="np.clongdouble",
        c="long double complex",
        ct="ctypes.c_longdouble",
        use=True,
        comment="Complex number type composed of two extended-precision floating-point numbers.",
        code="G",
        alias="Complex number type composed of 2 128-bit extended-precision floating-point numbers",
    )
)


def compile_cpp(
    cfgfile,
    fnames,
    vcvarsall_bat,
    cl_exe,
    link_exe,
    cppsource,
    output,
    compilerflags=(
        "/std:c++17",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
    ),
):
    config = configparser.ConfigParser()
    allcommand = [
        vcvarsall_bat,
        "x64",
        "&&",
        cl_exe,
        "/D_USRDL",
        "/D_WINDLL",
        cppsource,
        *compilerflags,
        "/link",
        "/DLL",
        f'/OUT:"{output}"',
        "/MACHINE:X64",
    ]
    subprocess.run(allcommand, shell=True)

    p = subprocess.run([link_exe, "/dump", "/exports", output], capture_output=True)
    fnamesre = [
        (
            x,
            re.compile(
                rf"[\r\n]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+(\?[^\s]*{x}@[^\s]+)"
            ),
        )
        for x in fnames
    ]
    decor = p.stdout.decode("utf-8", "ignore")
    print(decor)
    franmesre = [(x[0], x[1].findall(decor)) for x in fnamesre]
    config["DEFAULT"] = {k: v[0] for k, v in franmesre if v}
    with open(cfgfile, "w") as f:
        config.write(f)


def get_cpp_functions(
    modulename,
    all_functions,
    code=None,
    vcvarsall_bat=None,
    cl_exe=None,
    link_exe=None,
    recompile=False,
    compilerflags=(
        "/std:c++17",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
    ),
):
    sourcepath = get_file(f"{modulename}.cpp")
    dllpath = get_file(f"{modulename}.dll")
    cfgfile = get_file(f"{modulename}.ini")
    fnames = [x[0] for x in all_functions]
    if code is None or vcvarsall_bat is None or cl_exe is None or link_exe is None:
        load_cpp_functions(dllpath, cfgfile, all_functions)
    elif recompile or not os.path.exists(dllpath) or not os.path.exists(cfgfile):
        try:
            if os.path.exists(sourcepath):
                os.remove(sourcepath)
        except Exception:
            pass
        try:
            if os.path.exists(dllpath):
                os.remove(dllpath)
        except Exception:
            pass
        try:
            if os.path.exists(cfgfile):
                os.remove(cfgfile)
        except Exception:
            pass
        with open(sourcepath, mode="w", encoding="utf-8") as f:
            f.write(code)
        compile_cpp(
            cfgfile,
            fnames,
            vcvarsall_bat,
            cl_exe,
            link_exe,
            sourcepath,
            dllpath,
            compilerflags,
        )
        load_cpp_functions(dllpath, cfgfile, all_functions)
    else:
        load_cpp_functions(dllpath, cfgfile, all_functions)


def load_cpp_functions(dllpath, cfgfile, all_functions):
    lib = ctypes.CDLL(dllpath)
    confignew = configparser.ConfigParser()
    confignew.read(cfgfile)
    funcs = confignew.defaults()
    allfu = []
    for (
        fname,
        descri,
        function_prefix,
        functionnormalprefix,
        restype,
        argtypes,
    ) in all_functions:
        fun = lib.__getattr__(funcs[fname])
        fun.restype = restype
        if len(argtypes) != 0:
            fun.argtypes = argtypes
        allfu.append((fname, fun))
        setattr(c_functions, f"{functionnormalprefix}{fname}", fun)
        setattr(
            c_functions,
            f"{function_prefix}{fname}",
            FlexiblePartialOwnName(execute_function, descri, True, fun),
        )

    return allfu


def print_datatypes():
    nw = "\n"
    for k in d_typesall:
        print(
            f"""
Numpy:        {k.np}
C:            {k.c}
ctypes:       {k.ct}
code:         {k.code}
alias:        {k.alias}
comment:      {f"{nw}              ".join([sax for sax in k.comment.splitlines() if sax.strip()!=''])}
"""
        )


def create_signature_variations(
    basefunction: str,
    code_c_function: str,
    savepath_argtypes: str,
    savepath_cfunctions: str,
    c_file_header: str = "",
    c_file_footer: str = "",
    add_to_function_signature="",
    prefix_for_functions="",
    add_to_argtypes="",
    prefix_for_partial_functions="aa_",
    add_to_top_of_py_file="",
    ignored_dtypes=(
        "bool",
        "np.csingle",
        "np.cdouble",
        "np.clongdouble",
        "np.longdouble",
    ),
):
    touch(savepath_argtypes)
    touch(savepath_cfunctions)

    whole_c_code = ""

    whole_python_argtypes = ""

    add_to_python_file = "from numpy.ctypeslib import ndpointer\nimport ctypes\n"
    add_to_top_of_py_file += add_to_python_file

    for k in d_typesall:
        if k.np in ignored_dtypes or k.c in ignored_dtypes or k.ct in ignored_dtypes:
            continue
        if not k.use:
            continue
        comment0 = f"// np={k.np}, c={k.c}, ctypes={k.ct}, code={k.code}".replace(
            "\n", " "
        ).replace("\r", " ")
        comment1 = f"// {k.alias}".replace("\n", " ").replace("\r", " ")
        comment2 = f"// {k.comment}".replace("\n", " ").replace("\r", " ")
        newa = (
            code_c_function.replace("!C_DATA_DTYPE!", f" {k.c} ")
            .replace("!ADDEXTRA!", add_to_function_signature)
            .strip()
        )
        newfuna = f'{basefunction}_{k.ct.split(".")[-1].replace("c_", "").strip()}'
        newa = newa.replace("!BASE_FUNCTION_NAME!", newfuna)
        allcomments = f"{comment0}\n{comment1}\n{comment2}"
        allcommentsargs = f"{comment0[3:]}\n{comment1[3:]}\n{comment2[3:]}"
        whole_c_code += f"\n\n\n\n{allcomments}\n{newa}"
        argt = f"""
            (
            "{newfuna}",
            r'''{allcommentsargs}''',
            "{prefix_for_partial_functions}",
            "{prefix_for_functions}",
            None,
            [
                ndpointer({k.ct}, flags="aligned,C_CONTIGUOUS"),
                ctypes.c_size_t,
                ndpointer({k.ct}, flags="aligned,C_CONTIGUOUS,writeable"),
                {add_to_argtypes}
            ],
        ),
        """.replace("!CT_DATA_DTYPE!",k.ct)
        whole_python_argtypes += argt
    whole_c_code = f"{c_file_header}\n{whole_c_code}\n{c_file_footer}"
    whole_python_argtypes = f"all_functions = [{whole_python_argtypes}]"
    whole_python_argtypes = f"{add_to_top_of_py_file}\n{whole_python_argtypes}"
    with open(savepath_argtypes, mode="w", encoding="utf-8") as f:
        f.write(whole_python_argtypes)
    with open(savepath_cfunctions, mode="w", encoding="utf-8") as f:
        f.write(whole_c_code)
    return whole_python_argtypes, whole_c_code


def get_file(f):
    return os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), f))


def get_file_own_folder(f, folder):
    return os.path.normpath(os.path.join(folder, f))


def compile_c_code(gcc_exe, c_code, modulename, folder=None,compilerflags=("-O3",)):
    if folder is None:
        cfusource = get_file(f"{modulename}.c")
        sofile = get_file(f"{modulename}.so")
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        cfusource = get_file_own_folder(f=f"{modulename}.c", folder=folder)
        sofile = get_file_own_folder(f=f"{modulename}.so", folder=folder)
    with open(cfusource, mode="w", encoding="utf-8") as f:
        f.write(c_code)
    command = [gcc_exe, "-fPIC", "-shared", *compilerflags, "-o", sofile, cfusource]
    subprocess.run(command, shell=False)
    return sofile


def loadlib(so_file, all_functions):
    lib = ctypes.cdll.LoadLibrary(so_file)

    for (
        fname,
        descri,
        function_prefix,
        functionnormalprefix,
        restype,
        argtypes,
    ) in all_functions:
        fun = lib.__getattr__(fname)
        fun.restype = restype
        if len(argtypes) > 0:
            fun.argtypes = argtypes
        setattr(c_functions, f"{functionnormalprefix}{fname}", fun)
        setattr(
            c_functions,
            f"{function_prefix}{fname}",
            FlexiblePartialOwnName(execute_function, descri, True, fun),
        )


def load_module_extern_py_file(modulename):
    moduleinport = f"{modulename}_argtypes"
    try:
        baxax = importlib.import_module(f'cinpy.{moduleinport}')
    except Exception:
        try:
            baxax = importlib.import_module(f'.{moduleinport}')
        except Exception:
            baxax = importlib.import_module(f'{moduleinport}')

    all_functions = getattr(baxax, "all_functions")
    sofile = get_file(f"{modulename}.so")
    loadlib(sofile, all_functions)


def get_all_files_for_module(modulename):
    moduleinport = f"{modulename}_argtypes"
    folder = os.path.normpath((os.path.abspath(os.path.dirname(__file__))))
    argtypesfile = os.path.normpath(os.path.join(folder, f"{moduleinport}.py"))
    cfile = os.path.normpath(os.path.join(folder, f"{modulename}_cfunctions.c"))
    sofile = os.path.normpath(os.path.join(folder, f"{modulename}.so"))
    return moduleinport, folder, argtypesfile, cfile, sofile


def execute_function(
    f,
    arr,
    *args,
    **kwargs,
):
    arr2 = np.empty_like(arr)
    f(arr, arr.size, arr2, *args, **kwargs)
    return arr2
