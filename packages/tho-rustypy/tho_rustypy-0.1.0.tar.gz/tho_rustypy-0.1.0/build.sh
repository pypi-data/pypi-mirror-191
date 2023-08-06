pyenv virtualenv rustypy
pyenv activate rustypy

. ${PYENV_ROOT}/versions/rustypy/bin/activate

pip3 install maturin
pyenv local rustypy && PYTHON_CONFIGURE_OPTS="--enable-shared" maturin develop