# Building

Build the ARM64 lambda ready to deploy:

- create virtualenv

    ```bash
    deactivate
    cd <example_directory>
    python3.<your_python_version> -m venv .venv
    source .venv/bin/activate
    ```

- build lambda

    ```bash
      make build
    ```

For example, if you want to build `multithreading` example with `python3.12`:

- create virtualenv

    ```bash
    deactivate
    cd multithreading
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```

- build lambda

    ```bash
    make build
    ```

This lambda is over the GUI upload limit in the console, so you will have to use an S3 bucket.
