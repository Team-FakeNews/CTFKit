*****
Setup (and use) a development environment
*****

Install prerequisites
######################

* unittest : unit testing (no shit sherlock)
* sphinx : code documentation
* virtualenv : python environment handling
* pylint : keeping the code clean


Debian::
    sudo apt-get install sphinx pylint python3-venv
    pip3 install unittest


Setup Vim/Neovim
#################

If you're not using vim-plug yet::
    sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'

Then put this $MYVIMRC to get checks in your fav editor::
    " Install plugins
    call plug#begin('~/.local/share/nvim/plugged')
    Plug 'editorconfig/editorconfig-vim'
    Plug 'vim-scripts/pylint.vim'
    call plug#end()


Run tests
##########

A simple::
    python3 -m unittest discover

Should do the trick

