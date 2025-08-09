# main_test.py
from analyzer import analyze_job_description

def run_test():
    sample_title = "Staff Pajak"
    sample_desc = "Menyiapkan laporan pajak bulanan, melaporkan PPh dan PPN, melakukan rekonsiliasi."
    res = analyze_job_description(sample_title, sample_desc)
    import pprint
    pprint.pprint(res)

if __name__ == "__main__":
    run_test()
