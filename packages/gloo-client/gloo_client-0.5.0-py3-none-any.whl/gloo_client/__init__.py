from .client import GlooClient

x = GlooClient(api_key='asdfas')
x.app().create()
x.document_group().update_status()