### 1 Overview
This python module offers a framework which allows to execute given command in a modular fashion. 

### 2 Installation
#### 2.1 Setting Environment Variable
Before executing command you should set environment variable called "APP_RUNNER_ROOT_PATH" to the 
root directory of your python project.
```
APP_RUNNER_ROOT_PATH = /path/to/PYTHON_PROJECT_DIRECTORY
```

#### 2.2 Setting Directory Structure
Now we need to set the directory structure of our python project as shown below.
```
- PYTHON_PROJECT_DIRECTORY
  + modules
  - resources
    + commands
    + configs
```
For details about directory structure please refer to [Directory Structure](https://alperh.atlassian.net/wiki/spaces/APPRUNNER/pages/1848770580/User+Manual#2.2-Directory-Structure)

#### 2.3 Main Configuration
Main configuration is a yaml file which contains required configurations for command executor to run. Main configuration file name should be “main.config.yaml”.
```
- PYTHON_PROJECT_DIRECTORY
  - resources
    - configs
        main.config.yml
```

Main configuration file should have following content.
```yaml
application:
  name: Test Application
```
For details about main configuration please refer to [Main Configuration](https://alperh.atlassian.net/wiki/spaces/APPRUNNER/pages/1848770580/User+Manual#2.3-Main-Configuration)

#### 2.4 Generating Module
##### 2.4.1 Setting Directory Structure
Application expects module complies with following directory structure and files.
```
- PYTHON_PROJECT_DIRECTORY
  - modules
    - base
      - src
        + executor
      + commands
      base.settings.yaml  
```
#### 2.4.2 Adding Module Settings
We need to provide information about the module as shown below.

*base.settings.yaml*
```yaml
name: base
description: This is a test module.
version: 0.0.1
```

##### 2.4.2 Adding Command
We can define commands to be executed via a yaml file. System looks for yaml file “<COMMAND_ID>.yaml” in
“commands” directory in module’s root directory as shown below.
```
- PYTHON_PROJECT_DIRECTORY
  - modules
    - base    
      - commands
          cmd1.yaml
```
Command yaml file should comply with following structure.
```yaml
id: cmd1
title: Command 1
module: sample
executor: 
    class: TestCmdExecutor
    method: runCommand
```

#### 2.4.3 Generating Executor
With above configuration command executor framework will search and find TestCmdExector class in sample module. Once 
executor class is found, its given method "runCommand" will called.

We need to provide TestCmdExecutor class in following directory.

```
- PYTHON_PROJECT_DIRECTORY
  - modules
    - MODULE_NAME    
      - src
        - executor
            TestCmdExecutor
```

*TestCmdExecutor.py*
```python
from cmd_exec.classes.MarkupBuilder import MarkupBuilder
from cmd_exec.command.CmdResponse import CmdResponse
from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest

class TestCmdExecutor(CmdExecutor):

    def runCommand(self, request: CmdRequest) -> CmdResponse:
        response: CmdResponse = CmdResponse(True, 'view')
        builder: MarkupBuilder = MarkupBuilder()
        builder.addConstraintText("Hello World", 20)
        text = builder.getMarkupText()
        response.setContent(text)
        return response
```
For details about modules please refer to [Modules](https://alperh.atlassian.net/wiki/spaces/APPRUNNER/pages/1848770580/User+Manual#3-Modules)

#### 2.5 Initializing Command Executor Framework
Now we are all set with setting environment to executing command. Lets generate a python script which will initiate
command executor framework to execute a command with following content.

*run-command.py*
```python
from cmd_exec.app.CmdExecAppRunner import CmdExecAppRunner
CmdExecAppRunner.run()
```

#### 2.6 Executing Command
We can now execute command via command executor framework by calling python script generated in previous step.
Run above python script along with passing argument to identify the command to be executed.
```shell
python run-command.py -cmd base.cmd1
```

For details about other feature please refer to [Command Executor User Manual](https://alperh.atlassian.net/wiki/spaces/APPRUNNER/pages/1848770580/User+Manual#3-Modules)