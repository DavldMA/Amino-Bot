import random
import re

def rollDice(num, sides):
    try:
        sides = max(sides, 1)
        return [random.randint(1, sides) for _ in range(num)]
    except:
        return None

def parseNormalRoll(inputStr):
    try:
        match = re.match(r'(\d*)?d(\d+)', inputStr)

        if match:
            numDice = int(match.group(1)) if match.group(1) else 1
            sides = int(match.group(2))
            dice = rollDice(numDice, sides)
            
            if len(dice) >= 2:
                dice = evaluateExpression(dice, '+')
                dice = [dice]
                
            return dice

        return None
    except:
        return None

def parseCustomRoll(inputStr):
    try:
        match = re.match(r'(\d+)#(\d+)?d(\d+)', inputStr)

        if match:
            numTimes = int(match.group(1))
            numDice = int(match.group(2)) if match.group(2) else 1
            sides = int(match.group(3))

            results = []
            individualResults = []

            for _ in range(numTimes):
                dice = rollDice(numDice, sides)
                results.extend(dice)
                individualResults.append(dice)

            return results, individualResults

        return None, None
    except:
        return None, None

def parseInput(inputStr):
    try:
        inputStr = inputStr.lower()
        inputStr = inputStr.replace(" ", "")
        startsWithMinus = inputStr.startswith('-')
        operators = re.findall('([+\-*/])', inputStr)
        splitInput = re.split(r'[+\-*/]', inputStr)
        
        if (not startsWithMinus):
            operators.insert(0, '+')

        results = []
        extraNumbers = []
        individualResults = []

        for part in splitInput:
            if re.match(r'\d+d\d+|d\d+', part):
                rollResult = parseNormalRoll(part)
                if rollResult is not None:
                    results.extend(rollResult)
                total = evaluateExpression(results, operators)
            elif re.match(r'\d+#\d*d\d+', part):
                customRollResult, customIndividualResults = parseCustomRoll(part)
                if customRollResult is not None:
                    results.extend(customRollResult)
                    individualResults.extend(customIndividualResults)
            else:
                extraNumbers.append(part)
                results.append(part)
        if individualResults:
            string = ''
            
            for ir in individualResults:
                for e in extraNumbers:
                    ir.append(e)
            for ir in individualResults:

                total = evaluateExpression(ir, operators)
                string += f"\n[cib]{total} ⟵ {ir}"
            return string
        else:
            total = evaluateExpression(results, operators)
            return f"\n[cib]{total} ⟵ {results}"
    except:
        return None
    
def evaluateExpression(operands, operators):
    try:
        result = 0
        for i, operand in enumerate(operands):
            
            if (i < len(operators)):
                currentOperator = operators[i]

            rollResult = sum(operand) if isinstance(operand, list) else int(operand)
            if (currentOperator == '+'):
                result += rollResult
            elif (currentOperator == '-'):
                result -= rollResult
            elif (currentOperator == '*'):
                result *= rollResult
            elif (currentOperator == '/'):
                result /= rollResult 
        return result
    except:
        return "Um erro aconteceu"