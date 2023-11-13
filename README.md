# Iteration Shell Script Generator

## help
```
usage: itshellgen.py [-h] [--iter Key Loop] [--before Key 'Command'] [--after Key 'Command'] [--begin ['Command']] [--end ['Command']] [--shebang ['Shebang Command']] [--parallel [int]]
                     [--out [FileName]] [--version]
                     cmd

Example:
    prog.py "bc #M# + #N#" --iter M 2..=5 --iter N 7,8,9

positional arguments:
  cmd                   Comamnd (PlaceHolder #key#) (required)

options:
  -h, --help            show this help message and exit

  --iter Key Loop       Set Iteration
                        Loop Example
                            N : range(0, N)
                            M..N : range(M, N)
                            M..=N : range(M, N+1)
                            A,B,C : [A,B,C]

  --before Key 'Command'
                        Exec Before Iteration Command

  --after Key 'Command'
                        Exec After Iteration Command

  --begin ['Command']   Exec Start of Shell Script Command

  --end ['Command']     Exec End of Shell Script Command

  --shebang ['Shebang Command']
                        Shebang (default: #!/bin/bash)

  --parallel [int]      Parallel Number [int]

  --out [FileName]      Output FileName (Default: StdOut)
                        Empty Name is named "YYYYMMDD-HHMMSS"

  --version             show program's version number and exit
```