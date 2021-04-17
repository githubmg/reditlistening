import re
def getSubComments(comment, allComments, verbose=True):
    try:
        if comment.ups > 10:
            allComments.append(string_process(comment.body))
    except:
        pass
    if not hasattr(comment, "replies"):
        replies = comment.comments()
        if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies
    for child in replies:
        getSubComments(child, allComments, verbose=verbose)


def getAll(r, submissionId, verbose=False):  
    return_info = {}
    submission = r.submission(submissionId)
    return_info['submission'] = string_process(submission.title)
    return_info['submission_text'] = string_process(submission.selftext)
    comments = submission.comments
    commentsList = []
    for comment in comments:
        getSubComments(comment, commentsList, verbose=verbose)
    return_info['comments'] = commentsList
    return return_info

def string_process(string):
    return string.replace('\n\n','.').replace('\n','.').replace('\t',' ').replace("\'","'").replace("...",".").replace("..",".")

def get_phrases_index_comment(comment):
    phrase_sep = [regx.end() for regx in list(re.finditer('\.',comment))]
    phrase_sep.insert(0,0)
    return phrase_sep

def get_item_phrase(BeginOffset,EndOffset,phrase_sep,comment):
    for i in range(len(phrase_sep) - 1):
        if BeginOffset >= phrase_sep[i] and EndOffset <= phrase_sep[i +1]:
            return comment[phrase_sep[i]:phrase_sep[i +1]]
        

def get_item_offset(text,item_phrase):
    iters = list(re.finditer(text,item_phrase))
    item_position = (iters[0].start(),iters[0].end())
    return item_position

def is_valid_pos(pos_tag):
    if pos_tag['PartOfSpeech']['Tag'] in ['NOUN','NUM','O','PROPN','SYM']:
        return True
    if pos_tag['PartOfSpeech']['Tag'] == 'PUNCT':
        if pos_tag['Text'] not in [',','.',':','?','!','(']]:
                return True
    return False