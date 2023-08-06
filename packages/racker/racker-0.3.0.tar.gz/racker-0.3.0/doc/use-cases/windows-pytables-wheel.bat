@echo off
rem
rem Build wheels for PyTables on Windows. DIY, without a hosted CI provider.
rem https://github.com/cicerops/racker/blob/main/doc/use-cases/python-on-windows.rst
rem
rem Synopsis::
rem
rem   racker --verbose run -it --rm --platform=windows/amd64 python:3.9 -- cmd
rem   .\racker\doc\use-cases\windows-pytables-wheel.bat
rem

rem Install prerequisites.

rem Microsoft Visual C++ Build Tools 2017.
rem MSVC 14.16.27023, Windows SDK 10.0.17763.0
rem https://docs.microsoft.com/en-us/visualstudio/install/workload-and-component-ids
rem https://gist.github.com/mitchellmebane/7f3fc4db27cc41333437f88c450a62f7
rem https://docs.microsoft.com/en-us/visualstudio/install/use-command-line-parameters-to-install-visual-studio
rem https://devblogs.microsoft.com/cppblog/finding-the-visual-c-compiler-tools-in-visual-studio-2017/
sh -c "wget --no-clobber https://aka.ms/vs/15/release/vs_buildtools.exe"
echo Installing Microsoft Visual C++ Build Tools 2017
: .\vs_buildtools.exe --norestart --quiet --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Product.BuildTools
.\vs_buildtools.exe --quiet --wait --norestart --nocache --add Microsoft.VisualStudio.Workload.MSBuildTools --includeRecommended --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Product.BuildTools --add Microsoft.VisualStudio.Component.Windows10SDK


rem Windows SDK.
rem Needed for `stdlib.h`, `stdio.h`, etc.
rem https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/
rem choco install --yes windows-sdk-8.0
rem choco install --yes windows-sdk-8.1
rem choco install --yes windows-sdk-10.0
rem choco install --yes windows-sdk-10.1

: sh -c "wget --no-clobber https://github.com/brechtsanders/winlibs_mingw/releases/download/12.1.0-14.0.4-10.0.0-ucrt-r2/winlibs-x86_64-posix-seh-gcc-12.1.0-mingw-w64ucrt-10.0.0-r2.7z"
: 7z x -aos winlibs-x86_64-posix-seh-gcc-12.1.0-mingw-w64ucrt-10.0.0-r2.7z
: set INCLUDE=%INCLUDE%;C:\mingw64\include\c++\12.1.0


rem Miniconda - A minimal installer for Anaconda.
rem https://conda.io/miniconda.html
rem https://community.chocolatey.org/packages/miniconda3
rem choco install --yes miniconda3 --package-parameters="'/AddToPath:1'"

rem Miniconda - A minimal installer for Anaconda.
rem https://conda.io/miniconda.html
: echo 1
: scoop bucket rm extras
echo 2
call scoop bucket add extras
echo 3
call scoop install miniconda3
echo 4


rem Activate Anaconda and build tools prompt.
rem :: https://stackoverflow.com/questions/2323292/assign-output-of-a-program-to-a-variable-using-a-ms-batch-file
echo 5
for /f %%i in ('call scoop prefix miniconda3') do set MINICONDA_PATH=%%i
echo 6

: call "%MINICONDA_PATH%\condabin\activate.bat"

: Visual Studio 2017 Developer Command Prompt v15.0
: Activate Visual Studio command line prompt.
: "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\Common7\Tools\VsDevCmd.bat"
: "\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
: "\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
: "\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86
echo 7

rem "C:\tools\miniconda3\condabin\activate.bat"

: scsdc

rem Activate specific Anaconda environment.
: call conda create --yes --name=build && conda activate build && conda config --env --set subdir win-64
: call conda create --yes --name=build32 && conda activate build32 && conda config --env --set subdir win-32

rem Install build-time prerequisites.
: conda install --yes blosc bzip2 hdf5 lz4 lzo snappy zstd zlib

rem cibuildwheel - Build Python wheels for all the platforms on CI with minimal configuration.
rem https://cibuildwheel.readthedocs.io/
pip install --upgrade cibuildwheel

rem Configure cibuildwheel.
: set CIBW_BUILD=cp39-win_amd64
set CIBW_BUILD=cp39-win32
: set CIBW_BEFORE_ALL_WINDOWS='conda create --yes --name=build && conda activate build && conda config --env --set subdir win-64 && conda install --yes blosc bzip2 hdf5 lz4 lzo snappy zstd zlib'
set CIBW_ENVIRONMENT=PYTABLES_NO_EMBEDDED_LIBS=true DISABLE_AVX2=true
set CIBW_BEFORE_BUILD=pip install -r requirements.txt cython>=0.29.21 delvewheel
set CIBW_REPAIR_WHEEL_COMMAND_WINDOWS=delvewheel repair -w {dest_dir} {wheel}

rem Debugging.
rem env

rem Acquire sources.
mkdir -p C:\src
cd C:\src
test ! -d PyTables && git clone https://github.com/PyTables/PyTables --recursive --depth=1
cd PyTables

rem Build wheel.
cibuildwheel --platform=windows --output-dir=wheelhouse

cd \
