set nocompatible 
filetype off 

set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin() 

call vundle#begin('~/Documents/vimplugins')

" Installed Plugins -------------------{{{
Plugin 'gmarik/Vundle.vim'
Plugin 'maralla/completor.vim'
Plugin 'tmhedberg/SimpylFold'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'vim-scripts/a.vim'
Plugin 'nvie/vim-flake8'
Plugin 'jmcantrell/vim-virtualenv'
Plugin 'joshdick/onedark.vim'
Plugin 'vim-syntastic/syntastic'
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'scrooloose/nerdcommenter'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'tpope/vim-fugitive'
Plugin 'rust-lang/rust.vim'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'MarcWeber/vim-addon-mw-utils'
Plugin 'tomtom/tlib_vim'
Plugin 'garbas/vim-snipmate'
Plugin 'honza/vim-snippets'
Plugin 'christoomey/vim-tmux-runner'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'ryanoasis/vim-devicons'

Plugin 'dylanaraps/wal.vim'
" }}}

call vundle#end()

set exrc
set secure
set guifont=SauceCodePro\ Nerd\ Font\ Mono\ 11
set t_Co=256
set laststatus=2
set foldmethod=indent
set foldlevel=99
set nu
set encoding=utf-8
set tabstop=4 
set softtabstop=4 
set shiftwidth=4 
set textwidth=79 
set expandtab 
set autoindent 
set fileformat=unix 

" Must haves ---------------{{{
filetype plugin indent on
syntax enable
" }}}

" Colorscheme from atom text editor 
" colorscheme onedark
colorscheme wal

let python_highlight_all=1
let NERDTreeIgnore=['\.pyc$', '\~$', '\.out$', 'node_modules$', '__pycache__$']
let g:rustfmt_autosave=1
let g:airline_theme='murmur'
let g:airline_powerline_fonts=1
let g:airline#extensions#tabline#enabled=1
let g:VtrStripLeadingWhitespace = 0 
let g:VtrClearEmptyLines = 0
let g:VtrAppendNewline = 1

let g:completor_python_binary = '/usr/bin/python3'
let g:completor_racer_binary = '/home/johannes/.cargo/bin/racer'
let g:completor_clang_binary = '/usr/bin/clang'
let g:completor_auto_trigger = 0

" General mappings ------------{{{
map <leader>n <plug>NERDTreeTabsToggle<CR>
" }}}

" normal mode mappings----------------{{{
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
nnoremap <space> za
nnoremap <leader>ev :vsplit $MYVIMRC<CR>
nnoremap <leader>sv :source $MYVIMRC<CR>
nnoremap <S-Up> <C-Y>
nnoremap <S-Down> <C-E>
" }}}

" Insert mode mappings ----------------------{{{
inoremap jk <esc>
inoremap ( ()<left>
inoremap { {}<left>

" Use TAB to complete when typing words, else inserts TABs as usual.  Uses
" dictionary, source files, and completor to find matching words to complete.

" Note: usual completion is on <C-n> but more trouble to press all the time.
" Never type the same word twice and maybe learn a new spellings!
" Use the Linux dictionary when spelling is in doubt.
function! Tab_Or_Complete() abort
  " If completor is already open the `tab` cycles through suggested completions.
  if pumvisible()
    return "\<C-N>"
  " If completor is not open and we are in the middle of typing a word then
  " `tab` opens completor menu.
  elseif col('.')>1 && strpart( getline('.'), col('.')-2, 3 ) =~ '^\w'
    return "\<C-R>=completor#do('complete')\<CR>"
  else
    " If we aren't typing a word and we press `tab` simply do the normal `tab`
    " action.
    return "\<Tab>"
  endif
endfunction

" Use `tab` key to select completions.  Default is arrow keys.
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"

" Use tab to trigger auto completion.  Default suggests completions as you type.
inoremap <expr> <Tab> Tab_Or_Complete()
" }}}

" Visual mode mappings ---------------------{{{
vnoremap jk <esc>
" }}}

" Mapped operators -----------------------{{{
onoremap p i(
" }}}

" Vimscript file settings ----------------- {{{
augroup filetype_vim
	autocmd!
	autocmd FileType vim setlocal foldmethod=marker
augroup END
" }}}

" Mapping for execution ------------------- {{{
augroup execution
    autocmd!
    autocmd FileType python imap <F5> <ESC>:w<CR>:!clear;python %<CR>
    autocmd FileType c imap <F5> <ESC>:w<CR>:!clear;make<CR>
augroup END
" }}}
