import argparse
from hash_excel import hash_excel_file

parser = argparse.ArgumentParser(description='Hash IDs in an Excel file')
parser.add_argument('input_file', help='input Excel file')
parser.add_argument('output_file', help='output Excel file')
parser.add_argument('--id_column', default='ID', help='name of the ID column')
parser.add_argument('--key', default='y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L', help='secret key for hashing')
args = parser.parse_args()

hash_excel_file(args.input_file, args.output_file, args.id_column, args.key)