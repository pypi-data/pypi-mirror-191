import asyncio
import io
import subprocess


class SyncCmd:

    def ex(cmd, **kwargs):
        # universal_newlines = kwargs.get('universal_newlines', False)
        check = kwargs.get('check', False)
        shell = kwargs.get('shell', True)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(f"Cmd.ex_sync cmd = {cmd}")
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        xxx = subprocess.CompletedProcess(
                cmd, proc.returncode, proc.stdout, proc.stderr)
        if check and (proc.returncode != 0):
            raise subprocess.CalledProcessError(
                    proc.returncode, cmd, proc.stdout, proc.stderr)

        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(proc.stdout.decode())
        print(proc.stderr.decode())
        print(f"xxx = {xxx}")
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


class SyncArrCmd:

    def ex(a_cmd, **kwargs):
        for cmd in a_cmd:
            print("============================")
            print(f"ArrCmd.ex_sync cmd = {cmd}")
            print("============================")
            SyncCmd.ex(cmd, **kwargs)


class AsyncCmd:

    async def ex(cmd, **kwargs):
        universal_newlines = kwargs.get('universal_newlines', False)
        check = kwargs.get('check', False)
        # shell = kwargs.get('shell', False)
        proc = await asyncio.create_subprocess_shell(cmd)
        # stdout=asyncio.subprocess.PIPE,
        # stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()
        if universal_newlines:
            if stdout is not None:
                stdout = io.TextIOWrapper(io.BytesIO(stdout)).read()
            if stderr is not None:
                stderr = io.TextIOWrapper(io.BytesIO(stderr)).read()

        if check and (proc.returncode != 0):
            raise subprocess.CalledProcessError(
                    proc.returncode, cmd, stdout, stderr)

        return subprocess.CompletedProcess(
                 cmd, proc.returncode, stdout, stderr)


class AsyncArrCmd:

    async def ex(a_cmd, **kwargs):
        max_concurrent = kwargs.get('max_concurrent', 3)
        s_task = set()
        for cmd in a_cmd:
            print("============================")
            print(f"cmd = {cmd}")
            print("============================")
            if len(s_task) >= max_concurrent:
                # Wait for some task to finish before adding a new one
                _done, s_task = await asyncio.wait(
                    s_task, return_when=asyncio.FIRST_COMPLETED)
            task = asyncio.create_task(AsyncCmd.ex(cmd, **kwargs))
            s_task.add(task)

        # Wait for the remaining tasks to finish
        await asyncio.wait(s_task)
