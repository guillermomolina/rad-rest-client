# Remote debug with vscode

- Install debugpy in remote virtualenv 

```bash
(virtualenv)me@remote $ pip install debugpy
```

- Create launch configuration in vscode

```json
        {
            "name": "Python: Attach remote",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "hostname",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "remote_host_project_dir"
                }
            ],
            "redirectOutput": true
        }
```

- Launch tool with debug parameter in remote virtualenv

```bash
(virtualenv)me@remote $ tool -D ls
```

- Launch debug config in vscode



