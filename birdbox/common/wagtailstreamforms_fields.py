# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from wagtailstreamforms.fields import (
    BaseField,
    register,
)
from wagtailstreamforms.wagtailstreamforms_fields import CheckboxesField as OriginalCheckboxesField


@register("date")
class DateField(BaseField):
    field_class = forms.DateField
    icon = "date"
    label = "Date field"
    widget = forms.widgets.DateInput(attrs={"type": "date"})


@register("datetime")
class DateTimeField(BaseField):
    field_class = forms.SplitDateTimeField
    icon = "time"
    label = "Datetime field"
    widget = forms.widgets.SplitDateTimeWidget(
        date_attrs={"type": "date"},
        time_attrs={"type": "time"},
    )


@register("checkboxes")
class CheckboxesField(OriginalCheckboxesField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.widgets.CheckboxSelectMultiple(
            attrs={"class": "birdbox-checkbox-select-multiple-margin-fix"},
        )
