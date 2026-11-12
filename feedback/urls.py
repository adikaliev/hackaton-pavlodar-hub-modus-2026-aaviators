from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("as/<str:external_id>/", views.login_as, name="login_as"),
    path("switch/", views.switch_persona, name="switch"),
    path("demo/clock/", views.demo_clock, name="demo_clock"),
    path("demo/reset/", views.demo_reset, name="demo_reset"),
    path("new/", views.appeal_new, name="new"),
    path("hints/", views.api_hints, name="hints"),
    path("my/", views.my, name="my"),
    path("inbox/", views.inbox, name="inbox"),
    path("all/", views.registry, name="registry"),
    path("a/<str:number>/", views.appeal_detail, name="appeal"),
    path("a/<str:number>/do/<slug:action>/", views.appeal_action, name="action"),
    path("files/<int:pk>/", views.attachment, name="attachment"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("done/", views.done_feed, name="done"),
    path("notifications/", views.notifications, name="notifications"),
    path("rules/", views.rules, name="rules"),
    path("integrations/", views.integrations, name="integrations"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.open_admin, name="open_admin"),
]
