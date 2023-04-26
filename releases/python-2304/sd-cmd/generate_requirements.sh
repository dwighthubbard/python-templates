#!/usr/bin/env bash
# Copyright 2023, Yahoo Inc.
# Licensed under the terms of the Apache 2.0 license.  See the LICENSE file in the project root for termsnamespace: python-2304

if [ "${GEN_REQUIREMENTS_SRC_FILES}" = "" ]; then
    if [ -e "requirements.in" ]; then
        GEN_REQUIREMENTS_SRC_FILES="requirements.in"
    fi
fi

if [ ! -e "setup.py" ]; then
    REMOVE_SETUPPY="True"
    cat << EOF > setup.py
#!/usr/bin/env python3
import setuptools
setuptools.setup()
EOF
    chmod 755 setup.py
fi

${BASE_PYTHON_BIN}/pypirun pip-tools pip-compile -o requirements.txt --generate-hashes --allow-unsafe ${GEN_REQUIREMENTS_SRC_FILES}

if [ "$REMOVE_SETUPPY" = "True" ]; then
    rm setup.py
fi

mkdir -p "${SD_ARTIFACTS_DIR}/config"
cp requirements.txt "${SD_ARTIFACTS_DIR}/config"
