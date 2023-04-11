import os
import sys
import subprocess

# Este código é um script em Python que tem a finalidade de instalar as dependências necessárias para a execução de um programa chamado "JuliaTHREAD" e, em seguida, executá-lo.


script_path = os.path.dirname(__file__)
index_url = os.environ.get('INDEX_URL', "")
python = sys.executable

# A variável "skip_install" é usada para pular a instalação de dependências se ela já tiver sido feita anteriormente.
skip_install = False


# A função "run" é usada para executar comandos do sistema operacional, permitindo que o script execute comandos como se estivesse sendo executado em um terminal.
def run(command, desc=None, errdesc=None, custom_env=None, live=False):
    if desc is not None:
        print(desc)

    if live:
        result = subprocess.run(command, shell=True, env=os.environ if custom_env is None else custom_env)
        if result.returncode != 0:
            raise RuntimeError(f"""{errdesc or 'Error running command'}.
Command: {command}
Error code: {result.returncode}""")

        return ""

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ if custom_env is None else custom_env)

    if result.returncode != 0:

        message = f"""{errdesc or 'Error running command'}.
Command: {command}
Error code: {result.returncode}
stdout: {result.stdout.decode(encoding="utf8", errors="ignore") if len(result.stdout)>0 else '<empty>'}
stderr: {result.stderr.decode(encoding="utf8", errors="ignore") if len(result.stderr)>0 else '<empty>'}
"""
        raise RuntimeError(message)

    return result.stdout.decode(encoding="utf8", errors="ignore")

# A função "run_pip" usa o pip para instalar as dependências especificadas em um arquivo de requisitos (por padrão, "requirements_versions.txt").
def run_pip(args, desc=None):
    if skip_install:
        return

    index_url_line = f' --index-url {index_url}' if index_url != '' else ''
    return run(f'"{python}" -m pip {args} --prefer-binary{index_url_line}', desc=f"Installing {desc}", errdesc=f"Couldn't install {desc}")

# A função "prepare_environment" é chamada no início do programa para instalar as dependências necessárias e configurar o ambiente.
def prepare_environment():
    global skip_install

    requirements_file = os.environ.get('REQS_FILE', "requirements_versions.txt")

    print(f"Python {sys.version}")

    if not os.path.isfile(requirements_file):
        requirements_file = os.path.join(script_path, requirements_file)
    run_pip(f"install -r \"{requirements_file}\"", "requirements for VENV")


# No final, se o arquivo for executado diretamente,
# a função "prepare_environment" é chamada para configurar o ambiente e, em seguida, 
# o módulo "JuliaTHREAD" é importado e executado através da função "Start()".
if __name__ == "__main__":
    prepare_environment()
    import JuliaTHREAD
    JuliaTHREAD.call()