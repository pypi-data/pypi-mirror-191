from rest_framework import serializers


__all__ = [
    "AbstractAPIRequestLogSerializer",
    "AbstractAPIRequestLogListSerializer",
]


class AbstractAPIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = [
            "id",
            "created",
            "is_success",
            "url",
            "method",
            "params",
            "request_headers",
            "request_body",
            "status_code",
            "response_time",
            "response_headers",
            "response_body",
        ]


class AbstractAPIRequestLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = [
            "id",
            "created",
            "is_success",
            "url",
            "method",
            "status_code",
            "response_time",
        ]
