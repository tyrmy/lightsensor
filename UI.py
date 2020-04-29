import argparse, subprocess
from plotters import plotter as plt

parser = argparse.ArgumentParser(description='Lightsensor plotter')
parser.add_argument('--test', dest='test', const=True, nargs='?', default=False, required=False, help='Run plot test.')

args = parser.parse_args()

options = ['One day summary',
        'X-day summary',
        'X-day scatter',
        '2D Density function',
        'Update local database',
        'Make custom plot'
        ]

def makeMenu(l):
    index = 0
    result = ''
    for item in l:
        result += '{0}: {1}\n'.format(index, item)
        index += 1
    print(result)

if __name__ == '__main__':
    if args.test:
        print("--test given: running demonstration...")
        plotter = plt()
        plotter.demonstration()
        plotter.close()
        print("End of demonstration!")
        exit()
    else:
        ans = ''
        plotter = plt()
        while not (ans == 'exit'):
            makeMenu(options)
            ans = input('Give a number: (type \'exit\' to quit)\n')
            if ans == '0': 
                plotter.yesterday()
            elif ans == '1': 
                plotter.summary_plot()
            elif ans == '2': 
                plotter.gradient()
            elif ans == '3': 
                plotter.density2d()
            elif ans == '4': 
                try:
                    subprocess.call(['./get_database.sh'])
                except OSError:
                    print('Database update failed...')
            elif ans == '5': 
                print('Not implemented!')
            else:
                print('Invalid input!\n')
        plotter.close()
        print('Exiting...')
