from rest_framework import serializers

class LicenseSerializer(serializers.Serializer):
    mac_address_list = serializers.ListField(child=serializers.CharField())
    ip_address_list = serializers.ListField(child=serializers.CharField())