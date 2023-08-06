from main import BASE_URL, _format_http_response, get_headers
import requests
import os

class Incantation:
    def __init__(self, title: str, text: str, supp_id: str = None, description: str = None, incantation_id: str = None):
        self.incantation_id = incantation_id
        self.title = title
        self.text = text
        self.supp_id = supp_id
        self.description = description
        self.is_deployed = self.incantation_id is not None

    def create(self):
        if self.is_deployed:
            raise Exception('This incantation has already been deployed: ' + self.incantation_id)
        url = BASE_URL + 'incantations'
        payload = {
            'title': self.title,
            'text': self.text,
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        self.incantation_id = resp['body']['id']
        self.is_deployed = True
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This incantation has not been deployed yet. Please run `incantation.create()` before running `incantation.update()')
        url = BASE_URL + f'incantations/{self.incantation_id}'
        payload = {}
        if self.title is not None:
            payload['title'] = self.title
        if self.text is not None:
            payload['text'] = self.text
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=get_headers(), json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'incantations/{self.incantation_id}'
        _format_http_response(requests.delete(url, headers=get_headers()))


def get_incantations():
    incantations = {}
    url = BASE_URL + 'incantations'
    resp = requests.get(url, headers=get_headers())
    resp = _format_http_response(resp)
    for incantation in resp['body']:
        inc = Incantation(
            incantation_id=incantation['id'],
            title=incantation['title'],
            text=incantation['text'],
            supp_id=incantation['supp_id'],
            description=incantation['description']
        )
        incantations[incantation['id']] = inc
    return incantations

# create_incantation() is a convenience function that creates an Incantation object and then calls its create() method
def create_incantation(title: str, text: str):
    incantation_obj = Incantation(title=title, text=text)
    body_resp = incantation_obj.create()
    return incantation_obj

# get_incantation() is a convenience function that returns an Incantation object for an existing incantation, given its title
def get_incantation(incantation_title: str):
    incantations = get_incantations()
    
    # create incantation name to id map - incantations is a dict of incantation objects keyed on incantation_id
    incantation_from_title = {}
    for incantation_id in incantations.keys():
        incantation = incantations[incantation_id] # get the Incantation object
        title = incantation.title
        if title not in incantation_from_title:
            incantation_from_title[title] = incantation
        else:
            raise Exception('Duplicate incantation title: ' + title)
    
    if incantation_title in incantation_from_title:
        return incantation_from_title[incantation_title]
    else:
        raise Exception('Incantation title not found: ' + incantation_title)

# update_incantation() is a convenience function that updates an existing incantation, given its title
def update_incantation(incantation_title: str, new_text: str = None, new_title: str = None):
    incantation_obj = get_incantation(incantation_title)
    if new_title is not None:
        incantation_obj.title = new_title
    if new_text is not None:
        incantation_obj.text = new_text
    body_resp = incantation_obj.update()
    return incantation_obj

# list_incantations() is a convenience function that returns a dictionary of all Incantation objects for an account
def list_incantations(verbose=True):
    incantations = get_incantations()
    if verbose:
        print ("\nIncantations:")
        for incantation_obj in incantations.values():
            print (f"id: {incantation_obj.incantation_id}\ntitle: {incantation_obj.title}\ntext: {incantation_obj.text}\n")
    return incantations