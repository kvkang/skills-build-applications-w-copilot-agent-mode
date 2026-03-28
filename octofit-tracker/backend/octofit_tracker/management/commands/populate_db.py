from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # 先删除依赖表（外键依赖顺序）
            for model in [Activity, User, Leaderboard, Workout]:
                for obj in model.objects.all():
                    try:
                        obj.delete()
                    except Exception:
                        pass
            for obj in Team.objects.all():
                try:
                    obj.delete()
                except Exception:
                    pass

            # 创建团队
            marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
            dc = Team.objects.create(name='DC', description='DC Superheroes')

            # 创建用户
            tony = User.objects.create(email='tony@stark.com', username='IronMan', team=marvel)
            steve = User.objects.create(email='steve@rogers.com', username='CaptainAmerica', team=marvel)
            bruce = User.objects.create(email='bruce@banner.com', username='Hulk', team=marvel)
            clark = User.objects.create(email='clark@kent.com', username='Superman', team=dc)
            brucew = User.objects.create(email='bruce@wayne.com', username='Batman', team=dc)
            diana = User.objects.create(email='diana@prince.com', username='WonderWoman', team=dc)

            # 创建活动
            Activity.objects.create(user=tony, type='Run', duration=30, calories=300, date='2026-03-28')
            Activity.objects.create(user=steve, type='Swim', duration=45, calories=400, date='2026-03-27')
            Activity.objects.create(user=bruce, type='Lift', duration=60, calories=500, date='2026-03-26')
            Activity.objects.create(user=clark, type='Fly', duration=120, calories=1000, date='2026-03-25')
            Activity.objects.create(user=brucew, type='MartialArts', duration=50, calories=450, date='2026-03-24')
            Activity.objects.create(user=diana, type='Run', duration=40, calories=350, date='2026-03-23')

            # 创建锻炼
            w1 = Workout.objects.create(name='Avengers Circuit', description='Full body workout')
            w2 = Workout.objects.create(name='Justice League HIIT', description='High intensity interval training')
            w1.suggested_for.add(marvel)
            w2.suggested_for.add(dc)

            # 创建排行榜
            Leaderboard.objects.create(team=marvel, points=1200)
            Leaderboard.objects.create(team=dc, points=1100)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
