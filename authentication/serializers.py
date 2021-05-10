from rest_framework import serializers


class CredentialSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharFiels()
