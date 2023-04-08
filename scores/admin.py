from django.contrib import admin
from scores.models import Score
from django.utils.translation import gettext_lazy as _

class ScoreGreaterThanFilter(admin.SimpleListFilter):
    title = _('Score greater than')
    parameter_name = 'score_gt'

    def lookups(self, request, model_admin):
        return (
            ('1', _('1')),
            ('100', _('100')),
            ('1000', _('1000')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(score__gt=1)
        elif self.value() == '100':
            return queryset.filter(score__gt=100)
        elif self.value() == '1000':
            return queryset.filter(score__gt=1000)
        else:
            return queryset

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'user', 'date_submitted',)
    search_fields = ('score', 'user__username',)
    list_filter = (ScoreGreaterThanFilter, 'user', 'date_submitted',)

admin.site.register(Score, ScoreAdmin)