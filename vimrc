set nocompatible 
filetype off 

set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin() 

call vundle#begin('~/Documents/vimplugins')

" Installed Plugins -------------------{{{
Plugin 'gmarik/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
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
Plugin 'majutsushi/tagbar'
Plugin 'rust-lang/rust.vim'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'MarcWeber/vim-addon-mw-utils'
Plugin 'tomtom/tlib_vim'
Plugin 'garbas/vim-snipmate'
Plugin 'honza/vim-snippets'
Plugin 'christoomey/vim-tmux-runner'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'ryanoasis/vim-devicons'
" }}}

call vundle#end()

set exrc
set secure
set guifont=3270Medium\ Nerd\ Font\ Mono\ 11
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

filetype plugin indent on
syntax enable

colorscheme onedark

let python_highlight_all=1
let NERDTreeIgnore=['\.pyc$', '\~$', '\.out$', 'node_modules$', '__pycache__$']
let g:rustfmt_autosave=1
let g:airline_theme='murmur'
let g:airline_powerline_fonts=1
let g:airline#extensions#tabline#enabled=1
let g:ycm_autoclose_preview_window_after_competion=1
let g:VtrStripLeadingWhitespace = 0
let g:VtrClearEmptyLines = 0
let g:VtrAppendNewline = 1

" General mappings ------------{{{
map <leader>g :YcmCompleter GoToDefinitionElseDeclaration<CR>
map <leader>n <plug>NERDTreeTabsToggle<CR>
map <leader>t :TagbarToggle<cr>
" }}}

imap <C-Z> <Plug>snipMateNextOrTrigger
smap <C-Z> <Plug>snipMateNextOrTrigger


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
    autocmd FileType c imap <F5> <ESC>:w<CR>:!clear;gcc % && ./a.out<CR>
augroup END
" }}}
