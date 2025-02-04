



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'password']

