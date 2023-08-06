You can fix an open redirect by either preventing user input from being used in the target redirection or by validating the user input before the redirection.

If you known in advance the URLs to where you need to redirect you can remove the redirection functionality, thus removing the vulnerability.
If that is the case, you can replace each redirect by a direct link to the target URL.
You can also have a server-side list of target URLs and pass in the parameter a reference to the right index of that list.

If you need to have user input in the redirection parameter you can take a few measures to reduce the likelihood of an successful attack:

- validate the URL domain with a whitelist of domains you trust
- if you only need to redirect to your domain, allow only relative URLs by validating if they start with a single slash character and then prepend *https://youdomain.example* to the URL
- if you only need to redirect to your domain, allow only absolute URLs by validating if it starts with *https://yourdomain.example/*.
