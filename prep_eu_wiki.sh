#!/bin/bash

wget https://dumps.wikimedia.org/euwiki/latest/euwiki-latest-pages-articles.xml.bz2
bzip2 -d euwiki-latest-pages-articles.xml.bz2
git clone https://github.com/attardi/wikiextractor.git
./wikiextractor/WikiExtractor.py euwiki-latest-pages-articles.xml -o eu-wiki-docs -de gallery,timeline,noinclude,ref,div,center,nowiki,br,poem,table,pre,mapframe -it abbr,b,big,sup,span,blockquote,small,sub,u,font,li,chem,p,strong,i
cat eu-wiki-docs/*/* > eu-wiki.txt
sed -i '/<noinclude>/d' eu-wiki.txt
sed -i '/<br>/d' eu-wiki.txt
sed -i '/<onlyinclude>/d' eu-wiki.txt
sed -i '/<br clear=left>/d' eu-wiki.txt
sed -i '/<TR>/d' eu-wiki.txt
sed -i '/<doc/d' eu-wiki.txt
sed -i '/<\/doc/d' eu-wiki.txt
sed -i '/^$/d' eu-wiki.txt
