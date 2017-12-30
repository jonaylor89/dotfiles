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
Plugin 'joshdick/onedark.vim'
Plugin 'vim-syntastic/syntastic'
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'tpope/vim-fugitive'
Plugin 'ryanoasis/vim-devicons'
"Plugin 'majutsushi/tagbar'
" }}}

call vundle#end()

set exrc
set secure
set guifont=Droid\ Sans\ Mono\ Nerd\ Font\ 11
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
let g:airline_theme='murmur'
let g:airline_powerline_fonts=1
let g:airline#extensions#tabline#enabled=1
let g:ycm_autoclose_preview_window_after_competion=1

" General mappings ------------{{{
map <leader>g :YcmCompleter GoToDefinitionElseDeclaration<CR>
map <leader>n <plug>NERDTreeTabsToggle<CR>
map <F5> :!gcc % && ./a.out<CR>
" }}}

" normal mode mappings----------------{{{
nnoremap <Up> <nop>
nnoremap <Down> <nop>
nnoremap <Right> <nop>
nnoremap <Left> <nop>
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
nnoremap <space> za
nnoremap <F5> :!gcc % && ./a.out<CR>
nnoremap <leader>ev :vsplit $MYVIMRC<CR>
nnoremap <leader>sv :source $MYVIMRC<CR>
nnoremap <S-Up> <C-Y>
nnoremap <S-Down> <C-E>
"nnoremap <F8> :TagbarToggle<cr>
" }}}

" Insert mode mappings ----------------------{{{
inoremap jk <esc>
inoremap <esc> <nop>
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

" Autocommands for commenting code ------------------{{{
augroup Comments
	autocmd!
	autocmd FileType java nnoremap <buffer> <leader>c I//<esc>
	autocmd FileType python nnoremap <buffer> <leader>c I#<esc>
augroup END
" }}}

" Autocommands for logical statements in code -------------{{{
augroup ifstatement
	autocmd!
	autocmd FileType python iabbr <buffer> iff if:<left>
	autocmd FileType java iabbr <buffer> iff if()<left>
augroup END
" }}}





















