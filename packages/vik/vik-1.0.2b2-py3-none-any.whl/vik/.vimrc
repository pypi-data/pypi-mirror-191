set nocompatible
set noswapfile
set nobackup

set belloff=all

set ignorecase
set smartcase

set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set smarttab
set smartindent

set linebreak

set mouse=a
set backspace=2

set binary
set autoread

nnoremap <F2> :set invpaste paste?<CR>
set pastetoggle=<F2>
set showmode

nnoremap <F3> :set invhlsearch<CR>

nnoremap <F4> :set number!<CR>

command! -nargs=* Encrypt w !kek encrypt <args> -p 1> %
command! -nargs=* Decrypt w !kek decrypt <args> -p 1> % 
command! Commit !git add % && git commit -m "%"

set langmap=ФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯ;ABCDEFGHIJKLMNOPQRSTUVWXYZ,фисвуапршолдьтщзйкыегмцчня;abcdefghijklmnopqrstuvwxyz
