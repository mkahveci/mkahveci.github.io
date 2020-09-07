echo 'Killing all Jekyll instances'
kill -9 $(ps aux | grep '[j]ekyll' | awk '{print $2}')
clear

echo "Building PDF-friendly HTML site for Murat Kahveci's CV ...";
bundle exec jekyll serve --detach --config _config.yml,pdfconfigs/config_murat_pdf.yml;
echo "done";

echo "Building the PDF ...";
prince --javascript --input-list=_site/pdfconfigs/prince-list.txt -o pdf/cv_murat_kahveci.pdf;
echo "done";
