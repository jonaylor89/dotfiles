
"dein Scripts-----------------------------
if &compatible
  set nocompatible               " Be iMproved
endif

" Required:
set runtimepath+=/home/johannes/.cache/dein/repos/github.com/Shougo/dein.vim

" Required:
if dein#load_state('/home/johannes/.cache/dein')
  call dein#begin('/home/johannes/.cache/dein')

  " Let dein manage dein
  " Required:
  call dein#add('/home/johannes/.cache/dein/repos/github.com/Shougo/dein.vim')

  " Add or remove your plugins here like this:
  "call dein#add('Shougo/neosnippet.vim')
  "call dein#add('Shougo/neosnippet-snippets')

" Installed Plugins -------------------{{{
  call dein#add('maralla/completor.vim')
  call dein#add('tmhedberg/SimpylFold')
  call dein#add('vim-scripts/indentpython.vim')
  call dein#add('vim-scripts/a.vim')
  call dein#add('nvie/vim-flake8')
  call dein#add('jmcantrell/vim-virtualenv')
  call dein#add('joshdick/onedark.vim')
  call dein#add('vim-syntastic/syntastic')
  call dein#add('jnurmine/Zenburn')
  call dein#add('altercation/vim-colors-solarized')
  call dein#add('scrooloose/nerdtree')
  call dein#add('jistr/vim-nerdtree-tabs')
  call dein#add('scrooloose/nerdcommenter')
  call dein#add('vim-airline/vim-airline')
  call dein#add('vim-airline/vim-airline-themes')
  call dein#add('tpope/vim-fugitive')
  call dein#add('dag/vim-fish')
  call dein#add('rust-lang/rust.vim')
  call dein#add('rstacruz/sparkup', {'rtp': 'vim/'})
  call dein#add('MarcWeber/vim-addon-mw-utils')
  call dein#add('tomtom/tlib_vim')
  call dein#add('garbas/vim-snipmate')
  call dein#add('honza/vim-snippets')
  call dein#add('christoomey/vim-tmux-runner')
  call dein#add('christoomey/vim-tmux-navigator')
  call dein#add('ryanoasis/vim-devicons')

  call dein#add('dylanaraps/wal.vim')
" }}}

"
  " Required:
  call dein#end()
  call dein#save_state()
endif

" Required:
filetype plugin indent on
syntax enable

" If you want to install not installed plugins on startup.
if dein#check_install()
  call dein#install()
endif

"End dein Scripts-------------------------

filetype off 

" Change shell to POSIX shell for plugins
if &shell =~# 'fish$'
    set shell=sh
endif

" set rtp+=~/.vim/bundle/Vundle.vim

" call vundle#begin() 

" call vundle#begin('~/Documents/vimplugins')

" }}}

" call vundle#end()

set exrc
set secure
set guifont=SauceCodePro\ Nerd\ Font\ Mono\ 11
set t_Co=256
set laststatus=2
set foldmethod=indent
set foldlevel=99
set nu rnu
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
let g:snipMate = { 'snippet_version' : 1 }
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

" Line Numbering Style --------------------- {{{
augroup numbertoggle
    autocmd!
    autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
    autocmd BufLeave,FocusLost,InsertEnter * set norelativenumber
augroup END
" }}}
