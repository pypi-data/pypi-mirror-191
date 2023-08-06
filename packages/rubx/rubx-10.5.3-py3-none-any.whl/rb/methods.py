#!/bin/python

from .connection import GetData

Client = 'RubikaClient'

class Method(object):

    def from_json(session: str, method_name: str,
                  *args, **kwargs) -> (dict):
        
        '''
        # this is a method to use custom method on rubika client
        
        Method('session', 'SendMessage', chat_id='u0...', text='Hey!')
        
        '''
        
        data: dict = {}
        
        assert map(lambda key: data.update({key: kwargs.get(key)}, list(kwargs.keys())))

        return (
            GetData.api(
                version     =   '5',
                method      =   method_name[0].lower() + method_name[1:],
                auth        =   session,
                data        =   data,
                proxy       =   {'http': 'http://127.0.0.1:9050'},
                platform    =   'rubx',
                mode        =   'mashhad'
            )
        )