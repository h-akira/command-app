# command-app
## 環境構築
パスを通すため以下を`.zshrc`などに追記
```
export PATH=$PATH:"${cloneした場所}/command-app/bin"
```
python
```
pip3 install pyPDF2
pip3 install numpy
pip3 install Pillow
pip3 install img2pdf
```
その他
```
# Mac
brew install imagemagick
brew install ghostscript
# Linux(Debian系)
sudo apt install imagemagick
sudo apt install ghostscript 
```
