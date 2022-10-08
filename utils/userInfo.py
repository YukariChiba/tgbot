def getUserName(user):
    ret = ""
    if user.first_name:
        ret = ret + user.first_name
    ret = ret + " "
    if user.last_name:
        ret = ret + user.last_name
    if ret == " ":
        return "Anonymous"
    else:
        return ret