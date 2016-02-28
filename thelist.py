import re
import requests

def replace_none(x, y, z=None):
    if x == None:
        return y
    else:
        if z == None:
            return x
        else:
            return z

def choose_nonempty(a, b, c):
    if a is not '':
        return a
    elif b is not '':
        return b
    elif c is not '':
        return c
    else:
        # throw exception
        return ''

class TheList:
    """Dictionary representation of The List."""

    def __init__(self):

        url = 'http://www.jmarshall.com/events/list.txt'
        data = re.sub('\s+', ' ', requests.get(url).text)

        regex = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(?:(?:(\d{1,2})\s+(sun|mon|tue|wed|thr|fri|sat))|((?:\d{1,2}\/)+\d{1,2})|(\d{1,2}-\d{1,2}))\s+(?:(cancel{1,2}ed):\s+)?(?:(postponed):\s+)?((?:[^,\s]+(?:\s[^,\s]+)*?)(?:,\s+(?:[^,\s]+(?:\s[^,\s]+)*?))*)\s+at\s+((?:[^,+\/\s\(\)]+(?: [^,+\/\s\(\)]+)*)(?:, +(?:[^,+\/\s\(\)]+(?: [^,+\/\s\(\)]+)*))*)\s+(?:((?:a\/a|\?\/\?|\d{1,2}\+)(?:\s+\((?:.*?)\))?)\s+)?(?:((?:(?:free|(?:\${1,2}\d+(?:\.\d\d)?(?:[\/-]\${1,2}\d+(?:\.\d\d)?)*))(?:\s+\((?:.*?)\),?)?)(?:\s+(?:free|(?:\${1,2}\d+(?:\.\d\d)?(?:[\/-]\${1,2}\d+(?:\.\d\d)?)*))(?:\s+\((?:.*?)\),?)?)*)\s+)?(?:((?:(?:noon|(?:\d{1,2}(?:\:\d\d)?(?:[ap]m)?(?:\/\d{1,2}(?:\:\d\d)?(?:[ap]m)?)?))(?:\s+\((?:.*?)\),?)?)(?:\s+(?:noon|(?:\d{1,2}(?:\:\d\d)?(?:[ap]m)?(?:\/\d{1,2}(?:\:\d\d)?(?:[ap]m)?)?))(?:\s+\((?:.*?)\),?)?)*)\s+)?(?:(\^)\s+)?(?:(#)\s+)?(?:(\*+)\s+)?(?:(@)\s+)?(?:(\$)\s+)?(?:\((.*?)\))?'

        # parse the data and store in JSON
        data_dictionary = {'shows': [], 'venues': [], 'artists': []}

        for a_match in re.finditer(regex, data, flags=re.M):

            # if the show isn't cancelled, collect data
            cancelled = a_match.group(6)
            postponed = a_match.group(7)

            if cancelled == None and postponed == None:

                month = a_match.group(1) # always
                
                # will have one of the following 3:
                # 1
                day_of_month = replace_none(a_match.group(2), '')
                day_of_week = replace_none(a_match.group(3), '')
                # 2
                days_of_month_group = replace_none(a_match.group(4), '')
                # 3
                days_of_month_range = replace_none(a_match.group(5), '')
                
                lineup = a_match.group(8).split(', ')
                # always; comma-separated list, each may have a comment in parens
                venue = a_match.group(9)
                age = replace_none(a_match.group(10), '') # may have a comment
                price = replace_none(a_match.group(11), '') # may have more than one price, with each optionally having a comment in parentheses. may be comma separated
                show_time = replace_none(a_match.group(12), '') # optional; may have more than one group of times, with each optionally having a comment in parentheses. may be comma separated
                u21_pay_more = replace_none(a_match.group(13), '?', 'yes')
                no_ins_or_outs = replace_none(a_match.group(14), '?', 'yes')
                recommendation = replace_none(a_match.group(15), '')
                pit_warning = replace_none(a_match.group(16), '?', 'yes')
                will_sell_out = replace_none(a_match.group(17), '?', 'yes')
                comment = replace_none(a_match.group(18), '')
                
                # store this data in a dictionary
                show = {
                    'when': [
                        day_of_week.upper(),
                        month.upper(),
                        choose_nonempty(
                            day_of_month,
                            days_of_month_group,
                            days_of_month_range
                            ),
                        show_time
                    ],
                    'who': lineup,
                    'where': venue,
                    'what else': {
                        'age': 'all ages' if age == 'a/a' else age,
                        'price': price,
                        'u21 pay more': u21_pay_more,
                        'no ins or outs': no_ins_or_outs,
                        'recommendation': recommendation,
                        'pit warning': pit_warning,
                        'will sell out': will_sell_out,
                        'comment': comment
                    }
                }

                # add show
                data_dictionary['shows'].append(show)
                
        self.data = data_dictionary

    def get(self, path):
        if path == None:
            return self.data
        else:
            return self.data[path]
