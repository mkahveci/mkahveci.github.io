echo 'Killing all Jekyll instances'
kill -9 $(ps aux | grep '[j]ekyll' | awk '{print $2}')
clear

echo "Building PDF-friendly HTML site for CHE 135 ...";
bundle exec jekyll serve --detach --config _config.yml,pdfconfigs/config_che135_pdf.yml;
echo "done";

echo "Building the PDF ...";
prince --javascript --input-list=_site/pdfconfigs/prince-list.txt -o pdf/CHE135.pdf;
echo "done";
