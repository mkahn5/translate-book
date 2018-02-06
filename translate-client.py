import os
import sys
import time
import argparse
from google.cloud import translate


__github__ = 'https://github.com/AshuIX'


#####progress bar start #####
def format_interval(t):
    mins, s = divmod(int(t), 60)
    h, m = divmod(mins, 60)
    if h:
        return '%d:%02d:%02d' % (h, m, s)
    else:
        return '%02d:%02d' % (m, s)


def format_meter(n, total, elapsed):
    if n > total:
        total = None
    elapsed_str = format_interval(elapsed)
    rate = '%5.2f' % (n / elapsed) if elapsed else '?'
    if total:
        frac = float(n) / total
        N_BARS = 10
        bar_length = int(frac * N_BARS)
        bar = '#' * bar_length + '-' * (N_BARS - bar_length)
        percentage = '%3d%%' % (frac * 100)
        left_str = format_interval(elapsed / n * (total - n)) if n else '?'
        return '|%s| %d/%d %s [elapsed: %s left: %s, %s iters/sec]' % (bar, n, total, percentage, elapsed_str, left_str, rate)
    else:
        return '%d [elapsed: %s, %s iters/sec]' % (n, elapsed_str, rate)


class StatusPrinter(object):
    def __init__(self, file):
        self.file = file
        self.last_printed_len = 0

    def print_status(self, s):
        self.file.write('\r' + s + ' ' * max(self.last_printed_len - len(s), 0))
        self.file.flush()
        self.last_printed_len = len(s)


def tqdm(iterable, desc='', total=None, leave=False, file=sys.stderr, mininterval=0.5, miniters=1):
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    prefix = desc + ': ' if desc else ''
    sp = StatusPrinter(file)
    sp.print_status(prefix + format_meter(0, total, 0))
    start_t = last_print_t = time.time()
    last_print_n = 0
    n = 0
    for obj in iterable:
        yield obj
        n += 1
        if n - last_print_n >= miniters:
            cur_t = time.time()
            if cur_t - last_print_t >= mininterval:
                sp.print_status(prefix + format_meter(n, total, cur_t - start_t))
                last_print_n = n
                last_print_t = cur_t
    if not leave:
        sp.print_status('')
        sys.stdout.write('\r')
    else:
        if last_print_n < n:
            cur_t = time.time()
            sp.print_status(prefix + format_meter(n, total, cur_t - start_t))
        file.write('\n')
#####progress bar end #####

#####split file by new line and store in memory#####
def load_file(file_path, split_on='\n'):
    # function takes the text file path, read it, split it on passed split_on (default is \n [newline])
    # and returns the list acquired

    # open the file in read mode, encoding utf-8
    fp = open(file=file_path, encoding='utf-8', errors='ignore')
    # read the data from the file
    _data = fp.read()
    # close the file
    fp.close()
    # split the data over split_on
    _data = _data.strip().split(split_on)
    # return the list acquired above
    return _data


def handle_data(data, split_on='.'):
    # function receives text, split it over split_on (default is .) and returns the list acquired
    # split and return the data over split_on
    return data.split(split_on)

#####translate and build output#####
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument Parser For The Script.')
    parser.add_argument('input_file', help='Input text file name/path')
    parser.add_argument('output_file', help='Output text file name/path')

    args = parser.parse_args()
    # set the creds.json in the current directory as the GOOGLE_APPLICATION_CREDENTIALS of the system
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.curdir, 'creds.json')

    # create the translate client
    translate_client = translate.Client()
    # create an empty list called translated
    translated = list()
    # call load_file function with the input_file to get the list of sentences (splitted on \n)
    # put it in tqdm (to show the progress, and for each d in the result
    for d in tqdm(load_file(args.input_file), desc='Input Text Loop'):
        # try to append the result of the translation of d to the translated list
        try:
            translated.append(translate_client.translate(d, target_language='en')['translatedText'])
        # if it fails
        except Exception as e:
            # create empty _temp list
            _tmp = list()
            # call the handle_data function wih d to split it over . and for each _d in that
            for _d in handle_data(d):
                # try
                try:
                    # append the result of the translation of _d to the _tmp list
                    _tmp.append(translate_client.translate(_d, target_language='en')['translatedText'])
                except:
                    continue
            # join the results with .and append to the translated list
            translated.append('.'.join(_tmp))
    # at last open the outputfile in write mode, join the translated over \n and arite it to the file
    open(file=args.output_file, mode='w', encoding='utf-8', errors='ignore').write('\n'.join(translated))
