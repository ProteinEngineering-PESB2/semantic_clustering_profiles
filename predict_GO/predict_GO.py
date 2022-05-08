import pandas as pd
from random import random
import os

class gene_ontology:
    def __init__(self):
        pass

    def save_fasta(self, id, sequence, fasta_path, keep_fasta = False):#Save a fasta file in fasta_path
        f = open(fasta_path, "w")
        f.write(">{}\n{}".format(id, sequence))
        f.close()

    def parse_ontologies(self, molecular_function, biological_process, celular_component):
        
        self.molecular_function = molecular_function
        self.biological_process = biological_process
        self.celular_component = celular_component
        ontologies = []
        if(self.molecular_function):
            ontologies.append("MFO")
        if(self.biological_process):
            ontologies.append("BPO")
        if(self.celular_component):
            ontologies.append("CCO")
        return ",".join(ontologies)
        
    def process(self, fasta_path, output_path, ontologies):
        command= "metastudent -i {} -o {} --ontologies={}".format(fasta_path, output_path, ontologies)
        os.system(command)

    def find_and_load_data(self, molecular_function, biological_process, celular_component, output_path):
        results = []
        if(molecular_function):
            try:
                mf = pd.read_csv(output_path + ".MFO.txt", header=None, sep="\t")
                mf.rename(columns={0: "id_seq", 1: "id_go", 2: "probability", 3: "term"}, inplace=True)
                mfs = mf.id_seq.unique()
                mf_array = []
                for mfi in mfs:
                    temp = mf[mf.id_seq == mfi][["id_go", "probability", "term"]]
                    temp["id_seq"] = mfi
                    mf_array.append(temp)
                mf_array = pd.concat(mf_array)
                mf_array["type"] = "molecular_function"
                results.append(mf_array)
            except:
                print("No result for molecular function")

        if(biological_process):
            try:
                bp = pd.read_csv(output_path + ".BPO.txt", header=None, sep="\t")
                bp.rename(columns={0: "id_seq", 1: "id_go", 2: "probability", 3: "term"}, inplace=True)
                bps = mf.id_seq.unique()
                bp_array = []
                for bpi in bps:
                    temp = bp[bp.id_seq == bpi][["id_go", "probability", "term"]]
                    temp["id_seq"] = bpi
                    bp_array.append(temp)
                bp_array = pd.concat(bp_array)
                bp_array["type"] = "biological_process"
                results.append(bp_array)
            except:
                print("No result for biological process")
        if(celular_component):
            try:
                cc = pd.read_csv(output_path + ".CCO.txt", header=None, sep="\t")
                cc.rename(columns={0: "id_seq", 1: "id_go", 2: "probability", 3: "term"}, inplace=True)
                ccs = cc.id_seq.unique()
                cc_array = []
                for cci in ccs:
                    temp = cc[cc.id_seq == cci][["id_go", "probability", "term"]]
                    temp["id_seq"] = cci
                    cc_array.append(temp)
                cc_array = pd.concat(cc_array)
                cc_array["type"] = "celular_component"
                results.append(cc_array)
            except:
                print("No result for biological process")
        results = pd.concat(results)
        return results

    def run_go(self, id, sequence, molecular_function = True, biological_process = True, celular_component = True):
        fasta_path = str(round(random()*10**20)) + ".fasta"
        output_path = str(round(random()*10**20)) + ".blast"
        self.save_fasta(id, sequence, fasta_path)
        ontologies = self.parse_ontologies(molecular_function, biological_process, celular_component)
        self.process(fasta_path, output_path, ontologies)
        results = self.find_and_load_data(molecular_function, biological_process, celular_component, output_path)
        os.remove(fasta_path)
        try:
            os.remove(output_path+".BPO.txt")
        except:
            pass
        try:
            os.remove(output_path+".MFO.txt")
        except:
            pass
        try:
            os.remove(output_path+".CCO.txt")
        except:
            pass
        return pd.DataFrame(results)
        #return results

if __name__ == "__main__":

    id = "sp|P40337|VHL_HUMAN"
    sequence = """MPRRAENWDEAEVGAEEAGVEEYGPEEDGGEESGAEESGPEESGPEELGAEEEMEAGRPR
PVLRSVNSREPSQVIFCNRSPRVVLPVWLNFDGEPQPYPTLPPGTGRRIHSYRGHLWLFR
DAGTHDGLLVNQTELFVPSLNVDGQPIFANITLPVYTLKERCLQVVRSLVKPENYRRLDI
VRSLYEDLEDHPNVQKDLERLTQERIAHQRMGD"""

    go = gene_ontology()
    df = go.run_go(id, sequence)
    print(df)
