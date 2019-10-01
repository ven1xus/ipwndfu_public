import os, subprocess, sys, json
from glob import iglob
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='Directory where im4p files are located', required=True)
    args = parser.parse_args()

    files = []
    for r, d, f in os.walk(args.directory):
        for file in f:
            if file.endswith('.im4p'):
                files.append(os.path.join(r, file))

    if not os.path.exists('results.json'):
        os.system('echo "{}" > results.json')
    obj = {}
    for file in files:
        if file:
            try:
                kbag = str(subprocess.run(['/usr/local/bin/img4', '-i', os.path.realpath(file), '-b'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n', 1)[0]
                if len(kbag) > 25:
                    print('Decrypting and Parsing', file)
                    run = True
                    while run:
                        try:
                            # print('Getting IVKEY')
                            ivkey = str(subprocess.run(['./ipwndfu', '--decrypt-gid', kbag], stdout=subprocess.PIPE).stdout.strip(), 'utf-8').split('\n', 1)[1]
                            print('Got IVKEY')
                            run = False
                        except:
                            # print('Unplug And Try Again Press Enter To Continue')
                            input()
                        iv = str.encode(ivkey)[:32].decode("utf-8")
                        key = ivkey.split(iv, 1)[1]
                        # print('Creating Obj Filename Key')
                        obj.update({ os.path.basename(file) : {}})
                        # print(obj)
                        obj[os.path.basename(file)].update({
                            'ivkey': ivkey,
                            'iv': iv,
                            'key': key
                        })
            except Exception as e:
                print(e)

    with open('results.json', 'w+') as json_file:
        json_file.truncate()
        json_file.seek(0)
        json.dump(obj, json_file, indent=4)
        json_file.close()

if __name__ == "__main__":
    main()
    print('Saved Decrypted IVs and Keys to results.json') 
