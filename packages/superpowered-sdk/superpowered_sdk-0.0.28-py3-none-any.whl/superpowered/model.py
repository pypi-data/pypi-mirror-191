from main import BASE_URL, _format_http_response, get_headers
from incantation import get_incantation
import requests
import time

class Model:
    def __init__(self, model_spec: dict, supp_id: str = None, description: str = None, model_id: str = None):
        self.model_id = model_id
        self.model_spec = model_spec
        self.title = model_spec['model_title']
        self.supp_id = supp_id
        self.description = description
        self.is_deployed = self.model_id is not None
        self.model_instances = self.get_instances()

    def create(self):
        if self.is_deployed:
            raise Exception('This model has already been deployed: ' + self.model_id)
        url = BASE_URL + 'models'
        payload = {
            'model_spec': self.model_spec,
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description

        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        self.model_id = resp['body']['id']
        self.is_deployed = True
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This model has not been deployed yet. Please run `model.create()` before running `model.update()')
        url = BASE_URL + f'models/{self.model_id}'
        payload = {}
        if self.model_spec is not None:
            payload['model_spec'] = self.model_spec
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=get_headers(), json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'models/{self.model_id}'
        _format_http_response(requests.delete(url, headers=get_headers()))

    def get_instances(self):
        url = BASE_URL + f'models/{self.model_id}/instances'
        resp = _format_http_response(requests.get(url, headers=get_headers()))
        instances = {}
        for instance in resp['body']:
            inst = ModelInstance(
                ai_name=instance['ai_name'],
                model_id=instance['model_id'],
                supp_id=instance['supp_id'],
                description=instance['description'],
                instance_id=instance['id'],
            )
            instances[instance['id']] = inst
        return instances

    # convenience method
    def create_instance(self, ai_name: str = "AI", knowledge_bases: list = None):
        # TODO: add support for passing in knowledge bases by name instead of id
        instance_obj = ModelInstance(model_id=self.model_id, ai_name=ai_name, knowledge_bases=knowledge_bases)
        resp_body = instance_obj.create()
        return instance_obj

    # convenience method for non-conversational use case - TODO: this is not an efficient way to do this
    def run(self, prompt: str) -> str:
        # create a new instance
        instance_obj = self.create_instance()
        instance_id = instance_obj.instance_id

        # get the response
        url = BASE_URL + f'models/{self.model_id}/instances/{instance_id}/get_response'
        human_input = [{"prefix": "", "content": prompt}]
        payload = {
            'human_input': human_input
        }
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        return resp['body']['model_response']['content']


class ModelInstance:
    def __init__(self, ai_name: str, knowledge_bases: list = None, model_id: str = None, supp_id: str = None, description: str = None, instance_id = None):
        self.ai_name = ai_name
        self.knowledge_bases = knowledge_bases # list of knowledge base ids
        self.model_id = model_id
        self.supp_id = supp_id
        self.description = description
        self.instance_id = instance_id
        self.chat_history = []
        self.get_chat_history()
        self.is_deployed = self.instance_id is not None

    def get_chat_history(self):
        # get chat history interactions with pagination
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}/chat_history'
        response = _format_http_response(requests.get(url, headers=get_headers()))
        self.chat_history.extend(response['body']['interactions'])
        while 'next_page_token' in response:
            response = _format_http_response(requests.get(url, headers=get_headers(), params={'next_page_token': response['next_page_token']}))
            self.chat_history.extend(response['body']['interactions'])

    def create(self):
        if self.is_deployed:
            raise Exception('This model instance has already been deployed: ' + self.instance_id)
        url = BASE_URL + f'models/{self.model_id}/instances'
        payload = {'ai_name': self.ai_name}
        if self.knowledge_bases is not None:
            payload['knowledge_bases'] = self.knowledge_bases
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        self.instance_id = resp['body']['id']
        self.is_deployed = True
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This model instance has not been deployed yet. Please run `model_instance.create()` before running `model_instance.update()')
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}'
        payload = {}
        if self.knowledge_bases is not None:
            payload['knowledge_bases'] = self.knowledge_bases
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=get_headers(), json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}'
        resp = _format_http_response(requests.delete(url, headers=get_headers()))
        return resp['body']

    def respond(self, human_input):
        # human input can a list of dicts with prefix and content or just a single dict of that form
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}/get_response'
        payload = {
            'human_input': human_input
        }
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        self.chat_history.insert(0, resp['body']['interaction'])
        return resp['body']


