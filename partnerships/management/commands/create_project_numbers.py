from django.core.management.base import BaseCommand
from partnerships.models import ProjectNoInText


class Command(BaseCommand):
    help = 'Create default project numbers for the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of project numbers to create (default: 10)',
        )

    def handle(self, *args, **options):
        count = options['count']
        created_count = 0
        
        self.stdout.write('Creating project numbers...')
        
        for i in range(1, count + 1):
            project, created = ProjectNoInText.objects.get_or_create(
                project_no=i,
                defaults={'proj_type': 'Internal'}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created project number {i}')
            else:
                self.stdout.write(f'Project number {i} already exists')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new project numbers. '
                f'Total project numbers: {ProjectNoInText.objects.count()}'
            )
        )