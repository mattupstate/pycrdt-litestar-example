# Fun with yjs, pycrdt and litestar

An example app illustrating how to use Litestar, yjs, and pycrdt together for collaborative editing.

Give it a whirl by running:

    $ docker-compose up

Then open two different tabs and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

Or run the tests that use [testcontainers](https://testcontainers-python.readthedocs.io/en/latest/README.html) and [Playwright](https://playwright.dev/python/docs/intro):

    $ poetry install
    $ poetry run playwright install-deps
    $ poetry run playwright install
    $ npm install
    $ npx webpack --mode=development
    $ poetry run pytest
