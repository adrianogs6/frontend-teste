from typing import Sized
import PySimpleGUI as sg
import os
import subprocess
import sys
from tkinter import filedialog
import glob
import re


def getProjectName(projectPath):
    return os.path.basename(os.path.normpath(projectPath))

def getTestFilesFromProject(projectPath):
    # https://junit.org/junit5/docs/current/user-guide/#running-tests-build-maven-filter-test-class-names
    arr = glob.glob(f'{projectPath}/**/Test*.java', recursive=True)
    arr.extend(glob.glob(f'{projectPath}/**/*Test.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/**/*Tests.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/**/*TestCase.java', recursive=True))
    return arr

def codeFormat(code):

    return re.compile(r"\s+").sub(" ", code).strip()

def defineAppendWrite(fileName):

    if os.path.exists(fileName):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    return append_write

def openAndWriteInFile(fileName, append_write, code):
    f = open(fileName, append_write)
    f.write(code)
    f.close()

def parameterizer(projectPath, entity):
    projectName = getProjectName(projectPath)
    try:
        os.makedirs("input/{}_v1".format(projectName))
    except OSError as exc:  # Python ≥ 2.5
        pass
    fileName = "input/{}_v1/{}-{}.txt".format(projectName,projectName, entity)
    indexTestFilesPaths = "{}/{}-indexTestFilesPaths.txt".format(projectPath, projectName)
    arr = getTestFilesFromProject(projectPath+'/**/src/test/java')

    for fileTest in arr:

        f = open(fileTest, "r")

        code = codeFormat(f.read()) + '\n'

        append_write = defineAppendWrite(fileName)
        openAndWriteInFile(fileName, append_write, code)

        append_write = defineAppendWrite(indexTestFilesPaths)
        testFile = os.path.relpath(fileTest, projectPath) + '\n'
        openAndWriteInFile(indexTestFilesPaths, append_write, testFile)
        f.close()


class TelaFastR:
    def __init__(self):
        layout=[
            [sg.Text('1.Escolha o cenario :')],
            [sg.Radio('Budget Scenario','experimento',key='budget'),sg.Radio('Adequate Scenario','experimento',key='adequate')],

            [sg.Text('2.Escolha a cobertura :')],
            [sg.Radio('Function','coverage',key='function'),
            sg.Radio('Line','coverage',key='line'),
            sg.Radio('Branch','coverage',key='branch')],

            [sg.Text('3.Escolha o projeto e versão :')],
            [sg.Combo(['Flex v3', 'GrepV3', 'Gzip v1', 'Make v1', 'Sed v6', 'Chart v0', 'Closure v0', 'Lang v0', 'MAth v0', 'Time v0'], '', key='combo')],



            [sg.Button('Executar teste')]
        ]
        self.janela = sg.Window("Dados Usuario").layout(layout)

    def Iniciar(self):
        while True:

            cenario = ""
            cobertura = ""
            projeto = ""
            self.button, self.values = self.janela.Read()
            repeticao = self.values['repeticao']

            budget = self.values['budget']
            adequate = self.values['adequate']

            function = self.values['function']
            line = self.values['line']
            branch = self.values['branch']

            flex = self.values['flex']
            grep = self.values['grep']
            gzip = self.values['gzip']
            make = self.values['make']
            sed = self.values['sed']
            chart = self.values['chart']

            if(budget == True):
                cenario = "experimentBudget.py"
            elif(adequate == True):
                cenario = "experimentAdequate.py"

            if(function == True):
                cobertura = "function"
            elif(line == True):
                cobertura = "covarege"
            elif(branch == True):
                cobertura = "branch"

            if(flex == True):
                projeto = "TestParameterInjector v1"
                # projeto = "flex v3"
            elif(grep == True):
                projeto = "grep v3"
            elif(gzip == True):
                projeto = "gzip v1"
            elif(chart == True):
                projeto = "chart v0"
           
            if(self.button == '2'):
               fileNames = filedialog.askdirectory()
               print(fileNames)
               parameterizer(fileNames,"bbox")
           
            # executarCmd = f'py py/{cenario} {cobertura} {projeto} {repeticao}'
            executarCmd = f'py py/{cenario} {cobertura} {projeto}'
            print(executarCmd)
           # os.system('py experimentBudget.py function flex v3 10')
           # subprocess.run(['py experimentBudget.py function flex v3 10'], stderr=sys.stderr, stdout=sys.stdout)
            process = subprocess.Popen(executarCmd, stdout=subprocess.PIPE)
            output, error = process.communicate()

            if(process.returncode == 0):
                print("Done:")
            else:
                print("Failed:")

            print(output)
            # print(self.values)


tela = TelaFastR()
tela.Iniciar()