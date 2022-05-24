from badges.models import *
from rest_framework import serializers

from myapi.serializers.user_serializers import * 

class VariableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variable
        fields = "__all__"


class RulesSerializer(serializers.ModelSerializer):
    variable = VariableSerializer()
    group_key = serializers.IntegerField(required=False)
    class Meta:
        model = Rules
        fields = "__all__"

    def create(self, validated_data):
        var = validated_data.pop("variable")
        variable,created = Variable.objects.get_or_create(**var)
        rule = Rules.objects.create(**validated_data,variable=variable)
        return rule

    def update(self, instance, validated_data):
        '''
        updating rules attr 
        Note -> can't update achivement_level after created 
                delete rule & create new one or provide list of acheivement_level and 
        '''
        try:
            #update name of variable ``only``
            var_data = validated_data.pop("variable")
            variable = instance.variable
            VariableSerializer.update(variable,var_data)
        except KeyError:
            pass

        data = validated_data
        instance.formula = data.get("formula",instance.formula)
        instance.interval = data.get("interval",instance.interval)
        instance.evalution_type = data.get("evalution_type",instance.evalution_type)
        instance.variable = data.get("variable",instance.variable)
        instance.save()
        return instance
        