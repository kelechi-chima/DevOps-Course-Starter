echo -e 'if shopt -q login_shell; then' \
  '\n  export PYENV_ROOT="$HOME/.pyenv"' \
  '\n  export PATH="$PYENV_ROOT/bin:$PATH"' \
  '\n eval "$(pyenv init --path)"' \
  '\nfi' >> $HOME/.bashrc
echo -e 'if [ -z "$BASH_VERSION" ]; then'\
  '\n  export PYENV_ROOT="$HOME/.pyenv"'\
  '\n  export PATH="$PYENV_ROOT/bin:$PATH"'\
  '\n  eval "$(pyenv init --path)"'\
  '\nfi' >> $HOME/.profile
source $HOME/.profile