#  Created By Sushil

import pandas as pd
import random
import string

import config

df = pd.DataFrame(data={"Sentences": [None], "UseCase": [None], "classifications": [None]})


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_training_data():
    global df, df1
    usecases = ["range", "null_check", "date", "number", "length", "comparison", "email", "phone"]
    no_of_iteration = config.no_of_iteration
    print("Training data creation started with iteration:%d." % no_of_iteration)
    for usecase in usecases:
        if usecase == "range":
            for i in range(0, no_of_iteration):
                num1 = random.randint(0, 9999)
                num2 = random.randint(0, 99999)
                name = get_random_string(6)
                name2 = get_random_string(6)
                Sentences = ["%s should not be greater than %d ,but less than %d" % (name, num2, num1),
                             "%s must be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s could be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s is more than %d ,but less than %d" % (name, num1, num2),
                             "%s is greater than %d,but less than %d" % (name, num1, num2),
                             "%s must be greater than %d,but less than  %d" % (name, num1, num2),
                             "%s exceeds %d,but does not exceeds %d" % (name, num1, num2),
                             "%s could be less than %d and more than %d" % (name, num1, num2),
                             "%s might be in between %d to %d" % (name, num1, num2),
                             "%s can be in range %d to %d" % (name, num1, num2),
                             "%s is with in %d to %d" % (name, num1, num2),
                             "%s must be in between %d to %d" % (name, num1, num2),
                             "%s is more than %d and also %s should not exceed %d" % (name, num1, name, num2),
                             "%s is comprised between %d, excluded, and %d" % (name, num1, num2),
                             "%s is strictly greater than %d and strictly lower than %d" % (name, num1, num2),
                             "%s equals a number under %d and over %d" % (name, num1, num2),
                             "%s shall be found somewhere between %d and %d" % (name, num1, num2),
                             "%s should be in (%d; %d)" % (name, num1, num2),
                             "%s falls below %d and over %d" % (name, num1, num2),
                             "%s must be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s could be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s is more than %d ,but less than %d" % (name, num1, num2),
                             "%s is greater than %d,but less than %d" % (name, num1, num2),
                             "%s must be greater than %d,but less than %d" % (name, num1, num2),
                             "%s might be in between %d to %d" % (name, num1, num2),
                             "%s is between %d and %d" % (name, num1, num2),
                             "%s is between %d and %d, but is not %d or %d" % (name, num1, num2, num1, num2),
                             "%s is between %d and %d, but it cannot be %d or %d" % (name, num1, num2, num1, num2),
                             "%s is comprised between %d, excluded, and %d, excluded" % (name, num1, num2),
                             "%s is greater than %d and less than %d" % (name, num1, num2),
                             "%s is higher than %d and less than %d" % (name, num1, num2),
                             "%s is less than %d and more than %d" % (name, num1, num2),
                             "%s is lower than %d and higher than %d" % (name, num1, num2),
                             "%s is more than %d and also %s should not exceed %d" % (name, num1, name2, num2),
                             "%s is more than %d but less than %d" % (name, num1, num2),
                             "%s is over %d and under %d" % (name, num1, num2),
                             "%s is smaller than %d and bigger than %d" % (name, num1, num2),
                             "%s is strictly greater than %d and strictly lower than %d" % (name, num1, num2),
                             "%s lies between %d and %d" % (name, num1, num2),
                             "%s must be between %d and %d" % (name, num1, num2),
                             "%s must be bigger than %d and also smaller than %d" % (name, num1, num2),
                             "%s must be greater than %d and also %s must be lesser than %d" % (
                                 name, num1, name2, num2),
                             "%s must be greater than %d and less than %d" % (name, num1, num2),
                             "%s 's minimum is greater than %d, and it 's maximum is less than %d" % (name, num1, num2),
                             "%s IS BIGGER THAN %d AND ALSO %s IS SMALLER THAN %d" % (name, num1, name2, num2),
                             "%s IS GREATER THAN %d AND ALSO %s IS LESSER THAN %d" % (name, num1, name2, num2),
                             "%s value of %s is above %d and below %d" % (name, name2, num1, num2),
                             "%s value of %s is between %d and %d" % (name, name2, num1, num2),
                             "%s value of %s is between %d and %d, excluding %d and %d" % (
                                 name, name2, num1, num2, num1, num2),
                             ]
                if num1 > num2:
                    temp = num2
                    num2 = num1
                    num1 = temp
                for Sentence in Sentences:
                    expected_use_case = "Value is_within(%d,%d)" % (num1, num2)
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "null_check":
            null_not_null = ["not_null", "is_null"]
            for null_case in null_not_null:
                if null_case == "not_null":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = ["%s cannot be null" % name,
                                     "%s is defined" % name,
                                     "%s with Null value is invalid" % name,
                                     "%s is not null" % name,
                                     "%s can not be equal to null" % name,
                                     "%s can not be left empty" % name,
                                     "%s cannot be empty" % name,
                                     "%s is not empty" % name,
                                     "Email is not empty",
                                     "%s can not be equal to empty" % name,
                                     "%s can not be left blank" % name,
                                     "%s cannot be blank" % name,
                                     "%s is not blank" % name,
                                     "Email is not blank",
                                     "%s can not be equal to blank" % name,
                                     "%s could not be equal to blank" % name,
                                     "%s must not be blank" % name,
                                     "%s must not be empty" % name,
                                     "%s must not be null" % name,
                                     "%s should not be empty" % name,
                                     "%s should not be null" % name,
                                     "%s should not be blank" % name,
                                     "%s could not be empty" % name,
                                     "%s could not be null" % name,
                                     "%s could not be blank" % name,
                                     "%s would not be empty" % name,
                                     "%s would not be null" % name,
                                     "%s would not be blank" % name,
                                     "%s isn't empty" % name,
                                     "%s number should not be null" % name,
                                     "%s depth must not be null" % name,
                                     "%s is not null" % name,
                                     "%s could not be null" % name,
                                     "%s is not a null" % name,
                                     "%s mustn't be null" % name,
                                     "%s mustn't be empty" % name,
                                     "%s mustn't be an empty string" % name,
                                     "%s cannot be null" % name,
                                     "%s can't be a null" % name,
                                     "%s cannot be empty" % name,
                                     "%s can't be a empty" % name,
                                     "%s is expected to be not null" % name,
                                     "%s is required to be not null" % name,
                                     "%s is expected to be not empty" % name,
                                     "%s is required to be not empty" % name,
                                     "%s should have a expired indicator" % name,
                                     "A business associate credit check has the source of the check",
                                     "%s should have a lithology description" % name,
                                     "%s must have a non-null loan number" % name,
                                     "%s has some values" % name,
                                     "%s cannot have any characters" % name,
                                     "%s is always NOT NULL" % name,
                                     "Lets say %s cannot have null values" % name,
                                     "%s field cannot be blank or empty" % name,
                                     "%s should contain something" % name,
                                     "%s must be populated" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input Data is_not_equal NULL THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif null_case == "is_null":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = ["%s can be null" % name,
                                     "%s is null" % name,
                                     "Email is blank",
                                     "Email is not empty",
                                     "%s can be equal to null" % name,
                                     "%s can be left empty" % name,
                                     "%s can be empty" % name,
                                     "%s is empty" % name,
                                     "%s can be equal to empty" % name,
                                     "%s can be left blank" % name,
                                     "%s can be blank" % name,
                                     "%s is blank" % name,
                                     "%s can be equal to blank" % name,
                                     "%s could be equal to blank" % name,
                                     "%s must be blank" % name,
                                     "%s must be empty" % name,
                                     "%s must be null" % name,
                                     "%s should be empty" % name,
                                     "%s should be null" % name,
                                     "%s should be blank" % name,
                                     "%s could be empty" % name,
                                     "%s could be null" % name,
                                     "%s could be blank" % name,
                                     "%s would be empty" % name,
                                     "%s would be null" % name,
                                     "%s would be blank" % name,
                                     "%s is empty" % name,
                                     "%s number should be null" % name,
                                     "%s depth must be null" % name,
                                     "%s is null" % name,
                                     "%s could be null" % name,
                                     "%s is a null" % name,
                                     "%s must be null" % name,
                                     "%s must be empty" % name,
                                     "%s must be an empty string" % name,
                                     "%s can be null" % name,
                                     "%s can be a null" % name,
                                     "%s can be empty" % name,
                                     "%s can be a empty" % name,
                                     "%s is expected to be null" % name,
                                     "%s is required to be null" % name,
                                     "%s is expected to be empty" % name,
                                     "%s is required to be empty" % name,
                                     "%s should not have a expired indicator" % name,
                                     "%s should not have a lithology description" % name,
                                     "%s must have a null loan number" % name,
                                     "%s has not some values" % name,
                                     "%s can not have any characters" % name,
                                     "%s is always NULL" % name,
                                     "Lets say %s have null values" % name,
                                     "%s field can not be blank or empty" % name,
                                     "%s should not contain something" % name,
                                     "%s must not be populated" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input Data is_equal NULL THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "date":
            date = ["is_date", "is_not_date"]
            for date_case in date:
                if date_case == "is_date":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = ["%s can have values of type DATE only" % name,
                                     "%s can only be of type date" % name,
                                     "%s consists of a DATE" % name,
                                     "%s describes date" % name,
                                     "%s is comprised of a DATE" % name,
                                     "%s is equivalent to date" % name,
                                     "%s represents a date" % name,
                                     "%s represents a specific day, month and year" % name,
                                     "%s shall be 'DATE'" % name,
                                     "%s should contain the value of date" % name,
                                     "%s is equal to the value of date" % name,
                                     "%s may contain the value of date" % name,
                                     "%s is of value date" % name,
                                     "%s can only hold date data type" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_equal DATE THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif date_case == "is_not_date":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = ["%s isn't a date" % name,
                                     "%s is not a date" % name,
                                     "%s must not be a date" % name,
                                     "%s mustn't be date" % name,
                                     "%s should not be date" % name,
                                     "%s should not be of type date" % name,
                                     "%s shouldn't be a date" % name,
                                     "%s isn't of type date" % name,
                                     "%s may not contain the value of date" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_not_equal DATE THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "number":
            numbers = ["is_number", "is_not_number"]
            for number_case in numbers:
                if number_case == "is_number":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = ["%s must be of type integer" % name,
                                     "%s should be of type integer" % name,
                                     "%s must be a smallint" % name,
                                     "%s is number" % name,
                                     "%s must be of integer type" % name,
                                     "%s must be a smallint" % name,
                                     "%s Advances must be a whole number" % name,
                                     "%s Before Modification must be an integer" % name,
                                     "%s is number" % name,
                                     "%s is a number" % name,
                                     "%s should be a number" % name,
                                     "%s is of type number" % name,
                                     "%s must be of type number" % name,
                                     "%s must be of a type number" % name,
                                     "%s should be of type number" % name,
                                     "%s should be of a type number" % name,
                                     "%s needs to be of type number" % name,
                                     "%s must be a smallint" % name,
                                     "%s is a NUMBER" % name,
                                     "%s is a type number" % name,
                                     "The value of %s can only be number" % name,
                                     "%s is a value which is numerical" % name,
                                     "%s is always a number" % name,
                                     "%s is comprised by a number" % name,
                                     "%s must be numeric" % name,
                                     "%s belongs to numeric" % name,
                                     "%s is equal to numeric" % name,
                                     "%s can be numeric values" % name,
                                     "%s can have numerals" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_equal NUMBER THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif number_case == "is_not_number":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(5)
                        Sentences = ["%s isn't a number" % name,
                                     "%s is not a number" % name,
                                     "%s mustn't be a number" % name,
                                     "%s should not be a number" % name,
                                     "%s isn't of type number" % name,
                                     "%s isn't of a type number" % name,
                                     "%s is not of a type number" % name,
                                     "%s must not be of type number" % name,
                                     "%s should not be of a type number" % name,
                                     "%s shouldn't be of type number" % name,
                                     "%s is not of type integer" % name,
                                     "%s shouldn't be of type number" % name,
                                     "%s should not be of type number" % name,
                                     "%s cannot contain numerals" % name,
                                     "%s may not contain numeral" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_not_equal NUMBER THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "length":
            length = ["=", "!=", "<", "<=", ">", ">="]
            for use_case_length in length:
                if use_case_length == "=":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = ["length of %s can be equal to %d" % (name, num),
                                     "length of %s is equal to %d" % (name, num),
                                     "length of %s is %d" % (name, num),
                                     "length of %s must be %d" % (name, num),
                                     "length of %s should be equal to %d" % (name, num),
                                     "length of %s must be equal to %d" % (name, num),
                                     "length of %s should be %d" % (name, num),
                                     "length of %s could be equal to %d" % (name, num),
                                     "%s is %d characters long" % (name, num),
                                     "%s is %d digits" % (name, num),
                                     "%s is %d characters long" % (name, num),
                                     "%s %d characters long" % (name, num),
                                     "%s should be %d characters" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_equal %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "!=":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = [
                            "length of %s can not be equal to %d" % (name, num),
                            "length of %s is not equal to %d" % (name, num),
                            "length of %s is not %d" % (name, num),
                            "length of %s must not be %d" % (name, num),
                            "length of %s should not be equal to %d" % (name, num),
                            "length of %s must not be equal to %d" % (name, num),
                            "length of %s should not be %d" % (name, num),
                            "length of %s could not be equal to %d" % (name, num),
                            "%s isn't %d characters long" % (name, num),
                            "%s isn't %d digits" % (name, num),
                            "%s is not %d characters long" % (name, num),
                            "%s is not %d digits" % (name, num),
                            "%s length cannot be equal to %d" % (name, num),
                            "Length of %s is not %d" % (name, num),
                            "Length of %s can not be equals to %d" % (name, num),
                            "Length of %s must not be equals to %d" % (name, num),
                            "Length of %s should definitely not equal to %d" % (name, num),
                            "%s can not be %d characters long" % (name, num),
                            "Character length of %s is not equal to %d" % (name, num),
                            "%s must not exceed % d characters" % (name, num),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_not_equal %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "<":
                    for i in range(0, no_of_iteration):
                        num1 = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = [
                            "Character Length of %s is lower than %d" % (name, num1),
                            "Character count of %s is %d or lower" % (name, num1),
                            "%s must be shorter than %d characters" % (name, num1),
                            "%s length of %s is inferior to %d" % (name, name2, num1),
                            "%s length of %s is under %d" % (name, name2, num1),
                            "%s length of %s should measure below %d characters" % (name, name2, num1),
                            "%s number of characters of %s is lower than %d" % (name, name2, num1),
                            "%s length is less than %d" % (name, num1),
                            "The length of %s is less than %d" % (name, num1),
                            "The number of characters in %s is less than %d" % (name, num1),
                            "%s is smaller than %d characters" % (name, num1),
                            "%s must have less than %d characters" % (name, num1),
                            "Character length of %s is lower than %d" % (name, num1),
                            "The length measurement of %s will fall below %d" % (name, num1),
                            "%s will have a length that is fewer than %d" % (name, num1),
                            "%s will have a length that is underneath %d" % (name, num1),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_less_than %d THEN TRUE" % num1
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "<=":
                    for i in range(0, no_of_iteration):
                        num1 = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = ["Length of %s is less than or equal to %d characters" % (name, num1),
                                     "%s should be less than or equal to %d characters" % (name, num1),
                                     "%s must be less than or equal to %d characters" % (name, num1),
                                     "%s consists of either % d characters or less than % d characters" % (
                                         name, num1, num1),
                                     "Length of %s must not exceed %d" % (name, num1),
                                     "Length of %s must not exceed %d characters" % (name, num1),
                                     "%s must not be greater than %d characters" % (name, num1),
                                     "%s must not be longer than %d characters" % (name, num1),
                                     "%s must not be longer than %d symbol" % (name, num1),
                                     "Length of %s is smaller or equal to %d" % (name, num1),
                                     "%s must be at most %d characters" % (name, num1),
                                     "%s must be at most %d characters long" % (name, num1),
                                     "%s must not be longer than %d characters" % (name, num1),
                                     "%s may not be longer than %d characters" % (name, num1),
                                     "%s must not be longer than %d characters" % (name, num1),
                                     "%s must not be longer than %d symbols" % (name, num1),
                                     "%s must not be longer than %d letters and digits" % (name, num1),
                                     "%s length cannot be greater than %d" % (name, num1),
                                     "%s must not be greater than %d characters" % (name, num1),
                                     "%s must have a maximum of %d characters" % (name, num1),
                                     "%s has either %d characters or less than %d characters" % (name, num1, num1),
                                     "%s length of %s is no more than %d" % (name, name2, num1),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_less_than_equal_to %d THEN TRUE" % num1
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == ">":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = ["%s needs to be longer than %d characters" % (name, num),
                                     "%s number of characters of %s should be more than % d" % (name, name2, num),
                                     "%s length is higher than %d" % (name, num),
                                     "%s length is necessarily greater than %d" % (name, num),
                                     "%s length of %s is always greater than %d" % (name, name2, num),
                                     "%s length of %s is bigger than %d" % (name, name2, num),
                                     "%s length of %s must be bigger than %d" % (name, name2, num),
                                     "%s length of %s should be bigger than %d" % (name, name2, num),
                                     "%s length of %s surpasses %d" % (name, name2, num),
                                     "%s consists of more than %d characters %d" % (name, num, num),
                                     "%s contains more than %d characters" % (name, num),
                                     "%s number of characters of %s should be more than %d" % (name, name2, num),
                                     "%s needs to be longer than %d characters" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_greater_than %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == ">=":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = ["%s must be at least %d characters" % (name, num),
                                     "%s has at least %d elements" % (name, num),
                                     "%s is comprised of more than %d characters or %d characters" % (name, num, num),
                                     "Length of %s must be at least %d" % (name, num),
                                     "%s is as long as or longer than %d" % (name, num),
                                     "%s must not be less than %d characters" % (name, num),
                                     "%s must not be shorter than %d characters" % (name, num),
                                     "length of %s can be %d or bigger" % (name, num),
                                     "%s 's length is %d or bigger" % (name, num),
                                     "The length of %s cannot be a number less than %d" % (name, num),
                                     "%s should be longer or equal than %d characters" % (name, num),
                                     "The length of %s must be a positive number %d or greater" % (name, num),
                                     "%s is longer or equal than %d characters" % (name, num),
                                     "The length of characters of %s is either than or more than %d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) is_greater_than_equal_to %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "comparison":
            comparison = ['comparison_less_than', 'comparison_less_than_equal_to', 'neg_comparison']
            for comparison_use_case in comparison:
                if comparison_use_case == "comparison_equal_to":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = ["Water depth is %d" % num,
                                     "%s is %d" % (name, num),
                                     "%s should be %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s is be %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s is equal %d" % (name, num),
                                     "%s should be - %d" % (name, num),
                                     "%s cannot be greater than or less than %d" % (name, num),
                                     "The value of %s is %d" % (name, num),
                                     "The value of %s must be %d" % (name, num),
                                     "The value of %s is %d" % (name, num),
                                     "%s is %d" % (name, num),
                                     "%s is equal %d" % (name, num),
                                     "%s is equal to %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s MUST BE A %d" % (name, num),
                                     "%s must be equals to %d" % (name, num),
                                     "%s must be exactly %d" % (name, num),
                                     "%s must be just %d" % (name, num),
                                     "%s should be %d" % (name, num),
                                     "%s should be equal to %d" % (name, num),
                                     "%s should be equals to %d" % (name, num),
                                     "%s value is %d" % (name, num),
                                     "The value of %s equals %d" % (name, num),
                                     "The value of %s is the same as %d" % (name, num),
                                     "Value of %s should be equals to %d" % (name, num)
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_equal %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_not_equal_to":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["%s longitude should not be %d" % (name, num),
                                     "%s does not equal %d" % (name, num),
                                     "%s not equals to %d" % (name, num),
                                     "%s can be anything but %d" % (name, num),
                                     "%s can be anything other than %d" % (name, num),
                                     "%s should n't hold equal to %d" % (name, num),
                                     "%s can't have a value of %d" % (name, num),
                                     "%s does not consist of %d" % (name, num),
                                     "%s is not %d" % (name, num),
                                     "%s must not be equal to %d" % (name, num),
                                     "%s must not be %d" % (name, num),
                                     "%s can not be %d" % (name, num),
                                     "%s can't be %d" % (name, num),
                                     "%s can not be equal to %d" % (name, num),
                                     "%s is not able to equal %d" % (name, num),
                                     "%s is not equal to %d" % (name, num),
                                     "%s may not be %d" % (name, num),
                                     "%s must not be equal %d" % (name, num),
                                     "%s must not be equals to %d" % (name, num),
                                     "%s shall not be %d" % (name, num),
                                     "%s should not be %d" % (name, num),
                                     "%s should not be equal to %d" % (name, num),
                                     "%s should not be equals to %d" % (name, num),
                                     "%s must not be  %d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_not_equal %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                        df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_less_than":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["The value of %s cannot be %d or more" % (name, num),
                                     "The value of %s is less than %d" % (name, num),
                                     "The value %s is smaller than %d" % (name, num),
                                     "%s is less than %d" % (name, num),
                                     "%s is smaller than %d" % (name, num),
                                     "%s must be less than %d" % (name, num),
                                     "%s must be smaller than %d" % (name, num),
                                     "%s should be less than %d" % (name, num),
                                     "%s should be smaller than %d" % (name, num),
                                     "%s is not %d or a positive number" % (name, num),
                                     "The value of %s is fewer than %d" % (name, num),
                                     "%s consists of a number lower than %d" % (name, num),
                                     "%s equals a number lower than %d" % (name, num),
                                     "%s equals a number under %d" % (name, num),
                                     "%s falls under %d" % (name, num),
                                     "%s has a value that is less than %d" % (name, num),
                                     "%s holds a number that is lower than %d" % (name, num),
                                     "%s is a number lower than %d" % (name, num),
                                     "%s is below %d" % (name, num),
                                     "%s is fewer than %d" % (name, num),
                                     "%s is lower than %d" % (name, num),
                                     "%s is to be found below %d" % (name, num),
                                     "%s must be lower than %d" % (name, num),
                                     "%s shall not reach %d or higher" % (name, num),
                                     "%s should be lower than %d" % (name, num),
                                     "%s will be a value below %d" % (name, num),
                                     "%s has to be not as much as %d" % (name, num),
                                     "%s is not bigger or equal than %d" % (name, num),
                                     "%s is not %d or greater" % (name, num),
                                     "The value of %s is less than %d" % (name, num),
                                     "The %s is smaller than %d" % (name, num),
                                     "%s is a number less than %d" % (name, num),
                                     "%s is less than %d" % (name, num),
                                     "%s is strictly lesser than %d" % (name, num),
                                     "%s is under %d" % (name, num),
                                     "%s LESS THAN %d" % (name, num),
                                     "%s MUST LESS THAN %d" % (name, num),
                                     "%s shall not reach as high as %d" % (name, num),
                                     "%s will equal a number less than %d" % (name, num),
                                     "%s will equal some number beneath %d" % (name, num),
                                     "%s can not be %d or bigger" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_less_than %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_less_than_equal_to":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["%s has a value equal to or less than %d" % (name, num),
                                     "%s is %d, or less than %d" % (name, num, num),
                                     "%s is either %d or less than %d" % (name, num, num),
                                     "%s is smaller and also equal to %d" % (name, num),
                                     "%s must be %d, or less than %d" % (name, num, num),
                                     "The value of %s is less than or equal to %d" % (name, num),
                                     "%s can't be greater than %d" % (name, num),
                                     "%s is less than or equal to %d" % (name, num),
                                     "%s is not greater than %d" % (name, num),
                                     "%s must be less than or equal to %d" % (name, num),
                                     "%s should be less than or equal to %d" % (name, num),
                                     "%s should be smaller or equal to %d" % (name, num),
                                     "%s's value can not be greater than %d" % (name, num),
                                     "%s can be small or equal to %d" % (name, num),
                                     "%s could be small or equal to %d" % (name, num),
                                     "%s has a value less than or equal to %d" % (name, num),
                                     "%s is lower or equal to %d" % (name, num),
                                     "%s may be %d or less" % (name, num),
                                     "%s must be small or equal to %d" % (name, num),
                                     "%s can contain a number not exceeding %d" % (name, num),
                                     "%s can equal %d or be less than %d" % (name, num, num),
                                     "%s can not be bigger than %d" % (name, num),
                                     "%s can't be higher than %d" % (name, num),
                                     "%s equals or is less than %d" % (name, num),
                                     "%s is a number lower than %d or is %d" % (name, num, num),
                                     "%s is a number not higher than %d" % (name, num),
                                     "%s is either %d or lower than %d" % (name, num, num),
                                     "%s must be %d or below %d" % (name, num, num),
                                     "%s must be either %d or lower than %d" % (name, num, num),
                                     "%s must have a value equal to or less than %d" % (name, num),
                                     "%s shall not exceed %d" % (name, num),
                                     "%s's value could be as high as %d" % (name, num),
                                     "the value of %s must be less than %d, including %d" % (name, num, num),
                                     "%s can equal to %d but can't be greater than %d" % (name, num, num),
                                     "%s cannot be greater than %d" % (name, num),
                                     "The value of %s should be less than or equal to %d" % (name, num),
                                     "%s cannot be greater than %d" % (name, num),
                                     "%s is equal to or less than %d" % (name, num),
                                     "%s is less than or equal to %d" % (name, num),
                                     "%s is lesser or equal to %d" % (name, num),
                                     "%s is not greater than %d" % (name, num),
                                     "%s is smaller than or equal to %d" % (name, num),
                                     "%s must be equal or smaller than %d" % (name, num),
                                     "%s must be less than or equal to %d" % (name, num),
                                     "%s must be smaller than or equal to %d" % (name, num),
                                     "%s must not be greater than %d" % (name, num),
                                     "%s should not be more than %d" % (name, num),
                                     "the value of %s is %d to less" % (name, num),
                                     "The value of %s should be %d or less" % (name, num),
                                     "%s can be %d or smaller" % (name, num),
                                     "%s may be %d or less" % (name, num),
                                     "%s must have value less than or equal to %d" % (name, num),
                                     "the value of %s is %d to less, including %d" % (name, num, num),
                                     "%s can contain a value that can't exceed %d" % (name, num),
                                     "%s can not exceed %d" % (name, num),
                                     "%s can take values equal to or less than %d" % (name, num),
                                     "%s can't exceed %d" % (name, num),
                                     "%s cannot be bigger than %d" % (name, num),
                                     "%s consists of a number lower than %d or %d" % (name, num, num),
                                     "%s is a value below %d, which can also be %d" % (name, num, num),
                                     "%s is either %d or lower than %d" % (name, num, num),
                                     "%s is lower than %d or equal to it" % (name, num),
                                     "%s is not bigger than %d" % (name, num),
                                     "%s less than equal to %d" % (name, num),
                                     "%s must be lower than %d or %d" % (name, num, num),
                                     "%s shall be no higher than %d" % (name, num),
                                     "%s's value could be as high as %d" % (name, num),
                                     "%s is equal to %d or less than %d" % (name, num, num),
                                     "%s is less than %d or equal to %d" % (name, num, num),
                                     "%s is smaller than %d or equal to %d" % (name, num, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_less_than_equal_to %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_greater_than":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["%s should be more than %d" % (name, num),
                                     "The value of %s is greater than %d" % (name, num),
                                     "%s is greater than %d" % (name, num),
                                     "%s is more than %d" % (name, num),
                                     "%s is not equal to or less than %d" % (name, num),
                                     "%s is not smaller or equal than %d" % (name, num),
                                     "%s must be greater than %d" % (name, num),
                                     "%s must be more than %d" % (name, num),
                                     "%s should not be less than or equal to %d" % (name, num),
                                     "The %s is bigger than %d" % (name, num),
                                     "%s cannot be %d nor minor to %d" % (name, num, num),
                                     "%s equals a number higher than %d" % (name, num),
                                     "%s has a value greater than %d" % (name, num),
                                     "%s has a value that is greater than %d" % (name, num),
                                     "%s is a number bigger than %d" % (name, num),
                                     "%s is above %d" % (name, num),
                                     "%s is bigger than %d" % (name, num),
                                     "%s is higher than %d" % (name, num),
                                     "%s IS LARGER THAN %d" % (name, num),
                                     "%s is not %d and is not less than %d" % (name, num, num),
                                     "%s must be bigger than %d" % (name, num),
                                     "%s must be larger than %d" % (name, num),
                                     "%s should be bigger than %d" % (name, num),
                                     "%s takes value greater than %d" % (name, num),
                                     "%s's number must exceed %d" % (name, num),
                                     "%s's value is higher than %d" % (name, num),
                                     "the number %s is greater than %d" % (name, num),
                                     "The value of %s is greater than %d" % (name, num),
                                     "%s has a value more than %d" % (name, num),
                                     "%s has to be greater than %d" % (name, num),
                                     "%s is greater than %d" % (name, num),
                                     "%s is more than %d" % (name, num),
                                     "%s is much greater than %d" % (name, num),
                                     "%s is not equal or smaller than %d" % (name, num),
                                     "%s must be greater than %d" % (name, num),
                                     "%s must be more than %d" % (name, num),
                                     "%s should be greater than %d" % (name, num),
                                     "%s's value is more than %d" % (name, num),
                                     "The value of %s should exceed %d" % (name, num),
                                     "%s consists of a number bigger than %d" % (name, num),
                                     "%s is a number bigger than %d" % (name, num),
                                     "%s is a number larger than %d" % (name, num),
                                     "%s is bigger than %d" % (name, num),
                                     "%s is higher than %d" % (name, num),
                                     "%s is larger than %d" % (name, num),
                                     "%s isn't %d or less" % (name, num),
                                     "%s may only be more than %d" % (name, num),
                                     "%s must be bigger than %d" % (name, num),
                                     "%s must be larger than %d" % (name, num),
                                     "%s must be over the value of %d" % (name, num),
                                     "%s shall be at least higher than %d" % (name, num),
                                     "%s should be a number which is bigger than %d" % (name, num),
                                     "%s should be bigger than %d" % (name, num),
                                     "%s should hold a number which is more than %d" % (name, num),
                                     "%s's number must exceed %d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_greater_than %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_greater_than_equal_to":
                    for i in range(0, no_of_iteration):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["%s  has a value greater or equal to %d" % (name, num),
                                     "%s is at least %d" % (name, num),
                                     "%s is %d or more" % (name, num),
                                     "%s may be %d or more" % (name, num),
                                     "%s shall be at least %d" % (name, num),
                                     "The value of %s is more than %d or equal to it" % (name, num),
                                     "%s could be %d or greater than %d" % (name, num, num),
                                     "%s must have a value equal to or greater than %d" % (name, num),
                                     "%s is greater than or equal to %d" % (name, num),
                                     "the value of %s is equal to or greater than %d" % (name, num),
                                     "the value of %s must be equal to or greater than %d" % (name, num),
                                     "%s can be greater or equal to %d" % (name, num),
                                     "%s cannot be smaller than %d" % (name, num),
                                     "%s is greater or equal to %d" % (name, num),
                                     "%s is greater than or equal to %d" % (name, num),
                                     "%s is greater than or equal to %d" % (name, num),
                                     "%s is no smaller than %d" % (name, num),
                                     "%s is not less than %d" % (name, num),
                                     "%s is not less than %d" % (name, num),
                                     "%s is not smaller than %d" % (name, num),
                                     "%s must be greater or equal to %d" % (name, num),
                                     "%s must be greater than or equal to %d" % (name, num),
                                     "%s holds a number greater or equal to %d" % (name, num),
                                     "%s can be equal to %d but also be greater than %d" % (name, num, num),
                                     "%s can have a value of %d or more" % (name, num),
                                     "%s has a value of %d and up, including %d" % (name, num, num),
                                     "%s is equals or greater than %d" % (name, num),
                                     "%s is not lower than %d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_greater_than_equal_to %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "neg_comparison":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(5)
                        num = random.randint(0, 9999)
                        Sentences = ["%s can be negative" % name,
                                     "%s is a negative number" % name,
                                     "%s is negative" % name,
                                     "%s is -%d or not a positive number" % (name, num),
                                     "%s is not positive or not 0" % name,
                                     "%s is not positive or not zero" % name,
                                     "%s can not be positive" % name,
                                     "%s is not a positive number" % name,
                                     "%s is not positive " % name,
                                     "%s is negative or -%d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_less_than 0 THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "pos_comparison":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(5)
                        num = random.randint(0, 9999)
                        Sentences = ["%s can not be negative" % name,
                                     "%s is not a negative number" % name,
                                     "%s is not negative" % name,
                                     "%s is %d or a positive number" % (name, num),
                                     "%s is positive or 0" % name,
                                     "%s is positive or zero" % name,
                                     "%s can be positive" % name,
                                     "%s is a positive number" % name,
                                     "%s is positive " % name,
                                     "%s is not negative or not -%d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input is_greater_than_equal_to 0 THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "email":
            email_cases = ["email", "not_email"]
            for email_case in email_cases:
                if email_case == "email":
                    for i in range(0, no_of_iteration):
                        host = get_random_string(4)
                        domain = get_random_string(3)
                        name = get_random_string(6)
                        Sentences = ["%s@%s.%s for valid email" % (name, host, domain),
                                     "%s@%s.%s for validity of emails" % (name, host, domain),
                                     "%s@%s.%s e-mails" % (name, host, domain),
                                     "%s@%s.%s Id must be a valid email" % (name, host, domain),
                                     "%s@%s.%s is a email" % (name, host, domain),
                                     "%s@%s.%s must be of type email" % (name, host, domain),
                                     "%s@%s.%s is a valid email" % (name, host, domain),
                                     "%s@%s.%s should be of type email" % (name, host, domain),
                                     "%s@%s.%s is a email" % (name, host, domain),
                                     "%s@%s.%s is of type email" % (name, host, domain),
                                     "%s@%s.%s Id needs to be an email" % (name, host, domain),
                                     "%s@%s.%s Id needs to be of type email" % (name, host, domain),
                                     "%s@%s.%s has to be of type email" % (name, host, domain),
                                     "%s@%s.%s is a outlook email id" % (name, host, domain),
                                     "%s@%s.%s is of type gmail email id" % (name, host, domain),
                                     "%s@%s.%s is a facebook email id" % (name, host, domain),
                                     "%s@%s.%s is a yahoo email id" % (name, host, domain),
                                     "%s@%s.%s needs to be facebook email id" % (name, host, domain),
                                     "%s@%s.%s needs to be gmail email id" % (name, host, domain),
                                     "%s@%s.%s needs to be outlook email id" % (name, host, domain),
                                     "%s@%s.%s needs to be yahoo email id" % (name, host, domain),
                                     "%s@%s.%s is of type outlook email id" % (name, host, domain),
                                     "%s@%s.%s is of type facebook email id" % (name, host, domain),
                                     "%s@%s.%s is of type yahoo email id" % (name, host, domain),
                                     "%s@%s.%s can have values of type email only" % (name, host, domain),
                                     "%s for valid email" % name,
                                     "%s for validity of emails" % name,
                                     "%s e-mails" % name,
                                     "email should be valid",
                                     "%s Id must be a valid email" % name,
                                     "%s is a email" % name,
                                     "%s must be of type email" % name,
                                     "%s is a valid email" % name,
                                     "%s should be of type email" % name,
                                     "%s is a email" % name,
                                     "%s is of type email" % name,
                                     "%s Id needs to be an email" % name,
                                     "%s Id needs to be of type email" % name,
                                     "%s has to be of type email" % name,
                                     "%s is a outlook email id" % name,
                                     "%s is of type gmail email id" % name,
                                     "%s is a facebook email id" % name,
                                     "%s is a yahoo email id" % name,
                                     "%s needs to be facebook email id" % name,
                                     "%s needs to be gmail email id" % name,
                                     "%s needs to be outlook email id" % name,
                                     "%s needs to be yahoo email id" % name,
                                     "%s is of type outlook email id" % name,
                                     "%s is of type facebook email id" % name,
                                     "%s is of type yahoo email id" % name,
                                     "%s can have values of type email only" % name,

                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_equal EMAIL THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case],
                                 "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])

                elif email_case == "not_email":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        host = get_random_string(4)
                        domain = get_random_string(3)
                        Sentences = ["%s@%s .%s is invalid email" % (name, host, domain),
                                     "%s@%s. %s is not of type email" % (name, host, domain),
                                     "%s@ %s.%s should n't be a email" % (name, host, domain),
                                     "%s.%s should n't be of type email" % (host, domain),
                                     "@%s.%s should not be of type email" % (name, domain),
                                     "%s @ %s.%s should not be a email" % (name, host, domain),
                                     "%s@ %s. must n't be a email" % (name, host),
                                     "%s%s.%s must n't be of type email" % (name, host, domain),
                                     "%s@%s;%s must not be of type email" % (name, host, domain),
                                     "%s@%s,%s must not be a email" % (name, host, domain),
                                     "%s@%s1%s is not email" % (name, host, domain),
                                     "%s!%s.%s is n't email" % (name, host, domain),
                                     "%s&%s.%s is not email" % (name, host, domain),
                                     "%s*%s.%s is not of type email" % (name, host, domain),
                                     "%s~%s.%s is n't of type email" % (name, host, domain),
                                     "%s is invalid email" % name,
                                     "%s is not of type email" % name,
                                     "%s should n't be a email" % name,
                                     "%s should n't be of type email" % name,
                                     "%s should not be of type email" % name,
                                     "%s should not be a email" % name,
                                     "%s must n't be a email" % name,
                                     "%s must n't be of type email" % name,
                                     "%s must not be of type email" % name,
                                     "%s must not be a email" % name,
                                     "%s is not email" % name,
                                     "%s is n't email" % name,
                                     "%s is not email" % name,
                                     "%s is not of type email" % name,
                                     "%s is n't of type email" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_not_equal EMAIL THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case],
                                 "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "phone":
            phone_cases = ["valid_phone", "invalid_phone"]
            for phone_case in phone_cases:
                if phone_case == "valid_phone":
                    for i in range(0, no_of_iteration):

                        name = get_random_string(6)
                        Sentences = [
                            "%s for valid Phone Number" % name,
                            "%s for validity of Phone" % name,
                            "%s Phone Number" % name,
                            "Phone Number should be valid",
                            "%s contact must be a Phone Number" % name,
                            "%s is a contact number" % name,
                            "%s must be of type Phone contact" % name,
                            "%s is a valid contact number" % name,
                            "%s is a valid Phone number" % name,
                            "%s should be of type contact Number" % name,
                            "%s should be of type Phone Number" % name,
                            "%s should be of type Mobile Number" % name,
                            "%s is a Phone" % name,
                            "%s is of type Phone" % name,
                            "%s Id needs to be an Phone" % name,
                            "%s Id needs to be of type Phone" % name,
                            "%s has to be of type Phone number" % name,
                            "%s is a Phone number" % name,
                            "%s is of type Phone number" % name,
                            "%s is a contact Phone number" % name,
                            "%s is a contact number" % name,
                            "%s needs to be contact Phone number" % name,
                            "%s needs to be Phone number" % name,
                            "%s needs to be contact number" % name,
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_equal PHONE THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case],
                                 "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif phone_case == "invalid_phone":
                    for i in range(0, no_of_iteration):
                        name = get_random_string(6)
                        Sentences = [
                                     "%s is invalid Phone" % name,
                                     "%s is invalid Phone number" % name,
                                     "%s is not of type Phone Number" % name,
                                     "%s should n't be a Phone Number" % name,
                                     "%s should n't be of type Phone Number" % name,
                                     "%s should not be of type contact Number" % name,
                                     "%s should not be a Phone Number" % name,
                                     "%s must n't be a Phone Number" % name,
                                     "%s must n't be of type Phone Number" % name,
                                     "%s must not be of type contact Number" % name,
                                     "%s must not be a Phone Number" % name,
                                     "%s is not Phone Number" % name,
                                     "%s is n't contact Number" % name,
                                     "%s is not Phone Number" % name,
                                     "%s is not of type Phone Number" % name,
                                     "%s is n't of type contact Number" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) is_not_equal PHONE THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case],
                                 "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])

        print("Data created for :%s ,data size %d" % (usecase, len(df.dropna())))
    b_size_df = len(df)
    df.sort_values("Sentences", inplace=True)
    df.drop_duplicates(subset="Sentences", keep=False, inplace=True)
    df.to_csv("datasets/generated_training.csv", mode='w', index=False)
    a_size_df = len(df)
    print("before removing duplicate from df: %d and after removed duplicates size is : %d" % (b_size_df, a_size_df))
# create_training_data()
