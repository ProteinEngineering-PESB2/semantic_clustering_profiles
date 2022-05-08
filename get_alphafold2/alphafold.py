import requests

class alphafold:
    def __init__(self, output_path):
        self.output_path = output_path

    def get_alphafold(self, uniprot):
        uniprot_id = uniprot.split(".")[0]
        try:
            response = requests.get("https://alphafold.ebi.ac.uk/files/AF-{}-F1-model_v2.pdb".format(uniprot_id))
            f = open(self.output_path, "w")
            f.write(response.text)
            f.close()
            return {"status": "success", "path": self.output_path}
        except Exception as e:
            print(e)
            return {"status": "error"}
        
if __name__ == "__main__":
    af = alphafold("output.pdb")
    af.get_alphafold("P40337.2")