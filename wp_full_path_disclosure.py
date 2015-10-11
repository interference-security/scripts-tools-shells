#!/usr/bin/python

#Python script to perform WordPress FPD check
#Tested on:
#Windows,Linux
#WordPress v4.2.2

try:
	from bs4 import BeautifulSoup
	import urllib2
	import requests
	import sys
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\tbs4, urllib2, requests, sys, ssl, lxml"
	exit(0)

if len(sys.argv)!=2:
	print "Usage: %s <target>"%sys.argv[0]
	exit(0)

target = sys.argv[1]
	
if target.endswith("/"):
	target = target[:-1]
	
if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

def checker(base_path, target_paths):
	for i in target_paths:
		try:
			target_url = target+base_path+str(i)
			r = requests.get(target_url, verify=False)
			sc = r.status_code
			if sc != 404 and sc != 500:
				html = urllib2.urlopen(target_url)
				soup = BeautifulSoup(html.read(), "lxml")
				allb = soup.find_all("b")
				#print allb[1]
				try:
					res = (str(allb[1]).replace("<b>","")).replace("</b>","")
					print str(target_url) + " : " + str(res)
				except Exception,e:
					#print str(e)
					pass
		except Exception,e:
			#print "Exception occurred"
			print str(e)

print "[*] Started"
requests.packages.urllib3.disable_warnings()
#wp-includes check
wp_includes_path = "/wp-includes/"
target_paths=["admin-bar.php", "atomlib.php", "author-template.php", "bookmark-template.php", "bookmark.php", "cache.php", "canonical.php", "capabilities.php", "category-template.php", "category.php", "class-IXR.php", "class-feed.php", "class-http.php", "class-json.php", "class-oembed.php", "class-phpass.php", "class-phpmailer.php", "class-pop3.php", "class-simplepie.php", "class-smtp.php", "class-snoopy.php", "class-wp-admin-bar.php", "class-wp-ajax-response.php", "class-wp-customize-control.php", "class-wp-customize-manager.php", "class-wp-customize-panel.php", "class-wp-customize-section.php", "class-wp-customize-setting.php", "class-wp-customize-widgets.php", "class-wp-editor.php", "class-wp-embed.php", "class-wp-error.php", "class-wp-http-ixr-client.php", "class-wp-image-editor-gd.php", "class-wp-image-editor-imagick.php", "class-wp-image-editor.php", "class-wp-theme.php", "class-wp-walker.php", "class-wp-xmlrpc-server.php", "class-wp.php", "class.wp-dependencies.php", "class.wp-scripts.php", "class.wp-styles.php", "comment-template.php", "comment.php", "compat.php", "cron.php", "date.php", "default-constants.php", "default-filters.php", "default-widgets.php", "deprecated.php", "feed-atom-comments.php", "feed-atom.php", "feed-rdf.php", "feed-rss.php", "feed-rss2-comments.php", "feed-rss2.php", "feed.php", "files.txt", "formatting.php", "functions.php", "functions.wp-scripts.php", "functions.wp-styles.php", "general-template.php", "http.php", "kses.php", "l10n.php", "link-template.php", "load.php", "locale.php", "media-template.php", "media.php", "meta.php", "ms-blogs.php", "ms-default-constants.php", "ms-default-filters.php", "ms-deprecated.php", "ms-files.php", "ms-functions.php", "ms-load.php", "ms-settings.php", "nav-menu-template.php", "nav-menu.php", "option.php", "pluggable-deprecated.php", "pluggable.php", "plugin.php", "post-formats.php", "post-template.php", "post-thumbnail-template.php", "post.php", "query.php", "registration-functions.php", "registration.php", "revision.php", "rewrite.php", "rss-functions.php", "rss.php", "script-loader.php", "session.php", "shortcodes.php", "taxonomy.php", "template-loader.php", "template.php", "theme.php", "update.php", "user.php", "vars.php", "version.php", "widgets.php", "wp-db.php", "wp-diff.php"]
checker(wp_includes_path, target_paths)
#wp-admin check
wp_admin_path = "/wp-admin/"
target_paths=["about.php", "admin-ajax.php", "admin-footer.php", "admin-functions.php", "admin-header.php", "admin-post.php", "admin.php", "async-upload.php", "comment.php", "credits.php", "custom-background.php", "custom-header.php", "customize.php", "edit-comments.php", "edit-form-advanced.php", "edit-form-comment.php", "edit-link-form.php", "edit-tag-form.php", "edit-tags.php", "edit.php", "export.php", "freedoms.php", "import.php", "index.php", "install-helper.php", "install.php", "link-add.php", "link-manager.php", "link-parse-opml.php", "link.php", "load-scripts.php", "load-styles.php", "media-new.php", "media-upload.php", "media.php", "menu-header.php", "menu.php", "moderation.php", "ms-admin.php", "ms-delete-site.php", "ms-edit.php", "ms-options.php", "ms-sites.php", "ms-themes.php", "ms-upgrade-network.php", "ms-users.php", "my-sites.php", "nav-menus.php", "network.php", "options-discussion.php", "options-general.php", "options-head.php", "options-media.php", "options-permalink.php", "options-reading.php", "options-writing.php", "options.php", "plugin-editor.php", "plugin-install.php", "plugins.php", "post-new.php", "post.php", "press-this.php", "profile.php", "revision.php", "setup-config.php", "theme-editor.php", "theme-install.php", "themes.php", "tools.php", "update-core.php", "update.php", "upgrade-functions.php", "upgrade.php", "upload.php", "user-edit.php", "user-new.php", "users.php", "widgets.php"]
checker(wp_admin_path, target_paths)
print "[*] Completed"
