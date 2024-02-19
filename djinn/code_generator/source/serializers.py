from rest_framework import serializers
from ..models import Model


class ModelSerializer(serializers.ModelSerializer):  # Do not change name
    class Meta:
        model = Model
        fields = []
        read_only_fields = []
        depth = 1


# Assign(
#  targets=[
#   Name(id='owner', ctx=Store())],
#  value=Call(
#   func=Attribute(
#    value=Name(id='serializers', ctx=Load()),
#    attr='ReadOnlyField',
#    ctx=Load()),
#   args=[],
#   keywords=[
#    keyword(
#     arg='source',
#     value=Constant(value='owner.username'))]))
# -----------------
# Assign(
#  targets=[
#   Name(id='owner', ctx=Store())],
#  value=Call(
#   func=Name(id='CreateUserSerializer', ctx=Load()),
#   args=[],
#   keywords=[]))
# -----------------
# Assign(
#  targets=[
#   Name(id='model', ctx=Store())],
#  value=Name(id='Model', ctx=Load()))
# -----------------
# Assign(
#  targets=[
#   Name(id='fields', ctx=Store())],
#  value=List(
#   elts=[
#    Constant(value='id'),
#    Constant(value='name'),
#    Constant(value='owner'),
#    Constant(value='status'),
#    Constant(value='is_premium'),
#    Constant(value='file')],
#   ctx=Load()))
