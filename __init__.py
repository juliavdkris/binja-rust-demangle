from binaryninja import *
import ctypes
import os


BUFFER_LENGTH = 512
DIR = os.path.dirname(os.path.realpath(__file__))

print(f'LOADING {DIR}/rustc-demangle/target/release/librustc_demangle.so')
rustc_demangle = ctypes.CDLL(f'{DIR}/rustc-demangle/target/release/librustc_demangle.so').rustc_demangle



def demangle(bv):
	for f in bv.functions:
		name = f.name.encode('UTF-8')
		buf = bytes(BUFFER_LENGTH)
		res = rustc_demangle(name, buf, BUFFER_LENGTH)

		if res:
			log.log_debug(f'DEMANGLED: {f.name}  ->  {buf.decode("UTF-8")}')
			f.name = buf.decode('UTF-8')
		else:
			log.log_debug(f'SKIPPED: {f.name}')



PluginCommand.register("Rust demangle", "yeet", demangle)
