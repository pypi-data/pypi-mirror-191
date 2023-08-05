
EdX Analytics Logger
====================

Simple yet powerful OpenEdX plugin to send event tracking logs to a remote 
service in order to store additional information about user activity to perform
analytic research.

Usage with Tutor
----------------

This plugin has been tested with OpenEdX Lilac running under Tutor.
For more information about how to add custom requirements to a OpenEdX running
under Tutor see: `XBlock and edx-platform plugin development <https://docs.tutor.overhang.io/dev.html#xblock-and-edx-platform-plugin-development>`_

Once the package is added, you can add the ``ApiBackend`` to your CMS/LMS
settings. To do this, you should override the default ``TRACKING_BACKENDS`` and
``EVENT_TRACKING_BACKENDS`` from ``cms/envs/common.py`` and ``lms/evns/common.py``
settings files.

.. code-block:: python

   TRACKING_BACKENDS['api'] = {
       'ENGINE': 'edx_analytics_logger.api.ApiBackend',
       'OPTIONS': {
           'endpoint': <FILL_WITH_AN_URI>,
           'token': <FILL_WITH_AN_AUTHORIZATION_TOKEN>,
       }
   }

   EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['backends']['api'] = {
       'ENGINE': 'edx_analytics_logger.api.ApiBackend',
       'OPTIONS': {
           'endpoint': <FILL_WITH_AN_URI>,
           'token': <FILL_WITH_AN_AUTHORIZATION_TOKEN>,
       }
   }

This could be accomplished by writing a custom plugin to add these settings in
CMS/LMS settings.

Additional notes
----------------

This project has been tested using Django REST Framework service as backend. 
OpenEdX Analytics Logger could be hugely improved to support more settings, 
authentication mechanisms and more options. Feel free to contribute by
reporting bugs, suggesting improvements or opening Pull Requests.
