# Fun with yjs, pycrdt and litestar

An example app illustrating how to use Litestar, yjs, and pycrdt together for collaborative editing.

Assuming you have Docker installed, give it a whirl by running:

    $ docker-compose up

Then open two different tabs and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

Or run the tests using [Dagger](https://docs.dagger.io) and [Playwright](https://playwright.dev/python/docs/intro).

    $ pip install dagger-io
    $ dagger run python CI.py
