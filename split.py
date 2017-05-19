from lxml import etree
import os
import sys
import random
import shutil

class QAPairs:
    def __init__(self, id):
        self.id = id
        self.question = ""
        self.answers = []
    def addQuestion(self, question):
        self.question = question

    def addAnswer(self, answer, is_positive):
        self.answers.append((is_positive, answer))

    def addAllAnswers(self, answers):
        self.answers = answers

def split(filename):
    list_questions = []

    root = etree.parse(filename)

    qid = 0
    question = QAPairs(qid)
    for element in root.iter():
        if element.tag == "subject":
            if qid != 0:
                list_questions.append(question)

            qid+=1
            question = QAPairs(qid)
            question.addQuestion(element.text)


        elif element.tag == "bestanswer":
            best_ans = element.text
            question.addAnswer(element.text, True)
            best_answered = True

        elif element.tag == "answer_item":
            if element.text != best_ans:
                question.addAnswer(element.text, False)

    return list_questions

def save_to_file(file_obj, qa_list):
    for qa_pair in qa_list:
        file_obj.write("<QApairs id='%s'>\n"%qa_pair.id)
        file_obj.write("<question>\n")
        file_obj.write(qa_pair.question.encode("utf-8")+"\n")
        file_obj.write("</question>\n")

        for answer in qa_pair.answers:
            if answer[0]:
                file_obj.write("<positive>\n")
		print answer[0]
                file_obj.write(answer[1].encode("utf-8")+"\n")
                file_obj.write("</positive>\n")
            else:
                file_obj.write("<negative>\n")
                file_obj.write(answer[1].encode("utf-8")+"\n")
                file_obj.write("</negative>\n")
        file_obj.write("</QApairs>\n")

if __name__ == "__main__":
    name = sys.argv[1:][0]

    result = split(name)
    len_ext = len(name) - len('.xml')
    folder_name = name[:len_ext]
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.makedirs(folder_name)

    random.shuffle(result)

    train_file_obj = open(os.path.join(folder_name, 'train.xml'), "w")
    test_file_obj = open(os.path.join(folder_name, 'test.xml'), "w")
    dev_file_obj= open(os.path.join(folder_name, 'dev.xml'), "w")

    num_train = int(len(result)*0.7)
    num_dev = int(len(result)*0.15)
    save_to_file(train_file_obj, result[:num_train])
    save_to_file(dev_file_obj, result[num_train:num_train + num_dev])
    save_to_file(test_file_obj, result[num_train+num_dev:])
