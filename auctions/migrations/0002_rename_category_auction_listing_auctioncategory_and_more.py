# Generated by Django 4.2.7 on 2023-12-11 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listing',
            old_name='category',
            new_name='auctionCategory',
        ),
        migrations.RenameField(
            model_name='auction_listing',
            old_name='imageLink',
            new_name='auctionImageLink',
        ),
        migrations.RenameField(
            model_name='auction_listing',
            old_name='user',
            new_name='auctionOwner',
        ),
        migrations.RenameField(
            model_name='auction_listing',
            old_name='title',
            new_name='auctionTitle',
        ),
        migrations.RemoveField(
            model_name='auction_listing',
            name='price',
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='is_auctionOwner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('commentDate', models.DateTimeField(auto_now_add=True)),
                ('auctionName', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction_listing')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidPrice', models.FloatField(blank=True, default=0, null=True)),
                ('bid_Name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidTitleName', to='auctions.auction_listing')),
                ('bidderName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='Price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
