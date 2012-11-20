DJnfusion
---------

Simple InfusionSoft integration for Django.

The main feature of this package is to synchronize user accounts from your Django app with contacts in your InfusionSoft CRM.




Usage
-----

To make this work, you need to provide a few settings in your Django settings file:

* *DJNFUSION_COMPANY* -- the id of your registered company at InfusionSoft (available in Infusionsoft from Settings -> Misc Settings -> Application Settings -> Miscellaneous)

* *DJNFUSION_API_KEY* -- the API key for your application from InfusionSoft (available in Infusionsoft from Settings -> Misc Settings -> Application Settings -> Miscellaneous)


Further, you should make sure to invoke the hooks for syncing users at the right points in your code. That means you need to call the ``djnfusion.sync_user'' function whenever data in your system should be sent to InfusionSoft. A typical place to do this is ``post_save'' signal of Django's ``User'' model.

*TBD* document what exactly is synced

There are more settings that help you fine-tune the synchronization process:

* *DJNFUSION_USERID_FIELD_NAME* -- 
* *DJNFUSION_USER_ID_VALUE_PREPROCESSOR* --
* *DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_CREATE* --
* *DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_UPDATE* --

* *DJNFUSION_AUTO_OPTIN* --
* *DJNFUSION_OPTIN_ONLY_IF_ACTIVE* --
* *DJNFUSION_OPTIN_MESSAGE* --

* *DJNFUSION_DAILY_USER_STATISTICS* --

