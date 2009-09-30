==================
 Installing Audit 
==================

Follow these steps:

1. Download the source code from the git repository:
   http://git.andreanjos.org/audit.git/.git/ or
   andreanjos@git.andreanjos.org:git/audit.git, if you have the proper
   permissons. Go into the downloaded directory and execute:
   "python ./setup.py install" to install the module into your python site
   installation.

2. Link "audit/media" to your "media" directory in such way that
   $MEDIA_ROOT/audit contains the "db" directory.

3. Go into $MEDIA_ROOT/audit and download the GeoIP databases by issuing:
   "chmod 755 install.sh && make all"

4. Go into your project's "settings.py" file and make sure to include
   "audit.middleware.Activity" in your middleware stack, near to the end. Do
   not put it before authentication. The, include "audit" in your list of
   installed applications.

5. Go to the root of your project and execute "syncdb" to install the DB models

6. Add the "audit" URLs to your main "urls.py" file

7. Copy the templates at "audit/templates/audit" to your own templates
   directory and edit them as you see fit.

8. In the "admin" interface make sure all people that is allowed to access the
   statistics information has the "view_audit" permission.
