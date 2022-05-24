
from abc import ABC, abstractmethod
class Permission(ABC):
    @abstractmethod
    def check_permission(self,request,action=None,obj=None):
        pass

    def __and__(self,other):
        ''' & '''
        return And(self,other)
    def __or__(self,other):
        ''' |'''
        return Or(self,other)
        

class PermissionOperator(Permission):
    def __init__(self, *components):
        self.components = tuple(components)

    def check_permission(self, request, action=None, obj=None):
        return super().check_permission(request, action, obj)


class Not(PermissionOperator):
    """
    Negation operator as permission composable component.
    """

    # Overwrites the default constructor for fix
    # to one parameter instead of variable list of them.
    def __init__(self, component):
        super().__init__(component)

    def check_permission(self, *args, **kwargs):
        component = self.components[0]
        return (not component.check_permission(*args, **kwargs))


class Or(PermissionOperator):
    """
    Or logical operator as permission component.
    """

    def check_permission(self, *args, **kwargs):
        valid = False

        for component in self.components:
            if component.check_permission(*args, **kwargs):
                valid = True
                break

        return valid


class And(PermissionOperator):
    """
    And logical operator as permission component.
    """

    def check_permission(self, *args, **kwargs):
        valid = True

        for component in self.components:
            if not component.check_permission(*args, **kwargs):
                valid = False
                break

        return valid