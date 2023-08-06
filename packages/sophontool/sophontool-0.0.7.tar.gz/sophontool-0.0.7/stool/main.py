import argparse as arg
import os

# import .util as util 
try:
    import util
except:
    from . import util

def bmcompiler_parser():
    parser = arg.ArgumentParser(description     = "handle nas with command line",
                                formatter_class = arg.ArgumentDefaultsHelpFormatter,
                                prog            = "python -m stools")

    
    parser.add_argument("--method", type=str,help="method: upload, list, return, token", required=True, choices=['token', 'upload', 'list', 'return'])
    parser.add_argument("--csv_file", type=str,help="csv file, the file must named 'text_masks.csv'")
    parser.add_argument("--profile_file", type=str,help="profile file, the file must named 'profile.txt'")
    parser.add_argument("--temporary-token", type=str,help="nas dir. Attention : \n \
        1. temporary-token is a token given by Sophon official people for delivering files with time limition. \n ")
    parser.add_argument("--team_id", type=str, help='team id')
    return parser

def main():
    parser = bmcompiler_parser()
    a = parser.parse_args()
    
    if a.method == 'upload':
        util.upload_with_token(a.temporary_token, a.csv_file, a.profile_file)
        
    if a.method == 'list': 
        util.list_file_with_token(a.temporary_token)

    if a.method == 'token':
        util.generate_token(a.team_id)

    if a.method == 'return':
        util.return_result_with_token(a.temporary_token)
    

