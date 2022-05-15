from modules.alignment import alignment
from modules.utils import interface
from flask import Flask, request
from flask_cors import CORS
import os
temp_folder="/temp"
static_folder="/files"
alignments_folder = static_folder+"/alignments"
try:
    os.mkdir(temp_folder)
except Exception as e:
    print(e)
try:
    os.mkdir(static_folder)
except Exception as e:
    print(e)
try:
    os.mkdir(alignments_folder)
except Exception as e:
    print(e)

server = Flask(__name__)
CORS(server)
interface = interface()
class api:
    @server.route('/api/alignment/', methods=["POST"])
    def api_alignment():
        print(request)
        #Recieve either a fasta file or text. Interface will process and get data and bool variables. 
        data, is_json, is_file = interface.parse_information_no_options(request)
        align = alignment(data, temp_folder, static_folder, 
                        is_file, is_json, 1, 1)
        #Check file integrity
        if(align.check["status"] == "error"):
            return align.check
        #Get results and parse
        dbs = ["swissprot", "pdbaa"]
        response = {}
        for i in dbs:
            align.execute_blastp(i)
            table_parsed = align.parse_response()
            aligns = align.get_alignments()
            response[i] = {"table": table_parsed, "aligns": aligns}
        return response

    def get_server(self):
        return server