# Custom hook for ONNX Runtime
from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs

# Collect all ONNX Runtime files
datas, binaries, hiddenimports = collect_all('onnxruntime')

# CRITICAL: Explicitly collect DLLs
binaries += collect_dynamic_libs('onnxruntime')

# Hidden imports
hiddenimports += [
    'onnxruntime.capi._pybind_state',
    'onnxruntime.capi.onnxruntime_pybind11_state',
    'onnxruntime.backend',
    'onnxruntime.backend.backend',
]