def get_models():
    models = {}
    url = BASE_URL + 'models'
    resp = requests.get(url, headers=get_headers())
    resp = _format_http_response(resp)
    for model in resp['body']:
        m = Model(
            model_id=model['id'],
            model_spec=model['model_spec'],
            supp_id = model['supp_id'],
            description=model['description']
        )
        models[model['id']] = m
    return models

# use this to handle different formats of model_spec
def model_spec_preprocessing(model_spec: dict):
    # if incantation_names is in the model_spec, replace it with incantation_ids
    if "incantation_names" in model_spec and "incantation_ids" not in model_spec:
        incantation_names = model_spec["incantation_names"]
        incantation_ids = []
        for incantation_name in incantation_names:
            incantation_ids.append(get_incantation(incantation_name).incantation_id)
        model_spec["incantation_ids"] = incantation_ids
        del model_spec["incantation_names"] 
    return model_spec

# create_model() is a convenience function that creates a Model object and then calls its create() method
def create_model(model_spec: dict = {}, verbose: bool = False):
    # check for the two required fields and add default values if they are not present
    if "model_title" not in model_spec:
        model_spec["model_title"] = "Untitled model " + str(int(time.time()))
    if "incantation_names" not in model_spec and "incantation_ids" not in model_spec:
        model_spec["incantation_ids"] = []
    model_spec = model_spec_preprocessing(model_spec)
    if verbose: print ("Model spec:\n", model_spec)
    model_obj = Model(model_spec=model_spec)
    body_resp = model_obj.create()
    return model_obj

# get_model() is a convenience function that returns a Model object for an existing model, given its title
def get_model(model_title: str):
    models = get_models()
    # create model name to id map - models is a dict of model objects keyed on model_id
    model_from_title = {}
    for model_id in models.keys():
        model = models[model_id] # get the Model object
        title = model.title
        if title not in model_from_title:
            model_from_title[title] = model
        else:
            pass #raise Exception('Duplicate model title: ' + title)
    
    if model_title in model_from_title:
        return model_from_title[model_title]
    else:
        raise Exception('Model title not found: ' + model_title)

# update_model() is a convenience function that updates an existing model, given its title and a new model_spec
def update_model(model_title: str, new_model_spec: dict):
    new_model_spec = model_spec_preprocessing(new_model_spec)
    model_obj = get_model(model_title)
    current_model_spec = model_obj.model_spec
    
    # just update the keys that are in the new_model_spec
    for key in new_model_spec.keys():
        current_model_spec[key] = new_model_spec[key]
    model_obj.model_spec = current_model_spec
    resp_body = model_obj.update()
    return model_obj

# list_models() is a convenience function that returns a dictionary of all Model objects for an account
def list_models(verbose=False):
    models = get_models()
    if verbose:
        print ("\nModels:")
        for model_obj in models.values():
            print (f"id: {model_obj.model_id}\ntitle: {model_obj.title}\nmodel_spec: {model_obj.model_spec}\n")
    return models

# list_instances() is a convenience function that returns a dictionary of ModelInstance objects for an existing model, given its title
def list_instances(model_title: str, verbose=True):
    model = get_model(model_title)
    instances = model.get_instances()
    if verbose:
        print ("\nModel instances:")
        for instance_obj in instances.values():
            print (f"id: {instance_obj.instance_id}\nai name: {instance_obj.ai_name}\nlast chat: {instance_obj.chat_history[:1]}\n")
    return instances