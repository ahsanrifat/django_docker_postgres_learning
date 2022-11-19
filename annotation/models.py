from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class Data(models.Model):
    text = models.CharField(max_length=50, unique=True, null=False)
    project_id = models.IntegerField(null=False)
    group_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        db_table = 'data'
        indexes = [
            models.Index(fields=['is_done', ], name="data_is_done_indx"),
            models.Index(fields=['project_id', 'group_id'], name="pid_gid_indx"),
        ]


class Annotation(models.Model):
    annotator_id = models.IntegerField(null=False)
    is_annotated = models.BooleanField(default=False)
    is_accurate = models.BooleanField(default=None, blank=True, null=True)
    is_skipped = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="annotation")
    span_lines = ArrayField(
        models.JSONField(blank=True),
        default=[],
        size=50
    )

    class Meta:
        db_table = 'annotation'
        indexes = [
            models.Index(fields=['is_annotated', ], name="is_annotated_indx"),
            models.Index(fields=['annotator_id', ], name="annotator_id"),
            models.Index(fields=['data'], name="data_ann_indx"),
        ]


class Validation(models.Model):
    validator_id = models.IntegerField(null=False)
    is_validated = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.OneToOneField(Data, on_delete=models.CASCADE, related_name="validation")
    span_lines = ArrayField(
        models.JSONField(blank=True),
        default=[],
        size=50
    )

    class Meta:
        db_table = 'validation'
        indexes = [
            models.Index(fields=['validator_id', ], name="validator_id"),
            models.Index(fields=['is_validated', ], name="is_validated_indx"),
            models.Index(fields=['data'], name="data_val_indx"),
        ]
