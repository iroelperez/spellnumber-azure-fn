import logging

import azure.functions as func

import random

simpleNumbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                 "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

tens = ["", "ten", "twenty", "thirty", "forty",
        "fifty", "sixty", "seventy", "eighty", "ninety"]

largeNumbers = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion",
                "octillion", "nonillion", "decillion"]


def split_thousands(n):
    result = list()
    while n >= 1000:
        r = n % 1000
        n = n // 1000
        result.append(r)
    else:
        result.append(n)
    return result


def spell_tens(n):
    if n < 20:
        return simpleNumbers[n]
    else:
        if n % 10 == 0:
            return tens[n // 10]
        else:
            return "{}-{}".format(tens[n // 10], simpleNumbers[n % 10])


def spell_hundreds(n):
    if n < 20:
        return simpleNumbers[n]
    else:
        if n < 100:
            return spell_tens(n)
        else:
            if n == 100:
                return "one hundred"
            else:
                if n % 100 == 0:
                    return "{} hundred".format(simpleNumbers[n // 100])
                else:
                    return "{} hundred {}".format(simpleNumbers[n // 100], spell_tens(n % 100))


def spell_group(index, group):
    return "{} {}".format(spell_hundreds(group), largeNumbers[index])


def spell_group_tuple(t):
    (index, group) = t
    return spell_group(index, group)


def valid_group(t):
    (_, group) = t
    return group > 0


def spell_positive_number(n):
    groups = split_thousands(n)
    if len(groups) == 1:
        return spell_hundreds(n)
    else:
        return " ".join(list(reversed(list(map(spell_group_tuple,
                                               list(filter(valid_group, list(enumerate(groups)))))))))


def spell_signed(n, f):
    if n < 0:
        return "minus {}".format(f(-n))
    else:
        return f(n)


def spell_number(n):
    return spell_signed(n, spell_positive_number)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    number = req.params.get('number')
    if not number:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            number = req_body.get('number')

    if number:
        spelled = spell_number(int(number))
        # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(spelled)
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
