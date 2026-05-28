#!/bin/sh
# ident @(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
git config filter.ident-dynamic.clean "python3 local_tools/git-ident-filter.py clean"
git config filter.ident-dynamic.smudge "python3 local_tools/git-ident-filter.py smudge %f"
git config log.date "format:%Y/%m/%d %H:%M:%S"
echo "✅ Filtres Git configurés avec succès pour Unix / WSL."

