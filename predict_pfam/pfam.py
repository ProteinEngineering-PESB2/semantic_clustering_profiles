from random import random
import os
import subprocess
import time
import pandas as pd
import re
import json
from modules.utils import config_tool

class pfam():
    def __init__(self):
        pass


    def save_fasta(self, id, sequence, fasta_path, keep_fasta = False):#Save a fasta file in fasta_path
        f = open(fasta_path, "w")
        f.write(">{}\n{}".format(id, sequence))
        f.close()

    def process(self, fasta_path, output_path):
        os.system("pfam_scan.pl -dir /app/install_requisites/databases/ -fasta {} > {}".format(fasta_path, output_path))
        f = open(output_path, "r")
        text = f.read().split("\n\n")[-1]
        f.close()
        data = []
        for i in text.splitlines():
            result = re.sub('\s+','\t', i).strip()
            data.append(result.split("\t"))
        dataset = pd.DataFrame(data, 
        columns = ["seq_id", "alignment_start", "alignment_end",
        "envelope_start", "envelope_end", "hmm_acc", "hmm_name", 
        "type", "hmm_start", "hmm_end", "hmm_length", "bit_score", 
        "e-value", "clan", "predicted_active_site_residues"])
        dataset = dataset[["seq_id", "hmm_acc", "hmm_name", "type", 
        "bit_score", "e-value"]]
        dataset.rename(columns = {"hmm_acc": "Id_accession", "hmm_name":"Pfam", 
        "bit_score": "Bitscore", "type": "Class", "e-value": "Evalue", 
        "hmm_name": "Accession"}, inplace=True)
        dataset["Type"] = ""
        json_dataset = json.loads(dataset.to_json(orient="records"))
        response = []
        for id in dataset.seq_id.unique():
            response_dict = {}
            response_dict["id"] = id
            response_dict["data"] = []
            for j in json_dataset:
                if (j["seq_id"] == id):
                    dict_copy = j.copy()
                    dict_copy.pop("seq_id")
                    response_dict["data"].append(dict_copy)
            response.append(response_dict)
        return response

    def run_pfam(self, id, sequence):
        fasta_path = str(round(random()*10**20)) + ".fasta"
        output_path = str(round(random()*10**20)) + ".blast"
        self.save_fasta(id, sequence, fasta_path)
        result = self.process(fasta_path, output_path)
        os.remove(fasta_path)
        os.remove(output_path)
        return result

if __name__ == "__main__":
    id = "sp|P40337|VHL_HUMAN"
    sequence = """MPRRAENWDEAEVGAEEAGVEEYGPEEDGGEESGAEESGPEESGPEELGAEEEMEAGRPR
PVLRSVNSREPSQVIFCNRSPRVVLPVWLNFDGEPQPYPTLPPGTGRRIHSYRGHLWLFR
DAGTHDGLLVNQTELFVPSLNVDGQPIFANITLPVYTLKERCLQVVRSLVKPENYRRLDI
VRSLYEDLEDHPNVQKDLERLTQERIAHQRMGD"""
    pf = pfam()
    df = pf.run_pfam(id, sequence)
    print(df)
