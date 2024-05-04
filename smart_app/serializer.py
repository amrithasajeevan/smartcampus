from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, login 
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator


from django.utils.translation import gettext_lazy as _

class CustomUserSerializer(serializers.ModelSerializer):
    # Regular expression validators
    # password_regex = RegexValidator(
    #     regex=r'^[A-Za-z]{3}@[0-9]{3}$',
    #     message=_('Please enter a valid password')
    # )

    start_year_regex = RegexValidator(
        regex=r'^[0-9]{4}$',
        message=_('Start year must be a 4-digit number')
    )

    end_year_regex = RegexValidator(
        regex=r'^[0-9]{4}$',
        message=_('End year must be a 4-digit number')
    )

    # password = serializers.CharField(write_only=True, validators=[password_regex, validate_password])
    start_year = serializers.CharField(validators=[start_year_regex])
    end_year = serializers.CharField(validators=[end_year_regex])

    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'middle_name', 'last_name', 'image', 'admission_number', 'date_of_birth',
                  'blood_group', 'place', 'email', 'phone_number', 'department', 'course', 'batch', 'start_year',
                  'end_year', 'barcode', 'password']
        extra_kwargs = {
            'middle_name': {'required': False}
        }

    def validate(self, attrs):
        # Additional validation for start_year and end_year
        start_year = attrs.get('start_year')
        end_year = attrs.get('end_year')

        if start_year and end_year:
            if int(start_year) >= int(end_year):
                raise serializers.ValidationError(_('Start year must be lesser than end year'))

        return attrs
    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    


class Loginserializer(serializers.Serializer):
    admission_number=serializers.CharField(max_length=10)
    password=serializers.CharField(max_length=10)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'username','first_name', 'middle_name', 'last_name', 'email', 'image',  'date_of_birth', 'blood_group', 'place', 'phone_number', 'department', 'course', 'batch', 'start_year', 'end_year']