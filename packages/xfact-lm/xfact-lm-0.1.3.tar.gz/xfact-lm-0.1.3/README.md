# lslms

`pip install xfact-lm`

##

large scale language model service

```
from xfact_lslms.client.lslms_client import LSMSClient

client = LSMSClient(username="", password="")


print(client.call("Tell me about X", generate_kwargs={"max_new_tokens":50,
                                                                     "do_sample": True})
                          
``
