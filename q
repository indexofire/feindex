[1mdiff --git a/feindex/apps/initial/models.py b/feindex/apps/initial/models.py[m
[1mindex cda94af..e97d79b 100644[m
[1m--- a/feindex/apps/initial/models.py[m
[1m+++ b/feindex/apps/initial/models.py[m
[36m@@ -28,26 +28,34 @@[m [mPage.register_extensions([m
 # Register Templates used in pages[m
 Page.register_templates([m
     {[m
[31m-        'key': 'c1',[m
[32m+[m[32m        'key': 'index',[m
[32m+[m[32m        'title': _('Index Page'),[m
[32m+[m[32m        'path': 'site_index.html',[m
[32m+[m[32m        'regions': ([m
[32m+[m[32m            ('main', _('Main content area')),[m
[32m+[m[32m        ),[m
[32m+[m[32m    },[m
[32m+[m[32m    {[m
[32m+[m[32m        'key': 'col_1',[m
         'title': _('One Columns Page'),[m
[31m-        'path': 'col_one.html',[m
[32m+[m[32m        'path': 'site_col_one.html',[m
         'regions': ([m
             ('main', _('Main content area')),[m
         ),[m
     },[m
     {[m
[31m-        'key': 'c2',[m
[32m+[m[32m        'key': 'col_2',[m
         'title': _('Two Columns Page'),[m
[31m-        'path': 'col_two.html',[m
[32m+[m[32m        'path': 'site_col_two.html',[m
         'regions': ([m
             ('main', _('Main content area')),[m
             ('left', _('Left Side'), 'inherited'),[m
         ),[m
     },[m
     {[m
[31m-        'key': 'c3',[m
[32m+[m[32m        'key': 'col_3',[m
         'title': _('Three Columns Page'),[m
[31m-        'path': 'col_three.html',[m
[32m+[m[32m        'path': 'site_col_three.html',[m
         'regions': ([m
             ('main', _('Main content area')),[m
             ('sidebar', _('Sidebar'), 'inherited'),[m
[36m@@ -55,15 +63,7 @@[m [mPage.register_templates([m
         ),[m
     },[m
     {[m
[31m-        'key': 'index',[m
[31m-        'title': _('Index Page'),[m
[31m-        'path': 'index.html',[m
[31m-        'regions': ([m
[31m-            ('main', _('Main content area')),[m
[31m-        ),[m
[31m-    },[m
[31m-    {[m
[31m-        'key': 'uc',[m
[32m+[m[32m        'key': 'under_construction',[m
         'title': _('Under Construction'),[m
         'path': 'under_construction.html',[m
         'regions': ([m
[36m@@ -71,7 +71,7 @@[m [mPage.register_templates([m
         ),[m
     },[m
     {[m
[31m-        'key': 'labm',[m
[32m+[m[32m        'key': 'lab_member',[m
         'title': _('Lab Member'),[m
         'path': 'isotope.html',[m
         'regions': ([m
[1mdiff --git a/feindex/feindex/settings/common.py b/feindex/feindex/settings/common.py[m
[1mindex 97771cb..acf99ea 100644[m
[1m--- a/feindex/feindex/settings/common.py[m
[1m+++ b/feindex/feindex/settings/common.py[m
[36m@@ -173,3 +173,8 @@[m [mLOGGING = {[m
 [m
 # Use new feincms reverse[m
 FEINCMS_REVERSE_MONKEY_PATCH = False[m
[32m+[m
[32m+[m[32m# Feincms richtext editor[m
[32m+[m[32mFEINCMS_RICHTEXT_INIT_CONTEXT = {[m
[32m+[m[32m    'TINYMCE_JS_URL': '%slibs/tiny_mce/tiny_mce.js' % STATIC_URL,[m
[32m+[m[32m}[m
[1mdiff --git a/feindex/feindex/urls.py b/feindex/feindex/urls.py[m
[1mindex 72765cf..4182273 100644[m
[1m--- a/feindex/feindex/urls.py[m
[1m+++ b/feindex/feindex/urls.py[m
[36m@@ -1,6 +1,6 @@[m
 # -*- coding: utf-8 -*-[m
[31m-from django.conf import settings[m
 from django.contrib import admin[m
[32m+[m[32mfrom django.conf import settings[m
 from django.conf.urls import patterns, include, url[m
 from django.views.generic.base import RedirectView[m
 [m
[1mdiff --git a/feindex/templates/default/site_index.html b/feindex/templates/default/site_index.html[m
[1mindex 11db76c..3c36e20 100644[m
[1m--- a/feindex/templates/default/site_index.html[m
[1m+++ b/feindex/templates/default/site_index.html[m
[36m@@ -1,5 +1,5 @@[m
 {% extends "site_base.html" %}[m
[31m-{% load i18n article_tags account_tags applicationcontent_tags %}[m
[32m+[m[32m{% load i18n applicationcontent_tags %}[m
 [m
 {% block extra_head %}[m
 <link rel="stylesheet" href="{{ THEME_URL }}js/flexslider/flexslider.css" type="text/css"/>[m
[36m@@ -57,34 +57,6 @@[m [m$(window).load(function() {[m
 </div>[m
 <!-- intro end -->[m
 [m
[31m-<div class="container pad">[m
[31m-<div class="row">[m
[31m-  <div class="overline">[m
[31m-    <h3 style="margin-left:20px">Who We Are ?</h3>[m
[31m-  </div>[m
[31m-  <div class="span12">[m
[31m-  <h3 style="background: #EEE;padding: 10px;">最新成员</h3>[m
[31m-  {% get_accounts 12 as accounts %}[m
[31m-  {% for account in accounts %}[m
[31m-    {% if forloop.first %}[m
[31m-    <ul style="padding: 1px">[m
[31m-    {% endif %}[m
[31m-    <li style="list-style:none; display: inline;padding:1px"><a href="{% app_reverse 'account-profile-detail' 'account.urls' account.user.username %}" title="{{ account.name }}"><img src="{{ account.get_avatar_url }}" height="48" width="48" style="border:1px solid #BCBCBC; padding: 1px" /></a></li>[m
[31m-    {% if forloop.last %}[m
[31m-    </ul>[m
[31m-    {% endif %}[m
[31m-  {% endfor %}[m
[31m-  </div>[m
[31m-</div>[m
[31m-</div>[m
[31m-[m
[31m-<div class="container pad">[m
[31m-<div class="row">[m
[31m-  <div class="overline">[m
[31m-    <h3 style="margin-left:20px">Where We Are ?</h3>[m
[31m-  </div>[m
[31m-</div>[m
[31m-</div>[m
 {% endblock %}[m
 [m
 [m
[36m@@ -106,16 +78,7 @@[m [m$(window).load(function() {[m
   </div>[m
   <div class="span4">[m
     <h3>资料更新</h3>[m
[31m-    {% get_articles 5 as recent %}[m
[31m-    {% for article in recent %}[m
[31m-      {% if forloop.first %}[m
[31m-      <ul>[m
[31m-      {% endif %}[m
[31m-        <li><a href="{% app_reverse 'articles_display_article' 'article.urls' article.publish_date.year article.slug %}" title="Read this article">{{ article.title }}</a></li>[m
[31m-      {% if forloop.last %}[m
[31m-      </ul>[m
[31m-      {% endif %}[m
[31m-    {% endfor %}[m
[32m+[m
   </div>[m
   <div class="span4">[m
     <h3>联系我们</h3>[m
