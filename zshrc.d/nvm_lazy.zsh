# Lazy-load nvm only when a node tool is used to avoid slow shell startup.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

_nvm_lazy_load() {
  unset -f nvm node npm npx yarn

  if [ -s "$NVM_DIR/nvm.sh" ]; then
    # --no-use keeps nvm from switching versions during load; we handle .nvmrc below.
    . "$NVM_DIR/nvm.sh" --no-use
  fi

  if [ -s "$NVM_DIR/bash_completion" ]; then
    . "$NVM_DIR/bash_completion"
  fi

  if command -v nvm >/dev/null 2>&1 && [ -f ".nvmrc" ]; then
    nvm use --silent >/dev/null 2>&1
  fi
}

nvm()  { _nvm_lazy_load; nvm  "$@"; }
node() { _nvm_lazy_load; node "$@"; }
npm()  { _nvm_lazy_load; npm  "$@"; }
npx()  { _nvm_lazy_load; npx  "$@"; }
yarn() { _nvm_lazy_load; yarn "$@"; }
