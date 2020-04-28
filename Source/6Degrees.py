import sys
from optparse import OptionParser

client_id = None
client_secret = None
degrees = 1
playlist_name = '{0}Degrees of {1}'

"""
Parse args for the program. First must be sid filename, remaining are optional.
"""
def parse_args(args):
    usage = 'usage: {0} <sid_file> [options]'
    if len(args) > 1:
        filename = args[1]

        parser = OptionParser(usage=usage.format('%prog'))
        parser.add_option('-d', '--Degrees', default=1, dest='degrees', type='int', help='Set how many layers deep the application goes. The higher the number the longer the runtime and larger the playlist.')

        (options, args) = parser.parse_args()

        global degrees
        degrees = options.degrees

        parse_sid(filename)
    else:
        print (usage.format(args[0]))
        sys.exit()

"""
Set the client id and client secret found in the file specified by filename
"""
def parse_sid(filename):
    if filename.endswith('.sid'):
        try:
            sid = open(filename, 'r')

            global client_id
            client_id = sid.readline().strip()

            global client_secret
            client_secret = sid.readline().strip()
        except:
            print ('Problem reading file \'{0}\''.format(filename))
            sys.exit()
    else:
        print ('Invalid file format. File must be of type \'.sid\'')
        sys.exit()

if __name__ == '__main__':
    parse_args(sys.argv)
