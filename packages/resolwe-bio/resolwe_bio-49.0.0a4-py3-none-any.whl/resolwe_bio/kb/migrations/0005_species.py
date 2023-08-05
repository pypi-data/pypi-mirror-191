# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resolwe_bio_kb", "0004_add_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="mapping",
            name="source_species",
            field=models.CharField(default="unknown", max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mapping",
            name="target_species",
            field=models.CharField(default="unknown", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="feature",
            name="sub_type",
            field=models.CharField(
                choices=[
                    ("protein-coding", "Protein-coding"),
                    ("pseudo", "Pseudo"),
                    ("rRNA", "rRNA"),
                    ("ncRNA", "ncRNA"),
                    ("snRNA", "snRNA"),
                    ("snoRNA", "snoRNA"),
                    ("tRNA", "tRNA"),
                    ("asRNA", "asRNA"),
                    ("other", "Other"),
                    ("unknown", "Unknown"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="type",
            field=models.CharField(
                choices=[
                    ("gene", "Gene"),
                    ("transcript", "Transcript"),
                    ("exon", "Exon"),
                    ("probe", "Probe"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="mapping",
            name="relation_type",
            field=models.CharField(
                choices=[
                    ("crossdb", "Crossdb"),
                    ("ortholog", "Ortholog"),
                    ("transcript", "Transcript"),
                    ("exon", "Exon"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="feature",
            unique_together=set([("source", "feature_id", "species")]),
        ),
        migrations.AlterUniqueTogether(
            name="mapping",
            unique_together=set(
                [
                    (
                        "source_db",
                        "source_id",
                        "source_species",
                        "target_db",
                        "target_id",
                        "target_species",
                        "relation_type",
                    )
                ]
            ),
        ),
        migrations.AlterIndexTogether(
            name="mapping",
            index_together=set(
                [
                    ("source_db", "source_id", "source_species", "target_db"),
                    ("target_db", "target_id", "target_species"),
                ]
            ),
        ),
    ]
