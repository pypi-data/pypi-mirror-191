: racker --verbose run -it --rm --platform=windows/amd64 python:3.9 -- cmd
: C:\racker\doc\use-cases\foobar.bat

echo hello
echo world

call scoop bucket add extras
call scoop install miniconda3

: Activate Anaconda environment.
: https://github.com/conda/conda/issues/8702#issuecomment-494163721
for /f %%i in ('call scoop prefix miniconda3') do set MINICONDA_PATH=%%i
"%MINICONDA_PATH%\condabin\conda_hook.bat"

: call "%MINICONDA_PATH%\condabin\activate.bat"
: call "%MINICONDA_PATH%\condabin\conda_hook.bat"
: call conda activate
conda --version

echo hello
echo world
