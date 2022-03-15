Ventor Base
=========================

Base module that allow relation between Ventor modules

Changelog
---------

15.0.1.3.8 (2022-02-03)
***********************

* Added security group 'Warehouse Operations: Allow applying all qty of product'
* Added automatic switch on the 'Manage package' setting in all menus to default if setting "Package" is switched on
* Added the setting “Scan destination location” to all Operation Types
* Added dependency of settings 'Show next product' and 'Confirm product'
* Added the settings 'Behavior on split operation' and 'Behavior on backorder creation' to all Operation Types
* Added sudo rules for validating stock picking in transit
* Added post init hook and migration for setup Allowed Warehouses to users

15.0.1.3.7 (2021-12-2)
***********************

* [REM] Removed unused settings displayed in the Ventor Preferences tab on the user form
* [REM] Removed 'Default inventory location' from the Inventory settings from the Ventor Configuration
* [IMP] Changed 'Ventor Configuration' menu, added 'User Settings' menu item
* [REM] Removed 'Custom package name' field displayed in the Ventor Preferences tab on the user form
* [IMP] Added 'Custom Build Name' field in Ventor Configuration/Additional Settings
