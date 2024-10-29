from django.contrib import admin

from .models import *

admin.site.register(Certificate)
admin.site.register(CertificateCategory)
admin.site.register(CertificateSubCategory)
