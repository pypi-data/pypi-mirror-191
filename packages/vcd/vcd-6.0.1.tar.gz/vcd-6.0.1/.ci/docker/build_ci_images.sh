#! /bin/bash

py_versions=( 3.7 3.8 3.9 3.10 3.11 )


for py in "${py_versions[@]}"
do
    echo "Building image with Python version: ${py}"
    docker build --build-arg PYTHON_VERSION=${py} -t registry.gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/vcd_ci:py_${py} .
    docker push registry.gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/vcd_ci:py_${py}
done

echo "Building image for pre-commit jobs"
docker build -f dockerfile_precommit -t registry.gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/vcd_pre_commit .
docker pull registry.gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/vcd_pre_commit
