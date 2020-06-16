import sys

def printUsage():
    print('Resistor Combinator Tool v1.0')
    print()
    print('Usage:')
    print()
    print('rct.py resFile.txt [maxResults] [--rat rat] [--res res] [--volt volt ref]')
    print()
    print('resFile.txt  - list of resistor values')
    print('maxResults   - maximum results to print (default == 20)')
    print('rat          - finds best combination of 2 resistors (series or parallel) in the given ratio')
    print('res          - finds best combination of 2 resistors (series or parallel) giving res resistance')
    print('volt ref     - finds resistors for a voltage divider with ref reference voltage and volt desired voltage')

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
                    #print (mode, arg, number, goal, reference, not mode)
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
            return '%.1f' % val
        
        return '%d' % val
        
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

(resFile, mode, goal, reference, maxRes) = parseArgs()

results = []

# read the list of available resistors
with open(resFile) as inf:
    resList = [float(line.strip()) for line in inf]

# do the calcs
if mode == 'rat':
    for r1 in resList:
        for r2 in resList:
            rat = r1 / r2
            err = abs(rat - goal)
            results.append((round(err, 2), round(rat, 2), resistorValue(r1), resistorValue(r2)))
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
    print ('R\terror\tR1\tR2')
    for res in results:
        print(f'{res[1]}\t{res[0]}\t{res[2]}\t{res[3]}\t{res[4]}')
elif mode == 'volt':
    print ('V\terror\tRt\tRb')
    for res in results:
        print(f'{res[1]}\t{res[0]}\t{res[2]}\t{res[3]}')
