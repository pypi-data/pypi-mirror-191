from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_dx_review.models import ReasonsForTesting
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField
from edc_rx.model_mixins import TreatmentPayMethodsModelMixin

from ..model_mixins import ClinicalReviewModelMixin, CrfModelMixin


class ClinicalReview(
    TreatmentPayMethodsModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    hiv_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for HIV infection?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=format_html(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    hiv_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    hiv_reason = models.ManyToManyField(
        ReasonsForTesting,
        related_name="hiv_test_reason",
        verbose_name="Why was the patient tested for HIV infection?",
        blank=True,
    )

    hiv_reason_other = OtherCharField()

    hiv_dx = models.CharField(
        verbose_name="As of today, was the patient newly diagnosed with HIV infection?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    htn_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for hypertension?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=format_html(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    htn_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    htn_reason = models.ManyToManyField(
        ReasonsForTesting,
        related_name="htn_test_reason",
        verbose_name="Why was the patient tested for hypertension?",
        blank=True,
    )

    htn_reason_other = OtherCharField()

    htn_dx = models.CharField(
        verbose_name="As of today, was the patient newly diagnosed with hypertension?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    dm_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for diabetes?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=format_html(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    dm_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    dm_reason = models.ManyToManyField(
        ReasonsForTesting,
        related_name="dm_reason",
        verbose_name="Why was the patient tested for diabetes?",
        blank=True,
    )

    dm_reason_other = OtherCharField()

    dm_dx = models.CharField(
        verbose_name="As of today, was the patient newly diagnosed with diabetes?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    complications = models.CharField(
        verbose_name="Since last seen, has the patient had any complications",
        max_length=15,
        choices=YES_NO,
        help_text="If Yes, complete the `Complications` CRF",
    )

    reason_other = OtherCharField()

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review"
        verbose_name_plural = "Clinical Reviews"
