def string_to_list(message):
        output = []
        
        for item in message.split(","):
            if " " not in item:
                if item.isdigit():
                    output.append(int(item))
                else:
                    output.append(item)
            else:
                temp = []
                
                for element in item.split(" "):
                    temp.append(int(element))
                output.append(temp[:])
        return output
def list_to_string(message:list)->str:
        output = ""
        for item in message:
            if isinstance(item,(int,str)):
                output += str(item)
            elif isinstance(item,(list,tuple)):
                for element in item:
                    output += str(element)+" "
                output = output[:-1]
            output += ","
        
        return output[:-1]
