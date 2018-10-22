from logger import *
from Poll import Poll
import re
from string import ascii_uppercase as UPPERS
import collections

class Poller:
    Polls = []

    def __init__(self):
        self.logger = Logger()
        self.log(INFO, "INIT")

    def newPoll(self, pollString):
        self.log(INFO, "func -> newPoll")
        opts = self.parsePollString(pollString)
        self.log(DEBUG, "opts: {}".format(opts))
        poll = Poll(opts[0], opts[1], opts[2])
        self.Polls.append(poll)
        self.showOpenPolls()
        return poll

    def log(self, level, statement):
        self.logger.log(level, "Poller -- {}".format(statement))

    def savePolls(self):
        pass

    def loadPolls(self):
        pass

    def parsePollString(self,text):
        self.log(INFO, "func -> parsePollString")
        self.log(INFO, "QUERY")
        query_re = re.compile('Query:.*$')
        options_re = {letter:re.compile('{}:.*$'.format(letter)) for letter in UPPERS}
        end_date_re = re.compile('End:.*$')
    
        try:
            for line in text.split("\n"):
                query_match = query_re.search(line)
                query_line = ''
                if query_match is not None:
                    self.log(DEBUG, "Query Match: {}".format(query_match))
                    query_line = query_match.string
                    self.log(DEBUG, query_line)
                    query_line = re.sub('Query: ', '', query_line)
                    self.log(DEBUG, query_line)
                    break
                else:
                    pass # TODO Log Error and return Fail
        except Exception as e:
            self.log(ERROR, e)
        
        self.log(INFO, "OPTIONS")
        options = collections.OrderedDict()

        for line in text.split("\n"):
            for key, value in options_re.items():
                self.log(DEBUG, "options_re -- KEY: {} VALUE:{}".format(key, value))
                value_match = value.search(line)
                if value_match is not None:
                    self.log(INFO, "MATCH FOUND IN {}!!!".format(line))
                    #value_line = value_match.group(1)
                    value_line = re.sub('{}:'.format(key), '', line)
                    options[key] = value_line
                #else:
                #    break
        # TODO if no options the return fail
        
        
        self.log(INFO, "ENDDATE")
            
        for i in text.split("\n"):
            end_date_match = end_date_re.search(line)
            end_date_line = ''
            if end_date_match is not None:
                end_date_line = datetime.strptim(re.sub('End:', '', line), "%y-%m-%d--%H:%M")
            else:
                pass  # TODO Log Error and return Fail

        self.log(DEBUG, 'return: {}'.format((query_line, options, end_date_line)))
        return (query_line, options, end_date_line)


    def showOpenPolls(self):
        self.log(INFO, "func -> showOpenPolls")
        for poll in self.Polls:
            poll.displayPoll()
