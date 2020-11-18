from user_registeration.models import InfoMessages

def set_session_language(request):
    """Returns the session language."""

    if 'language' in request.session:
        get_language = request.session['language']
        print("get language in session", get_language)
        return get_language

    else:
        request.session['language'] = 1
        get_language = request.session['language']
        print("else set language in session", get_language)
        return get_language

def get_info_messages(get_language, messgae_label):

    """Returns the information  messages."""

    try:
        get_message_dict = InfoMessages.objects.filter(
                                                   language_name_id=get_language
                                                ).filter(
                                                    message_label=messgae_label
                                                ).values('message')[0]
        message = get_message_dict['message']
    
        print("message from database :", message)
        return message
    except Exception as e:
        print("Exception in fetching information labels", e)
        return "Error while getting information from database."