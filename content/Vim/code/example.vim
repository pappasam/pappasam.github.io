function! ToggleRelativeNumber()
  if &rnu
    set norelativenumber
  else
    set relativenumber
  endif
endfunction

function! RNUInsertEnter()
  if &rnu
    let w:line_number_state = 'rnu'
    set norelativenumber
  else
    let w:line_number_state = 'nornu'
  endif
endfunction

function! RNUInsertLeave()
  if w:line_number_state == 'rnu'
    set relativenumber
  else
    set norelativenumber
    let w:line_number_state = 'nornu'
  endif
endfunction

function! RNUWinEnter()
  if exists('w:line_number_state')
    if w:line_number_state == 'rnu'
      set relativenumber
    else
      set norelativenumber
    endif
  else
    set relativenumber
    let w:line_number_state = 'rnu'
  endif
endfunction

function! RNUWinLeave()
  if &rnu
    let w:line_number_state = 'rnu'
  else
    let w:line_number_state = 'nornu'
  endif
  set norelativenumber
endfunction

" autocmd that will set up the w:created variable
autocmd VimEnter * autocmd WinEnter * let w:created=1
autocmd VimEnter * let w:created=1
set number relativenumber
augroup rnu_nu
  autocmd!
  "Initial window settings
  autocmd WinEnter * if !exists('w:created') |
        \setlocal number relativenumber |
        \endif
  autocmd User Startified setlocal number relativenumber
  " Don't have relative numbers during insert mode
  autocmd InsertEnter * :call RNUInsertEnter()
  autocmd InsertLeave * :call RNUInsertLeave()
  " Set and unset relative numbers when buffer is active
  autocmd WinEnter * :call RNUWinEnter()
  autocmd WinLeave * :call RNUWinLeave()
augroup end
