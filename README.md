# Fun with yjs, pycrdt and litestar

An example app illustrating how to use Litestar, yjs, and pycrdt together for collaborative editing.

Give it a whirl by running the tests (uses Playwright):

    $ poetry install
    $ poetry run playwright install-deps
    $ poetry run playwright install
    $ npm install
    $ npx webpack --mode=development
    $ poetry run pytest

Or run it locally:

    $ docker run --rm -p 6379:6379 -d redis:7
    $ poetry run example-app run

Then open two different tabs and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).