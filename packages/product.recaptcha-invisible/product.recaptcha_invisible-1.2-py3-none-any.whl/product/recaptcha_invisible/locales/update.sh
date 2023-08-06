#!/bin/bash

domain=product.recaptcha_invisible
bin_path=/opt/Plone-5.2/zeocluster/bin
languages=("es" "en" "ca")

$bin_path/i18ndude rebuild-pot --pot $domain.pot --merge manual.pot --create $domain ../

for language in "${languages[@]}"
do
  if [ ! -e $language ]; then
    mkdir $language
  fi
  if [ ! -e $language/LC_MESSAGES ]; then
    mkdir $language/LC_MESSAGES
  fi
  if [ ! -e $language/LC_MESSAGES/$domain.po ]; then
    touch $language/LC_MESSAGES/$domain.po
  fi
  $bin_path/i18ndude sync --pot $domain.pot $language/LC_MESSAGES/$domain.po
done
