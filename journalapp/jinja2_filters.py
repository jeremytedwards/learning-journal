# coding=utf-8

# def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
#     return value.strftime(format)


def dateformat(date):
    return date.strftime('%Y-%m-%d')


def datetimeformat(date):
    return date.strftime('%Y-%m-%d %I:%M %p')


def dateformat_monthfull(date):
    return date.strftime('%B')


def dateformat_day(date):
    return date.strftime('%d')



