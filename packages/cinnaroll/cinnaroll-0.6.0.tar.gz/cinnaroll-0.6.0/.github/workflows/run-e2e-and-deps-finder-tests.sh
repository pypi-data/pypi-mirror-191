#!/bin/bash

find tests -regextype posix-extended -regex "tests/(e2e|infer_func_deps_finder)/test.*py" -print0 | while read -d $'\0' test_file
  do
    test_module=$(echo "$test_file" | rev | cut -c4- | rev | tr "/" ".")
    echo "Running test: $test_module"

    if ! python -m "$test_module"; then
      echo "$test_file" >> failed_tests.txt
    fi
  done

if [[ -f "failed_tests.txt" ]]; then
  echo "The following tests failed:"
  cat failed_tests.txt
  exit 1
fi
