import os
from re import split
import pandas as pd
from dotenv import load_dotenv
from random import random

class blastp:
    def __init__(self):#Use enviroment variables
        load_dotenv(dotenv_path=".env")

    def save_fasta(self, id, sequence, fasta_path, keep_fasta = False):#Save a fasta file in fasta_path
        f = open(fasta_path, "w")
        f.write(">{}\n{}".format(id, sequence))
        f.close()

    def execute_blastp(self, fasta_path, db, output_path):#Run blastp against selected database
        if db in ["pdbaa", "swissprot"]:
            os.system("{blastp} -db {db}/{db} -query {fasta_path} > {output_path}".format(
                blastp = os.getenv("BLASTP"), 
                db = db,
                fasta_path = fasta_path,
                output_path = output_path))
            f = open(output_path)
            text = f.read()
            f.close()
            return text

    def parse_response(self, res):
        inicio = res.find("Value") + 7
        text = res[inicio:]
        fin = text.find("\n\n")
        text = text[:fin]
        splitted = [row for row in text.splitlines() if row != ""]
        data = []
        for row in splitted:
            row_splitted = [a for a in split("\s+", row) if a != ""]
            data.append([row_splitted[0], float(row_splitted[-2]), float(row_splitted[-1])])
        new_text = [row.strip() for row in res[inicio+fin:].split("\n>") if row.strip() != '']
        df = pd.DataFrame(data, columns = ["id", "score", "e_value"])
        for index, row in enumerate(new_text):
            details_inicio = row.find("Identities =")
            details_final = row.find("\n\nQuery")
            details_text = row[details_inicio:details_final]
            row_details = []
            for detail in details_text.split(","):
                per_inicio = detail.find("(")
                percentaje = detail[per_inicio+1:-1]
                float_percentaje = float(percentaje.replace("%", ""))/100
                row_details.append(float_percentaje)
            df.loc[index,"identity"] = row_details[0]
            df.loc[index,"similarity"] = row_details[1]
            df.loc[index,"gaps"] = row_details[2]
        return df

    def run_blast(self, id, sequence, database, parse_response = True):
        fasta_path = str(round(random()*10**20)) + ".fasta"
        output_path = str(round(random()*10**20)) + ".blast"
        self.save_fasta(id, sequence, fasta_path)
        res = self.execute_blastp(fasta_path, database, output_path)
        os.remove(fasta_path)
        os.remove(output_path)
        if parse_response:
            return self.parse_response(res)
        return res
        

if __name__ == "__main__":
    id = ">sp|P40337|VHL_HUMAN"
    sequence = """MPRRAENWDEAEVGAEEAGVEEYGPEEDGGEESGAEESGPEESGPEELGAEEEMEAGRPR
    PVLRSVNSREPSQVIFCNRSPRVVLPVWLNFDGEPQPYPTLPPGTGRRIHSYRGHLWLFR
    DAGTHDGLLVNQTELFVPSLNVDGQPIFANITLPVYTLKERCLQVVRSLVKPENYRRLDI
    VRSLYEDLEDHPNVQKDLERLTQERIAHQRMGD"""

    bp = blastp()
    df = bp.run_blast(id, sequence, "swissprot")
    print(df)
