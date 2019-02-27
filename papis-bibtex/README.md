# Papis bibTeX

This is a python papis script to interact with a `bib` file
of any kind, it is still in experimental phase but it's highly hackable.

## Informal explanation

```
papis bibtex                            \
  read new_papers.bib                   \ # Read bib file
  cmd 'papis add --from-doi {doc[doi]}'   # For every entry run the command
```
I use it for opening some papers for instance
```
papis bibtex read new_papers.bib open
```
or to add papers to the bib
```
papis bibtex          \
  read new_papers.bib \ # Read bib file
  add einstein        \ # Pick a document with query 'einstein' from library
  add heisenberg      \ # Pick a document with query 'heisenberg' from library
  save new_papers.bib   # Save in new_papers.bib
```

or if I update some information in my papis `yaml` files then I can do
```
papis bibtex          \
  read new_papers.bib \ # Read bib file
  update -f           \ # Update what has been read from papis library
  save new_papers.bib   # save everything to new_papers.bib, overwriting
```

Maybe this is also interesting for you guys!

## Vim integration

Right now, you can easily use it from vim with these simple lines

```vimscript
function! PapisBibtexRef()
  let l:temp = tempname()
  echom l:temp
  silent exec "!papis bibtex ref -o ".l:temp
  let l:olda = @a
  let @a = join(readfile(l:temp), ',')
  normal! "ap
  redraw!
  let @a = l:olda
endfunction

command! -nargs=0 BibRef call PapisBibtexRef()
command! -nargs=0 BibOpen exec "!papis bibtex open"
```

And use like such:
[![asciicast](https://asciinema.org/a/8KbLQJSVYVYNXHVF3wgcxx5Cp.svg)](https://asciinema.org/a/8KbLQJSVYVYNXHVF3wgcxx5Cp)
