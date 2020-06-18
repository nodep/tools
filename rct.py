import sys

def printUsage():
    print('Resistor Combinator Tool v1.0')
    print()
    print('Usage:')
    print()
    print('rct.py resistors [maxResults] [--rat rat] [--res res] [--volt volt ref]')
    print()
    print('resistors    - either a file with a list of resistor values to combine,')
    print('               or e12, e24, e48, e96 for standard resistor series')
    print('maxResults   - maximum results to print (default == 20)')
    print('rat          - finds best combination of 2 resistors (series or parallel) in the given ratio')
    print('res          - finds best combination of 2 resistors (series or parallel) giving res resistance')
    print('volt ref     - finds resistors for a DC-DC feedback where ref is the reference voltage,')
    print('               and volt the desired output voltage')

def handleError(errorMsg):
    print ('Error:', errorMsg)
    exit(1)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def parseArgs():

    if len(sys.argv) < 3:
        printUsage()
        exit(1)

    maxRes = -1
    mode = ''
    goal = 0
    reference = 0
    resFile = ''

    # parse
    for arg in sys.argv[1:]:
        if arg == '--rat':
            if mode:
                handleError('multiple modes selected')
            else:
                mode = 'rat'
        elif arg == '--res':
            if mode:
                handleError('multiple modes selected')
            else:
                mode = 'res'
        elif arg == '--volt':
            if mode:
                handleError('multiple modes selected')
            else:
                mode = 'volt'
        else:
            if resFile:
                if isfloat(arg):
                    number = float(arg)

                    if number == 0:
                        handleError('argument of value == 0 is not allowed');
                    elif not mode  and  maxRes == -1:
                        maxRes = int(number)
                    elif mode and goal == 0:
                        goal = number
                    elif mode and reference == 0:
                        reference = number
                    else:
                        handleError('too many arguments: %s' % (arg))
                else:
                    handleError('invalid argument: %s' % (arg))
            else:
                resFile = arg

    if not mode:
        handleError('mode not selected')

    if maxRes == -1:
        maxRes = 20

    if goal == 0:
        handleError('ratio/resistance/voltage is not set')

    if mode == 'volt'  and  reference == 0:
        handleError('reference voltage is not set')

    return (resFile, mode, goal, reference, maxRes)

# converts a resistance in ohms (float) to a string in 4K7 notation
def resistorValue(val):
    if val < 1000:      # < 1K
        if val - int(val) != 0:
            str = '%.2f' % val
        else:
            return '%d' % val   # we have to return to avoid stripping trailing zeros

    else:
        str = '          %d' % val
        if val < 1e6:
            str = str[:-3] + 'K' + str[-3:]
        else:
            str = str[:-6] + 'M' + str[-6:]

    return str.strip(' 0')


##################################################################################################
##################################################################################################
##################################################################################################

e12series = (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2)

e24series = (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
             3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1)

e48series = (1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87,
             1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65,
             3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15,
             7.50, 7.87, 8.25, 8.66, 9.09, 9.53)

e96series = (1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37,
             1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91,
             1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67,
             2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74,
             3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23,
             5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
             7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76)

(resFile, mode, goal, reference, maxRes) = parseArgs()

results = []
resList = []

# create the list of available resistors
selectedSeries = None

if resFile == 'e12':
    selectedSeries = e12series
elif resFile == 'e24':
    selectedSeries = e24series
elif resFile == 'e48':
    selectedSeries = e48series
elif resFile == 'e96':
    selectedSeries = e96series
else:
    try:
        with open(resFile) as inf:
            resList = [float(line.strip()) for line in inf]
    except OSError as err:
        handleError(err.strerror + ': ' + resFile)

if selectedSeries:
    for r in selectedSeries:
        resList.append(r)
        resList.append(round(r * 10, 1))
        resList.append(round(r * 100))
        resList.append(round(r * 1000))
        resList.append(round(r * 10000))
        resList.append(round(r * 100000))
        resList.append(round(r * 1000000))

# do the calcs
if mode == 'rat':
    for r1 in resList:
        for r2 in resList:
            rat = r1 / r2
            err = abs(rat - goal)
            results.append((round(err, 3), round(rat, 3), resistorValue(r1), resistorValue(r2)))
elif mode == 'res':
    for ndx1 in range(0, len(resList)):
        r1 = resList[ndx1]
        for ndx2 in range(ndx1, len(resList)):
            r2 = resList[ndx2]

            ser = r1 + r2
            err = abs(goal - ser)
            results.append((round(err, 2), round(ser, 2), resistorValue(r1), resistorValue(r2), 'series'))

            par = (r1 * r2) / (r1 + r2)
            err = abs(goal - par)
            results.append((round(err, 2), round(par, 2), resistorValue(r1), resistorValue(r2), 'parallel'))
elif mode == 'volt':
    for r1 in resList:
        for r2 in resList:
            ratio = r2 / (r1 + r2)
            volt = reference / ratio
            err = abs(volt - goal)
            results.append((round(err, 2), round(volt, 2), resistorValue(r1), resistorValue(r2)))

# sort by error
results.sort()

# limit the results to maxRes elements
results = results[0:maxRes]

if mode == 'rat':
    print ('ratio\terror\tRt\tRb')
    for res in results:
        print(f'{res[1]}\t{res[0]}\t{res[2]}\t{res[3]}')
elif mode == 'res':
    print ('R\terror\tR1\tR2\tconfig')
    for res in results:
        print(f'{res[1]}\t{res[0]}\t{res[2]}\t{res[3]}\t{res[4]}')
elif mode == 'volt':
    print ('V\terror\tRt\tRb')
    for res in results:
        print(f'{res[1]}\t{res[0]}\t{res[2]}\t{res[3]}')
