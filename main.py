import csv
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

#Gerar pergunta Multichoice
def criarPerguntaMultichoice(root, nome, texto, respostas, resposta_correta, shuffle):
    tipo_questao = ET.SubElement(root, "question", attrib={"type": "multichoice"})

    name = ET.SubElement(tipo_questao, "name")
    text = ET.SubElement(name, "text")
    text.text = nome

    formato_questao = ET.SubElement(tipo_questao, "questiontext", attrib={"format": "html"})
    pergunta_text = ET.SubElement(formato_questao, "text")
    pergunta_text.text = texto

    shuffle_element = ET.SubElement(tipo_questao, "shuffleanswers")
    shuffle_element.text = str(shuffle).lower()

    for resposta in respostas:
        answer = ET.SubElement(tipo_questao, "answer", attrib={
            "fraction": "100" if resposta == resposta_correta else "0"
        })
        text_answer = ET.SubElement(answer, "text")
        text_answer.text = resposta

#Gerar pergunta True or False
def criarPerguntaTrueFalse(root, nome, texto, resposta_correta, shuffle):
    tipo_questao = ET.SubElement(root, "question", attrib={"type": "truefalse"})

    name = ET.SubElement(tipo_questao, "name")
    text = ET.SubElement(name, "text")
    text.text = nome

    formato_questao = ET.SubElement(tipo_questao, "questiontext", attrib={"format": "html"})
    pergunta_text = ET.SubElement(formato_questao, "text")
    pergunta_text.text = texto

    shuffle_element = ET.SubElement(tipo_questao, "shuffleanswers")
    shuffle_element.text = str(shuffle).lower()

    for resposta in ["true", "false"]:
        answer = ET.SubElement(tipo_questao, "answer", attrib={
            "fraction": "100" if resposta == resposta_correta.lower() else "-25"
        })
        text_answer = ET.SubElement(answer, "text")
        text_answer.text = resposta

root = ET.Element("quiz")

with open("quiz.csv", "r", encoding="utf-8") as ficheiro:
    linhas = csv.reader(ficheiro)
    next(linhas) #SKIPPAR CABECALHO

    for linha in linhas:
        dificuldade, tipo, nome, texto, respostas, resposta_correta, pontos_dados, pontos_tirados = linha
        respostas_lista = respostas.split(";")

        if tipo == "multichoice":
            criarPerguntaMultichoice(root, nome, texto, respostas_lista, resposta_correta, True)
        elif tipo == "truefalse":
            criarPerguntaTrueFalse(root, nome, texto, resposta_correta, True)

#FORMATAR XML
xml_string = ET.tostring(root, encoding="utf-8")
xml_formatado = parseString(xml_string).toprettyxml(indent="  ")

xml_formatado = "\n".join(xml_formatado.split("\n")[1:])

with open("quiz.xml", "w", encoding="utf-8") as xml_file:
    xml_file.write(xml_formatado)
