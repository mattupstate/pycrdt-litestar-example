#!/usr/bin/env python

import sys

import anyio
import dagger

from .app import AppPipelineTasks


async def pipeline():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        pipeline = AppPipelineTasks(client)
        webpack_build_output_dir = await pipeline.webpack()
        await pipeline.test(webpack_build_output_dir)

    print("CI Pipeline finished!")


if __name__ == "__main__":
    anyio.run(pipeline)
