# **kwargs  alows to pass any number of keyword arguement
## keyword arguement means that they contain key - value pair like python dictionary
def country(**kwargs):
    for (key,values) in kwargs.items():
        print(key,'->',values)
        
    return key ,values
print(country(india = 'Delhi', srilanka = 'colombo', europe = 'germany'))
    