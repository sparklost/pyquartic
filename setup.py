import glob
import os
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)


class BdistWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

class CustomBuildExt(_build_ext):
    def run(self):
        import compile_numba
        compile_numba.build_numba_extensions()

        build_lib_pyquartic = os.path.join(self.build_lib, "pyquartic")
        os.makedirs(build_lib_pyquartic, exist_ok=True)

        for so_file in glob.glob("*.so") + glob.glob("*.pyd"):
            target = os.path.join(build_lib_pyquartic, os.path.basename(so_file))
            os.rename(so_file, target)

        super().run()

        for so_file in glob.glob(os.path.join(self.build_lib, "pyquartic", "_dummy*.so")):
            os.remove(so_file)

    def build_extensions(self):
        self.extensions = [
            ext for ext in self.extensions
            if ext.name != "pyquartic._dummy"
        ]
        super().build_extensions()

setup(
    name="pyquartic",
    version="0.1.0",
    packages=["pyquartic"],
    ext_modules=[Extension("pyquartic._dummy", sources=[])],
    cmdclass={
        "build_ext": CustomBuildExt,
        "bdist_wheel": BdistWheel,
    },
)
