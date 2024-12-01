# zoho-sdk

**Not affiliated with Zoho!**

This is made for the specific needs at my workplace. Thus, the classes `BaseLead`, `BaseContact`, etc. contain the default fields for those modules, whereas `Lead`, `Contact`, etc. also contain our custom fields, which are probably not of use to anyone else. But feel free to use the `Base*` classes directly, or subclass them with your own custom fields. (The subclasses must also be decorated with `@dataclass`.)

Set `zoho.settings.client_id`, `zoho.settings.client_secret`, and `zoho.settings.refresh_token`. This can be done by settings the environment variables `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, and `ZOHO_REFRESH_TOKEN`, respectively.

You may also want to set `zoho.settings.timezone` (env. var `ZOHO_TIMEZONE`) to a valid timezone name, such as `Antarctica/Troll`, `Asia/Oral`, or `America/Pangnirtung`.

Installing this package also installs a `zoho-get-token` executable. Use this to get a refresh token.
