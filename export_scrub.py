
import argparse

def scrub(target, userscrub=""):
    target_file = open(target, "r")
    # Split target file by "|" and scrub if they contain quotes.
    scrubbed_output = ""
    target_parts = target_file.read().split("|")
    count = 0
    for target_part in target_parts:
        count = count + 1
        if '"' in target_part:
            scrubbed_output = scrubbed_output + '"' + target_part.strip('"').replace('"',"'") + '"'
        else:
            scrubbed_output = scrubbed_output + target_part
        if count < len(target_parts):
            scrubbed_output = scrubbed_output + "|"
    target_file.close()
    # Write scrubbed output to file.
    if len(userscrub) > 0:
        scrubbed_output = scrubbed_output.replace("." + userscrub + "|","|")
        scrubbed_output = scrubbed_output.replace("." + userscrub + ";",";")
    scrubbed_file = open(target.replace(".","_scrubbed."), "w")
    scrubbed_file.write(scrubbed_output)
    scrubbed_file.close()
    # Change scrubbed to Excel format as a test.
    excel_format = scrubbed_output.replace(',','').replace('|',',')
    excel_file = open(target.replace(".","_excel."), "w")
    excel_file.write(excel_format)
    excel_file.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="File to scrub.")
    parser.add_argument("-us", dest='userscrub', default="",
                        help="Scrubs a base off of a username separated by a '.' - This was added as an optional hack to get users importing right.")
    options = parser.parse_args()
    scrub(options.target, userscrub=options.userscrub)

