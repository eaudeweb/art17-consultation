#!/bin/bash

xsltproc --stringparam countrycode RO \
--stringparam dataset 1 \
--stringparam role 'assessment' \
 art17-species-sql-update.xsl $1
