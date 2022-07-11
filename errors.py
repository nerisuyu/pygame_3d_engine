def WrongTypeErrorMessage(InstanceName,VarName,VarType,RequiredType):
    print(f"{InstanceName}: Error, {VarName} is type {VarType}, but {RequiredType} is required.")

def CheckIfInstance(name, value, type_):
    if not isinstance(value, type_):
        WrongTypeErrorMessage(name, value, type(value), type_)
        return False
    return True