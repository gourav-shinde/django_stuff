from import_export import resources
from .models import Students


class StudentsResources(resources.ModelResource):
	class Meta:
		model=Students