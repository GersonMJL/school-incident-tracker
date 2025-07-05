# class SchoolAdminAdmin(admin.ModelAdmin):
#     form = SchoolAdminPageForm

#     list_display = ("name", "email", "created_at", "updated_at")
#     search_fields = ("name", "email")
#     list_filter = ("created_at",)
#     ordering = ["-created_at"]
#     fields = ("user", "name", "email", "password")
#     readonly_fields = ("created_at", "updated_at")

#     def save_model(self, request, obj, form, change):
#         # Save the user and password changes (if any)
#         obj.save()  # This triggers the custom save method in the model
#         if form.cleaned_data.get("password"):
#             obj.user.save()  # Save user after password change

#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # If the object already exists, make email readonly
#             return self.readonly_fields + ("email",)
#         return self.readonly_fields


# admin.site.register(SchoolAdmin, SchoolAdminAdmin)
