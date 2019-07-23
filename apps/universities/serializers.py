from rest_framework import serializers

from universities.models import Education, University

__all__ = (
    'UniversitySerializer',
    'EducationSerializer',
)


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ('is_verified', 'keywords', )


class EducationSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_name = serializers.CharField(write_only=True, source='university')

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        if context['request'].method == 'GET' and 'pk' not in context['view'].kwargs:
            # in case if it's a list action we don't need the description field
            self.fields.pop('description')
        super(EducationSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        university_name = data['university']
        data['university'], _ = University.objects.get_or_create(
            defaults={'name': university_name},
            name__iexact=university_name,
        )
        return data

    class Meta:
        model = Education
        exclude = ('user', )
